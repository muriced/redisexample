FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install wheel && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip cache purge && rm -rf /root/.cache

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]