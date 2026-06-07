import { TypeOrmModuleAsyncOptions, TypeOrmModuleOptions } from "@nestjs/typeorm";
import { ConfigService } from "@nestjs/config";

export const databaseConfig = {
  inject: [ConfigService],
  useFactory: (configService: ConfigService): TypeOrmModuleOptions => ({
    type: "postgres",
    host: configService.get<string>("DATABASE_HOST", "localhost"),
    port: configService.get<number>("DATABASE_PORT", 5432),
    username: configService.get<string>("DATABASE_USERNAME", "postgres"),
    password: configService.get<string>("DATABASE_PASSWORD", "postgres"),
    database: configService.get<string>("DATABASE_NAME", "review_cv_ai"),
    autoLoadEntities: true,
    synchronize: configService.get<string>("DATABASE_SYNCHRONIZE", "false") === "true"
  })
} satisfies TypeOrmModuleAsyncOptions;
