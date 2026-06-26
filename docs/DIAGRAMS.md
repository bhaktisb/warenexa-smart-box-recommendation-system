# UML & Architecture Diagrams
## Smart Box Recommendation System — Tradexa Warehouse

All diagrams below are derived **only** from the implemented codebase (`b:\Tradexa`).  
Actors, models, services, views, and workflows not present in code are excluded.

**Legend:** Solid lines = implemented · `DISPATCHED` order status exists in the model but has no service/UI workflow yet.

---

## 1. Use Case Diagram

Implemented actors:
- **Warehouse Staff** — `User` with `is_staff=True`, enforced by `StaffRequiredMixin`
- **Administrator** — Django `User` with admin access at `/admin/`

```mermaid
flowchart TB
    Staff((Warehouse Staff))
    Admin((Administrator))

    subgraph System["Smart Box Recommendation System"]
        direction TB

        subgraph Auth["Authentication"]
            UC_LOGIN[Login]
            UC_LOGOUT[Logout]
        end

        subgraph Browse["Read-Only Warehouse UI"]
            UC_DASH[View Dashboard]
            UC_PLIST[Browse Products]
            UC_PDET[View Product Detail]
            UC_BLIST[Browse Shipping Boxes]
            UC_BDET[View Shipping Box Detail]
            UC_OLIST[Browse Orders]
            UC_ODET[View Order Detail]
            UC_RLIST[Browse Recommendations]
            UC_RDET[View Recommendation Detail]
        end

        subgraph Packing["Packing Workflow"]
            UC_REC[Recommend Box]
            UC_CONF[Confirm Packing]
        end

        subgraph AdminUC["Django Admin /admin/"]
            UC_APROD[Manage Products]
            UC_ABOX[Manage Shipping Boxes]
            UC_AORD[Manage Orders and Order Items]
            UC_AREC[View Box Recommendations]
        end
    end

    Staff --> UC_LOGIN
    Staff --> UC_LOGOUT
    Staff --> UC_DASH
    Staff --> UC_PLIST
    Staff --> UC_PDET
    Staff --> UC_BLIST
    Staff --> UC_BDET
    Staff --> UC_OLIST
    Staff --> UC_ODET
    Staff --> UC_RLIST
    Staff --> UC_RDET
    Staff --> UC_REC
    Staff --> UC_CONF

    Admin --> UC_APROD
    Admin --> UC_ABOX
    Admin --> UC_AORD
    Admin --> UC_AREC

    UC_REC -.->|includes| UC_ODET
    UC_CONF -.->|includes| UC_ODET
```

| Use case | View / Entry point |
|----------|-------------------|
| Login | `LoginView` → `/accounts/login/` |
| Logout | `LogoutView` → `/accounts/logout/` |
| View Dashboard | `DashboardView` → `/` |
| Browse Products | `ProductListView` → `/products/` |
| View Product Detail | `ProductDetailView` → `/products/<pk>/` |
| Browse Shipping Boxes | `ShippingBoxListView` → `/boxes/` |
| View Shipping Box Detail | `ShippingBoxDetailView` → `/boxes/<pk>/` |
| Browse Orders | `OrderListView` → `/orders/` |
| View Order Detail | `OrderDetailView` → `/orders/<pk>/` |
| Recommend Box | `RecommendBoxView` → `POST /orders/<pk>/recommend/` |
| Confirm Packing | `ConfirmPackingView` → `POST /orders/<pk>/confirm-packing/` |
| Browse Recommendations | `RecommendationListView` → `/recommendations/` |
| View Recommendation Detail | `RecommendationDetailView` → `/recommendations/<pk>/` |

---

## 2. Activity Diagram — Recommend Box Workflow

Reflects `RecommendationService.recommend_for_order()` and `OrderService.validate_order_for_recommendation()`.

