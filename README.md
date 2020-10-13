# CAUPER
## Dependencies
* pandas
* flask
* Keras 
* PyTorch
* Tensorflow
* numpy 
* json 
* causalgraphicalmodels
* causalnex
* graphviz 
* py-causal 

## Run
To run experiment please use the following two commands:
```python
command: python RunService.py
```
Once the flask app is running and modelserver is ready use the following command: 
For example, to run optimization with GP in online with measurements.csv as initial data use: 
```python
command: python RunParams.py
```

To run causal models in the Data/Output directory please use the following command:
```python
command: python causal_model.py  datafile softwaresystem hardwaresystem
```
For example, to build causal models using NOTEARS and fci for image recognition software 
system and TX1 hardware with observational datafile irtx1.csv use the following: 
```python
command: python causal_model.py  irtx1.csv IR TX1
```
