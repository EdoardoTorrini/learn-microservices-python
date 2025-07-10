FROM python:3.13-bookworm

RUN mkdir /root/src
COPY ./src /root/src
RUN python -m pip install -r /root/src/requirements.txt

CMD ["python", "/root/src/main.py"]