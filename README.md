# CAUPER
This paper proposes CAUPER(short for Causal Performance Debugging) that enables users toidentify, explain, and 
fix the root cause of non-functional faults early and in a principled fashion. CAUPER builds a causal model by 
observing the performance of the system under different configurations. Then, it uses casual path extraction 
followed by counterfactual reasoning over the causal model to:  (a) identify the root causes of non-functional faults, 
(b) estimate the effects of various configurable parameters on the performance objective(s), and (c) prescribe candidate 
repairs to the relevant configuration options to fix the non-functional fault. 
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
## Contacts
|Name|Email|     
|---------------|------------------|      
|Shahriar Iqbal|miqbal@email.sc.edu|      
|Rahul Krishna|i.m.ralk@gmail.com|
