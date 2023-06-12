FROM python:3.8-slim-buster

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Copy the code into the container
COPY . /app/

# Install the Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
