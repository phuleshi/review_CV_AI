import { Injectable } from "@nestjs/common";

@Injectable()
export class HealthService {
  check() {
    return {
      status: "ok",
      service: "backend",
      database: "not connected yet"
    };
  }
}
