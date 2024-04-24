FROM python:3.12.3

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

ENV PORT=5000
EXPOSE 5000

CMD ["python", "/app/app.py"]