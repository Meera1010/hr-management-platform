.PHONY: install build run test clean

install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

build:
	cd frontend && npm run build

test:
	cd backend && python -m pytest

run:
	cd backend && python app.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