```mermaid
flowchart TD
    Start([Staff clicks Recommend Box]) --> A1[POST RecommendBoxView]
    A1 --> A2[RecommendationService.recommend_for_order]

    A2 --> V1{Order has items?}
    V1 -->|No| E1[ValidationError]
    V1 -->|Yes| V2{All products active?}
    V2 -->|No| E1
    V2 -->|Yes| V3{Order status is PACKED?}
    V3 -->|Yes| E1
    V3 -->|No| W1[Calculate total_weight]

    W1 --> D1[expand_order_units]
    D1 --> D2[calculate_required_dimensions PAME]
    D2 --> B1[Load active ShippingBox ordered by cost]

    B1 --> L1{More boxes?}
    L1 -->|No| NB[No box selected]
    L1 -->|Yes| B2{total_weight ≤ max_weight_capacity?}
    B2 -->|No| L1
    B2 -->|Yes| B3{PAME envelope fits box?}
    B3 -->|No| L1
    B3 -->|Yes| B4{Every unit fits with rotation?}
    B4 -->|No| L1
    B4 -->|Yes| SEL[Select this box — lowest cost]

    SEL --> S1[Create BoxRecommendation SUCCESS]
    S1 --> S2[Set Order.status = RECOMMENDED]
    S2 --> EndOK([Redirect with success message])

    NB --> F1[Create BoxRecommendation NO_SUITABLE_BOX]
    F1 --> EndWarn([Redirect with warning message])

    E1 --> EndErr([Redirect with error message])
```

---

## 3. Activity Diagram — Confirm Packing Workflow

Reflects `OrderService.confirm_packing()`.

```mermaid
flowchart TD
    Start([Staff clicks Confirm Packing]) --> A1[POST ConfirmPackingView]
    A1 --> A2[OrderService.confirm_packing]

    A2 --> V1{Order.status is PACKED?}
    V1 -->|Yes| E1[ValidationError: already packed]
    V1 -->|No| V2{Latest unconfirmed recommendation exists?}
    V2 -->|No| E2[ValidationError: no recommendation]
    V2 -->|Yes| V3{recommended_box is not null?}
    V3 -->|No| E2
    V3 -->|Yes| C1[Set recommendation.is_confirmed = True]
    C1 --> C2[Set recommendation.confirmed_at = now]
    C2 --> C3[Set Order.status = PACKED]
    C3 --> EndOK([Redirect with success message])

    E1 --> EndErr([Redirect with error message])
    E2 --> EndErr
```

---

## 4. Sequence Diagram — Recommend Box (End-to-End)

```mermaid
sequenceDiagram
    autonumber
    actor Staff as Warehouse Staff
    participant RBV as RecommendBoxView
    participant RS as RecommendationService
    participant OS as OrderService
    participant DIM as core.utils.dimensions
    participant DB as Database

    Staff->>RBV: POST /orders/{pk}/recommend/
    Note over RBV: StaffRequiredMixin checks is_staff

    RBV->>RS: recommend_for_order(order)

    RS->>OS: validate_order_for_recommendation(order)
    OS->>DB: order.items.exists()
    OS->>DB: order.items.select_related(product)
    alt validation fails
        OS-->>RS: raise ValidationError
        RS-->>RBV: ValidationError
        RBV-->>Staff: redirect + error message
    end

    RS->>DB: order.items.select_related(product)
    RS->>RS: calculate_total_weight(order_items)
    RS->>DIM: expand_order_units(order_items)
    DIM-->>RS: units[]
    RS->>DIM: calculate_required_dimensions(units)
    DIM-->>RS: required_dims (d1, d2, d3)

    loop each active ShippingBox ordered by cost, box_code
        RS->>RS: box_passes_weight_validation(box, total_weight)
        RS->>RS: box_passes_dimension_validation(box, required_dims, units)
        Note over RS: uses dimensions_fit, item_fits_in_box, sort_dimensions
    end

    alt box found
        RS->>DB: INSERT BoxRecommendation (SUCCESS)
        RS->>DB: UPDATE Order SET status=RECOMMENDED
        RS-->>RBV: BoxRecommendation
        RBV-->>Staff: redirect + success message
    else no suitable box
        RS->>DB: INSERT BoxRecommendation (NO_SUITABLE_BOX)
        Note over RS: Order.status unchanged
        RS-->>RBV: BoxRecommendation
        RBV-->>Staff: redirect + warning message
    end
```

---

## 5. Sequence Diagram — Confirm Packing

