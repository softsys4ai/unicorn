FROM python:3.6.9

RUN pip install --upgrade pip

RUN pip install -U numpy
RUN pip install -U pandas
RUN pip install -U javabridge
RUN pip install -U pydot
RUN pip install -U graphviz

RUN pip install git+git://github.com/bd2kccd/py-causal

RUN pip install git+git://github.com/fmfn/BayesianOptimization


RUN pip install scipy matplotlib \
    seaborn networkx causalgraphicalmodels \
    causality statsmodels pyyaml ananke-causal \
    tqdm mlxtend scikit-learn 

WORKDIR /root


