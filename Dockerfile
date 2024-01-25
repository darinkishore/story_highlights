# Use an official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the Django app runs on
EXPOSE 8000

# Specify the command to start the Django server using gunicorn
CMD ["gunicorn", "vercel_app.wsgi:application", "--bind", "0.0.0.0:8000"]