```mermaid
sequenceDiagram
    autonumber
    actor Staff as Warehouse Staff
    participant CPV as ConfirmPackingView
    participant OS as OrderService
    participant DB as Database

    Staff->>CPV: POST /orders/{pk}/confirm-packing/
    Note over CPV: StaffRequiredMixin checks is_staff

    CPV->>OS: confirm_packing(order)

    alt order.status == PACKED
        OS-->>CPV: ValidationError
        CPV-->>Staff: redirect + error message
    end

    OS->>DB: SELECT latest BoxRecommendation<br/>WHERE is_confirmed=False<br/>ORDER BY created_at DESC

    alt no row or recommended_box is null
        OS-->>CPV: ValidationError
        CPV-->>Staff: redirect + error message
    end

    OS->>DB: UPDATE BoxRecommendation SET is_confirmed=True, confirmed_at=now
    OS->>DB: UPDATE Order SET status=PACKED
    OS-->>CPV: Order
    CPV-->>Staff: redirect + success message
```

---

## 6. Class Diagram

Shows implemented domain models, abstract base, services, mixin, and PAME utility functions.

```mermaid
classDiagram
    direction TB

    class ValidatedModel {
        <<abstract>>
        +save()* void
    }

    class Product {
        +sku: CharField
        +name: CharField
        +category: CharField
        +price: DecimalField
        +length: DecimalField
        +width: DecimalField
        +height: DecimalField
        +weight: DecimalField
        +is_active: BooleanField
        +created_at: DateTimeField
        +updated_at: DateTimeField
    }

    class ShippingBox {
        +box_code: CharField
        +name: CharField
        +length: DecimalField
        +width: DecimalField
        +height: DecimalField
        +max_weight_capacity: DecimalField
        +cost: DecimalField
        +is_active: BooleanField
        +created_at: DateTimeField
        +updated_at: DateTimeField
        +clean() void
    }

    class Order {
        +order_number: CharField
        +customer_name: CharField
        +order_date: DateField
        +status: CharField
        +created_at: DateTimeField
        +updated_at: DateTimeField
    }

    class OrderItem {
        +quantity: PositiveIntegerField
        +created_at: DateTimeField
    }

    class BoxRecommendation {
        +total_weight: DecimalField
        +required_length: DecimalField
        +required_width: DecimalField
        +required_height: DecimalField
        +status: CharField
        +message: CharField
        +is_confirmed: BooleanField
        +confirmed_at: DateTimeField
        +created_at: DateTimeField
    }

    class OrderStatus {
        <<enumeration>>
        PENDING
        RECOMMENDED
        PACKED
        DISPATCHED
    }

    class RecommendationStatus {
        <<enumeration>>
        SUCCESS
        NO_SUITABLE_BOX
    }

    class OrderService {
        <<service>>
        +validate_order_for_recommendation(order)$ void
        +confirm_packing(order)$ Order
    }

    class RecommendationService {
        <<service>>
        +NO_SUITABLE_BOX_MESSAGE: str
        +recommend_for_order(order)$ BoxRecommendation
        +calculate_total_weight(order_items)$ Decimal
        +select_best_box(total_weight, required_dims, units)$ ShippingBox
        +box_passes_dimension_validation(box, required_dims, units)$ bool
        +box_passes_weight_validation(box, total_weight)$ bool
    }

    class StaffRequiredMixin {
        <<mixin>>
        +test_func() bool
    }

  class dimensions_module {
        <<module core.utils.dimensions>>
        +sort_dimensions(l, w, h)$ Dimensions
        +dimensions_fit(required, container)$ bool
        +item_fits_in_box(...)$ bool
        +calculate_required_dimensions(units)$ Dimensions
        +expand_order_units(order_items)$ list
    }

    ValidatedModel <|-- Product
    ValidatedModel <|-- ShippingBox
    ValidatedModel <|-- OrderItem

    Order "1" --> "*" OrderItem : items
    Product "1" --> "*" OrderItem : order_items
    Order "1" --> "*" BoxRecommendation : recommendations
    ShippingBox "0..1" --> "*" BoxRecommendation : recommendations

    Order --> OrderStatus : uses
    BoxRecommendation --> RecommendationStatus : uses

    RecommendationService ..> OrderService : validate_order_for_recommendation
    RecommendationService ..> dimensions_module : PAME calculations
    RecommendationService ..> ShippingBox : select_best_box
    RecommendationService ..> BoxRecommendation : create
    RecommendationService ..> Order : update status

    OrderService ..> BoxRecommendation : confirm latest
    OrderService ..> Order : update status
```

### Warehouse view classes (presentation layer)

