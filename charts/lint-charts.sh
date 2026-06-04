#!/bin/sh

set -eu

cd "$(dirname "$0")"

rc=0

for chart_yaml in */Chart.yaml; do
	[ -f "$chart_yaml" ] || continue
	chart_dir="$(dirname "$chart_yaml")"
	echo "======= VERIFYING CHART: $chart_dir ======="

	# Ensure local chart dependencies are present if any are declared.
	for stat in $(helm dependency list "$chart_dir" | tail -n +2 | awk '{print $4}'); do
		if [ "$stat" != "ok" ]; then
			helm dependency update "$chart_dir"
			break
		fi
	done

	for values_file in "$chart_dir"/examples/*.yaml; do
		[ -f "$values_file" ] || continue

		echo "------- VERIFYING EXAMPLE: $values_file --------"

		helm template "$chart_dir" -f "$values_file" >/dev/null || {
			rc=1
			echo "--------- TEMPLATE VERIFICATION FAILED: $values_file --------"
		}

		helm lint "$chart_dir" -f "$values_file" || {
			rc=1
			echo "--------- LINT VERIFICATION FAILED: $values_file --------"
		}

		echo "------- FINISHED VERIFYING EXAMPLE: $values_file --------"
		echo
	done

	echo "======= FINISHED CHART: $chart_dir ======="
	echo
done

exit "$rc"
