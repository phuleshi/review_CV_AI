import { Body, Controller, Get, Post } from "@nestjs/common";
import { ReviewCvDto } from "./dto/review-cv.dto";
import { ReviewService } from "./review.service";
import { ReviewResult } from "./review.types";

@Controller("review-cv")
export class ReviewController {
  constructor(private readonly reviewService: ReviewService) {}

  // POST /api/review-cv  (global prefix "api")
  @Post()
  reviewCv(@Body() dto: ReviewCvDto): Promise<ReviewResult> {
    return this.reviewService.review(dto);
  }

  // GET /api/review-cv/history
  @Get("history")
  getHistory() {
    return this.reviewService.getHistory();
  }
}
