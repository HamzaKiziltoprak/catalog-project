# Set the python version as a build-time argument
ARG PYTHON_VERSION=3.13-slim
FROM python:${PYTHON_VERSION}

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Add src folder to Python module search path
ENV PYTHONPATH=/app/src

# Install system packages required for dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libjpeg-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only requirements.txt first
COPY requirements.txt /app/

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Now copy all code
COPY . /app/

# Create startup script
RUN printf "#!/bin/bash\n" > ./run.sh && \
    printf "RUN_PORT=\"\${PORT:-8000}\"\n\n" >> ./run.sh && \
    printf "cd src && python manage.py collectstatic --noinput\n" >> ./run.sh && \
    printf "python manage.py migrate --no-input\n" >> ./run.sh && \
    printf "gunicorn product_catalog.wsgi:application --bind \"0.0.0.0:8000\" --log-level debug\n" >> ./run.sh

# Make the script executable
RUN chmod +x run.sh

# Clean up unnecessary packages
RUN apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Start the application
CMD ["./run.sh"]
