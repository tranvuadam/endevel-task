FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /endevel_blog_app_workdir
COPY requirements.txt /endevel_blog_app_workdir/
RUN pip install -r requirements.txt
COPY . /endevel_blog_app_workdir/