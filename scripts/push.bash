#!/bin/bash

# Git Push Script
# Usage: ./scripts/push.bash "Your commit message"

if [ -z "$1" ]; then
    echo "Please provide a commit message"
    echo "Usage: ./scripts/push.bash \"Your commit message\""
    exit 1
fi

COMMIT_MSG="$1"

echo "Adding all changes..."
git add .

echo "Committing changes..."
git commit -m "$COMMIT_MSG"

echo "Pushing to remote repository..."
git push

echo "Done!"

