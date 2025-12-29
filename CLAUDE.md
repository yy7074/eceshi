# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

E测试 (eceshi) is a scientific research testing service platform (小程序) with a uni-app frontend and FastAPI backend.

## Development Commands

### Frontend (WeChat Mini Program)

```bash
cd frontend
npm install
npm run dev:mp-weixin    # Development with watch mode
npm run build:mp-weixin  # Production build
```

Output goes to `dist/dev/mp-weixin` - import this into WeChat DevTools.

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt

# Run development server
python -m app.main
# Or with uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

API docs available at `/api/docs` (Swagger) and `/api/redoc` in debug mode.

### Environment Setup

Backend requires `.env` file (copy from `env.example.txt`):
- `DATABASE_URL` - MySQL connection string
- `JWT_SECRET_KEY` - JWT signing key
- `SMS_ACCESS_KEY`, `SMS_SECRET_KEY` - Aliyun SMS
- `WECHAT_APPID`, `WECHAT_SECRET` - WeChat Mini Program

## Architecture

### Backend Structure (`backend/app/`)

```
app/
├── main.py           # FastAPI app entry, lifespan management
├── api/
│   ├── __init__.py   # Router aggregation (all v1 routes)
│   └── v1/           # API endpoints by domain
│       ├── deps.py   # Dependency injection (get_db, get_current_user)
│       ├── auth.py   # SMS/WeChat login
│       ├── users.py  # User management
│       ├── orders.py # Order CRUD
│       └── ...       # ~20 more domain modules
├── models/           # SQLAlchemy ORM models
├── schemas/          # Pydantic request/response schemas
├── services/         # Business logic (sms_service, wechat_service, alipay_service)
└── core/
    ├── config.py     # pydantic-settings configuration
    ├── database.py   # SQLAlchemy engine, SessionLocal, Base
    ├── security.py   # JWT utilities
    └── response.py   # Standardized response format
```

### Frontend Structure (`frontend/`)

```
frontend/
├── pages/            # Main package pages (index, category, order, user, login, project, search)
├── pagesA/           # Sub-package pages (booking, address, points, invite, etc.)
├── utils/
│   ├── request.js    # HTTP client with token handling, auto-redirect on 401
│   └── api.js        # API endpoint definitions
└── pages.json        # Page routing configuration
```

### Key Patterns

**API Response Format**: All API responses use `{code: 200, message: string, data: any}` structure.

**Authentication Flow**:
- `get_current_user` dependency extracts user from JWT Bearer token
- `get_current_user_optional` for routes that work with or without auth
- `get_current_admin_user` for admin-only endpoints (checks `is_admin` in JWT payload)

**Database Sessions**: Use `db: Session = Depends(get_db)` dependency injection.

**Frontend API Calls**: Use `request.get/post/put/delete()` from `utils/request.js` - handles token attachment and error toasts automatically.

## API Routes

All routes prefixed with `/api/v1/`. Major modules:
- `/auth` - SMS login, WeChat login, admin login
- `/users` - User profile, balance, certification
- `/projects` - Testing project listing and details
- `/orders` - Order creation, listing, cancellation
- `/addresses` - User address management
- `/payments` - Payment creation and callbacks
- `/points` - Points system
- `/admin` - Admin management endpoints

## Notes

- `backend/backendtemp/` contains experimental/temp code - primary backend is `backend/app/`
- Frontend uses Vuex for state management
- Static files served from `static/` directory, uploads go to `static/uploads/`
- Admin panel mounted at `/admin` (if `admin/` directory exists)
