#!/bin/sh
set -eu

mkdir -p /run/cups /run/dbus /var/spool/cups/tmp /var/log/cups /data/uploads /data/logs
chown -R lp:lp /run/cups /var/spool/cups /var/log/cups
chown -R autoprint:lp /data

if [ ! -f /run/dbus/pid ]; then
  dbus-daemon --system --fork
fi
avahi-daemon --daemonize --no-chroot >/dev/null 2>&1 || true
cupsd

attempt=0
while [ ! -S /run/cups/cups.sock ]; do
  attempt=$((attempt + 1))
  if [ "$attempt" -ge 50 ]; then
    echo "CUPS did not create its socket" >&2
    exit 1
  fi
  sleep 0.2
done

proxy_headers="--no-proxy-headers"
if [ "${TRUST_PROXY_HEADERS:-false}" = "true" ]; then
  proxy_headers="--proxy-headers"
fi

exec gosu autoprint uvicorn app.main:app \
  --host "${APP_HOST:-0.0.0.0}" \
  --port "${APP_PORT:-8080}" \
  "$proxy_headers" \
  --no-server-header
