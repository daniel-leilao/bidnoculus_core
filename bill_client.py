"""
Cliente HTTP mínimo para o bidnoculus_bill (balance + consume).

O Bill exige JWT com `email` ou `sub` no payload (Authorization: Bearer ...).
Para testes, use `npm run token:atualizar-agent-env` no repo Bill para gerar BILL_API_TOKEN.
"""

from __future__ import annotations

import os
from typing import Any, Optional

import httpx

DEFAULT_TIMEOUT = 30.0


def bill_base_url(explicit: Optional[str] = None) -> str:
    base = explicit or os.environ.get("BILL_API_URL", "http://localhost:3003")
    return str(base).rstrip("/")


def _headers(token: str, json_body: bool = False) -> dict[str, str]:
    h = {"Authorization": f"Bearer {token.strip()}"}
    if json_body:
        h["Content-Type"] = "application/json"
    return h


def get_balance(*, token: str, base_url: Optional[str] = None) -> tuple[int, dict[str, Any]]:
    url = f"{bill_base_url(base_url)}/balance"
    with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
        r = client.get(url, headers=_headers(token))
    try:
        body: dict[str, Any] = r.json() if r.content else {}
    except Exception:
        body = {"_raw": r.text}
    return r.status_code, body


def consume_credits(
    *,
    token: str,
    amount: int,
    reason: str,
    reference_id: str,
    source_project: str = "bidnoculus_core",
    reference_type: str = "project_action",
    action_type: Optional[str] = None,
    metadata: Optional[dict[str, Any]] = None,
    base_url: Optional[str] = None,
) -> tuple[int, dict[str, Any]]:
    """
    POST /credits/consume — idempotente por reference_id + utilizador (email do JWT).
    """
    url = f"{bill_base_url(base_url)}/credits/consume"
    payload: dict[str, Any] = {
        "amount": int(amount),
        "reason": reason,
        "source_project": source_project,
        "reference_id": reference_id,
        "reference_type": reference_type,
    }
    if action_type is not None:
        payload["action_type"] = action_type
    if metadata:
        payload["metadata"] = metadata

    with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
        r = client.post(url, headers=_headers(token, json_body=True), json=payload)
    try:
        body: dict[str, Any] = r.json() if r.content else {}
    except Exception:
        body = {"_raw": r.text}
    return r.status_code, body
