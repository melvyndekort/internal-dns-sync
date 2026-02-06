FROM docker.io/rust:alpine AS builder

WORKDIR /build
RUN apk add --no-cache musl-dev

COPY toml-merge/ .
RUN cargo build --release

FROM alpine:latest

RUN apk add --no-cache git bash openssh-client

COPY --from=builder /build/target/release/toml-merge /usr/local/bin/toml-merge
COPY pihole-dns-sync.sh /usr/local/bin/pihole-dns-sync.sh
RUN chmod +x /usr/local/bin/pihole-dns-sync.sh

CMD ["/usr/local/bin/pihole-dns-sync.sh"]
