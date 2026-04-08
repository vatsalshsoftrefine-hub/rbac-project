FROM python:3.10

# Prevent Python from buffering output
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install django djangorestframework pynamodb

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]