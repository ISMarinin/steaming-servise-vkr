FROM python:3.10.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /education
WORKDIR /education
COPY requirements.txt /education/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /education/