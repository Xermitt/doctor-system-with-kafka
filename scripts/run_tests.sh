#!/bin/bash

echo "Running tests..."


echo "Running tests for api-service..."
docker exec docapp-api-service-1 pytest /app/tests/ -v
if [ $? -ne 0 ]; then
    echo "API Service tests failed!"
    exit 1
fi


echo "Running tests for data-service..."
docker exec docapp-data-service-1 pytest /app/tests/ -v
if [ $? -ne 0 ]; then
    echo "Data Service tests failed!"
    exit 1
fi

echo "All tests completed successfully!"