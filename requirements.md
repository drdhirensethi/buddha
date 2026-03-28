# Technical Design Document: Geriatric Patient Data Collection Web App

## 1. Purpose

This document defines the technical design for a secure web application used by a geriatric specialist and clinic staff to collect, manage, and store patient information in a database. The system will support structured patient intake, longitudinal follow-up, clinical assessments, medication tracking, and audit-ready access to patient records.

The primary goal is to provide a reliable internal clinical application that improves data quality, reduces paper-based workflows, and creates a foundation for future reporting and care coordination features.

## 2. Goals

- Capture patient demographic, contact, caregiver, and clinical data through a web interface.
- Store patient data in a relational database with strong integrity and auditability.
- Support repeated visits and longitudinal tracking over time.
- Enable role-based access for physicians, nurses, and administrative staff.
- Provide secure authentication, authorization, and activity logging.
- Make the system maintainable, extensible, and suitable for healthcare environments.

## 3. Non-Goals

- Full hospital EMR replacement.
- Billing, insurance claims, and payment processing in the first version.
- External health information exchange integrations in the first version.
- Mobile native apps in the first version.

## 4. Primary Users

- Geriatric specialist
- Nurses and clinical assistants
- Front-desk or administrative staff
- System administrator

## 5. Core Use Cases

### 5.1 Patient Registration

- Create a new patient record
- Capture demographics, identifiers, address, and emergency contacts
- Record caregiver and family support details

### 5.2 Clinical Intake

- Record presenting complaints
- Capture medical history, surgical history, allergies, immunizations, and family history
- Record medication list and adherence concerns

### 5.3 Geriatric Assessment

- Capture functional status
- Record cognitive screening results
- Record fall risk, frailty, nutrition, mood, continence, mobility, and ADL/IADL assessments
- Store clinician notes and care plans

### 5.4 Follow-Up Visits

- Add visit notes over time
- Update medication and diagnoses
- Compare current and historical status

### 5.5 Search and Review

- Search patients by name, phone, date of birth, or identifier
- View patient summary dashboard
- Review visit timeline and assessment history

## 6. Functional Requirements

### 6.1 Authentication and Access Control

- Users must log in with username/email and password.
- The system must support role-based access control.
- Roles should include `admin`, `doctor`, `nurse`, and `reception`.
- Sensitive actions must be auditable.

### 6.2 Patient Management

- Create, view, edit, and archive patient records
- Maintain unique patient identifiers
- Store multiple phone numbers, addresses, and contacts if needed
- Support caregiver linkage to the patient

### 6.3 Visit Management

- Create a visit for each encounter
- Record visit date, provider, chief complaint, vitals, notes, and plan
- Support draft and completed visit states

### 6.4 Clinical Data Capture

- Diagnoses
- Allergies
- Medications
- Laboratory results if entered manually
- Standard geriatric assessment forms
- Free-text notes

### 6.5 Reporting

- Patient list export for authorized users
- Daily visit summary
- Basic counts by diagnosis, age band, and risk category

### 6.6 Audit Logging

- Log record creation, modification, deletion/archival, login, logout, and failed access attempts

## 7. Non-Functional Requirements

### 7.1 Security

- Encrypt data in transit using HTTPS.
- Store passwords using a strong hashing algorithm such as Argon2 or bcrypt.
- Enforce least-privilege access.
- Maintain audit logs for regulated environments.
- Encrypt backups and sensitive environment secrets.

### 7.2 Performance

- Patient search should return results within 2 seconds for normal clinic scale.
- Typical page loads should complete within 3 seconds on clinic broadband.

### 7.3 Reliability

- Daily automated backups
- Restore procedure documented and tested
- Graceful handling of application errors

### 7.4 Maintainability

- Modular backend architecture
- API-first backend design
- Clear schema migrations
- Automated tests for critical flows

### 7.5 Compliance

- Design should align with local medical privacy and record retention requirements.
- If deployed in the United States, implementation should be reviewed for HIPAA compliance before production use.
- If deployed elsewhere, local health-data laws must be validated before go-live.

## 8. Proposed Architecture

### 8.1 High-Level Architecture

The system will use a standard three-tier architecture:

1. Frontend web application
2. Backend API service
3. Relational database

Optional supporting components:

- Background task worker for reports and notifications
- Object storage for documents and attachments
- Reverse proxy for TLS termination
- Monitoring and centralized logging

### 8.2 Recommended Technology Stack

#### Frontend

