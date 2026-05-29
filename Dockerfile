FROM python:3.12-slim 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN pip3 install --upgrade pip -i https://package-mirror.liara.ir/repository/pypi/simple

COPY requirements.txt /app/

RUN pip3 install --no-cache-dir -r requirements.txt -i https://package-mirror.liara.ir/repository/pypi/simple

COPY . /app/
