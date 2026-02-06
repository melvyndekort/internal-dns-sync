FROM alpine:latest

RUN apk add --no-cache git bash openssh-client

COPY pihole-dns-sync.sh /usr/local/bin/pihole-dns-sync.sh
RUN chmod +x /usr/local/bin/pihole-dns-sync.sh

CMD ["/usr/local/bin/pihole-dns-sync.sh"]
