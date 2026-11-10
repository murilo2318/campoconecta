from fastapi import APIRouter

router = APIRouter(tags=["saude"])


@router.get("/health")
def health():
    return {"status": "ok"}
