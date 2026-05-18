#!/usr/bin/env bash
set -eu

LAB_NAME="vp9-parity-coeff-stego"
SENDER_LOCAL_IMAGE="vp9-parity-coeff-stego.sender.student:latest"
ANALYST_LOCAL_IMAGE="vp9-parity-coeff-stego.analyst.student:latest"

if [ -z "${GITHUB_REPO_URL:-}" ]; then
  echo "Missing GITHUB_REPO_URL"
  echo "Example: export GITHUB_REPO_URL=https://github.com/USER/vp9-parity-coeff-stego.git"
  exit 1
fi

if [ -z "${DOCKERHUB_USERNAME:-}" ]; then
  echo "Missing DOCKERHUB_USERNAME"
  echo "Example: export DOCKERHUB_USERNAME=mydockeruser"
  exit 1
fi

if [ -z "${DOCKERHUB_TOKEN:-}" ]; then
  echo "Missing DOCKERHUB_TOKEN"
  echo "Example: export DOCKERHUB_TOKEN='...'"
  exit 1
fi

echo "Preparing Git repository..."
git branch -M main
if git remote | grep -qx origin; then
  git remote set-url origin "$GITHUB_REPO_URL"
else
  git remote add origin "$GITHUB_REPO_URL"
fi

echo "Pushing source to GitHub..."
git push -u origin main

echo "Logging in to Docker Hub as $DOCKERHUB_USERNAME..."
printf '%s' "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

SENDER_REMOTE_IMAGE="$DOCKERHUB_USERNAME/vp9-parity-coeff-stego-sender:latest"
ANALYST_REMOTE_IMAGE="$DOCKERHUB_USERNAME/vp9-parity-coeff-stego-analyst:latest"

echo "Tagging Docker images..."
docker tag "$SENDER_LOCAL_IMAGE" "$SENDER_REMOTE_IMAGE"
docker tag "$ANALYST_LOCAL_IMAGE" "$ANALYST_REMOTE_IMAGE"

echo "Pushing Docker images..."
docker push "$SENDER_REMOTE_IMAGE"
docker push "$ANALYST_REMOTE_IMAGE"

echo "Updating docker-compose.yml image namespace..."
sed -i "s#YOUR_DOCKERHUB_USERNAME#$DOCKERHUB_USERNAME#g" docker-compose.yml
git add docker-compose.yml
if ! git diff --cached --quiet; then
  git commit -m "Set Docker Hub image namespace"
  git push
fi

echo "Done."
echo "GitHub: $GITHUB_REPO_URL"
echo "Docker:"
echo "  $SENDER_REMOTE_IMAGE"
echo "  $ANALYST_REMOTE_IMAGE"

