import { Injectable, OnModuleInit } from "@nestjs/common";
import { InjectRepository } from "@nestjs/typeorm";
import { Repository } from "typeorm";
import { User } from "./entities/user.entity";

@Injectable()
export class UsersService implements OnModuleInit {
  constructor(
    @InjectRepository(User)
    private readonly userRepository: Repository<User>
  ) {}

  async onModuleInit() {
    await this.ensureDefaultUser();
  }

  async ensureDefaultUser(): Promise<User> {
    const defaultEmail = "test@example.com";
    let user = await this.userRepository.findOne({ where: { email: defaultEmail } });
    if (!user) {
      user = this.userRepository.create({
        email: defaultEmail,
        name: "Nguyen Van A"
      });
      user = await this.userRepository.save(user);
    }
    return user;
  }
}
