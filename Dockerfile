FROM ghcr.io/sagernet/sing-box:v1.12.25 AS sing-box

FROM python:3.12.12-alpine3.23

COPY --from=sing-box /usr/local/bin/sing-box /bin/sing-box

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

COPY proto/ /app/proto/
COPY convert.py /app/convert.py

CMD ["python3", "convert.py"]
