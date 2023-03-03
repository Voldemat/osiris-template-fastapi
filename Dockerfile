FROM python:3.10-alpine as builder

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN apk update && apk add gcc musl-dev g++
RUN pip install --upgrade pip && pip install --user --no-warn-script-location pipenv Cython

ENV REPOSITORY_USER=vladimirdev635
ENV REPOSITORY_PASSWORD=glpat-ms2sRwwwVd5yKVXaL9J4

COPY Pipfile* ./
RUN python3 -m pipenv install --system --deploy --dev
RUN pip uninstall -y setuptools pipenv distlib virtualenv Cython pip

FROM python:3.10-alpine as prod
COPY --from=builder /usr/local/lib/python3.10/ /usr/local/lib/python3.10/
COPY --from=builder /root/.local/lib/python3.10/ /root/.local/lib/python3.10/
WORKDIR /usr/local/app
COPY ./ ./
CMD ["python3", "."]
