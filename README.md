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
* causality 
* python 3.6
## Run
To run experiment please use the following two commands:
```python
command: python RunService.py softwaresystem
```
Once the flask app is running and modelserver is ready use the following command: 
For example, to run optimization with GP in online with measurements.csv as initial data use: 
```python
command: python RunParams.py softwaresystem
```

To run causal models for a single-objective bug please run the following:
```python
command: python RunCausalModel.py  -o objective1 -d datafile -s softwaresystem -k hardwaresystem
```
For example, to build causal models using NOTEARS and fci for image recognition software 
system in TX1 with initial datafile irtx1.csv use the following for a latency (single objective) bug : 
```python
command: python RunCausalModel.py  -o inference_time -d irtx1.csv -s Image -k TX1
```

To run causal models for a multi-objective bug please run the following:
```python
command: python RunCausalModel.py  -o objective1 -o objective2 -d datafile -s softwaresystem -k hardwaresystem
```
For example, to build causal models using NOTEARS and fci for image recognition software 
system in TX1 with initial datafile irtx1.csv use the following for a latency and energy consumption (multi-ojective) bug : 
```python
command: python RunCausalModel.py  -o inference_time -o total_energy_consumption -d irtx1.csv -s Image -k TX1
```
