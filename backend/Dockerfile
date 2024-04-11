FROM python:latest

WORKDIR /api_code

COPY . .

RUN pip install --no-cache-dir -r /api_code/requirements.txt

EXPOSE 8400

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8400", "--reload"]