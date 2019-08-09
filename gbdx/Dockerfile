FROM continuumio/miniconda:latest

# create the conda environment
RUN mkdir /helper
COPY ./environment.yml /helper
RUN conda env create -f /helper/environment.yml

# get Sen2Cor executables
RUN  cd /helper && wget http://step.esa.int/thirdparties/sen2cor/2.8.0/Sen2Cor-02.08.00-Linux64.run
# install
RUN sh /helper/Sen2Cor-02.08.00-Linux64.run --target /helper/sen2cor
## add the path to hit the excutables
ENV PATH /helper/sen2cor/bin:$PATH

# move the scripts over
ADD . /s2_preprocessor
SHELL ["/bin/bash", "-c"]
RUN echo "source activate s2_preprocessor" > ~/.bashrc
ENV PATH /opt/conda/envs/s2_preprocessor/bin:$PATH
ENV PATH /opt/conda/envs/s2_preprocessor/bin:$PATH
RUN cd /s2_preprocessor && python setup.py install

ENV PYTHONPATH /s2_preprocessor









