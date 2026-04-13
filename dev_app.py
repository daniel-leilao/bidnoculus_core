"""
API mínima de desenvolvimento (MVP). Produção pode substituir por app completa.

  uvicorn dev_app:app --host 127.0.0.1 --port 3005 --reload
"""

from fastapi import FastAPI

app = FastAPI(title="bidnoculus_core", version="0.0.1")


@app.get("/health")
def health():
    return {"ok": True, "service": "bidnoculus_core"}
