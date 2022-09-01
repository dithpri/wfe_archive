#!/bin/sh

rm -r archive; mkdir -p archive
total=$(git rev-list main | wc -l)
i=0
git rev-list main | tac | while read -r commit; do
    changedate="$(git rev-list --no-commit-header --format=%B --max-count=1 "$commit")"
    rev="$(git rev-list --no-commit-header --format=%H --max-count=1 "$commit")"
    git diff --name-only "$commit^" "$commit" | while read -r file; do
        if [ "$(dirname "$file")" = "archive" ]; then
            html_file="${file%.txt}.html"
            region_name="$(basename "$file" .txt)"
            if [ ! -f "$html_file" ]; then
                printf '<head><title>%s</title><link rel="stylesheet" href="../style.css"></head>' "$region_name" > "$html_file"
                printf '<h1>%s</h1>' "$region_name" >> "$html_file"
            fi
            printf '<a class="wfe-link" href="%s">%s</a><br/>' "https://raw.github.com/dithpri/wfe_archive/$rev/$file" "$changedate" >> "$html_file"
            echo "$file" >> idx
        fi
    done
    sort -Vu idx > idx_sorted
    mv idx_sorted idx
    i=$((i+1))
    printf "\r%s/%s\t%s" "$i" "$total" "$changedate"
done
printf '<head><title>WFE Archive</title><link rel="stylesheet" href="./style.css"></head>\n' > "full-index.html"
awk '{match($0, /^(archive\/)(.*)(\.txt)$/, arr); print "<a class=\"region-archive-link\" href=\"" arr[1] arr[2] ".html\">" arr[2] "</a><br/>"}' idx >> full-index.html
