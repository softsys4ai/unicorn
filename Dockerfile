FROM python:3.6.9

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends openjdk-11-jdk

#----- Set JAVA environment variable -----
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

RUN pip install -U numpy pandas pydot graphviz requests \
    scipy matplotlib seaborn networkx causalgraphicalmodels apscheduler\
    causality statsmodels pyyaml ananke-causal tqdm mlxtend scikit-learn 

# RUN pip install git+git://github.com/bd2kccd/py-causal

RUN pip install git+git://github.com/fmfn/BayesianOptimization

WORKDIR /root


