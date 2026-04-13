# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-04-13

### Added

- FastAPI backend with CRUD endpoints for products and sales
- SQLAlchemy ORM models with SQLite storage
- Pydantic request/response schemas with validation
- Paginated product listing
- Sale recording with automatic stock decrement
- React frontend with Vite and Tailwind CSS
- Landing page with feature highlights and CTAs
- Dashboard page with live metrics and inventory table
- Low stock badge (red when stock < 10)
- Dark/light theme toggle with localStorage persistence
- Auth modal with password and OTP tab switcher
- Google sign-in placeholder button
- CORS middleware for frontend-backend communication
- Python test suite with mocked database
- CI workflow for automated testing
- Project documentation (README, CONTRIBUTING, LICENSE)
