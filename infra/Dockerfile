# Use the official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

# Copy the application code
COPY app/ /app/
COPY scripts/ /scripts/

# Expose the Flask app port
EXPOSE 8080

# Command to run the Flask app
CMD ["python", "app.py"]
