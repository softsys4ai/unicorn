# Unicorn (EuroSys 2022)
Unicorn can be used for performance analyses of highly configurable systems with causal reasoning. Users or developers can query Unicorn for a performance task.
## Overview
![overview](https://user-images.githubusercontent.com/12802456/151218680-5456bcdc-27c0-4736-b54c-7483bc394b8c.png)
## Abstract
Modern computer systems are highly configurable, with the total variability space sometimes larger than the number of atoms in the universe. Understanding and reasoning about the performance behavior of highly configurable systems, due to a vast variability space, is challenging. State-of-the-art methods for performance modeling and analyses rely on predictive machine learning models, therefore, they become (i) unreliable in unseen environments (e.g., different hardware, workloads), and (ii) produce incorrect explanations. To this end, we propose a new method, called Unicorn, which (i) captures intricate interactions between configuration options across the software-hardware stack and (ii) describes how such interactions impact performance variations via causal inference. We evaluated Unicorn on six highly configurable systems, including three on-device machine learning systems, a video encoder, a database management system, and a data analytics pipeline. The experimental results indicate that Unicorn outperforms state-of-the-art performance optimization and debugging methods. Furthermore, unlike the existing methods, the learned causal performance models reliably predict performance for new environments.


## Pre-requisites
* ``` python 3.6 ```
* ``` json ```
* ``` pandas ```
* ``` numpy ```    
* ``` flask ```
* ``` causalgraphicalmodels ```
* ``` causalnex ```
* ``` graphviz ```
* ``` py-causal ```
* ``` causality ```

Please run the following commands to have your system ready to run Unicorn:
```
pip install pandas
pip install numpy
pip install flask
pip install causalgraphicalmodels
pip install causalnex
pip install graphviz
pip install py-causal
pip install causality
pip install tensorflow-gpu==1.15
pip install keras
pip install torch==1.4.0 torchvision==0.5.0
```
## How to use Unicorn
Unicorn can be used for performing different tasks such as performance optimization and performance debugging.

## Debugging
To run causal models for a multi-objective performance fault please run the following:
```python
command: python unicorn.py  -o objective1 -o objective2 -s softwaresystem -k hardwaresystem
### Single-objective
To run causal models for a multi-objective performance fault please run the following:
```python
command: python unicorn.py  -o objective1 -o objective2 -s softwaresystem -k hardwaresystem
### Multi-objective
To run causal models for a multi-objective performance fault please run the following:
```python
command: python unicorn.py  -o objective1 -o objective2 -s softwaresystem -k hardwaresystem
## Optimization
To run causal models for a multi-objective performance fault please run the following:
```python
command: python unicorn.py  -o objective1 -o objective2 -s softwaresystem -k hardwaresystem
### Single-objective
To run causal models for a multi-objective performance fault please run the following:
```python
command: python unicorn.py  -o objective1 -o objective2 -s softwaresystem -k hardwaresystem
### Multi-objective
To run causal models for a multi-objective performance fault please run the following:
```python
command: python unicorn.py  -o objective1 -o objective2 -s softwaresystem -k hardwaresystem
## Efficiency
To run causal models for a multi-objective performance fault please run the following:
```python
command: python unicorn.py  -o objective1 -o objective2 -s softwaresystem -k hardwaresystem
## Transferability
To run causal models for a multi-objective performance fault please run the following:
```python
command: python unicorn.py  -o objective1 -o objective2 -s softwaresystem -k hardwaresystem

## Data generation
To run experiments on NVIDIA Jetson TX1 or TX2 or Xavier devices please use the following command to launch a flask on localhost:
```python
command: python run_service.py softwaresystem
```
For example to initialize a flask app with image recogntion software system please use:
```python
command: python run_service.py Image
```

## Performance faults dataset
Once the flask app is running and modelserver is ready then please use the following command to collect performance measurements for different configurations:
```python
command: python run_params.py softwaresystem
```

To run causal models for a single-objective performance fault please run the following:
```python
command: python unicorn.py  -o objective1  -s softwaresystem -k hardwaresystem
```
For example, to build causal models using FCI and Entropy for image recognition software system in TX1 with initial datafile irtx1.csv use the following for a latency (single objective) fault :
```python
command: python unicorn.py  -o inference_time  -s Image -k TX1
```

To run causal models for a multi-objective performance fault please run the following:
```python
command: python unicorn.py  -o objective1 -o objective2 -s softwaresystem -k hardwaresystem
```
For example, to build causal models using FCI and Entropy for image recognition software system in TX1 with initial datafile irtx1.csv use the following for a latency and energy consumption (multi-ojective) performance fault:
```python
command: python unicorn.py  -o inference_time -o total_energy_consumption -s Image -k TX1
```
## Unicorn usage on a different dataset
If you want to run Unicorn on your own dataset you will only need unicorn.py and src/causal_model.py. To perform interventions using the recommended configuration by unicorn.py you need to develop your own utilities (similar to run_params.py etc.). In addition to that, you need to make some changes in the etc/config.yml file based on your need. The necessary steps are the following:

### Step 1:
Update ```init_dir``` variable in the ```config.yml``` file with the location of the initial data.

### Step 2:
Update bug_dir variable in the config.yml file with the location of the bug data.

### Step 3:
Update output_dir variable in the config.yml file where you want to save the output data.

### Step 4:
Update hardware_columns in the config.yml with the hardware configuration options you want to use.

### Step 5:
Update kernel_columns in the config.yml with the kernel configuration options you want to use.

### Step 6:
Update perf_columns in the config.yml with the events you want to track using perf. If you use any other monitoring tool you need to update it accordingly.

### Step 7:
Update measurment_colums in the config.yml based on the performance objectives you want to use for bug resolve.

### Step 8:
Update is_intervenable variables in the config.yml with the configuration options you want to use and based on your application change their values to True or False. True indicates the configuration options can be intervened upon and vice-versa for False.

### Step 9:
Update the option_values variables in the config.yml based on the allowable values your option can take.

At this stage you can run unicorn.py with your own specification. Please notice that you also need to update the directories according to your software and hardware name in data directory. If you change the name of the variables in the config file or use a new config fille you need to make changes accordingly from line 49 - 58 in unicorn.py.
If you use your own intervention utility you need to update line 6 and line 126 of unicorn.py.



## Contacts
|Name|Email|     
|---------------|------------------|      
|Md Shahriar Iqbal|miqbal@email.sc.edu|     


## 📘&nbsp; License
Unicorn is released under the under terms of the [MIT License](LICENSE).
