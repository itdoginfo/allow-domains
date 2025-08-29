FROM ghcr.io/sagernet/sing-box:v1.11.15 AS sing-box

FROM golang:1.22.12-alpine3.21 AS go-builder

RUN CGO_ENABLED=0 GOOS=linux go install -ldflags="-s -w" \
    github.com/v2fly/domain-list-community@20250207120917

FROM python:3.10.16-alpine3.21

COPY --from=sing-box /usr/local/bin/sing-box /bin/sing-box

COPY --from=go-builder /go/bin/domain-list-community /bin/domain-list-community

RUN pip install --no-cache-dir tldextract

WORKDIR /app

COPY convert.py /app/convert.py

CMD ["python3", "convert.py"]