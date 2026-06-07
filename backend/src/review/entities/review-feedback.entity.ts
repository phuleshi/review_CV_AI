import { Entity, PrimaryGeneratedColumn, Column, ManyToOne, JoinColumn } from "typeorm";
import { Review } from "./review.entity";

@Entity("review_feedbacks")
export class ReviewFeedback {
  @PrimaryGeneratedColumn("uuid")
  id!: string;

  @Column()
  category!: string; // structure, skills, experience, projects, ats

  @Column({ type: "integer" })
  score!: number;

  @Column({ type: "jsonb" })
  strengths!: string[];

  @Column({ type: "jsonb" })
  weaknesses!: string[];

  @Column({ type: "jsonb" })
  suggestions!: string[];

  @ManyToOne(() => Review, (review) => review.feedbacks, { onDelete: "CASCADE" })
  @JoinColumn({ name: "review_id" })
  review!: Review;
}
