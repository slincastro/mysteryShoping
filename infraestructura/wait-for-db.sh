#!/bin/bash

# Espera a que la base de datos esté lista
until mysql -h "db" -u "mysteryUser" -p"pass-mystery" -e "SELECT 1"; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 10
done

>&2 echo "MySQL is up - executing command"
