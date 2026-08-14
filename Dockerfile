FROM python:3.12-slim

# libs de runtime do Qt (mesmo conjunto necessário no sandbox pra rodar PySide6 headless)
# + Xvfb/x11vnc/noVNC pra expor a janela por navegador, sem servidor X no host
RUN apt-get update && apt-get install -y --no-install-recommends \
    libegl1 libgl1 libxkbcommon0 libxkbcommon-x11-0 libxcb-cursor0 libxcb-icccm4 libxcb-image0 \
    libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxcb-xinerama0 \
    libdbus-1-3 libnss3 fonts-dejavu-core \
    xvfb x11vnc fluxbox novnc websockify \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV QT_QPA_PLATFORM=xcb \
    DISPLAY=:99

EXPOSE 6080

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
