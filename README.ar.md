<div dir="rtl">

<div align="center">

# Koshino CRM

**نظام CRM حديث ومتعدد المستأجرين لوكالات البرمجيات والأعمال الخدمية**

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

## جدول المحتويات

1. [نظرة عامة](#نظرة-عامة)
2. [المزايا](#المزايا)
3. [حزمة التقنيات](#حزمة-التقنيات)
4. [البنية](#البنية)
5. [مخطط قاعدة البيانات](#مخطط-قاعدة-البيانات)
6. [مرجع API](#مرجع-api)
7. [البدء السريع](#البدء-السريع)
8. [متغيرات البيئة](#متغيرات-البيئة)
9. [الاختبار](#الاختبار)
10. [النشر](#النشر)
11. [الأمان](#الأمان)
12. [لقطات الشاشة](#لقطات-الشاشة)
13. [خارطة الطريق](#خارطة-الطريق)
14. [الترخيص](#الترخيص)

---

## نظرة عامة

**Koshino CRM** منصة متكاملة لإدارة علاقات العملاء، مبنية للفرق التي تبيع وتنفذ وتصدر الفواتير — وتحديدًا **وكالات البرمجيات، شركات الاستشارات، والأعمال الخدمية**. تغطي دورة حياة العميل الكاملة: من التقاط العميل المحتمل عبر إغلاق الصفقة، تسليم المشروع، وإصدار الفواتير.

التطبيق **متعدد المستأجرين** (تثبيت واحد يخدم عدة مؤسسات مع عزل صارم للبيانات)، و**متعدد اللغات** (الفارسية والإنجليزية والعربية مع تخطيط RTL أصلي)، و**قابل للتثبيت كتطبيق ويب تقدمي (PWA)** على سطح المكتب والجوال.

هذا المشروع هو تنفيذ مرجعي بجودة الإنتاج يُظهر بنية نظيفة، ومبادئ SOLID، واختبارًا شاملاً، وهندسة واجهة أمامية حديثة.

---

## المزايا

### إدارة المبيعات وخط الأنابيب
- **لوحة كانبان** بالسحب والإفلات بين المراحل
- **انتقال تلقائي للحالة** — عند نقل صفقة إلى مرحلة "won" تتحدث حالتها تلقائيًا
- **إجمالي لكل مرحلة** — يتم تجميع الإيرادات لكل عمود في الوقت الفعلي
- **خطوط أنابيب متعددة** لكل مؤسسة، ولكل منها مراحل مخصصة
- **خط أنابيب افتراضي تلقائي** للمؤسسات الجديدة (Qualified → Proposal → Negotiation → Won / Lost)

### نواة CRM
- **الشركات** — العملاء والعملاء المحتملون، مع القطاع ومعلومات الاتصال والملاحظات
- **جهات الاتصال** — الأشخاص في الشركات، مع علامة أساسي والمنصب
- **العملاء المحتملون** — العملاء الواردون قبل التأهيل
- **الصفقات** — الفرص مع المبلغ والعملة والاحتمال والتاريخ المتوقع للإغلاق
- **المشاريع** — المخرجات بعد إغلاق الصفقة، مع الحالة والميزانية
- **الفواتير** — ترقيم تلقائي لكل مؤسسة، مع حساب الضريبة وتتبع الدفع

### تحويل العميل المحتمل
- تحويل بنقرة واحدة من عميل محتمل إلى صفقة
- إنشاء شركة تلقائيًا إذا لم يكن للعميل شركة
- تعليم العميل المحتمل كـ `qualified` وربط السجلين

### الأنشطة والمهام
- **سجل الأنشطة** — المكالمات، رسائل البريد، الاجتماعات، والملاحظات، مرتبطة متعددة الأشكال بالصفقات أو العملاء المحتملين أو جهات الاتصال أو الشركات
- **المهام** — الأولوية (منخفضة/متوسطة/عالية/عاجلة)، تواريخ الاستحقاق، المسؤول، إكمال/إعادة فتح
- **إبراز التأخر** — تظهر المهام المتأخرة بصريًا

### لوحة التحكم
- **مؤشرات حية** — عدد وقيمة الصفقات المفتوحة، الصفقات المكسوبة، الشركات، العملاء المحتملون، المهام المفتوحة، المهام المتأخرة
- **قمع المبيعات** — عدد وقيمة الصفقات لكل مرحلة
- **مخطط الإيرادات** — مجموع ستة أشهر من الصفقات المكسوبة (قائم على SVG، بدون مكتبة رسوم بيانية)
- **تغذية آخر الأنشطة** — 10 أحدث التفاعلات

### تعدد المستأجرين
- عزل البيانات على مستوى الصف عبر `organization_id` في كل نموذج نطاق
- هيدر `X-Organization-Id` يحدد السياق النشط
- رجوع تلقائي إلى أول عضوية نشطة للمستخدم
- أدوار العضوية: `owner`، `admin`، `member`
- تدفق دعوة لكل مؤسسة مع رموز منتهية الصلاحية

### المصادقة والتفويض
- **JWT في كوكيز HttpOnly** (محمي من XSS)
- **حماية CSRF** عبر double-submit
- **تسجيل الدخول بـ Google OAuth 2.0**
- **أذونات حسب الدور** مفروضة على مستوى العرض
- **التحقق من كلمة المرور** عبر مدققات Django
- **تجزئة Argon2** لكلمات المرور
- **تحديد معدل الطلبات** على نقاط نهاية المصادقة والدعوات

### التدويل
- واجهة كاملة **بالفارسية / الإنجليزية / العربية**
- **تبديل تخطيط RTL تلقائي**
- خصائص CSS منطقية (`ms-`، `me-`، `ps-`، `pe-`) في كل مكان
- تفضيل اللغة لكل مستخدم محفوظ
- تواريخ وأرقام وعناصر نائبة محلية

### PWA
- قابل للتثبيت على Android و iOS وسطح المكتب
- استراتيجية تخزين مؤقت **Service Worker**:
  - Network-first لواجهة API
  - Cache-first للخطوط والصور والأصول الثابتة
- **صفحة عدم اتصال** مع إعادة المحاولة
- **إشعار تثبيت** و**إشعار تحديث** مخصص (إعادة تحميل اختيارية)
- **شريط عدم اتصال** عند فقدان الشبكة

### التدقيق والأمان
- **سجل تدقيق** على إنشاء/تحديث الصفقات والشركات
- **رفع ملفات آمن** — قائمة بيضاء للامتدادات، 10 ميجابايت كحد أقصى، تحقق MIME
- **تنزيلات موثّقة** — المرفقات لا تُكشف أبدًا عبر MEDIA_URL الثابت
- **حذف ناعم** مع `deleted_at` وإمكانية الاستعادة
- **تجزئة Argon2** لكلمات المرور
- **رؤوس أمان** في الإنتاج (HSTS، جاهز لـ CSP، X-Frame-Options)

---

## حزمة التقنيات

### الواجهة الخلفية
| الطبقة | التقنية |
|--------|---------|
| اللغة | Python 3.12 |
| الإطار | Django 5.1 + Django REST Framework 3.15 |
| قاعدة البيانات | PostgreSQL 16 |
| التخزين المؤقت/الوسيط | Redis 7 |
| غير متزامن | Celery 5.4 |
| المصادقة | `djangorestframework-simplejwt` (كوكيز HttpOnly) |
| OAuth | Google OAuth 2.0 |
| التوثيق | `drf-spectacular` (OpenAPI 3.1) |
| الاختبار | pytest + pytest-django + factory_boy |

### الواجهة الأمامية
| الطبقة | التقنية |
|--------|---------|
| الإطار | Vue 3.5 (Composition API + `<script setup>`) |
| اللغة | TypeScript 5.6 (وضع صارم) |
| البناء | Vite 6 |
| التنسيق | Tailwind CSS v4 (رموز CSS-first) |
| الحالة | Pinia + TanStack Query |
| التوجيه | Vue Router 4 |
| i18n | vue-i18n 10 |
| السحب والإفلات | vue-draggable-plus |
| PWA | vite-plugin-pwa + Workbox |
| الأيقونات | lucide-vue-next |

### البنية التحتية
| الطبقة | التقنية |
|--------|---------|
| تنسيق dev | Docker Compose (`docker-compose.infra.yml`) |
| تنسيق prod | Docker Compose (`docker-compose.prod.yml`) |
| خدمة الواجهة | Nginx 1.27 (رؤوس أمان، gzip، تخزين مؤقت للأصول) |
| خدمة الخلفية | Gunicorn (4 عمال) |
| TLS | Certbot / Let's Encrypt |
| CI/CD | GitHub Actions |

---

## البنية

### هيكل الدلائل

```
koshino-crm/
├── backend/
│   ├── config/                 إعدادات مشروع Django
│   │   ├── settings/
│   │   │   ├── base.py         إعدادات مشتركة
│   │   │   ├── dev.py          تطوير محلي
│   │   │   ├── test.py         بيئة اختبار معزولة (locmem cache، تجزئة MD5)
│   │   │   └── prod.py         إنتاج محصّن
│   │   ├── urls.py             URL conf الجذر
│   │   ├── asgi.py
│   │   ├── wsgi.py
│   │   └── celery.py
│   ├── apps/
│   │   ├── common/             BaseModel، استثناءات، تقسيم صفحات، mixins، أذونات
│   │   ├── accounts/           User، Organization، Membership، Invitation، JWT، OAuth
│   │   ├── crm/                Company، Contact، Pipeline، Stage، Lead، Deal
│   │   ├── activities/         Activity، Task
│   │   ├── audit/              AuditLog مع تسجيل تلقائي بالإشارات
│   │   ├── dashboard/          Selectors و views التجميع
│   │   ├── projects/           Project، Invoice
│   │   ├── attachments/        رفع ملفات آمن
│   │   └── core/               Health check والأدوات المشتركة
│   ├── tests/
│   │   ├── conftest.py         fixtures مشتركة
│   │   ├── accounts/           اختبارات auth، org، invitation
│   │   ├── crm/                اختبارات deal، lead، kanban
│   │   ├── activities/         اختبارات activity و task
│   │   ├── projects/           اختبارات project و invoice
│   │   ├── attachments/        اختبارات أمان الرفع
│   │   └── dashboard/          اختبارات التجميع
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── core/
│   │   │   ├── api/            عميل Axios، interceptors، وحدات endpoint
│   │   │   ├── stores/         Pinia stores (auth، organization، ui)
│   │   │   ├── router/         تعريفات المسارات وحراسها
│   │   │   ├── i18n/           ملفات locale والإعدادات
│   │   │   ├── pwa/            تسجيل Service Worker
│   │   │   ├── seo/            إدارة meta tags
│   │   │   ├── config.ts
│   │   │   └── utils/
│   │   ├── modules/
│   │   │   ├── auth/           صفحات login، register، callback
│   │   │   ├── landing/        صفحة الهبوط التسويقية
│   │   │   ├── dashboard/      KPI cards، funnel، مخطط الإيرادات
│   │   │   ├── deals/          لوحة Kanban، صفحة التفاصيل
│   │   │   ├── companies/      CRUD مع بحث
│   │   │   ├── contacts/       CRUD مرتبط بالشركة
│   │   │   ├── leads/          CRUD مع حوار التحويل
│   │   │   ├── tasks/          CRUD مع تصفية الحالة
│   │   │   ├── activities/     عرض الجدول الزمني
│   │   │   ├── projects/       CRUD مع اختيار العميل
│   │   │   ├── invoices/       CRUD مع إجراء mark-paid
│   │   │   └── settings/       المؤسسة، الأعضاء، التفضيلات
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
│   │   │   └── styles/main.css رموز التصميم
│   │   ├── App.vue
│   │   └── main.ts
│   ├── public/                 manifest PWA، service worker، صفحة عدم الاتصال
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── package.json
├── docker/
│   ├── backend.Dockerfile      متعدد المراحل
│   ├── frontend.Dockerfile     متعدد المراحل
│   ├── nginx.conf
│   └── nginx.prod.conf
├── docker-compose.yml          production full stack
├── docker-compose.infra.yml    dev محلي (فقط db + redis)
├── docker-compose.prod.yml     بناء production
├── .env.example
├── .env.prod.example
└── README.md                   ← هذا الملف
```

### طبقات الواجهة الخلفية

تتبع الواجهة الخلفية **بنية طبقية** صارمة:

1. **Views** (رقيقة) — تحليل الطلب، التفويض إلى service أو selector، استجابة envelope
2. **Serializers** — التحقق من الإدخال، حل المفاتيح الأجنبية مقابل المؤسسة الحالية
3. **Services** (`services/*.py`) — منطق العمل، العمليات المعاملاتية
4. **Selectors** (`selectors.py`) — استعلامات معقدة N+1-safe
5. **Models** — قيود سلامة البيانات، الفهارس، وراثة `BaseModel`

**مثال — تدفق إنشاء Deal:**

```
POST /api/v1/deals/
   ↓
DealListCreateView (OrgScopedViewMixin + EnvelopeModelViewMixin)
   ↓
DealSerializer.validate_* → يحل company_id، pipeline_id، stage_id مقابل org
   ↓
deal_service.create_deal (atomic)
   ↓   يحسب order (max+1 داخل stage)
   ↓   يعيّن stage افتراضيًا للأول في pipeline
Deal.objects.create
   ↓
AuditLog (عبر إشارة)
   ↓
استجابة envelope { success, data, message, errors, meta }
```

### Envelope API

كل نقطة نهاية تُرجع:

```json
{
  "success": true,
  "data": { ... },
  "message": "OK",
  "errors": null,
  "meta": { "count": 42, "page": 1, "page_size": 20, "total_pages": 3 }
}
```

هذا مفروض من خلال:
- `apps/common/responses.py` (فئة APIResponse)
- `apps/common/exceptions.py` (custom_exception_handler)
- `apps/common/pagination.py` (EnvelopePagination)

---

## مخطط قاعدة البيانات

### الجداول الأساسية

| الجدول | الغرض | الأعمدة الرئيسية |
|--------|-------|------------------|
| `accounts_user` | مستخدم مخصص (تسجيل بالبريد) | `email` (فريد)، `google_id`، `language` |
| `accounts_organization` | المستأجر | `slug` (فريد)، `default_currency`، `default_language` |
| `accounts_membership` | ربط المستخدم ↔ Org | `role`، `is_active` |
| `accounts_invitation` | دعوات معلقة | `token`، `expires_at` |
| `crm_company` | مؤسسة عميل | `name`، `industry`، `owner` |
| `crm_contact` | شخص في شركة | `first_name`، `email`، `company` FK |
| `crm_pipeline` | خط مبيعات | `name`، `is_default` |
| `crm_stage` | مرحلة خط | `order`، `color`، `is_won`، `is_lost` |
| `crm_lead` | عميل محتمل قبل التأهيل | `status`، `source`، `owner` |
| `crm_deal` | فرصة | `amount`، `stage` FK، `order`، `status` |
| `activities_activity` | تفاعل مسجّل | `type`، `occurred_at` + FK متعدد الأشكال |
| `activities_task` | مهمة | `priority`، `due_date`، `status` |
| `projects_project` | مخرج | `status`، `budget`، `client_company` |
| `projects_invoice` | وثيقة فاتورة | `number` (فريد لكل org)، `total`، `paid_at` |
| `audit_audit_log` | تتبع التغييرات | `action`، `entity_type`، `entity_id`، `changes` JSONB |
| `attachments_attachment` | ملف | `file`، `mime_type`، `size`، FK متعدد الأشكال |

### قرارات التصميم

- **مفاتيح أساسية UUID** — مقاومة للتصادم، آمنة للكشف في URLs
- **`organization_id` في كل جدول نطاق** — تمكين تعدد المستأجرين على مستوى الصف بدون تعقيد schema-per-tenant
- **حذف ناعم** (`deleted_at`) مع `ActiveManager` — إمكانية الاستعادة وأثر التدقيق
- **فهارس مركبة** على أنماط الفلترة عالية الحركة:
  - `(organization_id, status, owner_id)` على Deal
  - `(organization_id, pipeline_id, stage_id)` على Deal
  - `(organization_id, assigned_to_id, status, due_date)` على Task
- **قيد فريد شرطي** على رقم الفاتورة لكل org (مع احترام الحذف الناعم)
- **`order` صحيح** على Stage و Deal — يتيح ترتيب السحب والإفلات بدون جداول إضافية

---

## مرجع API

التوثيق التفاعلي الكامل متاح على **`/api/docs/`** (Swagger UI) بمجرد تشغيل الواجهة الخلفية.

### الاصطلاحات

| الجانب | القاعدة |
|--------|---------|
| Base URL | `/api/v1/` |
| المصادقة | JWT في كوكيز HttpOnly |
| CSRF | هيدر `X-CSRFToken` مطلوب لـ POST/PUT/PATCH/DELETE |
| تعدد المستأجرين | هيدر `X-Organization-Id` (اختياري؛ يرجع لأول عضوية) |
| تقسيم الصفحات | `?page=1&page_size=20` (بحد أقصى 100) |
| الفلترة | معاملات query مخصصة لكل endpoint (أدناه) |
| الترتيب | `?ordering=-created_at` حيثما كان مدعومًا |
| الاستجابة | Envelope `{ success, data, message, errors, meta }` |

### ملخص نقاط النهاية

**المصادقة**
- `POST /auth/register/` — إنشاء مستخدم + مؤسسة
- `POST /auth/login/` — ضبط الكوكيز
- `POST /auth/logout/` — مسح الكوكيز
- `POST /auth/token/refresh/` — تدوير access token
- `GET|PATCH /auth/me/` — الملف الشخصي
- `POST /auth/password/change/`
- `GET /auth/csrf/` — الحصول على CSRF token
- `GET /auth/google/` — URL موافقة OAuth
- `GET /auth/google/callback/` — callback OAuth (ضبط الكوكيز، إعادة توجيه)
- `POST /auth/invitations/accept/`

**المؤسسات**
- `GET|POST /organizations/`
- `GET|PATCH|DELETE /organizations/{id}/`
- `GET /organizations/{id}/members/`
- `PATCH|DELETE /organizations/{id}/members/{mid}/`
- `POST /organizations/{id}/invitations/`

**CRM**
- `GET|POST /companies/` — فلترة: `search`, `industry`, `owner`
- `GET|PATCH|DELETE /companies/{id}/`
- `GET|POST /contacts/` — فلترة: `search`, `company`, `owner`
- `GET|PATCH|DELETE /contacts/{id}/`
- `GET|POST /pipelines/`
- `GET|PATCH|DELETE /pipelines/{id}/`
- `POST /pipelines/ensure-default/` — idempotent
- `GET|POST /pipelines/{id}/stages/`
- `PATCH|DELETE /stages/{id}/`
- `GET|POST /leads/` — فلترة: `search`, `status`, `source`, `owner`
- `GET|PATCH|DELETE /leads/{id}/`
- `POST /leads/{id}/convert/` — ينشئ deal، يتطلب `pipeline_id`
- `GET|POST /deals/` — فلترة: `search`, `pipeline`, `stage`, `status`, `owner`
- `GET|PATCH|DELETE /deals/{id}/`
- `GET /deals/kanban/?pipeline={id}` — بنية board جاهزة للواجهة
- `PATCH /deals/{id}/move/` — `{ stage_id, order? }` للسحب والإفلات

**الأنشطة**
- `GET|POST /activities/` — فلترة: `search`, `type`, `deal`, `lead`, `company`, `date_from`, `date_to`
- `GET|PATCH|DELETE /activities/{id}/`
- `GET|POST /tasks/` — فلترة: `search`, `status`, `priority`, `assigned_to`, `deal`, `due_before`
- `GET|PATCH|DELETE /tasks/{id}/`
- `POST /tasks/{id}/complete/`
- `POST /tasks/{id}/reopen/`

**المشاريع والفواتير**
- `GET|POST /projects/` — فلترة: `search`, `status`, `client`, `owner`
- `GET|PATCH|DELETE /projects/{id}/`
- `GET|POST /invoices/` — فلترة: `search`, `status`, `project`
- `GET|PATCH|DELETE /invoices/{id}/`
- `POST /invoices/{id}/mark-paid/`

**لوحة التحكم**
- `GET /dashboard/stats/` — كائن KPI
- `GET /dashboard/funnel/` — مصفوفة المراحل مع الأعداد والإجماليات
- `GET /dashboard/revenue/?months=6` — مبالغ شهرية
- `GET /dashboard/recent-activities/` — آخر 10

**البحث والتدقيق**
- `GET /search/?q={query}` — بحث شامل عبر الشركات، جهات الاتصال، الصفقات، العملاء المحتملين
- `GET /audit-logs/` — فلترة: `entity_type`, `entity_id` (owner/admin فقط)

**المرفقات**
- `GET|POST /attachments/` — رفع multipart، فلترة حسب `deal`, `company`, `project`
- `GET|DELETE /attachments/{id}/`
- `GET /attachments/{id}/download/` — بث موثّق

---

## البدء السريع

### المتطلبات الأساسية

- **Python 3.12+**
- **Node 20+**
- **Docker** (فقط لـ Postgres + Redis في dev)
- **Git**

### التطوير المحلي (موصى به)

```bash
git clone https://github.com/koshino-ir/koshino-crm.git
cd koshino-crm

# 1. البيئة
cp .env.example .env

# 2. البنية التحتية (Postgres على :55432، Redis على :56379)
docker compose -f docker-compose.infra.yml up -d

# 3. الخلفية
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python manage.py migrate
python manage.py runserver
# → http://localhost:8000  (health: /api/v1/health/، docs: /api/docs/)

# 4. الأمامية (طرفية جديدة)
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

افتح **http://localhost:5173**، أنشئ مؤسسة، وابدأ.

### Docker كامل (مشابه للإنتاج)

```bash
cp .env.prod.example .env.prod
# عدّل .env.prod — عيّن DJANGO_SECRET_KEY، كلمة مرور DB، كلمة مرور Redis بشكل آمن

# توليد مفتاح آمن
python -c "import secrets; print(secrets.token_urlsafe(50))"

docker compose -f docker-compose.prod.yml --env-file .env.prod up --build -d
# → http://localhost
```

---

## متغيرات البيئة

### التطوير (`.env`)

```env
# Django
DJANGO_SECRET_KEY=dev-insecure-change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# قاعدة البيانات
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

# Google OAuth (اختياري)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback/
FRONTEND_URL=http://localhost:5173
```

### الإنتاج (`.env.prod`)

انظر `.env.prod.example` في المستودع.

---

## الاختبار

```bash
cd backend
source .venv/bin/activate
pytest -q
```

تغطية الاختبار:
- تدفقات المصادقة (تسجيل، دخول، خروج، تدوير token، تغيير كلمة المرور)
- عزل تعدد المستأجرين (رفض الوصول عبر المؤسسات)
- إنشاء Deal، تجميع kanban، نقل stage
- تحويل Lead (إنشاء Deal، تعليم qualified، منع التحويل المزدوج)
- ترقيم الفواتير (فريد لكل org)، mark-paid، التحقق من التواريخ
- أمان رفع المرفقات (قائمة بيضاء للامتدادات، حد الحجم، قاعدة single-target)
- تفويض تنزيل المرفقات
- إنشاء سجل التدقيق عند حفظ Deal/Company
- تجميعات لوحة التحكم (KPI، funnel، revenue)
- البحث الشامل عبر الكيانات

بيئة الاختبار تستخدم:
- `config.settings.test` (cache locmem، تجزئة MD5 للسرعة)
- حدود throttle في الذاكرة (بدون تلوث بين التشغيلات)
- مجلد temp لملفات media (بدون مشاكل إذن)

---

## النشر

### بنية الإنتاج

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

### الخطوات على VPS جديد

1. **تجهيز الخادم** — Ubuntu 22.04+ أو Debian 12، بحد أدنى 2 vCPU / 4 GB RAM
2. **تثبيت Docker & Compose**
3. **الجدار الناري** — افتح فقط 22، 80، 443
4. **DNS** — سجل A إلى IP الخادم
5. **النشر** — انسخ المستودع، أنشئ `.env.prod`، شغّل `docker compose -f docker-compose.prod.yml up -d --build`
6. **TLS** — Certbot + إعداد SSL في Nginx (انظر `docs/deployment.md`)
7. **النسخ الاحتياطي** — `pg_dump` يوميًا + سياسة الاحتفاظ

### ملاحظات التوسع

- **Gunicorn workers** — `(2 × cores) + 1` افتراضي جيد؛ اضبط حسب الحمل
- **Celery** — قسّم إلى طوابير (`default`, `email`, `reports`) للعزل
- **Postgres** — connection pooling عبر PgBouncer فوق ~50 worker
- **Redis** — نسخ منفصلة لـ cache و broker في المقاييس الكبيرة
- **الأصول الثابتة** — CDN أمام `/assets/*`

---

## الأمان

يطبق التطبيق دفاعًا متعدد الطبقات:

| الطبقة | التحكم |
|--------|--------|
| **النقل** | HTTPS مفروض (HSTS مع `includeSubDomains`، `preload`) |
| **الجلسة** | JWT في كوكيز HttpOnly + Secure + SameSite=Lax |
| **CSRF** | رمز double-submit + هيدر `X-CSRFToken` على التغييرات |
| **المصادقة** | تجزئة Argon2، مدققات كلمة المرور، تحديد المعدل |
| **API** | فحوصات object-level على كل view مقابل org |
| **البيانات** | UUID PK (بدون enumeration)، حذف ناعم (أثر التدقيق) |
| **الملفات** | قائمة بيضاء للامتداد + MIME + الحجم، تنزيل موثّق، منع MEDIA_URL المباشر |
| **الرؤوس** | `X-Frame-Options`، `X-Content-Type-Options`، `Referrer-Policy`، `Permissions-Policy` |
| **السجلات** | سجل تدقيق على الكيانات الحساسة، سجلات إنتاج منظمة |
| **التبعيات** | `ruff` + `mypy` في CI، يوصى بـ `pip-audit` |

---

## لقطات الشاشة


| | |
|---|---|
| **كانبان الصفقات** | **لوحة التحكم** |
| ![Kanban](docs/screenshots/ar/deals-kanban.png) | ![Dashboard](docs/screenshots/ar/dashboard.png) |
| **الشركات** | **تسجيل الدخول** |
| ![Companies](docs/screenshots/ar/companies.png) | ![Login](docs/screenshots/ar/login.png) |

---

## خارطة الطريق

### منجز
- [x] MVP: CRM مع خط أنابيب كامل، صفقات، شركات، جهات اتصال، عملاء محتملون
- [x] مهام وأنشطة
- [x] مشاريع وفواتير
- [x] لوحة تحكم مع رسوم بيانية
- [x] عزل متعدد المستأجرين
- [x] مصادقة JWT في كوكيز + Google OAuth
- [x] واجهة ثلاثية اللغات مع RTL أصلي
- [x] PWA (قابل للتثبيت، غير متصل، service worker)
- [x] سجل تدقيق
- [x] Docker production + Nginx + رؤوس أمان

### مخطط
- [ ] إشعارات بريد إلكتروني (دعوات، تذكيرات)
- [ ] تصدير CSV/Excel للصفقات والفواتير وجهات الاتصال
- [ ] واجهة رفع المرفقات في صفحة تفاصيل Deal
- [ ] تكامل Webhook (Slack، Zapier)
- [ ] تقارير نشاط الفريق (لكل عضو)
- [ ] ضبط تلقائي لاحتمال Deal بناءً على تاريخ stage
- [ ] عمليات جماعية (تعيين جماعي، تحديث جماعي)
- [ ] حقول مخصصة لكل مؤسسة

---

## الترخيص

ترخيص MIT — انظر [LICENSE](LICENSE).

---

## المؤلف

**Koshino** — [github.com/koshino-ir](https://github.com/koshino-ir)

أسئلة، ملاحظات، أو مشروع في ذهنك؟  
📧 `info@koshino.ir`

---

<div align="center">

**صُنع بـ ❤️ للفرق التي تبيع وتنفذ.**

⭐ أعطِ هذا المستودع نجمة إذا وجدته مفيدًا.

</div>

</div>
