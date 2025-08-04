#!/bin/bash

cd "$(dirname "$(realpath $0)")"

npm install -g concurrently
concurrently "cd backend; python3 backendApp.py" "cd frontend-gui; npm run dev"
