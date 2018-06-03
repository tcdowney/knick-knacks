#!/usr/bin/env bash

set -eu -o pipefail

SECONDS=${1:-60}

iso8601_timestamp() {
  date -u +%FT%TZ
}

current_cpu_temp() {
  /opt/vc/bin/vcgencmd measure_temp
}

current_cpu_clock_speed() {
  cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
}

for i in `seq 1 $SECONDS`; do
 echo "$(iso8601_timestamp), $(current_cpu_temp), $(current_cpu_clock_speed)"
 sleep 1
done
