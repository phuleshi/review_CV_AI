import { Module } from "@nestjs/common";
import { TypeOrmModule } from "@nestjs/typeorm";
import { ReviewController } from "./review.controller";
import { ReviewService } from "./review.service";
import { Review } from "./entities/review.entity";
import { ReviewFeedback } from "./entities/review-feedback.entity";
import { UsersModule } from "../users/users.module";
import { CvsModule } from "../cvs/cvs.module";

@Module({
  imports: [
    TypeOrmModule.forFeature([Review, ReviewFeedback]),
    UsersModule,
    CvsModule
  ],
  controllers: [ReviewController],
  providers: [ReviewService]
})
export class ReviewModule {}
