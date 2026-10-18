from fastapi import APIRouter, HTTPException, status

from debt_api.services.health import is_healthy

router = APIRouter()


@router.get("/api/healthz")
def healthcheck():
    if is_healthy():
        return {"status": "healthy"}
    else:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not connected",
        )
