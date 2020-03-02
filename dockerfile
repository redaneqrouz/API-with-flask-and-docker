FROM python:3 

WORKDIR /project

ADD . /project

LABEL Author="Reda NEQROUZ"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

RUN pip3 install -r requirements.txt 

EXPOSE 5001

ENTRYPOINT [ "python" ] 


CMD [ "main.py"] 
