import { HttpException, Injectable, Logger } from "@nestjs/common";
import { ConfigService } from "@nestjs/config";
import { InjectRepository } from "@nestjs/typeorm";
import { Repository } from "typeorm";
import { ReviewCvDto } from "./dto/review-cv.dto";
import { ReviewResult } from "./review.types";
import { UsersService } from "../users/users.service";
import { Cv } from "../cvs/entities/cv.entity";
import { Review } from "./entities/review.entity";
import { ReviewFeedback } from "./entities/review-feedback.entity";

@Injectable()
export class ReviewService {
  private readonly logger = new Logger(ReviewService.name);
  private readonly aiServiceUrl: string;
  private readonly internalApiKey: string;

  constructor(
    private readonly config: ConfigService,
    private readonly usersService: UsersService,
    @InjectRepository(Cv)
    private readonly cvRepository: Repository<Cv>,
    @InjectRepository(Review)
    private readonly reviewRepository: Repository<Review>,
    @InjectRepository(ReviewFeedback)
    private readonly feedbackRepository: Repository<ReviewFeedback>
  ) {
    this.aiServiceUrl = this.config.get<string>("AI_SERVICE_URL", "http://localhost:8000");
    this.internalApiKey = this.config.get<string>("INTERNAL_API_KEY", "change-me");
  }

  async review(dto: ReviewCvDto): Promise<ReviewResult> {
    const url = `${this.aiServiceUrl}/api/v1/review-cv`;

    let res: Response;
    try {
      res = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Internal-Api-Key": this.internalApiKey
        },
        body: JSON.stringify({
          cv_text: dto.cv_text,
          job_description: dto.job_description ?? null
        })
      });
    } catch (err) {
      this.logger.error(`AI service unreachable at ${url}: ${String(err)}`);
      throw new HttpException("AI service is unreachable", 502);
    }

    if (!res.ok) {
      const detail = await res.text().catch(() => "");
      this.logger.warn(`AI service returned ${res.status}: ${detail}`);
      throw new HttpException(detail || `AI service error (${res.status})`, res.status);
    }

    const result = (await res.json()) as ReviewResult;

    try {
      // 1. Ensure test user exists
      const user = await this.usersService.ensureDefaultUser();

      // 2. Save CV record
      let cv = this.cvRepository.create({
        cvText: dto.cv_text,
        jobDescription: dto.job_description ?? null,
        user: user
      });
      cv = await this.cvRepository.save(cv);

      // 3. Save Review record
      let review = this.reviewRepository.create({
        overallScore: result.overall_score,
        summary: result.summary,
        jdMatch: result.jd_match ?? null,
        cv: cv
      });
      review = await this.reviewRepository.save(review);

      // 4. Save ReviewFeedback records (category scores and general feedback lists)
      const feedBackRows: ReviewFeedback[] = [];

      // Save category scores
      const categories = ["structure", "skills", "experience", "projects", "ats"] as const;
      for (const cat of categories) {
        feedBackRows.push(
          this.feedbackRepository.create({
            category: cat,
            score: result.category_scores[cat],
            strengths: [],
            weaknesses: [],
            suggestions: [],
            review: review
          })
        );
      }

      // Save overall strengths, weaknesses, and suggestions under category "general"
      feedBackRows.push(
        this.feedbackRepository.create({
          category: "general",
          score: 0,
          strengths: result.strengths,
          weaknesses: result.weaknesses,
          suggestions: result.suggestions,
          review: review
        })
      );

      await this.feedbackRepository.save(feedBackRows);
    } catch (dbErr) {
      this.logger.error(`Failed to save review to database: ${String(dbErr)}`);
    }

    return result;
  }

  async getHistory(): Promise<any[]> {
    const reviews = await this.reviewRepository.find({
      relations: ["cv", "feedbacks"],
      order: {
        createdAt: "DESC"
      }
    });

    return reviews.map((review) => {
      const categoryScores = {
        structure: 0,
        skills: 0,
        experience: 0,
        projects: 0,
        ats: 0
      };
      let strengths: string[] = [];
      let weaknesses: string[] = [];
      let suggestions: string[] = [];

      for (const fb of review.feedbacks) {
        if (fb.category === "general") {
          strengths = fb.strengths;
          weaknesses = fb.weaknesses;
          suggestions = fb.suggestions;
        } else if (fb.category in categoryScores) {
          categoryScores[fb.category as keyof typeof categoryScores] = fb.score;
        }
      }

      return {
        id: review.id,
        cv_text: review.cv.cvText,
        job_description: review.cv.jobDescription,
        overall_score: review.overallScore,
        category_scores: categoryScores,
        strengths,
        weaknesses,
        suggestions,
        summary: review.summary,
        jd_match: review.jdMatch,
        createdAt: review.createdAt
      };
    });
  }
}
