#!/usr/bin/env bash

if docker info >/dev/null 2>&1; then
  echo "Docker działa."
  exit 0
fi

echo "Docker nie działa. Próba uruchomienia..."
sudo systemctl start docker

if docker info >/dev/null 2>&1; then
  echo "Docker został uruchomiony."
else
  echo "Nie udało się uruchomić Dockera." >&2
  exit 1
fi