from sqlalchemy.orm import Session

from findora.models.claim import Claim, ClaimStatus
from findora.schemas.claim_schema import ClaimCreate


def create_claim(
    db: Session,
    item_id: int,
    claimer_user_id: int,
    claim_data: ClaimCreate,
) -> Claim:
    claim = Claim(
        item_id=item_id,
        claimer_user_id=claimer_user_id,
        message=claim_data.message,
        proof_text=claim_data.proof_text,
        status=ClaimStatus.PENDING.value,
    )

    db.add(claim)
    db.commit()
    db.refresh(claim)

    return claim


def get_claim_by_id(db: Session, claim_id: int) -> Claim | None:
    return db.query(Claim).filter(Claim.id == claim_id).first()


def get_claims_for_user(db: Session, user_id: int) -> list[Claim]:
    return (
        db.query(Claim)
        .filter(Claim.claimer_user_id == user_id)
        .order_by(Claim.created_at.desc())
        .all()
    )


def get_claims_for_item(db: Session, item_id: int) -> list[Claim]:
    return (
        db.query(Claim)
        .filter(Claim.item_id == item_id)
        .order_by(Claim.created_at.desc())
        .all()
    )


def update_claim_status(db: Session, claim: Claim, new_status: str) -> Claim:
    claim.status = new_status

    db.add(claim)
    db.commit()
    db.refresh(claim)

    return claim