#Start with an official clean Python environment image
FROM python:3.10-slim

#Install hidden Linux updates required for processing images (OpenCV)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

#Create a folder inside the container called /app to hold our project
WORKDIR /app

#Copy our list of packages over and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy the rest of our application code into the container
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# The final command that runs the app automatically when the container starts
CMD ["python", "app.py"]