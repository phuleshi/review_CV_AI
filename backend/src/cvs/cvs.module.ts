import { Module } from "@nestjs/common";
import { TypeOrmModule } from "@nestjs/typeorm";
import { Cv } from "./entities/cv.entity";

@Module({
  imports: [TypeOrmModule.forFeature([Cv])],
  exports: [TypeOrmModule]
})
export class CvsModule {}
