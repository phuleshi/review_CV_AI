import { Injectable } from "@nestjs/common";
import { DataSource } from "typeorm";

@Injectable()
export class HealthService {
  constructor(private readonly dataSource: DataSource) {}

  check() {
    const dbConnected = this.dataSource.isInitialized;
    return {
      status: "ok",
      service: "backend",
      database: dbConnected ? "connected" : "disconnected"
    };
  }
}
