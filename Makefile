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
	cd ${BACKEND_REPO} && docker-compose up -d

db_down:
	cd ${BACKEND_REPO} && docker-compose down