#!/bin/bash
homedir=$1
destdir=$2
cd "$homedir/$destdir" || exit 0
mkdir -p .local/result
script_dir="$(cd "$(dirname "$0")" && pwd)"
if command -v python3 >/dev/null 2>&1; then
    python3 "$script_dir/check_lab2.py" "$homedir" "$destdir" > .local/result/vp9_parity_checkwork.txt 2>&1
else
    echo "N - coefficients_created" > .local/result/vp9_parity_checkwork.txt
    echo "N - coefficients_inspected" >> .local/result/vp9_parity_checkwork.txt
    echo "N - parity_embedding_completed" >> .local/result/vp9_parity_checkwork.txt
    echo "N - message_extracted" >> .local/result/vp9_parity_checkwork.txt
    echo "N - magnitude_analyzed" >> .local/result/vp9_parity_checkwork.txt
    echo "N - labtainer_outputs_ready" >> .local/result/vp9_parity_checkwork.txt
fi
