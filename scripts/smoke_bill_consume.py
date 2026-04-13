"""
Smoke: GET /balance + POST /credits/consume (alinhado a scripts/smoke-degustacao.js no Bill).

Requisitos: Bill a correr, Mongo ligado, .env com BILL_API_TOKEN e opcionalmente BILL_API_URL.

  cd bidnoculus_core
  pip install -r requirements.txt
  copy .env.example .env
  # preencher BILL_API_TOKEN (ex.: npm run token:atualizar-agent-env no repo Bill)
  python scripts/smoke_bill_consume.py
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv
except ImportError:
    print("Instale dependencias: pip install -r requirements.txt", file=sys.stderr)
    raise

load_dotenv(ROOT / ".env")

from bill_client import bill_base_url, consume_credits, get_balance


def main() -> int:
    token = (os.environ.get("BILL_API_TOKEN") or "").strip()
    if not token:
        print(
            "Defina BILL_API_TOKEN no .env (JWT com email). "
            "No repo Bill: npm run token:atualizar-agent-env",
            file=sys.stderr,
        )
        return 1

    base = bill_base_url()
    print("BILL_API_URL:", base)

    s1, b1 = get_balance(token=token)
    print("\nGET /balance", s1, b1)
    if s1 != 200:
        print("Falha no balance. Bill a correr? Mongo?", file=sys.stderr)
        return 1

    ref = f"smoke_py_{int(time.time() * 1000)}"
    s2, c = consume_credits(
        token=token,
        amount=1,
        reason="profile_create",
        reference_id=ref,
        source_project="bidnoculus_core_smoke",
        reference_type="smoke_test",
        action_type="create",
    )
    print("\nPOST /credits/consume", s2, c)

    s3, b3 = get_balance(token=token)
    print("\nGET /balance (apos 1 debito)", s3, b3)

    if s2 != 200:
        return 1
    expected_after = (b1.get("creditos_perfil_total") or 0) - 1
    if c.get("balance_after") != expected_after:
        print(
            "Aviso: balance_after esperado",
            expected_after,
            "obtido",
            c.get("balance_after"),
        )
    print("\nOK smoke Python — alinhado ao npm run smoke:degustacao no Bill.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
