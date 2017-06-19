FROM python:2-onbuild
RUN pip install -r requirements.txt
COPY ./src /usr/src/app
CMD ["python", "server.py"]
EXPOSE 5000
