FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -e .

CMD ["python", "scripts/audit_laws_of_ux.py", "--help"]
