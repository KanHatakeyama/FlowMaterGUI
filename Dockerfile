FROM continuumio/miniconda3

RUN conda create -n chemodel python==3.9

SHELL ["conda", "run", "-n", "chemodel", "/bin/bash", "-c"]

# pip
RUN pip3 install --upgrade pip
RUN pip3 install django-nested-inline
RUN pip3 install django-bootstrap5
RUN pip3 install django-ckeditor
RUN pip3 install django-import-export
RUN pip3 install django-cleanup
RUN pip3 install gunicorn

# conda
RUN conda install -c anaconda django
RUN conda install -c rdkit -c conda-forge rdkit --override-channels
RUN conda install -c anaconda pillow
RUN conda install dtale -c conda-forge
RUN conda install django-heroku -c conda-forge --override-channels


RUN mkdir /code
WORKDIR /code
ADD . /code

CMD gunicorn --bind 0.0.0.0:$PORT config.wsgi