| Class | Base classes |
|-------|----------------|
| `DashboardView` | `StaffRequiredMixin`, `TemplateView` |
| `ProductListView` | `StaffRequiredMixin`, `ListView` |
| `ProductDetailView` | `StaffRequiredMixin`, `DetailView` |
| `ShippingBoxListView` | `StaffRequiredMixin`, `ListView` |
| `ShippingBoxDetailView` | `StaffRequiredMixin`, `DetailView` |
| `OrderListView` | `StaffRequiredMixin`, `ListView` |
| `OrderDetailView` | `StaffRequiredMixin`, `DetailView` |
| `RecommendBoxView` | `StaffRequiredMixin`, `View` |
| `ConfirmPackingView` | `StaffRequiredMixin`, `View` |
| `RecommendationListView` | `StaffRequiredMixin`, `ListView` |
| `RecommendationDetailView` | `StaffRequiredMixin`, `DetailView` |

---

## 7. ER Diagram

Matches Django models and foreign-key `on_delete` behaviour.

```mermaid
erDiagram
    PRODUCT {
        bigint id PK
        varchar sku UK
        varchar name
        varchar category
        decimal price
        decimal length
        decimal width
        decimal height
        decimal weight
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    SHIPPING_BOX {
        bigint id PK
        varchar box_code UK
        varchar name
        decimal length
        decimal width
        decimal height
        decimal max_weight_capacity
        decimal cost
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    ORDER {
        bigint id PK
        varchar order_number UK
        varchar customer_name
        date order_date
        varchar status
        datetime created_at
        datetime updated_at
    }

    ORDER_ITEM {
        bigint id PK
        bigint order_id FK
        bigint product_id FK
        int quantity
        datetime created_at
    }

    BOX_RECOMMENDATION {
        bigint id PK
        bigint order_id FK
        bigint recommended_box_id FK "nullable"
        decimal total_weight
        decimal required_length
        decimal required_width
        decimal required_height
        varchar status
        varchar message
        boolean is_confirmed
        datetime confirmed_at "nullable"
        datetime created_at
    }

    ORDER ||--|{ ORDER_ITEM : "has items CASCADE"
    PRODUCT ||--o{ ORDER_ITEM : "referenced PROTECT"
    ORDER ||--o{ BOX_RECOMMENDATION : "has recommendations CASCADE"
    SHIPPING_BOX ||--o{ BOX_RECOMMENDATION : "recommended SET_NULL"
```

### Constraints (implemented)

| Table | Constraint |
|-------|------------|
| `ORDER_ITEM` | `UNIQUE (order_id, product_id)` — `unique_order_product` |
| `PRODUCT` | `UNIQUE (sku)` |
| `SHIPPING_BOX` | `UNIQUE (box_code)` |
| `ORDER` | `UNIQUE (order_number)` |

---

## 8. Component Diagram

```mermaid
flowchart TB
    subgraph Presentation["Presentation Layer"]
        TPL[Django Templates<br/>Bootstrap 5]
        VIEWS[Warehouse CBVs<br/>core · products · boxes · orders · recommendations]
        AUTHV[Django Auth Views<br/>LoginView · LogoutView]
        MIXIN[StaffRequiredMixin]
        ADMINUI[Django Admin UI]
    end

    subgraph Business["Business Service Layer"]
        OSVC[OrderService<br/>orders/services/]
        RSVC[RecommendationService<br/>recommendations/services/]
    end

    subgraph Domain["Domain / Utility Layer"]
        PAME[core/utils/dimensions.py<br/>PAME functions]
        VAL[core/validators.py]
        VM[ValidatedModel<br/>core/models.py]
    end

    subgraph Data["ORM Layer"]
        PM[products.Product]
        BM[boxes.ShippingBox]
        OM[orders.Order · OrderItem]
        RM[recommendations.BoxRecommendation]
    end

    subgraph Infra["Infrastructure"]
        CFG[config/settings.py]
        URLS[config/urls.py]
        DB[(SQLite / PostgreSQL)]
        WN[WhiteNoise Middleware]
        LOG[LOGGING config]
    end

    Browser([Warehouse Staff Browser]) --> TPL
    Browser --> AUTHV
    AdminBrowser([Admin Browser]) --> ADMINUI

    TPL --> VIEWS
    VIEWS --> MIXIN
    VIEWS --> OSVC
    VIEWS --> RSVC
    AUTHV --> CFG

    RSVC --> OSVC
    RSVC --> PAME
    RSVC --> BM
    RSVC --> RM
    RSVC --> OM

    OSVC --> OM
    OSVC --> RM

    PM & BM & OM & RM --> VM
    PM & BM & OM & RM --> VAL
    PM & BM & OM & RM --> DB

    ADMINUI --> PM & BM & OM & RM
    CFG --> WN
    CFG --> LOG
    URLS --> VIEWS & AUTHV & ADMINUI
```

