#!/usr/bin/env bash
# Live-site fetcher. VERIFICATION ONLY -- never an extraction source (plan decision 1).
# Sequential, 2s between requests, never parallel (owner, 2026-08-13).
# Records raw bytes + headers + fetch timestamp so a truth census is re-derivable.
set -uo pipefail
url="$1"; out="$2"
mkdir -p "$(dirname "$out")"
date -u +%Y-%m-%dT%H:%M:%SZ > "$out.fetched-at"
curl -sS --compressed --max-time 30 \
     -A 'maja-explosiv migration verification (owner-operated, 1 req/2s)' \
     -D "$out.headers" -o "$out" "$url"
rc=$?
printf 'url=%s rc=%s bytes=%s\n' "$url" "$rc" "$(wc -c < "$out" 2>/dev/null || echo 0)"
sleep 2
exit $rc
