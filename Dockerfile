# Python runtime image
FROM python:3.11.0-slim

# Set environment variables: Prevent .pyc files and enable real-time logging
ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1

# Set the working dir
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy lock + project file
COPY pyproject.toml poetry.lock ./

# Install deps (no venv creation)
RUN poetry config virtualenvs.create false && poetry install --no-root

# Copy rest of the application
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8080

# Run the FastAPI application
CMD ["uvicorn", "object_detection.backend.main_api:app", "--host", "0.0.0.0", "--port", "8080"]