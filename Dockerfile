FROM ghcr.io/sagernet/sing-box:v1.10.7 AS sing-box

FROM golang:1.23.1-alpine3.20 AS golang

FROM python:3.10.16-alpine3.21

COPY --from=sing-box /usr/local/bin/sing-box /bin/sing-box

COPY --from=golang /usr/local/go /usr/local/go

ENV GOROOT=/usr/local/go

ENV PATH="/usr/local/go/bin:${PATH}"

RUN pip install --no-cache-dir tldextract

COPY src/xray-geosite /app/xray-geosite

WORKDIR /app/xray-geosite

RUN go mod download

WORKDIR /app

COPY convert.py /app/convert.py

CMD ["python3", "convert.py"]