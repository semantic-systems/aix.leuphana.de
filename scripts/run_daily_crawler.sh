#!/usr/bin/env bash
set -u

cd /site
site_snapshot=/tmp/aix-link-check-site

while true; do
    run_started=$(date +%s)
    echo "Starting daily publication fetch, site build, and link check at $(date -u '+%Y-%m-%d %H:%M:%S UTC')"

    if ! python3 /site/scripts/fetch_publications.py; then
        echo 'Publication fetch failed; building from the current source files.'
    fi

    if bundle exec jekyll build --disable-disk-cache --destination "$site_snapshot"; then
        echo "Fresh site build completed in $site_snapshot; checking links..."
        python3 -u /site/scripts/check_broken_links.py --site-dir "$site_snapshot" || \
            echo 'Link check failed; no result was sent for this run.'
    else
        echo 'Jekyll build failed; link check skipped. No clean result was sent.'
    fi

    elapsed=$(( $(date +%s) - run_started ))
    delay=$(( 86400 - elapsed ))
    if (( delay > 0 )); then
        echo "Sleeping ${delay} seconds until the next daily run..."
        sleep "$delay"
    fi
done
