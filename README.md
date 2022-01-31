# Unicorn ([paper](https://arxiv.org/pdf/2201.08413.pdf))
```
EuroSys 2022 Title: Reasoning about Configurable System Performance through the lens of Causality
Md Shahriar Iqbal, Rahul Krishna, Mohammad Ali Javidian, Baishakhi Ray, and Pooyan Jamshidi
``` 
Unicorn is a performance analysis, debugging and optimization tool designed for highly configurable systems with causal reasoning and inference. Users or developers can query Unicorn to resolve a performance issue or for performance improvement.

## Overview
![overview](https://user-images.githubusercontent.com/12802456/151218680-5456bcdc-27c0-4736-b54c-7483bc394b8c.png)
## Abstract
Modern computer systems are highly configurable, with the total variability space sometimes larger than the number of atoms in the universe. Understanding and reasoning about the performance behavior of highly configurable systems, due to a vast variability space, is challenging. State-of-the-art methods for performance modeling and analyses rely on predictive machine learning models, therefore, they become (i) unreliable in unseen environments (e.g., different hardware, workloads), and (ii) produce incorrect explanations. To this end, we propose a new method, called Unicorn, which (i) captures intricate interactions between configuration options across the software-hardware stack and (ii) describes how such interactions impact performance variations via causal inference. We evaluated Unicorn on six highly configurable systems, including three on-device machine learning systems, a video encoder, a database management system, and a data analytics pipeline. The experimental results indicate that Unicorn outperforms state-of-the-art performance optimization and debugging methods. Furthermore, unlike the existing methods, the learned causal performance models reliably predict performance for new environments.


## Pre-requisites

Please run the following commands to have your system ready to run Unicorn:
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.6
pip install json
pip install numpy
pip install scipy
pip install pandas
pip install matplotlib
pip install networkx
pip install pydot
pip install flask
pip install causalgraphicalmodels
pip install causalnex
pip install graphviz
pip install py-causal
pip install causality
pip install mlxtend
pip install -U scikit-learn
pip install basyesian-optimization
pip install statsmodels
pip install tqdm
pip install tensorflow-gpu==1.15
pip install keras
pip install torch==1.4.0 torchvision==0.5.0
```
## How to use Unicorn
Unicorn can be used for performing different tasks such as performance optimization and performance debugging. Unicorn can be run on both offline and online modes. In the offline mode, Unicorn can be run on any device that uses previously measured configurations. In the online mode, the measurements are performed from ```NVIDIA Jetson Xavier```, ```NVIDIA Jetson TX2```, and ```NVIDIA Jetson TX1``` devices directly while the experiments are running. To collect measurements from these devices ```sudo``` privilege is required as it requires setting a device to a new configuration before measurement. 


In both offline and online modes, Unicorn can be used for debugging and optimization for objectives such as latency (```inference_time```) and energy (```total_energy_consumption```). Unicorn has been implemented on six software systems such as DEEPSTREAM (```Deepstream```), XCEPTION (```Image```), BERT (```NLP```), DEEPSPEECH (```Speech```), X264 (```x264```), and SQLITE (```sqlite```). 

## Artifact evaluation (EuroSys 2022)
Please use [functionality](./artifact/FUNCTIONALITY.md) and [reproducibility](./artifact/REPRODUCE.md) for artifact evaluation. All tests should be run from the ```unicorn``` directory using ```python 3.6.9```. 

## Debugging
Unicorn supports debugging and fixing single-objective and multi-objective performance faults in offline and online modes. It also supports root cause analysis of these fixes using metrics such as accuracy, precision, recall and gain. 

### Single-objective debugging
To debug single-objective faults in the using Unicorn please use the following command:
```
python ./tests/run_unicorn_debug.py  -o objective -s softwaresystem -k hardwaresystem -m mode
```

#### Example
To debug single-objective ```latency``` faults for ```Xception``` in ```JETSON TX2``` in the ```offline``` mode using Unicorn please use the following command:
```
python ./tests/run_unicorn_debug.py  -o inference_time -s Image -k TX2 -m offline
```
To debug single-objective ```energy``` faults for ```Bert``` in ```JETSON Xavier``` in the ```online``` mode using Unicorn please use the following command:
```
python ./tests/run_unicorn_debug.py  -o total_energy_consumption -s NLP -k Xavier -m online
```

### Multi-objective debugging
To debug multi-objective faults using Unicorn please use the following command:
```
python ./tests/run_unicorn_debug.py  -o objective1 -o objective2 -s softwaresystem -k hardwaresystem -m mode
```
#### Example
To debug multi-objective ```latency``` and ```energy``` faults for ```Deepspeech``` in ```JETSON TX2``` in the ```offline``` mode using Unicorn please use the following command:
```
python ./tests/run_unicorn_debug.py  -o inference_time -o total_energy_consumption -s Speech  -k TX2 -m offline
```

## Optimization
Unicorn supports single-objective and multi-objective optimization in offline and online modes.

### Single-objective optimization
To run single-objective optimization using Unicorn please use the following command:
```
python ./tests/run_unicorn_optimization.py  -o objective -s softwaresystem -k hardwaresystem -m mode
```
#### Example
To run single-objective ```latency``` optimization for ```Xception``` in ```JETSON TX2``` in the ```offline``` mode using Unicorn please use the following command:
```
python ./tests/run_unicorn_optimization.py  -o inference_time -s Image -k TX2 -m offline
```
To run single-objective ```energy``` optimization for ```Bert``` in ```JETSON Xavier``` in the ```online``` mode using Unicorn please use the following command:
```
python ./tests/run_unicorn_optimization.py  -o total_energy_consumption -s NLP -k Xavier -m online
```

### Multi-objective debugging
To run multi-objective optimization in the using Unicorn please use the following command:
```
python ./tests/run_unicorn_optimization.py  -o objective1 -o objective2 -s softwaresystem -k hardwaresystem -m mode
```
#### Example
To run multi-objective ```latency``` and ```energy``` optimization for ```Deepspeech``` in ```JETSON TX2``` in the ```offline``` mode using Unicorn please use the following command:
```
python ./tests/run_unicorn_optimization.py  -o inference_time -o total_energy_consumption -s Deepspeech  -k TX2 -m offline
```

## Transferability
Unicorn supports both single and multi-objective transferability in online and offline modes. However, the current version is not tested for multi-objective transferability. To determine single-objective transferability of Unicorn please use the following command:
```
python ./tests/run_unicorn_transferability.py  -o objective -s softwaresystem -k hardwaresystem -m offline
```
#### Example
To run single-objective ```latency``` transferability for ```Xception``` in ```JETSON TX2``` in the ```offline``` mode using Unicorn please use the following command:
```
python ./tests/run_unicorn_transferability.py  -o inference_time -s Image -k TX2 -m offline
```
To run single-objective ```energy``` transferability for ```Bert``` in ```JETSON Xavier``` in the ```offline``` mode using Unicorn please use the following command:
```
python ./tests/run_unicorn_transferability.py  -o total_energy_consumption -s NLP -k Xavier -m offline
```
## Data generation
To run experiments on ```NVIDIA Jetson Xavier```, ```NVIDIA Jetson TX2```, and ```NVIDIA Jetson TX1``` devices for a particular software a flask app is required to be launched. Please use the first command to start the app in the ```localhost```. Once the app is up and running please use the second command to start measuring consfigurations.


```
python ./services/run_service.py softwaresystem
python ./services/run_params.py softwaresystem
```
#### Example
To initialize a flask app with ```Xception``` software system please use:
```
python ./services/run_service.py Image
```

Once the flask app is running and modelserver is ready then please use the following command to collect performance measurements for different configurations:
```
python ./services/run_params.py Image
```
## Baselines 

Instructions to run the debugging and optimizations baselines used in Unicorn is described in [baselines](./artifact/BASELINES.md).

## Unicorn usage with different datasets

Instructions to use Unicorn with a different dataset are described in [others](./artifact/OTHERS.md).

## How to cite
If you use Unicorn in your research or the dataset in this repository please cite the following:
```
@article{iqbal2022unicorn,
  title={Unicorn: Reasoning about Configurable System Performance through the lens of Causality},
  author={Iqbal, Md Shahriar and Krishna, Rahul and Javidian, Mohammad Ali and Ray, Baishakhi and Jamshidi, Pooyan},
  journal={arXiv preprint arXiv:2201.08413},
  year={2022}
}
```

## Contacts
Please please feel free to contact via email if you find any issues or have any feedbacks. Thank you for using Unicorn.
|Name|Email|     
|---------------|------------------|      
|Md Shahriar Iqbal|miqbal@email.sc.edu|     


## 📘&nbsp; License
Unicorn is released under the terms of the [MIT License](LICENSE).
