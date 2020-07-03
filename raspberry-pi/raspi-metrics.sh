#!/usr/bin/env bash

set -eu -o pipefail

SECONDS=${1:-60}

iso8601_timestamp() {
  date -u +%FT%TZ
}

current_cpu_temp_in_c() {
  /opt/vc/bin/vcgencmd measure_temp | cut -d"=" -f2 | cut -d"'" -f1
}

actual_cpu_clock_speed() {
  /opt/vc/bin/vcgencmd measure_clock arm | cut -d"=" -f2 | cut -d"'" -f1
}

desired_cpu_clock_speed() {
  cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
}

for i in `seq 1 $SECONDS`; do
  echo "$(iso8601_timestamp), $(current_cpu_temp_in_c), $(actual_cpu_clock_speed), $(desired_cpu_clock_speed)"
  sleep 1
done
