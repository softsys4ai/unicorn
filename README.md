# unicorn
![image](https://user-images.githubusercontent.com/1433964/95892741-f6905480-0d54-11eb-82cb-140254d844c5.png)

Modern computer systems are highly configurable. They often are composed of heterogeneous components-each component consists of numerous configurations, giving a total variability space sometimes larger than the number of atoms in the universe. The performance of a system configured with different configuration options can widely vary. Thus, given the vast configuration space, understanding and reasoning about the performance behavior of such systems become challenging. These configuration options interact with each other within and across the system stack, and such interactions typically vary in different deployment environments or workload conditions. So, it becomes almost impossible to track down configuration options that should be set to different values to improve performance if the system’s performance shows wide variability during operation time. As a result, existing performance models that rely on predictive machine learning models suffer from (i) high cost: given a deployment environment, regression-based performance models require a large number of configuration samples for accurate predictions, and more importantly, (ii) unreliable predictions: even if they predict performance for the environment where configurations are measured, since they may infer correlations as causation, they typically do not transfer well for predicting system performance behavior in a new environment (e.g., change of hardware from the canary environment to production). The main problem we address here is to understand why the performance degradation is happening and reason based on a reliable model to improve it. To this end, this paper proposes a new methodology, called Unicorn, which initially learns a Causal Performance Model to reliably capture intricate interactions between options across software-hardware stack by tracing system-level performance events across the stack (hardware, software, cache, and tracepoint). Then, it uses them to explain how such interactions impact the variation in performance objectives causally. Given a limited sampling budget, Unicorn iteratively updates the learned performance model by estimating the causal effects of configuration options to performance objectives, then selecting the highest-impact options to adjust in order to address performance issues by improving the performance objective of interest without deteriorating other objectives in debugging task or recommend a near-optimal configuration. We evaluated Unicorn on six highly configurable systems, including three on-device machine learning systems, a video encoder, a database, and a data analytics pipeline. In addition, we compared the results with state-of-the-art configuration optimization and debugging methods. The experimental results indicate that Unicorn can find effective repairs for performance faults and find configurations with near-optimal performance. Furthermore, unlike the existing methods, the learned causal performance models in Unicorn reliably predict performance for new environments where it has not been used during the learning process
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
## Run instructions using Jetson faults dataset
To run experiments on NVIDIA Jetson TX1 or TX2 or Jetson Xavier devices please use the
following command to launch a flask on localhost:
```python
command: python run_service.py softwaresystem
```
For example to initialize a flask app with image recogntion softwrae system please use:
```python
command: python run_service.py Image
```

Once the flask app is running and modelserver is ready then please use the following command
to collect performance measurments for different configurations:
```python
command: python run_params.py softwaresystem
```

To run causal models for a single-objective bug please run the following:
```python
command: python unicorn.py  -o objective1  -s softwaresystem -k hardwaresystem
```
For example, to build causal models using NOTEARS and fci for image recognition software
system in TX1 with initial datafile irtx1.csv use the following for a latency (single objective) bug :
```python
command: python unicorn.py  -o inference_time  -s Image -k TX1
```

To run causal models for a multi-objective bug please run the following:
```python
command: python unicorn.py  -o objective1 -o objective2 -s softwaresystem -k hardwaresystem
```
For example, to build causal models using NOTEARS and fci for image recognition software
system in TX1 with initial datafile irtx1.csv use the following for a latency and energy consumption (multi-ojective) bug :
```python
command: python unicorn.py  -o inference_time -o total_energy_consumption -s Image -k TX1
```
## Run instructions using a different dataset
If you want to run CADET on your own dataset you will only need unicorn.py and src/causal_model.py.
To perform interventions using the recommended configuration by unicorn.py you need to develop
your own utilities (similar to run_params.py etc.). In addition to that, you need to
make some changes in the etc/config.yml file based on your need. The necessary steps are
the following:

### Step 1:
Update init_dir variable in the config.yml file with the location of the initial data.

### Step 2:
Update bug_dir variable in the config.yml file with the location of the bug data.

### Step 3:
Update output_dir variable in the config.yml file where you want to save the output data.

### Step 4:
Update hardware_columns in the config.yml with the hardware configuration options you want to use.

### Step 5:
Update kernel_columns in the config.yml with the kernel configuration options you want to use.

### Step 6:
Update perf_columns in the config.yml with the events you want to track using perf use. If you use any other monitoring tool you need to update it accordingly.

### Step 7:
Update measurment_colums in the config.yml based on the performance objectives you want to use for bug resolve.

### Step 8:
Update is_intervenable variables in the config.yml with the configuration options you want to use and based on your application change their values to True or False. True indicates the configuration options can be intervened upon and vice-versa for False.

### Step 9:
Update the option_values variables in the config.yml based on the allowable values your option can take.

At this stage you can run unicorn.py with your own specification. Please notice that you also need to update the directories according to your software and hardware name in data directory.
If you change the name of the variables in the config file or use a new config fille you need to make changes accordingly from line 49 - 58 in unicorn.py.
If you use your own intervention uitility you need to update line 6 and line 126 of unicorn.py.



## Contacts
|Name|Email|     
|---------------|------------------|      
|Shahriar Iqbal|miqbal@email.sc.edu|      
|Rahul Krishna|i.m.ralk@gmail.com|


## 📘&nbsp; License
CADET is released under the under terms of the [MIT License](LICENSE).
