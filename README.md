# bidnoculus_core

Serviço MVP: **pesquisa**, **perfis/filtros**, acesso ao **MongoDB de veículos** (`leiloes` ou equivalente), integração com **`bidnoculus_bill`** (`POST /credits/consume`).

**Irmãos:** [`bidnoculus_frontgpt`](https://github.com/daniel-leilao/bidnoculus_frontgpt) · [`bidnoculus_bill`](https://github.com/daniel-leilao/bidnoculus_bill)

**Guarda-chuva:** [`bidnoculus_lancto`](https://github.com/daniel-leilao/bidnoculus_lancto) (submódulos)

## Integração com o Bill (já no repo)

- **`bill_client.py`** — `get_balance()` e `consume_credits()` via `httpx` (JWT `Bearer` com `email` ou `sub`).
- **`.env.example`** — `BILL_API_URL`, `BILL_API_TOKEN`.
- **`scripts/smoke_bill_consume.py`** — smoke alinhado ao `npm run smoke:degustacao` do Bill.

```powershell
pip install -r requirements.txt
copy .env.example .env
# No repo bidnoculus_bill: npm run token:atualizar-agent-env  (escreve BILL_API_TOKEN neste .env)
# Com o Bill em http://localhost:3003:
python scripts/smoke_bill_consume.py
```

**Dev server (porta 3005):** `python -m uvicorn dev_app:app --host 127.0.0.1 --port 3005 --reload` — ou use o script do guarda-chuva `bidnoculus_lancto/scripts/start-mvp-stack.ps1`.

Em rotas do Core que criem/reativem perfil, importar `consume_credits` e passar o **JWT do utilizador** (recomendado) ou um token de serviço gerado com o mesmo `JWT_SECRET` que o Bill.

## Variáveis (alinhamento Bill)

- `BILL_API_URL` — URL base do Bill (ex.: `http://localhost:3003`).
- `BILL_API_TOKEN` — JWT com claim `email` ou `sub` (para smoke e chamadas server-side; regenerar após rotação: `npm run token:atualizar-agent-env` no Bill).

Documentação: [`bidnoculus_bill` — ALINHAMENTO](https://github.com/daniel-leilao/bidnoculus_bill/blob/master/docs/ALINHAMENTO_ECOSISTEMA_BIDNOCULUS.md) · [`CONSUMO_CREDITOS_SUBPROJETOS`](https://github.com/daniel-leilao/bidnoculus_bill/blob/master/docs/arquitetura/CONSUMO_CREDITOS_SUBPROJETOS.md)
