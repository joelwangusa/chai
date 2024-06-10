#!/bin/bash

message=$1

curl -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" -d '{
  "input_text": "'"${message}"'"
}'