#!/bin/sh

if [[ $# -lt 1 ]]; then
  echo "ERROR: crontab file must be provided." >&2
  exit 1
fi

case ${1} in
  shell)
    /bin/sh
    ;;
  cron)
    crond -s /opt/cron/periodic \
      -c /opt/cron/crontabs \
      -t /opt/cron/cronstamps \
      -L /dev/stdout \
      -f &
    wait
    ;;
esac
