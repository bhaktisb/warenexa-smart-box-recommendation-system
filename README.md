# Smart Box Recommendation System

Production-oriented Django module for WareNexa Warehouse Suite, delivered for TechNest Electronics by WareNexa Technologies Pvt. Ltd.

## Overview

This application helps warehouse staff recommend the cheapest suitable shipping box for an order based on product dimensions, product weight, box dimensions, maximum box weight capacity, and box cost.

## Architecture

```
Presentation Layer (Templates / Views)
        ↓
Business Service Layer (OrderService, RecommendationService)
        ↓
ORM Layer (Django Models)
        ↓
Database (SQLite dev / PostgreSQL production)
```

Business logic lives in services under `orders/services/` and `recommendations/services/`. Views remain thin orchestration layers.

## Apps

- `core` – shared validators, dimension utilities, dashboard, staff mixins
- `products` – product catalog
- `boxes` – shipping box catalog
- `orders` – warehouse orders and line items
- `recommendations` – recommendation engine and history

## Security

- Warehouse UI requires **staff login** (`is_staff=True`)
- Create a staff user via `createsuperuser` (superusers are staff by default)
- Set `DJANGO_SECRET_KEY` and `DJANGO_DEBUG=False` in production
- Copy `.env.example` and configure environment variables before deployment

## Recommendation Algorithm

1. Validate order eligibility
2. Calculate total order weight
3. Calculate required dimensions using **PAME** (Per-Axis Maximum Envelope) documented in `core/utils/dimensions.py`
4. Retrieve active shipping boxes
5. Remove boxes failing dimension validation
6. Remove boxes exceeding maximum weight
7. Select the lowest-cost qualifying box
8. Persist recommendation outcome

### PAME (Per-Axis Maximum Envelope)

For each product unit, dimensions are sorted ascending (`d1 ≤ d2 ≤ d3`). The order envelope is:

- `required_d1 = max(d1)` across all units
- `required_d2 = max(d2)` across all units
- `required_d3 = max(d3)` across all units

A box qualifies when its sorted internal dimensions are greater than or equal to this envelope, every unit fits individually (rotation allowed), and total weight is within capacity.

**Assumption:** Smaller items pack into void space within the largest item's bounding prism. This simplification suits consumer-electronics orders but does not model two equally large items requiring separate floor space.

### Demo order expectations (after `seed_demo_data`)

| Order | Expected box |
|-------|----------------|
| ORD001 | BX-S01 (Small) |
| ORD002 | BX-S01 (Small) |
| ORD003 | BX-L01 (Large) |
| ORD004 | BX-L01 (Large) |
| ORD005 | BX-M01 (Medium) |
| ORD006 | BX-M01 (Medium) |
| ORD007 | BX-M01 (Medium) |
| ORD008 | BX-XL01 (Extra Large) |
| ORD009 | BX-XL01 (Extra Large) |
| ORD010 | BX-XL01 (Extra Large) |

## Quick Start (SQLite)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py createsuperuser
python manage.py runserver
```

Open:

- Login: http://127.0.0.1:8000/accounts/login/
- Dashboard: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## PostgreSQL

Set environment variables before running migrations (see `.env.example`):

```bash
set POSTGRES_DB=warenexa_warehouse
set POSTGRES_USER=postgres
set POSTGRES_PASSWORD=postgres
set POSTGRES_HOST=localhost
set POSTGRES_PORT=5432
python manage.py migrate
```

## Production Deployment

1. Set environment variables:
   - `DJANGO_SECRET_KEY` (required when `DEBUG=False`)
   - `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS=your.domain.com`
   - `DJANGO_CSRF_TRUSTED_ORIGINS=https://your.domain.com`
   - PostgreSQL variables (recommended)
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Collect static files: `python manage.py collectstatic --noinput`
5. Load catalog (optional): `python manage.py seed_demo_data`
6. Create staff user: `python manage.py createsuperuser`
7. Run with Gunicorn:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

WhiteNoise serves static files in production. HTTPS settings (`SECURE_SSL_REDIRECT`, secure cookies, HSTS) activate automatically when `DEBUG=False`.

## Running Tests

```bash
python manage.py test
```

## Warehouse Workflow

1. Sign in with a staff account
2. Open an order from the Orders page
3. Click **Recommend Box**
4. Review the suggested box and PAME envelope metrics
5. Click **Confirm Packing** after physical packing is complete

## Seed Data

```bash
python manage.py seed_demo_data
python manage.py seed_demo_data --flush-orders   # also remove non-demo orders
```

## Project Structure

```
config/                 # Django project settings and URLs
core/                   # Dashboard, validators, dimension utilities, mixins
products/               # Product models and views
boxes/                  # Shipping box models and views
orders/                 # Order models, services, and views
recommendations/        # Recommendation models, engine, and views
templates/              # Bootstrap 5 warehouse UI
```

## Notes

- Product `price` is catalog metadata only; it does not affect box recommendation.
- `BoxRecommendation.required_length/width/height` store the PAME sorted envelope `(d₁, d₂, d₃)`.
- `DISPATCHED` order status is reserved for future workflow extensions.
