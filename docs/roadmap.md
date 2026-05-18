# Findora Roadmap

Findora will be built step by step using clean milestones.

## v0.0 — Open-source Planning

Status: In progress

Tasks:

- GitHub repository
- main branch
- dev branch
- contribution guide
- code of conduct
- license
- pull request template
- issue templates
- Git workflow documentation
- roadmap

## v0.1.0 — Project Skeleton

Tasks:

- FastAPI app setup
- API v1 router
- Health endpoint
- Basic homepage
- Core folder structure
- Config placeholder
- Security placeholder
- CSRF placeholder
- RBAC placeholder
- Error schema placeholder
- Pagination schema placeholder
- Initial pytest setup

## v0.2.0 — Database Foundation

Tasks:

- SQLAlchemy setup
- SQLite development database
- Alembic setup
- Base model
- Category model
- Seed default categories
- Test database isolation

## v0.3.0 — Item Module

Tasks:

- Item model
- Item schemas
- Item service
- Create item
- List items
- Item detail
- Search and filter
- Pagination
- Soft delete fields
- Basic item pages

## v0.4.0 — Image Upload

Tasks:

- ItemImage model
- Upload service
- File type validation
- File size validation
- Random filename generation
- Controlled media route
- Show item images

## v0.5.0 — Auth System

Tasks:

- User model
- Register
- Login
- Logout
- Password hashing
- Session-based authentication
- Current user dependency
- CSRF validation
- Login and register rate limits

## v0.6.0 — Claim System

Tasks:

- Claim model
- Submit claim
- View own claims
- Owner views claims for own item
- Accept claim
- Reject claim
- Claim permissions
- Claim rate limit

## v0.7.0 — Admin and Moderator Panel

Tasks:

- Admin dashboard
- Moderator dashboard
- Review all items
- Review claims
- Mark item resolved
- Soft-delete item
- Category CRUD
- RBAC route guards

## v0.8.0 — Hardening

Tasks:

- Global exception handlers
- Standard error responses
- Upload error responses
- Rate limit error handling
- 401, 403, 404, 413, 415, 422, 429 handling
- Error handling documentation

## v0.9.0 — Tests and Documentation

Tasks:

- Health tests
- Item tests
- Auth tests
- Claim tests
- Admin permission tests
- Upload tests
- Rate limit tests
- Setup documentation
- API documentation
- Security documentation
- RBAC documentation
- Alembic workflow documentation

## v1.0.0 — Stable MVP Release

Tasks:

- Final QA
- UI polish
- Mobile responsiveness
- PostgreSQL config
- Production settings
- Deployment guide
- README update
- Changelog
- GitHub release
- Tag v1.0.0

## Future Roadmap

### v1.1

- Docker setup
- GitHub Actions CI
- Redis rate limiting
- Audit log table

### v1.2

- Email verification
- Notifications
- Auto item matching

### v1.3

- Cloud image storage
- Chat between owner and finder

### v2.0

- React or Next.js frontend
- JWT authentication
- Advanced admin analytics
- Monitoring and logging
