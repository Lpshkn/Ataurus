FROM snakepacker/python:3.7 as ataurus
MAINTAINER lpshkn
COPY . /Ataurus
WORKDIR /Ataurus

RUN pip install -U pip && pip install -Ur requirements.txt
RUN python3 setup.py test && python3 setup.py install
ENTRYPOINT ["Ataurus"]