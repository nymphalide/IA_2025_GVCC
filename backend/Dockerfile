# backend/Dockerfile

# Utilizează imaginea Python 3.11 Slim (eficientă și stabilă)
FROM python:3.11-slim

# Setează variabile de mediu
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Setează directorul de lucru în container
WORKDIR /app

# Copiază fișierul de dependențe și le instalează
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiază restul codului Python (main.py, api/, logic/)
COPY . .

# Pornește serverul (Comanda este suprascrisă în docker-compose pentru hot-reload)
EXPOSE 8000