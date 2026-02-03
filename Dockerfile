FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Create an internal virtual environment (to mirror local .venv usage)
RUN python -m venv .venv
ENV PATH="/app/.venv/Scripts:/app/.venv/bin:$PATH"

# Install runtime dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8000

# Run the FastAPI app via uvicorn inside the venv
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

