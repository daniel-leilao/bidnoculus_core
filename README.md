# bidnoculus_core

Serviço MVP: **pesquisa**, **perfis/filtros**, acesso ao **MongoDB de veículos** (`leiloes` ou equivalente), integração com **`bidnoculus_bill`** (`POST /credits/consume`).

**Irmãos:** [`bidnoculus_frontgpt`](https://github.com/daniel-leilao/bidnoculus_frontgpt) · [`bidnoculus_bill`](https://github.com/daniel-leilao/bidnoculus_bill)

**Guarda-chuva:** [`bidnoculus_lancto`](https://github.com/daniel-leilao/bidnoculus_lancto) (submódulos)

## Próximo passo (repositório GitHub)

1. Criar no GitHub o repositório **`daniel-leilao/bidnoculus_core`** (público ou privado).
2. Na pasta deste projeto:

```powershell
cd C:\Users\Joao Bolsoni\ProjetosAI\bidnoculus_core
git init -b main
git add README.md .gitignore
git commit -m "chore: esqueleto inicial bidnoculus_core"
git remote add origin https://github.com/daniel-leilao/bidnoculus_core.git
git push -u origin main
```

3. No repo **`bidnoculus_lancto`**, adicionar submódulo:

```powershell
cd C:\Users\Joao Bolsoni\ProjetosAI\bidnoculus_lancto
git submodule add https://github.com/daniel-leilao/bidnoculus_core.git bidnoculus_core
git commit -m "chore: submodule bidnoculus_core"
git push
```

## Variáveis (alinhamento Bill)

- `BILL_API_URL` — URL pública do Bill  
- `JWT_SECRET` — mesmo segredo que o Bill valida (ou fluxo só com `BILL_API_TOKEN` server-side; ver doc do Bill)

Documentação: [`bidnoculus_bill` — ALINHAMENTO](https://github.com/daniel-leilao/bidnoculus_bill/blob/master/docs/ALINHAMENTO_ECOSISTEMA_BIDNOCULUS.md)
