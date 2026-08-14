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

## Estrutura

- `core/` — álgebra linear pura (numpy), sem dependência de UI
- `plotting/` — canvas matplotlib embutido no Qt + animação
- `ui/` — janela e controles PySide6
- `main.py` — ponto de entrada

## Próximos passos

- Extensão para R³ (matriz 3x3, `Axes3D`)
- Sistemas lineares Ax=b, visualização da solução
