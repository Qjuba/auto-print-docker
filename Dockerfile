FROM node:22-bookworm-slim AS styles

WORKDIR /build
COPY package.json package-lock.json ./
RUN npm ci
COPY app/static ./app/static
COPY app/templates ./app/templates
COPY scripts ./scripts
RUN npm run build:css

FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DATA_DIR=/data \
    CUPS_SERVER=/run/cups/cups.sock \
    APP_PORT=8080

RUN apt-get update && apt-get install -y --no-install-recommends \
      avahi-daemon \
      cups \
      cups-client \
      cups-filters \
      cups-ipp-utils \
      dbus \
      fonts-dejavu-core \
      ghostscript \
      gosu \
      libjpeg62-turbo \
      libmagic1 \
      tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --system --uid 10001 --gid lp --groups lpadmin --home-dir /nonexistent --shell /usr/sbin/nologin autoprint

WORKDIR /opt/autoprint
COPY requirements.txt ./
RUN pip install --requirement requirements.txt

COPY app ./app
COPY --from=styles /build/app/static ./app/static
COPY config/cupsd.conf /etc/cups/cupsd.conf
COPY config/cups-files.conf /etc/cups/cups-files.conf
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod 0755 /usr/local/bin/docker-entrypoint.sh \
    && mkdir -p /data/uploads /data/logs /var/spool/cups/tmp /var/log/cups \
    && chown -R autoprint:lp /data

EXPOSE 8080
VOLUME ["/data", "/etc/cups", "/var/spool/cups"]
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=3)" || exit 1

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
