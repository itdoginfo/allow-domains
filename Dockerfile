FROM ghcr.io/sagernet/sing-box:v1.10.7 AS sing-box

FROM python:3.10.16-alpine3.21

COPY --from=sing-box /usr/local/bin/sing-box /bin/sing-box

RUN pip install --no-cache-dir tldextract

WORKDIR /app

COPY convert.py /app/convert.py

CMD ["python3", "convert.py"]