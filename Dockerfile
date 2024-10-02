FROM python:3.9

WORKDIR /wiki-proxy

COPY requirements.txt .

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]