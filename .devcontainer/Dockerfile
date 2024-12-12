# Use a lightweight ARM64 Python 3.12 base image
#change it if you use it on windows
#FROM arm64v8/python:3.12-bullseye
FROM python:3.10-slim

# Install bash if it's missing
RUN apt-get update && apt-get install -y bash
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

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
    wget\
    portaudio19-dev\ 
    alsa-utils
    
COPY config/.tmux.conf /home/$USERNAME/.tmux.conf

USER $USERNAME
    

    
# Install Poetry for Python dependency management
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to the PATH
ENV PATH="/home/$USERNAME/.local/bin:$PATH"

# Set DEBIAN_FRONTEND back to dialog for a standard apt-get experience
ARG DEBIAN_FRONTEND=dialog

# Optional: Pre-install project dependencies
#COPY pyproject.toml poetry.lock ./
#COPY ../pyproject.toml ../poetry.lock ./
#RUN poetry install --no-root --only main
