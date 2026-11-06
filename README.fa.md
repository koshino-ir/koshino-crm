<div dir="rtl">

<div align="center">

# کوشینو CRM

**یک CRM مدرن و Multi-Tenant برای آژانس‌های نرم‌افزاری و کسب‌وکارهای خدماتی**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Vue](https://img.shields.io/badge/Vue-3.5-4FC08D?logo=vuedotjs&logoColor=white)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![PWA](https://img.shields.io/badge/PWA-installable-5A0FC8?logo=pwa&logoColor=white)](https://web.dev/progressive-web-apps/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[English](README.en.md) · [فارسی](README.fa.md) · [العربية](README.ar.md)

</div>

---

## فهرست مطالب

1. [معرفی](#معرفی)
2. [امکانات](#امکانات)
3. [پشته فناوری](#پشته-فناوری)
4. [معماری](#معماری)
5. [ساختار دیتابیس](#ساختار-دیتابیس)
6. [مرجع API](#مرجع-api)
7. [شروع سریع](#شروع-سریع)
8. [متغیرهای محیطی](#متغیرهای-محیطی)
9. [تست](#تست)
10. [استقرار](#استقرار)
11. [امنیت](#امنیت)
12. [تصاویر](#تصاویر)
13. [نقشه راه](#نقشه-راه)
14. [مجوز](#مجوز)

---

## معرفی

**کوشینو CRM** یک پلتفرم کامل مدیریت ارتباط با مشتری است که برای تیم‌هایی ساخته شده که می‌فروشند، اجرا می‌کنند و صورت‌حساب صادر می‌کنند — به‌ویژه **آژانس‌های نرم‌افزاری، شرکت‌های مشاوره، و کسب‌وکارهای خدماتی**. چرخه‌ی کامل عمر مشتری را پوشش می‌دهد: از ثبت سرنخ تا بستن معامله، تحویل پروژه، و صدور فاکتور.

این برنامه **Multi-Tenant** است (یک نصب، چندین سازمان با جداسازی کامل داده‌ها)، **چندزبانه** (فارسی، انگلیسی، عربی با چیدمان بومی راست‌به‌چپ)، و **قابل نصب به‌صورت PWA** روی دسکتاپ و موبایل.

این پروژه یک پیاده‌سازی مرجع در سطح محصول است که معماری تمیز، اصول SOLID، تست‌های جامع، و مهندسی مدرن فرانت‌اند را به نمایش می‌گذارد.

---

## امکانات

### مدیریت فروش و خط فروش
- **تخته کانبان** با drag & drop بین مراحل
- **انتقال خودکار وضعیت** — وقتی معامله‌ای به مرحله‌ی «برنده» می‌رود، وضعیتش هم خودکار به `won` تغییر می‌کند
- **جمع درآمد در هر ستون** به‌صورت بلادرنگ
- **چندین خط فروش** در هر سازمان، هر کدام با مراحل اختصاصی
- **خط فروش پیش‌فرض خودکار** برای سازمان‌های جدید (Qualified → Proposal → Negotiation → Won / Lost)

### هسته CRM
- **شرکت‌ها** — مشتریان و سرنخ‌ها با صنعت، اطلاعات تماس، و یادداشت
- **مخاطبین** — افراد در شرکت‌ها با پرچم اصلی و سمت
- **سرنخ‌ها** — مشتریان بالقوه پیش از واجد شرایط شدن
- **معاملات** — فرصت‌ها با مبلغ، واحد پول، احتمال، و تاریخ بستن احتمالی
- **پروژه‌ها** — تحویل‌شدنی‌ها بعد از بسته شدن معامله، با وضعیت و بودجه
- **فاکتورها** — شماره‌گذاری خودکار در هر سازمان، با محاسبه‌ی مالیات و پیگیری پرداخت

### تبدیل سرنخ
- تبدیل یک‌کلیکی سرنخ به معامله
- ساخت خودکار شرکت در صورت نبود
- علامت‌گذاری سرنخ به `qualified` و اتصال دو رکورد

### فعالیت‌ها و وظایف
- **گزارش فعالیت** — تماس‌ها، ایمیل‌ها، جلسات، و یادداشت‌ها، به‌صورت چندریختی به معاملات، سرنخ‌ها، مخاطبین، یا شرکت‌ها متصل
- **وظایف** — اولویت (کم/متوسط/زیاد/فوری)، تاریخ سررسید، مسئول، تکمیل/بازگشایی
- **هایلایت تأخیر** — وظایف سررسید گذشته به‌صورت بصری متمایز

### داشبورد
- **شاخص‌های زنده** — تعداد و ارزش معاملات باز، معاملات برنده، شرکت‌ها، سرنخ‌ها، وظایف باز، وظایف تأخیری
- **قیف فروش** — تعداد و ارزش معاملات در هر مرحله
- **نمودار درآمد** — جمع شش‌ماهه‌ی معاملات برنده (بر پایه‌ی SVG، بدون وابستگی به کتابخانه‌ی چارت)
- **فید فعالیت‌های اخیر** — ۱۰ تعامل آخر

### Multi-Tenancy
- جداسازی داده‌ها در سطح هر سازمان از طریق `organization_id` در همه‌ی مدل‌های دامنه
- هدر `X-Organization-Id` سازمان فعال را تعیین می‌کند
- بازگشت خودکار به اولین عضویت فعال کاربر
- نقش‌های عضویت: `owner`، `admin`، `member`
- جریان دعوت‌نامه در هر سازمان با توکن‌های منقضی‌شدنی

### احراز هویت و مجوزها
- **JWT در کوکی HttpOnly** (محافظت در برابر XSS)
- **محافظت CSRF** با الگوی double-submit
- **ورود با Google OAuth 2.0**
- **مجوزهای مبتنی بر نقش** در سطح view
- **اعتبارسنجی رمز عبور** با validatorهای Django
- **هش Argon2** برای رمز عبور
- **محدودیت نرخ درخواست** روی endpointهای احراز هویت و دعوت‌نامه

### بین‌المللی‌سازی
- رابط کامل **فارسی / انگلیسی / عربی**
- **سوئیچ خودکار RTL** برای چیدمان
- پراپرتی‌های منطقی CSS (`ms-`، `me-`، `ps-`، `pe-`) در همه‌جا
- ترجیح زبان هر کاربر ذخیره می‌شود
- تاریخ‌ها، اعداد، و placeholderهای بومی

### PWA
- قابل نصب روی Android، iOS، و دسکتاپ
- استراتژی کش **Service Worker**:
  - Network-first برای API
  - Cache-first برای فونت‌ها، تصاویر، assetهای استاتیک
- **صفحه‌ی آفلاین** با قابلیت تلاش دوباره
- **اعلان نصب** و **اعلان به‌روزرسانی** سفارشی (reload اختیاری)
- **بنر آفلاین** هنگام از دست رفتن شبکه

### حسابرسی و امنیت
- **لاگ حسابرسی** روی ایجاد/به‌روزرسانی معاملات و شرکت‌ها
- **آپلود امن فایل** — whitelist پسوند، حداکثر ۱۰ مگابایت، اعتبارسنجی MIME
- **دانلود احرازشده** — پیوست‌ها هرگز از طریق MEDIA_URL استاتیک expose نمی‌شوند
- **حذف نرم** با `deleted_at` و قابلیت بازیابی
- **هش Argon2** برای رمز عبور
- **هدرهای امنیتی** در production (HSTS، آماده‌ی CSP، X-Frame-Options)

---

## پشته فناوری

### بک‌اند
| لایه | فناوری |
|------|--------|
| زبان | Python 3.12 |
| فریم‌ورک | Django 5.1 + Django REST Framework 3.15 |
| دیتابیس | PostgreSQL 16 |
| کش/بروکر | Redis 7 |
| Async | Celery 5.4 |
| احراز هویت | `djangorestframework-simplejwt` (کوکی HttpOnly) |
| OAuth | Google OAuth 2.0 |
| مستندات | `drf-spectacular` (OpenAPI 3.1) |
| تست | pytest + pytest-django + factory_boy |

### فرانت‌اند
| لایه | فناوری |
|------|--------|
| فریم‌ورک | Vue 3.5 (Composition API + `<script setup>`) |
| زبان | TypeScript 5.6 (حالت strict) |
| بیلد | Vite 6 |
| استایل | Tailwind CSS v4 (توکن‌های CSS-first) |
| State | Pinia + TanStack Query |
| Routing | Vue Router 4 |
| i18n | vue-i18n 10 |
| Drag & drop | vue-draggable-plus |
| PWA | vite-plugin-pwa + Workbox |
| آیکون‌ها | lucide-vue-next |

### زیرساخت
| لایه | فناوری |
|------|--------|
| ارکستراسیون dev | Docker Compose (`docker-compose.infra.yml`) |
| ارکستراسیون prod | Docker Compose (`docker-compose.prod.yml`) |
| سرو فرانت‌اند | Nginx 1.27 (هدرهای امنیتی، gzip، کش immutable asset) |
| سرو بک‌اند | Gunicorn (۴ worker) |
| TLS | Certbot / Let's Encrypt |
| CI/CD | GitHub Actions |

---

## معماری

### ساختار پوشه‌ها

```
koshino-crm/
├── backend/
│   ├── config/                 پیکربندی پروژه Django
│   │   ├── settings/
│   │   │   ├── base.py         تنظیمات مشترک
│   │   │   ├── dev.py          محیط توسعه لوکال
│   │   │   ├── test.py         محیط تست ایزوله (cache locmem، هش MD5)
│   │   │   └── prod.py         production سخت‌شده
│   │   ├── urls.py             URL conf ریشه
│   │   ├── asgi.py
│   │   ├── wsgi.py
│   │   └── celery.py
│   ├── apps/
│   │   ├── common/             BaseModel، exceptions، pagination، mixins، permissions
│   │   ├── accounts/           User، Organization، Membership، Invitation، JWT، OAuth
│   │   ├── crm/                Company، Contact، Pipeline، Stage، Lead، Deal
│   │   ├── activities/         Activity، Task
│   │   ├── audit/              AuditLog با signal-based auto-logging
│   │   ├── dashboard/          Selectorها و viewهای تجمیع
│   │   ├── projects/           Project، Invoice
│   │   ├── attachments/        آپلود امن فایل
│   │   └── core/               Health check و ابزارهای مشترک
│   ├── tests/
│   │   ├── conftest.py         fixtureهای مشترک
│   │   ├── accounts/           تست‌های auth، org، invitation
│   │   ├── crm/                تست‌های deal، lead، kanban
│   │   ├── activities/         تست‌های activity و task
│   │   ├── projects/           تست‌های project و invoice
│   │   ├── attachments/        تست‌های امنیت آپلود
│   │   └── dashboard/          تست‌های تجمیع
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── core/
│   │   │   ├── api/            کلاینت Axios، interceptorها، ماژول‌های endpoint
│   │   │   ├── stores/         Pinia storeها (auth، organization، ui)
│   │   │   ├── router/         تعریف routeها و guardها
│   │   │   ├── i18n/           فایل‌های locale و پیکربندی
│   │   │   ├── pwa/            ثبت Service Worker
│   │   │   ├── seo/            مدیریت meta tag
│   │   │   ├── config.ts
│   │   │   └── utils/
│   │   ├── modules/
│   │   │   ├── auth/           صفحات login، register، callback
│   │   │   ├── landing/        صفحه‌ی Landing بازاریابی
│   │   │   ├── dashboard/      KPI cardها، funnel، نمودار درآمد
│   │   │   ├── deals/          تخته Kanban، صفحه‌ی جزئیات
│   │   │   ├── companies/      CRUD با جستجو
│   │   │   ├── contacts/       CRUD متصل به شرکت
│   │   │   ├── leads/          CRUD با دیالوگ تبدیل
│   │   │   ├── tasks/          CRUD با فیلتر وضعیت
│   │   │   ├── activities/     نمای تایم‌لاین
│   │   │   ├── projects/       CRUD با انتخاب مشتری
│   │   │   ├── invoices/       CRUD با اقدام mark-paid
│   │   │   └── settings/       سازمان، اعضا، ترجیحات
│   │   ├── shared/
│   │   │   ├── components/
│   │   │   │   ├── ui/         Button، Input، Select، Card، Avatar، Spinner، Skeleton، Textarea
│   │   │   │   ├── layout/     Sidebar، Topbar، UserMenu، LangSwitcher، ThemeToggle، PwaPrompts
│   │   │   │   ├── DataTable.vue
│   │   │   │   ├── Pagination.vue
│   │   │   │   ├── ConfirmDialog.vue
│   │   │   │   └── FormModal.vue
│   │   │   ├── layouts/        AppLayout، AuthLayout
│   │   │   └── composables/
│   │   ├── assets/
│   │   │   └── styles/main.css توکن‌های طراحی
│   │   ├── App.vue
│   │   └── main.ts
│   ├── public/                 manifest PWA، service worker، صفحه‌ی آفلاین
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── package.json
├── docker/
│   ├── backend.Dockerfile      Multi-stage
│   ├── frontend.Dockerfile     Multi-stage
│   ├── nginx.conf
│   └── nginx.prod.conf
├── docker-compose.yml          production full stack
├── docker-compose.infra.yml    dev لوکال (فقط db + redis)
├── docker-compose.prod.yml     بیلد production
├── .env.example
├── .env.prod.example
└── README.md                   ← این فایل
```

### لایه‌بندی بک‌اند

بک‌اند از یک **معماری لایه‌ای** سخت‌گیرانه پیروی می‌کند:

1. **Viewها** (نازک) — parse درخواست، واگذاری به service یا selector، پاسخ envelope
2. **Serializerها** — اعتبارسنجی ورودی، resolve کلیدهای خارجی در برابر org فعلی
3. **Serviceها** (`services/*.py`) — منطق کسب‌وکار، عملیات تراکنشی
4. **Selectorها** (`selectors.py`) — کوئری‌های پیچیده‌ی N+1-safe
5. **مدل‌ها** — قیود یکپارچگی داده، ایندکس‌ها، ارث‌بری از `BaseModel`

**مثال — جریان ایجاد Deal:**

```
POST /api/v1/deals/
   ↓
DealListCreateView (OrgScopedViewMixin + EnvelopeModelViewMixin)
   ↓
DealSerializer.validate_* → resolve company_id، pipeline_id، stage_id در برابر org
   ↓
deal_service.create_deal (atomic)
   ↓   محاسبه order (max+1 در stage)
   ↓   مقدار پیش‌فرض stage اولین stage در pipeline
Deal.objects.create
   ↓
AuditLog (via signal)
   ↓
پاسخ envelope { success, data, message, errors, meta }
```

### Envelope API

هر endpoint برمی‌گرداند:

```json
{
  "success": true,
  "data": { ... },
  "message": "OK",
  "errors": null,
  "meta": { "count": 42, "page": 1, "page_size": 20, "total_pages": 3 }
}
```

این از طریق سه فایل تضمین می‌شود:
- `apps/common/responses.py` (کلاس APIResponse)
- `apps/common/exceptions.py` (custom_exception_handler)
- `apps/common/pagination.py` (EnvelopePagination)

---

## ساختار دیتابیس

### جداول اصلی

| جدول | کاربرد | ستون‌های کلیدی |
|------|--------|----------------|
| `accounts_user` | کاربر سفارشی (ورود با ایمیل) | `email` (unique)، `google_id`، `language` |
| `accounts_organization` | مستأجر | `slug` (unique)، `default_currency`، `default_language` |
| `accounts_membership` | اتصال کاربر ↔ Org | `role`، `is_active` |
| `accounts_invitation` | دعوت‌های معلق | `token`، `expires_at` |
| `crm_company` | سازمان مشتری | `name`، `industry`، `owner` |
| `crm_contact` | فرد در شرکت | `first_name`، `email`، `company` FK |
| `crm_pipeline` | خط فروش | `name`، `is_default` |
| `crm_stage` | مرحله‌ی خط | `order`، `color`، `is_won`، `is_lost` |
| `crm_lead` | مشتری بالقوه پیش از واجد شرایط شدن | `status`، `source`، `owner` |
| `crm_deal` | فرصت | `amount`، `stage` FK، `order`، `status` |
| `activities_activity` | تعامل ثبت‌شده | `type`، `occurred_at` + FK چندریختی |
| `activities_task` | کار | `priority`، `due_date`، `status` |
| `projects_project` | تحویل‌شدنی | `status`، `budget`، `client_company` |
| `projects_invoice` | سند صورتحساب | `number` (unique per org)، `total`، `paid_at` |
| `audit_audit_log` | پیگیری تغییرات | `action`، `entity_type`، `entity_id`، `changes` JSONB |
| `attachments_attachment` | فایل | `file`، `mime_type`، `size`، FK چندریختی |

### تصمیمات طراحی

- **کلید اصلی UUID** — مقاوم در برابر collision، امن برای expose در URL
- **`organization_id` در همه‌ی جداول دامنه** — فعال‌سازی Multi-Tenancy سطح-ردیف بدون پیچیدگی schema-per-tenant
- **حذف نرم** (`deleted_at`) با `ActiveManager` — قابلیت بازیابی و مسیر حسابرسی
- **ایندکس‌های ترکیبی** روی الگوهای فیلتر پرترافیک:
  - `(organization_id, status, owner_id)` روی Deal
  - `(organization_id, pipeline_id, stage_id)` روی Deal
  - `(organization_id, assigned_to_id, status, due_date)` روی Task
- **قید unique شرطی** روی شماره‌ی فاکتور در هر org (با احترام به حذف نرم)
- **`order` عددی** روی Stage و Deal — فعال‌سازی ترتیب drag-and-drop بدون جدول اضافه

---

## مرجع API

مستندات تعاملی کامل در **`/api/docs/`** (Swagger UI) پس از اجرای بک‌اند در دسترس است.

### قواعد

| جنبه | قاعده |
|------|-------|
| Base URL | `/api/v1/` |
| احراز هویت | JWT در کوکی HttpOnly |
| CSRF | هدر `X-CSRFToken` برای POST/PUT/PATCH/DELETE الزامی |
| Multi-tenancy | هدر `X-Organization-Id` (اختیاری؛ fallback به اولین عضویت) |
| صفحه‌بندی | `?page=1&page_size=20` (حداکثر ۱۰۰) |
| فیلترینگ | پارامترهای query اختصاصی هر endpoint (پایین‌تر) |
| مرتب‌سازی | `?ordering=-created_at` در صورت پشتیبانی |
| پاسخ | Envelope `{ success, data, message, errors, meta }` |

### خلاصه‌ی endpointها

**احراز هویت**
- `POST /auth/register/` — ایجاد کاربر + سازمان
- `POST /auth/login/` — set کوکی‌ها
- `POST /auth/logout/` — پاک‌کردن کوکی‌ها
- `POST /auth/token/refresh/` — چرخش access token
- `GET|PATCH /auth/me/` — پروفایل
- `POST /auth/password/change/`
- `GET /auth/csrf/` — دریافت CSRF token
- `GET /auth/google/` — URL رضایت OAuth
- `GET /auth/google/callback/` — callback OAuth (set کوکی‌ها، redirect)
- `POST /auth/invitations/accept/`

**سازمان‌ها**
- `GET|POST /organizations/`
- `GET|PATCH|DELETE /organizations/{id}/`
- `GET /organizations/{id}/members/`
- `PATCH|DELETE /organizations/{id}/members/{mid}/`
- `POST /organizations/{id}/invitations/`

**CRM**
- `GET|POST /companies/` — فیلتر: `search`, `industry`, `owner`
- `GET|PATCH|DELETE /companies/{id}/`
- `GET|POST /contacts/` — فیلتر: `search`, `company`, `owner`
- `GET|PATCH|DELETE /contacts/{id}/`
- `GET|POST /pipelines/`
- `GET|PATCH|DELETE /pipelines/{id}/`
- `POST /pipelines/ensure-default/` — idempotent
- `GET|POST /pipelines/{id}/stages/`
- `PATCH|DELETE /stages/{id}/`
- `GET|POST /leads/` — فیلتر: `search`, `status`, `source`, `owner`
- `GET|PATCH|DELETE /leads/{id}/`
- `POST /leads/{id}/convert/` — ایجاد deal، نیازمند `pipeline_id`
- `GET|POST /deals/` — فیلتر: `search`, `pipeline`, `stage`, `status`, `owner`
- `GET|PATCH|DELETE /deals/{id}/`
- `GET /deals/kanban/?pipeline={id}` — ساختار board آماده برای UI
- `PATCH /deals/{id}/move/` — `{ stage_id, order? }` برای drag-and-drop

**فعالیت‌ها**
- `GET|POST /activities/` — فیلتر: `search`, `type`, `deal`, `lead`, `company`, `date_from`, `date_to`
- `GET|PATCH|DELETE /activities/{id}/`
- `GET|POST /tasks/` — فیلتر: `search`, `status`, `priority`, `assigned_to`, `deal`, `due_before`
- `GET|PATCH|DELETE /tasks/{id}/`
- `POST /tasks/{id}/complete/`
- `POST /tasks/{id}/reopen/`

**پروژه‌ها و فاکتورها**
- `GET|POST /projects/` — فیلتر: `search`, `status`, `client`, `owner`
- `GET|PATCH|DELETE /projects/{id}/`
- `GET|POST /invoices/` — فیلتر: `search`, `status`, `project`
- `GET|PATCH|DELETE /invoices/{id}/`
- `POST /invoices/{id}/mark-paid/`

**داشبورد**
- `GET /dashboard/stats/` — شیء KPI
- `GET /dashboard/funnel/` — آرایه‌ی مراحل با تعداد و جمع
- `GET /dashboard/revenue/?months=6` — جمع ماهانه
- `GET /dashboard/recent-activities/` — ۱۰ مورد آخر

**جستجو و حسابرسی**
- `GET /search/?q={query}` — جستجوی سراسری در شرکت‌ها، مخاطبین، معاملات، سرنخ‌ها
- `GET /audit-logs/` — فیلتر: `entity_type`, `entity_id` (فقط owner/admin)

**پیوست‌ها**
- `GET|POST /attachments/` — آپلود multipart، فیلتر بر اساس `deal`, `company`, `project`
- `GET|DELETE /attachments/{id}/`
- `GET /attachments/{id}/download/` — stream احرازشده

---

## شروع سریع

### پیش‌نیازها

- **Python 3.12+**
- **Node 20+**
- **Docker** (فقط برای Postgres + Redis در dev)
- **Git**

### توسعه لوکال (پیشنهادی)

```bash
git clone https://github.com/koshino-ir/koshino-crm.git
cd koshino-crm

# 1. محیط
cp .env.example .env

# 2. زیرساخت (Postgres روی :55432، Redis روی :56379)
docker compose -f docker-compose.infra.yml up -d

# 3. بک‌اند
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python manage.py migrate
python manage.py runserver
# → http://localhost:8000  (health: /api/v1/health/، docs: /api/docs/)

# 4. فرانت‌اند (ترمینال جدید)
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

سپس **http://localhost:5173** را باز کن، یک سازمان بساز، و شروع کن.

### Docker کامل (مشابه production)

```bash
cp .env.prod.example .env.prod
# .env.prod را ویرایش کن — DJANGO_SECRET_KEY، رمز DB، رمز Redis را امن بساز

# تولید کلید امن
python -c "import secrets; print(secrets.token_urlsafe(50))"

docker compose -f docker-compose.prod.yml --env-file .env.prod up --build -d
# → http://localhost
```

---

## متغیرهای محیطی

### توسعه (`.env`)

```env
# Django
DJANGO_SECRET_KEY=dev-insecure-change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# دیتابیس
POSTGRES_DB=koshino_crm
POSTGRES_USER=koshino
POSTGRES_PASSWORD=dev-password
DATABASE_URL=postgres://koshino:dev-password@localhost:55432/koshino_crm

# Redis
REDIS_PASSWORD=dev-redis-password
REDIS_URL=redis://:dev-redis-password@localhost:56379/0

# CORS / CSRF
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:8000
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://localhost:8000

# Google OAuth (اختیاری)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback/
FRONTEND_URL=http://localhost:5173
```

### Production (`.env.prod`)

فایل `.env.prod.example` در مخزن را ببینید.

---

## تست

```bash
cd backend
source .venv/bin/activate
pytest -q
```

پوشش تست:
- جریان‌های احراز هویت (ثبت‌نام، ورود، خروج، چرخش token، تغییر رمز)
- جداسازی Multi-tenant (دسترسی cross-org رد می‌شود)
- ایجاد Deal، گروه‌بندی kanban، جابه‌جایی stage
- تبدیل Lead (ایجاد Deal، علامت qualified، عدم امکان تبدیل دوباره)
- شماره‌گذاری فاکتور (unique per org)، mark-paid، اعتبارسنجی تاریخ‌ها
- امنیت آپلود پیوست (whitelist پسوند، محدودیت حجم، قاعده‌ی single-target)
- احراز هویت دانلود پیوست
- ایجاد لاگ حسابرسی روی save Deal/Company
- تجمیع‌های داشبورد (KPI، funnel، revenue)
- جستجوی سراسری در موجودیت‌ها

محیط تست استفاده می‌کند از:
- `config.settings.test` (cache locmem، هش MD5 برای سرعت)
- محدودیت throttle درون‌حافظه‌ای (بدون آلودگی بین اجراها)
- پوشه‌ی temp برای فایل‌های media (بدون مشکل permission)

---

## استقرار

### معماری production

```
                   ┌─────────────────────────┐
       :80/:443 ──▶│ Nginx (frontend + proxy) │
                   └───────────┬─────────────┘
                               │
                    ┌──────────┴───────────┐
                    ▼                      ▼
         ┌──────────────────┐   ┌────────────────────┐
         │  Vue SPA (dist)  │   │  /api → Gunicorn   │
         └──────────────────┘   └─────────┬──────────┘
                                          │
                          ┌───────────────┼───────────────┐
                          ▼               ▼               ▼
                    ┌──────────┐   ┌──────────┐   ┌──────────┐
                    │ Postgres │   │  Redis   │   │  Celery  │
                    └──────────┘   └──────────┘   └──────────┘
```

### گام‌ها روی VPS تازه

1. **آماده‌سازی سرور** — Ubuntu 22.04+ یا Debian 12، حداقل ۲ vCPU / ۴ گیگ رم
2. **نصب Docker & Compose**
3. **Firewall** — فقط 22، 80، 443 باز باشد
4. **DNS** — رکورد A به IP سرور
5. **استقرار** — کپی مخزن، ساخت `.env.prod`، اجرای `docker compose -f docker-compose.prod.yml up -d --build`
6. **TLS** — Certbot + پیکربندی SSL در Nginx (به `docs/deployment.md` مراجعه کنید)
7. **پشتیبان‌گیری** — `pg_dump` روزانه + سیاست نگهداری

### نکات مقیاس‌پذیری

- **Gunicorn workers** — `(2 × cores) + 1` پیش‌فرض مناسب؛ بر اساس بار تنظیم کنید
- **Celery** — تقسیم به queueها (`default`, `email`, `reports`) برای جداسازی
- **Postgres** — connection pooling با PgBouncer بالای ~۵۰ worker
- **Redis** — نمونه‌های جدا برای cache و broker در مقیاس بالا
- **فایل‌های استاتیک** — CDN در جلوی `/assets/*`

---

## امنیت

برنامه دفاع چندلایه‌ای اجرا می‌کند:

| لایه | کنترل |
|------|-------|
| **انتقال** | HTTPS اجباری (HSTS با `includeSubDomains`، `preload`) |
| **نشست** | JWT در کوکی HttpOnly + Secure + SameSite=Lax |
| **CSRF** | توکن double-submit + هدر `X-CSRFToken` روی mutationها |
| **احراز هویت** | هش Argon2، validatorهای رمز، محدودیت نرخ |
| **API** | چک object-level در هر view نسبت به org |
| **داده** | UUID PK (بدون enumeration)، حذف نرم (مسیر حسابرسی) |
| **فایل‌ها** | whitelist پسوند + MIME + حجم، دانلود احرازشده، MEDIA_URL مستقیم ممنوع |
| **هدرها** | `X-Frame-Options`، `X-Content-Type-Options`، `Referrer-Policy`، `Permissions-Policy` |
| **لاگ** | لاگ حسابرسی روی موجودیت‌های حساس، لاگ production ساختاریافته |
| **وابستگی‌ها** | `ruff` + `mypy` در CI، توصیه‌ی `pip-audit` |

---

## تصاویر


| | |
|---|---|
| **کانبان معاملات** | **داشبورد** |
| ![Kanban](docs/screenshots/fa/deals-kanban.png) | ![Dashboard](docs/screenshots/fa/dashboard.png) |
| **شرکت‌ها** | **ورود** |
| ![Companies](docs/screenshots/fa/companies.png) | ![Login](docs/screenshots/fa/login.png) |

---

## نقشه راه

### انجام‌شده
- [x] MVP: CRM با خط فروش کامل، معاملات، شرکت‌ها، مخاطبین، سرنخ‌ها
- [x] وظایف و فعالیت‌ها
- [x] پروژه‌ها و فاکتورها
- [x] داشبورد با نمودارها
- [x] جداسازی Multi-tenant
- [x] احراز هویت JWT در کوکی + Google OAuth
- [x] رابط سه‌زبانه با RTL بومی
- [x] PWA (نصب‌پذیر، آفلاین، service worker)
- [x] لاگ حسابرسی
- [x] Docker production + Nginx + هدرهای امنیتی

### برنامه‌ریزی‌شده
- [ ] اعلان‌های ایمیلی (دعوت‌نامه، یادآور)
- [ ] خروجی CSV/Excel برای معاملات، فاکتورها، مخاطبین
- [ ] رابط آپلود پیوست در صفحه‌ی جزئیات Deal
- [ ] یکپارچه‌سازی Webhook (Slack، Zapier)
- [ ] گزارش‌های فعالیت تیم (به تفکیک عضو)
- [ ] تنظیم خودکار احتمال Deal بر اساس تاریخچه‌ی stage
- [ ] عملیات گروهی (assign گروهی، update گروهی)
- [ ] فیلدهای سفارشی برای هر سازمان

---

## مجوز

مجوز MIT — فایل [LICENSE](LICENSE) را ببینید.

---

## نویسنده

**کوشینو** — [github.com/koshino-ir](https://github.com/koshino-ir)

سؤال، بازخورد، یا پروژه‌ای در ذهن دارید؟  
📧 `info@koshino.ir`

---

<div align="center">

**ساخته‌شده با ❤️ برای تیم‌هایی که می‌فروشند و اجرا می‌کنند.**

⭐ اگر مفید بود، به این مخزن ستاره بدهید.

</div>

</div>
