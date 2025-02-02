FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Add migration step
RUN python -c "from app.models import Base; from app.database import engine; Base.metadata.create_all(bind=engine)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]