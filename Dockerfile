# Use an official lightweight Python image as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# --- ADD THESE TWO LINES TO INSTALL CPU-ONLY TORCH ---
# This version is much smaller and faster to download
RUN pip install torch==2.2.1 --index-url https://download.pytorch.org/whl/cpu

# Copy the requirements file and install the rest of the packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ... (rest of your Dockerfile remains the same) ...
COPY . .
CMD ["python", "run.py"]