# matriz-visual

App desktop para estudar transformações lineares em R²: edite os 4 elementos de uma matriz
2x2 e veja em tempo real o efeito sobre a grade cartesiana, o quadrado unitário, os vetores
da base e os autovetores/autovalores.

## Rodando

### Com Python instalado

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Com Docker Desktop (sem Python na máquina)

```bash
docker compose up --build
```

Abra `http://localhost:6080/vnc.html?autoconnect=true&resize=scale` no navegador — o
container roda um display virtual (Xvfb) + noVNC, então a janela do app aparece na aba
do navegador, sem precisar de servidor X no host. Funciona igual em Mac/Windows/Linux.

### Rodando na nuvem (Railway), sem expor na internet

O serviço `matriz-visual` já está deployado no projeto Railway `autonomous-agents`
(rede privada, **sem domínio público** — não é alcançável da internet). Acesso é só
via túnel SSH até o sandbox (que está na mesma rede privada):

```bash
ssh -L 6080:matriz-visual.railway.internal:6080 dev@sakura.proxy.rlwy.net -p 34783
```

Com o túnel de pé, abra `http://localhost:6080/vnc.html?autoconnect=true&resize=scale`
no navegador local. Deploy de código novo não é automático (serviço criado via API não
ganha o webhook do GitHub) — precisa disparar manualmente.

## Estrutura

- `core/` — álgebra linear pura (numpy), sem dependência de UI
- `plotting/` — canvas matplotlib embutido no Qt + animação
- `ui/` — janela e controles PySide6
- `main.py` — ponto de entrada

## Próximos passos

- Extensão para R³ (matriz 3x3, `Axes3D`)
- Sistemas lineares Ax=b, visualização da solução
