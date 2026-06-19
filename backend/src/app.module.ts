import { Module } from "@nestjs/common";
import { ConfigModule } from "@nestjs/config";
import { TypeOrmModule } from "@nestjs/typeorm";
import { AppController } from "./app.controller";
import { AppService } from "./app.service";
import { databaseConfig } from "./config/database.config";
import { HealthModule } from "./health/health.module";
import { ReviewModule } from "./review/review.module";
import { UsersModule } from "./users/users.module";
import { CvsModule } from "./cvs/cvs.module";

const databaseImports =
  process.env.DATABASE_ENABLED === "true" ? [TypeOrmModule.forRootAsync(databaseConfig)] : [];

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: [".env"]
    }),
    ...databaseImports,
    HealthModule,
    UsersModule,
    CvsModule,
    ReviewModule
  ],
  controllers: [AppController],
  providers: [AppService]
})
export class AppModule {}
