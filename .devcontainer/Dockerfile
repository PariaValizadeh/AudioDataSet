# Use a lightweight ARM64 Python 3.12 base image
#change it if you use it on windows
#FROM arm64v8/python:3.12-bullseye
FROM ubuntu/python:3.10-22.04_stable



# Set non-interactive mode to avoid prompts during installation
ARG DEBIAN_FRONTEND=noninteractive

# Install necessary build tools and system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcairo2-dev \
    pkg-config \
    python3-dev \
    git \
    curl \
    bash-completion \
    ssh \
    vim \
    tmux \
    htop \
    ffmpeg \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libffi-dev \
    wget

# Install Poetry for Python dependency management
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to the PATH
ENV PATH="/root/.local/bin:$PATH"

# Set DEBIAN_FRONTEND back to dialog for a standard apt-get experience
ARG DEBIAN_FRONTEND=dialog

# Optional: Pre-install project dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --only main
