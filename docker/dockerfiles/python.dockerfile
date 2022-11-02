FROM python:3.9
ENV PYTHONUNBUFFERED 1
# Adding new user inside container
ARG USER_ID
ARG GROUP_ID
RUN addgroup --gid 1000 fastapi
RUN adduser --disabled-password --gecos '' --uid 1000 --gid 1000 fastapi
USER fastapi
# Use bash shell
SHELL ["/bin/bash", "-c"]
ENV PATH "/home/fastapi/.local/bin:$PATH"
RUN mkdir /home/fastapi/code
WORKDIR /home/fastapi/code
COPY requirements.txt /home/fastapi/code/
# Cashing pip
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

