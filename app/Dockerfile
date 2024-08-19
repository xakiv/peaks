FROM python:3.10.12-bullseye
LABEL name="peaksapp"
WORKDIR /code
COPY ./requirements /code/requirements
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /code/requirements/dev.txt
COPY . /code/app
RUN chmod +x /code/app/entrypoint/wait_for_it.py
RUN chmod +x /code/app/entrypoint/02-start.sh
