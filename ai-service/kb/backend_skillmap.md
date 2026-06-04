# Backend Skill Map — V1

Reference for scoring the `skills` category and JD keyword matching for **backend**
roles. Used to judge relevance and depth, and to spot missing core skills.

## Core (expected for most backend roles)

- **Languages** (role-dependent): Node.js/TypeScript, Python, Java, Go, C#, PHP, Ruby
- **Frameworks**: NestJS/Express (Node), FastAPI/Django/Flask (Python), Spring Boot (Java), .NET, Gin (Go)
- **APIs**: REST, JSON, HTTP fundamentals, GraphQL
- **Databases**: PostgreSQL/MySQL (SQL), MongoDB (NoSQL), basic data modeling, indexing
- **Auth**: JWT, OAuth2, sessions, password hashing
- **Fundamentals**: data structures & algorithms, OOP, error handling, logging
- **Tooling**: Git, npm/pip, environment config, Postman/curl

## Strong / mid-level signals

- ORMs/query: Prisma, TypeORM, SQLAlchemy, Hibernate; query optimization
- Caching: Redis, in-memory caches, cache invalidation
- Messaging/queues: RabbitMQ, Kafka, SQS, Celery, BullMQ
- Testing: unit + integration, mocking, pytest/Jest, test coverage
- Containers: Docker, docker-compose
- API design: versioning, pagination, rate limiting, validation, OpenAPI/Swagger
- Cloud basics: AWS/GCP/Azure core services (S3, EC2/Cloud Run, RDS)

## Senior / standout signals

- Architecture: microservices, event-driven, CQRS, DDD, clean/hexagonal architecture
- Scalability: load balancing, horizontal scaling, sharding, read replicas
- Observability: metrics, tracing, structured logging, alerting
- CI/CD, IaC (Terraform), Kubernetes
- Security: OWASP, secrets management, threat modeling
- Performance tuning, DB schema design at scale, system design

## Adjacent / nice-to-have

- gRPC, WebSockets, serverless (Lambda/Cloud Functions)
- Data: ETL, warehousing basics
- DevOps overlap: monitoring stacks (Prometheus/Grafana)

## Scoring hints

- **Junior**: one language + one framework + SQL basics + REST + Git = on track.
- **Mid**: + ORM, caching, testing, Docker, API design, a cloud provider.
- **Senior**: + architecture, scalability, observability, security, system design.
- Penalize: framework listed with no DB/API evidence; "knows SQL" but no schema/query work shown.
- Reward: production concerns (auth, caching, testing, deployment) evidenced in experience.
