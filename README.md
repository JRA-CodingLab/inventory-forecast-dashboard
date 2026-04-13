# Inventory Forecast Dashboard

[![CI](https://github.com/JRA-CodingLab/inventory-forecast-dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/JRA-CodingLab/inventory-forecast-dashboard/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![React 18](https://img.shields.io/badge/react-18-blue.svg)](https://react.dev/)

A full-stack inventory management dashboard built with **FastAPI** and **React**. Track products, monitor stock levels, record sales, and prepare for AI-driven demand forecasting.

## Features

- 📊 **Live Dashboard** — Real-time metrics for total products, stock value, and low-stock alerts
- 🔔 **Low Stock Alerts** — Items with stock below 10 are highlighted in red
- 🌗 **Dark/Light Theme** — Toggle between themes with persistent preference
- 🔐 **Auth Modal** — Login form with password and one-time code tabs
- 📦 **CRUD API** — Full product and sales management via REST endpoints
- 🤖 **Forecast Ready** — Architecture prepared for ML-based demand prediction

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.10+, FastAPI, SQLAlchemy, SQLite, Pydantic |
| Frontend | React 18, Vite, Tailwind CSS, React Router |
| Testing | pytest, FastAPI TestClient |

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.server:app --reload
```

The API will be available at `http://localhost:8000`. Visit `/docs` for interactive Swagger documentation.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend dev server starts at `http://localhost:5173` and proxies API requests to the backend.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/products/` | Create a product |
| `GET` | `/products/` | List products (paginated) |
| `GET` | `/products/{id}` | Get a product |
| `PATCH` | `/products/{id}` | Update a product |
| `DELETE` | `/products/{id}` | Delete a product |
| `POST` | `/sales/` | Record a sale |
| `GET` | `/sales/` | List sales |

## Running Tests

```bash
pip install pytest httpx
pytest -v
```

## Project Structure

```
├── backend/          # FastAPI application
│   ├── app/
│   │   ├── db.py         # Database engine & session
│   │   ├── entities.py   # ORM models
│   │   ├── dto.py        # Pydantic schemas
│   │   └── server.py     # API endpoints
│   └── requirements.txt
├── frontend/         # React SPA
│   ├── src/
│   │   ├── pages/        # Landing & Dashboard views
│   │   └── components/   # TopBar & LoginDialog
│   └── package.json
├── tests/            # Python test suite
├── pyproject.toml
└── README.md
```

## License

[MIT](LICENSE) © 2026 Juan Ruiz Alonso
