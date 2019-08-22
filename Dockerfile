FROM ubuntu:18.04 AS BUILD

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y python3.7 python3-pip cmake make libsm6 libxext6 libxrender-dev
RUN python3.7 -m pip install --upgrade pip
RUN apt-get install -y git

RUN git clone https://github.com/opencv/opencv.git
WORKDIR /opencv/build
RUN cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local ..
RUN make -j10
RUN make install

COPY . /app
WORKDIR /app

RUN git checkout $BRANCH_NAME
RUN make deps
RUN pip3 install matplotlib
RUN pip3 install pandas
RUN pip3 install tqdm
CMD PYTHON=python3.7 PIP=pip3.7 make run
