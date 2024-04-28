FROM pytorch/pytorch

RUN conda update -n base -c defaults conda && \
    conda install -y python=3.11 && \
    conda update --all --yes

WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY recommender/requirements.txt /app/recommender/requirements.txt
COPY . /app
RUN pip3 install -r requirements.txt
RUN pip3 install -r recommender/requirements.txt
RUN pip3 install -i https://pypi.org/simple/ bitsandbytes

EXPOSE 26601

ENTRYPOINT [ "python" ]
CMD ["main.py" ]