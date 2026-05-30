# Backend scaffold

This is a minimal NestJS backend scaffold prepared for PostgreSQL.

## Included

- `AppModule` with global config
- `TypeORM` PostgreSQL connection config
- `health` module with `/api/health`
- Root endpoint at `/api`

## Run locally

1. `cd backend`
2. `npm install`
3. Copy `.env.example` to `.env`
4. Update PostgreSQL credentials
5. `npm run start:dev`

## Notes

- Database connection is scaffolded but not migrated or seeded yet.
- The actual tables/entities will be added next when you start implementing review features.
