# Base image with PyTorch and CUDA support.
# If a GPU is not available, PyTorch will automatically fallback to CPU.
FROM pytorch/pytorch:2.2.1-cuda12.1-cudnn8-runtime

# Set environment variables to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies required for audio processing (ffmpeg)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Gradio default port
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

# Command to run the application
CMD ["python", "app.py"]
