import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, ManyToOne, OneToMany, JoinColumn } from "typeorm";
import { Cv } from "../../cvs/entities/cv.entity";
import { ReviewFeedback } from "./review-feedback.entity";
import { JdMatch } from "../review.types";

@Entity("reviews")
export class Review {
  @PrimaryGeneratedColumn("uuid")
  id!: string;

  @Column({ name: "overall_score", type: "integer" })
  overallScore!: number;

  @Column({ type: "text" })
  summary!: string;

  @Column({ name: "jd_match", type: "jsonb", nullable: true })
  jdMatch!: JdMatch | null;

  @ManyToOne(() => Cv, (cv) => cv.reviews, { onDelete: "CASCADE" })
  @JoinColumn({ name: "cv_id" })
  cv!: Cv;

  @OneToMany(() => ReviewFeedback, (feedback) => feedback.review)
  feedbacks!: ReviewFeedback[];

  @CreateDateColumn({ name: "created_at" })
  createdAt!: Date;
}
