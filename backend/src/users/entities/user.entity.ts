import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, OneToMany } from "typeorm";
import { Cv } from "../../cvs/entities/cv.entity";

@Entity("users")
export class User {
  @PrimaryGeneratedColumn("uuid")
  id!: string;

  @Column({ unique: true })
  email!: string;

  @Column()
  name!: string;

  @OneToMany(() => Cv, (cv) => cv.user)
  cvs!: Cv[];

  @CreateDateColumn({ name: "created_at" })
  createdAt!: Date;
}
