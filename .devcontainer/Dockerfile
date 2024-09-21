FROM mcr.microsoft.com/devcontainers/python:3.12

ARG USER=vscode

USER ${USER}

ENV HOME=/home/${USER}
ENV PYTHONUNBUFFERED 1
ENV PYTHONPYCACHEPREFIX=/home/${USER}/.cache/python

# Update OS packages
RUN export DEBIAN_FRONTEND=noninteractive \
    && sudo apt-get update \
    && sudo apt-get upgrade -y \
    && sudo apt-get install -y build-essential git

ENV PATH="/home/vscode/.local/bin:$PATH"

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
