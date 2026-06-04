import { IsOptional, IsString, MinLength } from "class-validator";

/**
 * Request body for POST /api/review-cv.
 * Field names are snake_case to match the AI service contract exactly, so the
 * backend forwards them without remapping.
 */
export class ReviewCvDto {
  @IsString()
  @MinLength(1)
  cv_text!: string;

  @IsOptional()
  @IsString()
  job_description?: string;
}
