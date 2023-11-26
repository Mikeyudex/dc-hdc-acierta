# Use Python 3.11 as the base image
FROM python:3.7

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install Python dependencies
RUN apt-get update && apt-get install libxmlsec1-dev -y && pip install xmlsec


# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

EXPOSE 5500

# Set the default command to run the application
CMD ["python", "app.py"]