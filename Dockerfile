FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Install system dependencies (none needed for SQLite)

# Copy project files
COPY . /app/

# Create virtual environment and install Python dependencies
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir django djangorestframework openai requests



# Expose port for Django
EXPOSE 8000

# Run migrations, create default user and simulate conversations on container start
CMD ["bash", "-c", \
     ". /opt/venv/bin/activate && \
      python manage.py migrate --noinput && \
      # Run simulation (also creates default user) and start server\n\
      python manage.py simulate_conversations && \
      python manage.py runserver 0.0.0.0:8000" ]