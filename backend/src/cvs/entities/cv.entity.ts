import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, ManyToOne, OneToMany, JoinColumn } from "typeorm";
import { User } from "../../users/entities/user.entity";
import { Review } from "../../review/entities/review.entity";

@Entity("cvs")
export class Cv {
  @PrimaryGeneratedColumn("uuid")
  id!: string;

  @Column({ name: "cv_text", type: "text" })
  cvText!: string;

  @Column({ name: "job_description", type: "text", nullable: true })
  jobDescription!: string | null;

  @ManyToOne(() => User, (user) => user.cvs, { onDelete: "CASCADE" })
  @JoinColumn({ name: "user_id" })
  user!: User;

  @OneToMany(() => Review, (review) => review.cv)
  reviews!: Review[];

  @CreateDateColumn({ name: "created_at" })
  createdAt!: Date;
}
