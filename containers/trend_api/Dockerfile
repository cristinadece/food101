FROM python:2-onbuild
RUN pip install -r requirements.txt
COPY ./src /usr/src/app
CMD ["sh", "services.sh"]
EXPOSE 5000
