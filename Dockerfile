FROM alpine:latest

RUN apk add --no-cache python3 py3-cryptography py3-lxml py3-twisted

RUN pip3 install scrapy scrapyd

EXPOSE 6800

ENTRYPOINT ["scrapyd"]
