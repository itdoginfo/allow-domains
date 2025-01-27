FROM ghcr.io/sagernet/sing-box:v1.10.7 AS sing-box

FROM python:3.10.16-alpine3.21

COPY --from=sing-box /usr/local/bin/sing-box /bin/sing-box

WORKDIR /app

COPY compile-srs.py /app/compile-srs.py

VOLUME ["/app/Categories", "/app/Services"]

CMD ["python3", "compile-srs.py"]