- React with TypeScript
- Next.js or Vite-based SPA
- Component library: MUI or Ant Design
- Form handling: React Hook Form
- Validation: Zod

#### Backend

- Python 3.12+
- FastAPI for REST API
- Pydantic for request/response models
- SQLAlchemy 2.x ORM
- Alembic for migrations

#### Database

- PostgreSQL

#### Authentication

- JWT-based auth for API sessions or secure server-managed sessions
- Role-based authorization middleware

#### Infrastructure

- Docker for containerization
- Nginx or Traefik as reverse proxy
- Ubuntu Linux server or cloud-hosted container platform

## 9. Backend Design

### 9.1 Service Structure

Recommended backend module layout:

```text
backend/
  app/
    api/
      routes/
    core/
      config.py
      security.py
    db/
      base.py
      session.py
    models/
    schemas/
    services/
    repositories/
    audit/
    main.py
  migrations/
  tests/
```

### 9.2 API Style

- RESTful JSON API
- Versioned routes under `/api/v1`
- OpenAPI documentation generated automatically by FastAPI

### 9.3 Example API Endpoints

#### Auth

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`

#### Patients

- `POST /api/v1/patients`
- `GET /api/v1/patients`
- `GET /api/v1/patients/{patient_id}`
- `PUT /api/v1/patients/{patient_id}`
- `DELETE /api/v1/patients/{patient_id}` for soft delete/archive

#### Visits

- `POST /api/v1/patients/{patient_id}/visits`
- `GET /api/v1/patients/{patient_id}/visits`
- `GET /api/v1/visits/{visit_id}`
- `PUT /api/v1/visits/{visit_id}`

#### Assessments

- `POST /api/v1/visits/{visit_id}/assessments`
- `GET /api/v1/visits/{visit_id}/assessments`

#### Medications

- `POST /api/v1/patients/{patient_id}/medications`
- `PUT /api/v1/medications/{medication_id}`
- `GET /api/v1/patients/{patient_id}/medications`

## 10. Database Design

### 10.1 Database Choice

PostgreSQL is recommended because it is robust, widely supported, transactional, and well suited for structured medical data.

### 10.2 Core Entities

- users
- roles
- patients
- caregivers
- visits
- diagnoses
- medications
- allergies
- assessments
- vitals
- documents
- audit_logs

### 10.3 Suggested Schema

#### users

- `id`
- `email`
- `password_hash`
- `full_name`
- `role_id`
- `is_active`
- `created_at`
- `updated_at`

#### roles

- `id`
- `name`

#### patients

- `id`
- `patient_code`
- `first_name`
- `last_name`
- `date_of_birth`
- `sex`
- `phone`
- `email`
- `address`
- `emergency_contact_name`
- `emergency_contact_phone`
- `primary_caregiver_id`
- `created_at`
- `updated_at`
- `archived_at`

#### caregivers

- `id`
- `full_name`
- `relationship_to_patient`
- `phone`
- `email`
- `address`

#### visits

- `id`
- `patient_id`
- `provider_id`
- `visit_date`
- `chief_complaint`
- `history_of_present_illness`
- `assessment_summary`
- `plan`
- `status`
- `created_at`

#### vitals

- `id`
- `visit_id`
- `blood_pressure`
- `heart_rate`
- `respiratory_rate`
- `temperature`
- `oxygen_saturation`
- `height_cm`
- `weight_kg`
- `bmi`

#### diagnoses

- `id`
- `patient_id`
- `visit_id`
- `code`
- `description`
- `is_active`
- `recorded_at`

#### medications

- `id`
- `patient_id`
- `name`
- `dose`
- `frequency`
- `route`
- `start_date`
- `end_date`
- `adherence_notes`
- `active`

#### allergies

- `id`
- `patient_id`
- `allergen`
- `reaction`
- `severity`

#### assessments

- `id`
- `visit_id`
- `assessment_type`
- `score`
- `result_json`
- `notes`
- `performed_at`

#### documents

- `id`
- `patient_id`
- `visit_id`
- `file_name`
- `storage_path`
- `content_type`
- `uploaded_by`
- `uploaded_at`

#### audit_logs

- `id`
- `user_id`
- `action`
- `entity_type`
- `entity_id`
- `old_value_json`
- `new_value_json`
- `ip_address`
- `created_at`

### 10.4 Data Modeling Notes

- Use foreign keys for all clinical relationships.
- Use soft deletion for patient records where legally appropriate.
- Store flexible assessment payloads in `result_json` for evolving forms.
- Track `created_at` and `updated_at` on all major tables.
- Add database indexes on patient name, patient code, date of birth, and visit date.

## 11. Frontend Design

### 11.1 Main Screens

- Login page
- Dashboard
- Patient list and search
- Patient registration form
- Patient detail page
- Visit entry page
- Assessment entry page
- Medication management page
- Admin user management page

### 11.2 UI Principles

- Fast data entry with clear forms
- Large readable typography suitable for clinic use
- Minimal clicks for repeat workflows
- Validation errors shown inline
- Autosave for long forms if feasible

### 11.3 Form Design

- Multi-section patient intake form
- Reusable field components
- Client-side validation plus server-side validation
- Support draft save for incomplete visits

## 12. Security Design

### 12.1 Authentication

- Login with secure password policy
- Session timeout and token expiration
- Optional multi-factor authentication for admins

### 12.2 Authorization

- Doctors can access full clinical data.
- Nurses can create and update allowed clinical fields.
- Reception can create demographic records but should have restricted clinical access.
- Admins can manage users and configuration.

### 12.3 Audit and Traceability

- Record who created or modified patient data
- Log timestamps and source IP when available
- Protect logs from ordinary user modification

### 12.4 Data Protection

- Enforce HTTPS everywhere
- Encrypt backups
- Limit database access to backend services only
- Store secrets in environment variables or a secrets manager

## 13. Validation Rules

- Required patient demographics: name, date of birth, sex, and at least one contact method
- Unique patient code required
- Visit must belong to an existing patient
- Medication entries require name and dose/frequency structure
- Assessment type must be from an approved catalog

## 14. Deployment Design

### 14.1 Environments

- Local development
- Staging
- Production

### 14.2 Container Strategy

- One container for frontend
- One container for backend API
- One container for PostgreSQL
- Optional worker container for background jobs

### 14.3 CI/CD

- Run linting, tests, and migrations checks on every pull request
- Build Docker images on main branch
- Deploy to staging first, then production after approval

## 15. Logging, Monitoring, and Backups

### 15.1 Logging

- Application logs
- Authentication logs
- Audit logs
- Error tracking

### 15.2 Monitoring

- API health endpoint
- Database connection monitoring
- CPU, memory, and disk alerts

### 15.3 Backups

- Daily PostgreSQL backup
- Backup retention policy
- Periodic restore drills

## 16. Testing Strategy

### 16.1 Backend Tests

- Unit tests for services and validation
- Integration tests for API endpoints
- Migration tests

### 16.2 Frontend Tests

- Component tests for forms
- End-to-end tests for patient registration and visit workflows

### 16.3 Security Tests

- Authorization tests per role
- Input validation tests
- Session and token handling tests

## 17. Suggested Development Phases

### Phase 1: Foundation

- Project setup
- Authentication
- User roles
- Patient CRUD
- Basic search

### Phase 2: Clinical Workflow

- Visit management
- Vitals
- Medications
- Diagnoses
- Basic notes

### Phase 3: Geriatric Assessments

- Functional and cognitive assessment forms
- Risk scoring
- Timeline/history view

### Phase 4: Operations and Reporting

- Audit dashboard
- Export and reports
- Monitoring and backup automation

## 18. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Unclear clinical form requirements | Rework and delays | Validate forms early with clinician input |
| Sensitive health data exposure | Severe | Apply strong access controls, audit logs, HTTPS, and secure hosting |
| Poor data quality from manual entry | Medium | Use validation, dropdowns, required fields, and review workflows |
| Growth in custom assessment logic | Medium | Store configurable assessment definitions where possible |
| Compliance gaps | Severe | Review deployment and operations with legal/compliance stakeholders before production |

## 19. Recommended MVP Scope

The first production-ready MVP should include:

- Secure login
- Role-based access
- Patient registration
- Patient search and detail page
- Visit entry and history
- Medication list
- Basic geriatric assessment form
- PostgreSQL persistence
- Audit logging

## 20. Open Questions

- Which geriatric assessment scales must be included in the MVP?
- Will the app be used by a single clinic or multiple facilities?
- Are scanned documents or file uploads required in phase 1?
- Are there local regulatory storage or consent requirements that must be built in?
- Is offline support needed for low-connectivity environments?

## 21. Final Recommendation

Build the application as a React frontend with a FastAPI backend and PostgreSQL database, using a modular API-first design with strong audit logging and role-based access control. This approach balances speed of development, clinical data integrity, security, and future extensibility for a geriatric care setting.