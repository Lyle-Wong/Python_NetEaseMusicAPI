FROM python:3.9

ENV APP_ROOT /src

RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}

COPY Pipfile ${APP_ROOT}/Pipfile

RUN pip install pipenv
RUN pipenv install

ADD . ${APP_ROOT}