from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_user, get_db, require_roles
from app.models.patient import Patient
from app.models.user import User
from app.schemas.patient import PatientCreate, PatientListItem, PatientRead, PatientUpdate
from app.services.audit import log_audit_event


router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("", response_model=list[PatientListItem])
def list_patients(
    q: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[PatientListItem]:
    query = db.query(Patient).filter(Patient.archived_at.is_(None))
    if q:
        term = f"%{q}%"
        query = query.filter(
            or_(
                Patient.first_name.ilike(term),
                Patient.last_name.ilike(term),
                Patient.patient_code.ilike(term),
                Patient.phone.ilike(term),
            )
        )
    patients = query.order_by(Patient.last_name, Patient.first_name).all()
    return [PatientListItem.model_validate(item) for item in patients]


@router.post(
    "",
    response_model=PatientRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin", "doctor", "nurse", "reception"))],
)
def create_patient(
    payload: PatientCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PatientRead:
    existing = db.query(Patient).filter(Patient.patient_code == payload.patient_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Patient code already exists")

    patient = Patient(**payload.model_dump())
    db.add(patient)
    db.flush()
    log_audit_event(
        db=db,
        user_id=current_user.id,
        action="create",
        entity_type="patient",
        entity_id=patient.id,
        new_value=payload.model_dump(mode="json"),
        ip_address=request.client.host if request.client else None,
    )
    db.commit()
    db.refresh(patient)
    return PatientRead.model_validate(patient)


@router.get("/{patient_id}", response_model=PatientRead)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PatientRead:
    patient = (
        db.query(Patient)
        .options(joinedload(Patient.visits), joinedload(Patient.medications))
        .filter(Patient.id == patient_id, Patient.archived_at.is_(None))
        .first()
    )
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return PatientRead.model_validate(patient)


@router.put(
    "/{patient_id}",
    response_model=PatientRead,
    dependencies=[Depends(require_roles("admin", "doctor", "nurse"))],
)
def update_patient(
    patient_id: int,
    payload: PatientUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PatientRead:
    patient = db.get(Patient, patient_id)
    if not patient or patient.archived_at is not None:
        raise HTTPException(status_code=404, detail="Patient not found")

    before = PatientRead.model_validate(patient).model_dump(mode="json")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(patient, field, value)

    log_audit_event(
        db=db,
        user_id=current_user.id,
        action="update",
        entity_type="patient",
        entity_id=patient.id,
        old_value=before,
        new_value=payload.model_dump(exclude_unset=True, mode="json"),
        ip_address=request.client.host if request.client else None,
    )
    db.commit()
    db.refresh(patient)
    return PatientRead.model_validate(patient)

