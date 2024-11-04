# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Install GCC and other dependencies
RUN apt-get update && apt-get install -y build-essential -y libsqlite3-dev

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory into the container
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "CloudBot.py", "--server.port=8501", "--server.address=0.0.0.0", "--browser.gatherUsageStats=false"]

