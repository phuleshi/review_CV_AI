import { Injectable } from "@nestjs/common";

@Injectable()
export class AppService {
  getRoot() {
    return {
      name: "AI CV Review API",
      status: "ok"
    };
  }
}
