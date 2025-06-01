#!/bin/bash

echo "Initializing database..."

docker exec docapp-postgres-1 psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "SELECT 1" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "Database connection successful!"
else
    echo "Failed to connect to database!"
    exit 1
fi

echo "Database initialization completed."