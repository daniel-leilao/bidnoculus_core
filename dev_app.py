"""
API mínima de desenvolvimento (MVP). Produção pode substituir por app completa.

  uvicorn dev_app:app --host 127.0.0.1 --port 3005 --reload
"""

from __future__ import annotations

import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI

from bill_client import bill_base_url, get_balance

load_dotenv(Path(__file__).resolve().parent / ".env")

app = FastAPI(title="bidnoculus_core", version="0.0.1")


@app.get("/health")
def health():
    return {"ok": True, "service": "bidnoculus_core"}


@app.get("/ready")
def ready():
    """Stack local: Core + reachability do Bill; se BILL_API_TOKEN existir, testa GET /balance."""
    out: dict = {"ok": True, "service": "bidnoculus_core", "bill": {}}
    base = bill_base_url()
    try:
        with httpx.Client(timeout=5.0) as c:
            r = c.get(f"{base}/health")
        out["bill"]["health_status"] = r.status_code
        out["bill"]["reachable"] = r.status_code == 200
        out["bill"]["bill_api_url"] = base
    except Exception as e:
        out["bill"]["reachable"] = False
        out["bill"]["error"] = str(e)[:300]

    token = (os.environ.get("BILL_API_TOKEN") or "").strip()
    if token:
        status, body = get_balance(token=token)
        out["bill"]["balance_status"] = status
        out["bill"]["balance_ok"] = status == 200
        if status == 200 and isinstance(body, dict):
            out["bill"]["creditos_perfil_total"] = body.get("creditos_perfil_total")
    else:
        out["bill"]["balance_skipped"] = "defina BILL_API_TOKEN no .env para testar JWT no Bill"

    return out
