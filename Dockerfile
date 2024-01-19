FROM python:3.8-slim

WORKDIR /app

COPY version.txt .

COPY Craftdemo.py .

RUN pip install --no-cache-dir -r version.txt

RUN pip install --no-cache-dir Flask Werkzeug requests

CMD ["python", "Craftdemo.py"]

