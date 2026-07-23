"""Campaign generation and export endpoints.

`POST /api/campaigns` is the one meaningful endpoint: Request Validation
(Pydantic, via the `CampaignRequest` body) -> Guardrail Manager -> the
LangGraph Coordinator. The export endpoints are stateless converters: the
caller sends back the exact `CampaignResult` it already has (from the
create-campaign response) and gets a file back — no server-side
persistence is involved, per the v1 "no database" requirement.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response

from app.api.dependencies import get_coordinator, get_guardrail_manager
from app.graph.coordinator import CampaignCoordinator
from app.guardrails.exceptions import GuardrailViolation
from app.guardrails.manager import GuardrailManager
from app.schemas.campaign_request import CampaignRequest
from app.schemas.campaign_result import CampaignResult
from app.services.export_service import ExportService
from app.utils.text import slugify

router = APIRouter(prefix="/api/campaigns", tags=["campaigns"])
_export_service = ExportService()


@router.post("", response_model=CampaignResult)
def create_campaign(
    request: CampaignRequest,
    coordinator: CampaignCoordinator = Depends(get_coordinator),
    guardrails: GuardrailManager = Depends(get_guardrail_manager),
) -> CampaignResult:
    try:
        guardrails.run_pre_checks(request)
    except GuardrailViolation as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return coordinator.run(request)


@router.post("/export/markdown")
def export_markdown(result: CampaignResult) -> Response:
    markdown = _export_service.to_markdown(result)
    filename = f"{slugify(result.request.product_name)}-campaign.md"
    return Response(
        content=markdown,
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/export/pdf")
def export_pdf(result: CampaignResult) -> Response:
    pdf_bytes = _export_service.to_pdf(result)
    filename = f"{slugify(result.request.product_name)}-campaign.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
