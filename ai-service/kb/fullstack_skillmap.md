# Full-Stack Skill Map — V1

Reference for scoring the `skills` category and JD keyword matching for **full-stack**
roles. A full-stack candidate is judged on credible breadth across frontend + backend,
plus the glue that connects them. Depth on at least one side is expected.

See also: `frontend_skillmap.md`, `backend_skillmap.md`.

## Core (expected for most full-stack roles)

- **Frontend**: HTML/CSS, JavaScript/TypeScript, one framework (React/Next.js/Vue/Angular)
- **Backend**: one server framework (NestJS/Express, FastAPI/Django, Spring Boot)
- **Database**: SQL (PostgreSQL/MySQL) and/or NoSQL (MongoDB), basic data modeling
- **API layer**: designing + consuming REST/GraphQL, auth (JWT/OAuth2)
- **Fundamentals**: Git, HTTP, JSON, env config, end-to-end feature ownership

## Strong / mid-level signals

- Connecting the stack: typed API contracts, shared types (e.g. monorepo), validation both ends
- ORM + migrations (Prisma, TypeORM, SQLAlchemy)
- Testing across layers (unit + integration + a little E2E)
- Docker / docker-compose for local full-stack dev
- Caching (Redis), background jobs/queues
- Deployment: Vercel/Netlify (FE) + a backend host; basic CI/CD
- State management + data fetching (React Query) wired to a real backend

## Senior / standout signals

- Architecture across the stack: clean separation, BFF, microservices or modular monolith
- Performance both ends: Core Web Vitals + backend latency/throughput
- Observability, security (OWASP), scalability
- IaC, Kubernetes, multi-environment CI/CD
- Owning a product end-to-end: design → build → ship → operate

## Adjacent / nice-to-have

- Mobile (React Native), serverless, GraphQL federation
- DevOps depth (Terraform, monitoring), cloud architecture

## Scoring hints

- **Junior full-stack**: can build + ship a CRUD app end-to-end (FE + API + DB) = on track.
- **Mid**: typed contracts, testing across layers, Docker, a real deployment.
- **Senior**: architecture + operations across the stack, with clear depth on one side.
- Penalize: claiming "full-stack" but evidence on only one side; no end-to-end project.
- Reward: at least one project that demonstrably spans FE + API + DB (deployed, with a link).
- Balance: don't expect senior-level depth on *both* sides — credible breadth + one deep side is the bar.
