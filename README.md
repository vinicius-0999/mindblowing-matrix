# matriz-visual

App desktop para estudar transformações lineares em R²: edite os 4 elementos de uma matriz
2x2 e veja em tempo real o efeito sobre a grade cartesiana, o quadrado unitário, os vetores
da base e os autovetores/autovalores.

## Rodando

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Estrutura

- `core/` — álgebra linear pura (numpy), sem dependência de UI
- `plotting/` — canvas matplotlib embutido no Qt + animação
- `ui/` — janela e controles PySide6
- `main.py` — ponto de entrada

## Próximos passos

- Extensão para R³ (matriz 3x3, `Axes3D`)
- Sistemas lineares Ax=b, visualização da solução
