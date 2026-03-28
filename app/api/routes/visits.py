from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_roles
from app.models.patient import Patient
from app.models.user import User
from app.models.visit import Visit
from app.schemas.visit import VisitCreate, VisitRead
from app.services.audit import log_audit_event


router = APIRouter(prefix="/visits", tags=["visits"])


@router.post(
    "",
    response_model=VisitRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin", "doctor", "nurse"))],
)
def create_visit(
    payload: VisitCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> VisitRead:
    patient = db.get(Patient, payload.patient_id)
    if not patient or patient.archived_at is not None:
        raise HTTPException(status_code=404, detail="Patient not found")

    visit = Visit(**payload.model_dump(), provider_id=current_user.id)
    db.add(visit)
    db.flush()
    log_audit_event(
        db=db,
        user_id=current_user.id,
        action="create",
        entity_type="visit",
        entity_id=visit.id,
        new_value=payload.model_dump(mode="json"),
        ip_address=request.client.host if request.client else None,
    )
    db.commit()
    db.refresh(visit)
    return VisitRead.model_validate(visit)


@router.get("/{visit_id}", response_model=VisitRead)
def get_visit(
    visit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> VisitRead:
    visit = db.get(Visit, visit_id)
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    return VisitRead.model_validate(visit)

