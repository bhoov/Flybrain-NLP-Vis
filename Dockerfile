FROM python:3.8-slim

# Need cmake for this project...
RUN apt update && apt install -y gcc clang clang-tools cmake
# Make bash the default shell
#SHELL [ "/bin/bash", "--login", "-c" ]
# RUN conda config --set auto_activate_base false

WORKDIR /app

# Backend
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend backend
COPY setup.py setup.py
RUN pip install -e .

COPY biohash_project.yaml biohash_project.yaml
# Frontend
# RUN mkdir -p /client
# COPY client/dist client/dist

CMD ["uvicorn",  "--host=0.0.0.0", "--port=8001", "--log-level=debug", "backend.server:app"]