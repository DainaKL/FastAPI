FROM python:3.13.13-alpine

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH /app/src

COPY ./src /app/src
COPY alembic /app/alembic
COPY alembic.ini /app/
COPY requirements.txt /app/
COPY main.py /app/

WORKDIR /app

RUN mkdir -p /app/media

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]