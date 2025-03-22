# Directories
BACKEND_REPO = object_detection/backend

# Format
format:
	cd ${BACKEND_REPO} && poetry run black .

# Format Check
format_check:
	cd ${BACKEND_REPO} && poetry run black --check .
