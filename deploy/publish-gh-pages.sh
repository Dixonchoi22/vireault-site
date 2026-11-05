#!/usr/bin/env bash
# Build and publish dist/ to the gh-pages branch (GitHub Pages "deploy from branch").
# Custom domain later: SITE_URL=https://yourdomain BASE_PATH=/ ./deploy/publish-gh-pages.sh
set -euo pipefail
cd "$(dirname "$0")/.."
npm run build
rev=$(git rev-parse --short HEAD)
tmp=$(mktemp -d)
cp -r dist/. "$tmp"/
touch "$tmp/.nojekyll"
[ -f public/CNAME ] && cp public/CNAME "$tmp/"
git -C "$tmp" init -q -b gh-pages
git -C "$tmp" add -A
git -C "$tmp" -c user.name="$(git config user.name)" -c user.email="$(git config user.email)" commit -qm "Deploy $rev"
git -C "$tmp" push -f "$(git remote get-url origin)" gh-pages
rm -rf "$tmp"
