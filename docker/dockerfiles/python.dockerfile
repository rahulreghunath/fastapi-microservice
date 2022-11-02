FROM python:3.9
ENV PYTHONUNBUFFERED 1
# Adding new user inside container
ARG USER_ID
ARG GROUP_ID
ARG APP_DIR
RUN addgroup --gid $GROUP_ID fastapi
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID fastapi
USER fastapi
ENV RUN_TIME=123  
# Use bash shell
SHELL ["/bin/bash", "-c"]
ENV PATH "/home/fastapi/.local/bin:$PATH"
ENV PYTHONPATH "/home/fastapi/code/$APP_DIR:$PYTHONPATH"
RUN mkdir /home/fastapi/code
WORKDIR /home/fastapi/code
COPY requirements.txt /home/fastapi/code/
# Cashing pip
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

