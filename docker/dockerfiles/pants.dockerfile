FROM python:3.9
ENV PYTHONUNBUFFERED 1
# Adding new user inside container
SHELL ["/bin/bash", "-c"]
ENV PATH "/home/fastapi/.local/bin:$PATH"
WORKDIR /home/fastapi/code
# COPY docker/scripts/startup.sh /home/fastapi/code/
# ENTRYPOINT ["./startup.sh"]

