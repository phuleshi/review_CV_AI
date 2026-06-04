import { HttpException, Injectable, Logger } from "@nestjs/common";
import { ConfigService } from "@nestjs/config";
import { ReviewCvDto } from "./dto/review-cv.dto";
import { ReviewResult } from "./review.types";

/**
 * Proxies CV reviews to the FastAPI AI service. The backend owns request
 * validation + the internal auth header; the AI service owns scoring/feedback.
 */
@Injectable()
export class ReviewService {
  private readonly logger = new Logger(ReviewService.name);
  private readonly aiServiceUrl: string;
  private readonly internalApiKey: string;

  constructor(private readonly config: ConfigService) {
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

    return (await res.json()) as ReviewResult;
  }
}
