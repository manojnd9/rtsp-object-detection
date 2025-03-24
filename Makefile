# Directories
BACKEND_REPO = object_detection/backend

# Format
format:
	cd ${BACKEND_REPO} && poetry run black .

# Format Check
format_check:
	cd ${BACKEND_REPO} && poetry run black --check .


# Database set-up
db:
	docker-compose up -d

db_down:
	docker-compose down

# Export requirements.txt
requirements:
	poetry export --without-hashes --format=requirements.txt --output requirements.txt