---

## 9. Deployment Diagram

Reflects `config/settings.py`, `config/wsgi.py`, and `requirements.txt` (Django, Gunicorn, WhiteNoise, psycopg2-binary).

### Development deployment

```mermaid
flowchart LR
    DEV([Developer])
    RS[manage.py runserver]
    APP[Django Application]
    SQLITE[(db.sqlite3)]

    DEV --> RS
    RS --> APP
    APP --> SQLITE
```

### Production deployment

```mermaid
flowchart TB
    subgraph ClientTier["Client Tier"]
        STAFF([Warehouse Staff Browser])
    end

    subgraph NetworkTier["Network Tier"]
        HTTPS[HTTPS / TLS]
    end

    subgraph AppTier["Application Server"]
        PROXY[Reverse Proxy<br/>e.g. Nginx]
        GUNICORN[Gunicorn WSGI<br/>config.wsgi:application]
        DJANGO[Django 4.2 Application]
        WN[WhiteNoise<br/>StaticFilesStorage]
    end

    subgraph DataTier["Data Tier"]
        PG[(PostgreSQL)]
    end

    subgraph Config["Environment Configuration"]
        ENV[DJANGO_SECRET_KEY<br/>DJANGO_DEBUG=False<br/>DJANGO_ALLOWED_HOSTS<br/>DJANGO_CSRF_TRUSTED_ORIGINS<br/>POSTGRES_*]
    end

    STAFF --> HTTPS
    HTTPS --> PROXY
    PROXY --> GUNICORN
    GUNICORN --> DJANGO
    DJANGO --> WN
    DJANGO --> PG
    ENV -.-> DJANGO

    Note1[python manage.py collectstatic<br/>STATIC_ROOT = staticfiles/]
    Note1 -.-> WN
```

| Node | Technology (as implemented) |
|------|----------------------------|
| WSGI entry | `config.wsgi.application` |
| App server | Gunicorn (`requirements.txt`) |
| Framework | Django 4.2.30 |
| Static files | `STATIC_ROOT`, WhiteNoise `CompressedManifestStaticFilesStorage` (production) |
| Database (dev) | SQLite `db.sqlite3` |
| Database (prod) | PostgreSQL when `POSTGRES_DB` is set |
| Security (prod) | `SECURE_SSL_REDIRECT`, secure cookies, optional HSTS via env |

---

## 10. Order Status State (Reference)

Implemented transitions only:

```mermaid
stateDiagram-v2
    [*] --> PENDING : Order created

    PENDING --> RECOMMENDED : RecommendationService<br/>successful recommendation
    RECOMMENDED --> PACKED : OrderService.confirm_packing

    PENDING --> PENDING : RecommendationService<br/>NO_SUITABLE_BOX
    RECOMMENDED --> RECOMMENDED : RecommendationService<br/>re-recommend allowed

    PACKED --> PACKED : confirm_packing blocked
    PACKED --> PACKED : recommend blocked

    note right of DISPATCHED
        DISPATCHED exists in OrderStatus
        but no implemented transition
    end note
```

---

## Source file index

| Diagram area | Primary source files |
|--------------|---------------------|
| Models / ER | `products/models.py`, `boxes/models.py`, `orders/models.py`, `recommendations/models.py` |
| Services | `orders/services/order_service.py`, `recommendations/services/recommendation_service.py` |
| PAME | `core/utils/dimensions.py` |
| Views / use cases | `*/views.py`, `config/urls.py`, `*/urls.py` |
| Auth | `core/mixins.py`, `config/urls.py` |
| Deployment | `config/settings.py`, `config/wsgi.py`, `requirements.txt` |

---

*Generated from finalized implementation. Suitable for internship / academic submission alongside `docs/ARCHITECTURE.md`.*
