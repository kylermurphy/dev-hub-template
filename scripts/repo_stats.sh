#!/usr/bin/env bash
# repo_stats.sh — clone a repo and print the mechanical facts for the dev-hub Repo Overview.
# Usage: scripts/repo_stats.sh <repo-url | owner/name | name>
# Bare name defaults to github.com/$DEVHUB_OWNER/<name> (set DEVHUB_OWNER to your GitHub user/org).
# No pipefail: several pipelines end in `head`/`grep -q`, which close the pipe early and
# would otherwise trip `set -e` via SIGPIPE upstream.
set -eu

arg="${1:?usage: repo_stats.sh <repo-url|owner/name|name>}"
case "$arg" in
  http*://*) url="$arg" ;;
  */*)       url="https://github.com/$arg" ;;
  *)         url="https://github.com/${DEVHUB_OWNER:?set DEVHUB_OWNER or pass owner/name}/$arg" ;;
esac
name="$(basename "${url%.git}")"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

if ! git clone --quiet "$url" "$tmp/$name" 2>/dev/null; then
  echo "$name: CLONE FAILED ($url)"
  echo "  -> private repo needs GitHub access, or the URL is wrong."
  echo "  -> Repo Overview State for this repo: \"unreachable — needs GitHub access\""
  exit 1
fi
cd "$tmp/$name"

commits=$(git rev-list --count HEAD 2>/dev/null || echo '?')
first=$(git log --reverse --format=%cs 2>/dev/null | head -1)
last=$(git log -1 --format=%cs 2>/dev/null)
branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)

# Top file extensions (a hint for the Stack column; Claude names the real languages)
langs=$(git ls-files | awk -F. 'NF>1{print tolower($NF)}' | sort | uniq -c | sort -rn \
  | awk '{print $2}' | head -6 | tr '\n' ',' | sed 's/,$//')

has_ci='no'
if ls .github/workflows/*.y*ml >/dev/null 2>&1; then has_ci='yes'; fi

has_tests='no'
if find . -path ./.git -prune -o -type d -name tests -print 2>/dev/null | grep -q . \
   || find . -path ./.git -prune -o -name 'test_*.py' -print 2>/dev/null | grep -q . ; then
  has_tests='yes'
fi

pkg=''
for f in pyproject.toml setup.py setup.cfg Gemfile package.json; do
  [ -f "$f" ] && pkg="$pkg $f"
done

echo "=== $name ==="
echo "url:        $url"
echo "commits:    $commits"
echo "first:      ${first:-?}"
echo "last:       ${last:-?}"
echo "branch:     $branch"
echo "extensions: ${langs:-none}"
echo "CI:         $has_ci"
echo "tests:      $has_tests"
echo "packaging: ${pkg:- none}"
echo
echo "Repo Overview row (fill Purpose, Stack, State by judgment; format Last active e.g. 'May 2026'):"
echo "| $name | <purpose> | $commits | ${last:-?} | <stack> | <state> |"
