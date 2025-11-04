"""Deliverability and domain diagnostics endpoints."""
from __future__ import annotations

import asyncio

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.deps import get_db
from app.schemas.checks import DomainCheckResponse
from app.services.dns_checker import check_domain_health
from app.services.spam_check_service import summarize_domain_scores

router = APIRouter(prefix="/api/v1/check", tags=["deliverability"])


@router.get("/domain", response_model=DomainCheckResponse)
async def domain_check(domain: str = Query(..., min_length=2), db: Session = Depends(get_db)) -> DomainCheckResponse:
    dns_task = asyncio.to_thread(check_domain_health, domain)
    dns_result = await dns_task
    spam_stats = summarize_domain_scores(db, dns_result["domain"])
    return DomainCheckResponse(**dns_result, spam=spam_stats)
