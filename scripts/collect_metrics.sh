#!/bin/bash
# collect_metrics.sh
# Recolecta métricas del sistema y las imprime en formato JSON
# Uso: ./collect_metrics.sh

set -euo pipefail
# set -e  → el script falla si cualquier comando falla
# set -u  → falla si usas una variable no definida
# set -o pipefail → falla si cualquier comando en un pipe falla

# ── funciones ─────────────────────────────────────────────

get_cpu() {
    grep 'cpu ' /proc/stat | awk '{
        usage=($2+$4)*100/($2+$3+$4+$5)
        printf "%d", usage
    }'
}

get_ram() {
    # free -m: muestra memoria en megabytes
    # awk 'NR==2': procesa solo la segunda línea (Mem:)
    # $2=total, $3=usado — calcula porcentaje
    free -m | awk 'NR==2 {
        total=$2
        used=$3
        pct=int(used*100/total)
        printf "%d %d %d", used, total, pct
    }'
}

get_disk() {
    # df -h /: uso del disco en la raíz
    # awk 'NR==2': segunda línea (datos, no header)
    # $3=usado, $2=total, $5=porcentaje
    df -h / | awk 'NR==2 {
        gsub(/%/,"",$5)    # elimina el % del porcentaje
        printf "%s %s %s", $3, $2, $5
    }'
}

get_uptime() {
    # uptime -p: uptime en formato legible ("up 2 days, 3 hours")
    uptime -p | sed 's/up //'    # elimina el "up " del inicio
}

get_load() {
    # /proc/loadavg: archivo del kernel con load average
    # cut -d' ' -f1,2,3: toma los primeros 3 campos (1m, 5m, 15m)
    cat /proc/loadavg | cut -d' ' -f1,2,3
}

# ── recolectar datos ───────────────────────────────────────

CPU=$(get_cpu)
read RAM_USED RAM_TOTAL RAM_PCT <<< $(get_ram)
read DISK_USED DISK_TOTAL DISK_PCT <<< $(get_disk)
UPTIME=$(get_uptime)
read LOAD_1 LOAD_5 LOAD_15 <<< $(get_load)
HOSTNAME=$(hostname)
TIMESTAMP=$(date -u '+%Y-%m-%dT%H:%M:%SZ')    # formato ISO 8601

# ── output en JSON ────────────────────────────────────────
# printf es más preciso que echo para formatear strings
cat << EOF
{
  "timestamp": "$TIMESTAMP",
  "hostname": "$HOSTNAME",
  "cpu": {
    "usage_pct": $CPU
  },
  "ram": {
    "used_mb": $RAM_USED,
    "total_mb": $RAM_TOTAL,
    "usage_pct": $RAM_PCT
  },
  "disk": {
    "used": "$DISK_USED",
    "total": "$DISK_TOTAL",
    "usage_pct": $DISK_PCT
  },
  "load_average": {
    "1m": $LOAD_1,
    "5m": $LOAD_5,
    "15m": $LOAD_15
  },
  "uptime": "$UPTIME"
}
EOF
