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
git clone https://github.com/softsys4ai/unicorn.git
cd unicorn
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
Unicorn can be used for performing different tasks such as performance optimization and performance debugging. Unicorn supports both offline and online modes. In the offline mode, Unicorn can be run on any device that uses previously measured configurations. In the online mode, the measurements are performed from ```NVIDIA Jetson Xavier```, ```NVIDIA Jetson TX2```, and ```NVIDIA Jetson TX1``` devices directly. To collect measurements from these devices ```sudo``` privilege is required as it requires setting a device to a new configuration before measurement.

## Debugging (offline)
Unicorn supports debugging and fixing single-objective and multi-objective performance faults. It also supports root cause analysis of these fixes such as determining accuracy, computing gain etc.

### Single-objective debugging
To debug single-objective faults in the offline mode using Unicorn please use the following command:
```
python run_unicorn_debug.py  -o objective -s softwaresystem -k hardwaresystem -m mode
```

#### Example
To debug single-objective ```latency``` faults for ```Xception``` in ```JETSON TX2``` in the ```offline``` mode using Unicorn please use the following command:
```
python run_unicorn_debug.py  -o inference_time -s Image -k TX2 -m offline
```
To debug single-objective ```energy``` faults for ```Bert``` in ```JETSON Xavier``` in the ```offline``` mode using Unicorn please use the following command:
```
python run_unicorn_debug.py  -o total_energy_consumption -s NLP -k Xavier -m offline
```

### Multi-objective debugging
To debug multi-objective faults in the offline mode using Unicorn please use the following command:
```
python run_unicorn_debug.py  -o objective1 -o objective2 -s softwaresystem -k hardwaresystem -m mode
```
#### Example
To debug multi-objective ```latency``` and ```energy``` faults for ```Deepspeech``` in ```JETSON TX2``` in the ```offline``` mode using Unicorn please use the following command:
```
python run_unicorn_debug.py  -o inference_time -o total_energy_consumption -s Speech  -k TX2 -m offline
```

## Optimization (offline)
Unicorn supports single-objective and multi-objective optimization..

### Single-objective optimization
To run single-objective optimization in the offline mode using Unicorn please use the following command:
```
python run_unicorn_optimization.py  -o objective -s softwaresystem -k hardwaresystem -m mode
```
#### Example
To To run single-objective ```latency``` optimization for ```Xception``` in ```JETSON TX2``` in the ```offline``` mode using Unicorn please use the following command:
```
python run_unicorn_optimization.py  -o inference_time -s Image -k TX2 -m offline
```
To run single-objective ```energy``` optimization for ```Bert``` in ```JETSON Xavier``` in the ```offline``` mode using Unicorn please use the following command:
```
python run_unicorn_optimization.py  -o total_energy_consumption -s NLP -k Xavier -m offline
```

### Multi-objective debugging
To run multi-objective optimization in the offline mode using Unicorn please use the following command:
```
python run_unicorn_optimization.py  -o objective1 -o objective2 -s softwaresystem -k hardwaresystem -m mode
```
#### Example
To run multi-objective ```latency``` and ```energy``` optimization for ```Deepspeech``` in ```JETSON TX2``` in the ```offline``` mode using Unicorn please use the following command:
```
python run_unicorn_optimization.py  -o inference_time -o total_energy_consumption -s Deepspeech  -k TX2 -m offline
```

## Transferability
Unicorn supports both single and multi-objective transferability. However, multi-objective transferability is not comprehensively investigated in this version. To determine single-objective transferability of Unicorn use the following command:
```
python run_unicorn_transferability.py  -o objective -s softwaresystem -k hardwaresystem
```
#### Example
To run single-objective ```latency``` transferability for ```Xception``` in ```JETSON TX2``` in the ```offline``` mode using Unicorn please use the following command:
```
python run_unicorn_transferability.py  -o inference_time -s Image -k TX2 -m offline
```
To run single-objective ```energy``` transferability for ```Bert``` in ```JETSON Xavier``` in the ```offline``` mode using Unicorn please use the following command:
```
python run_unicorn_transferability.py  -o total_energy_consumption -s NLP -k Xavier -m offline
```
## Debugging baselines
Unicorn supports four debugging baselines such as CBI, Delta Debugging, Encore and BugDoc. To run the baselines use the following commands:
```
python run_baseline_debug.py  -o objective -s softwaresystem -k hardwaresystem -m mode -b baseline
```
#### Example
To run single-objective ```latency``` debugging for ```Xception``` in ```JETSON TX2``` in the ```offline``` mode using CBI please use the following command:
```
python run_baseline_debug  -o inference_time -s Image -k TX2 -m offline -b c
```
To run single-objective ```latency``` debugging for ```Deespspeech``` in ```JETSON TX2``` in the ```offline``` mode using delta debugging please use the following command:
```
python run_baseline_debug  -o inference_time -s Speech -k TX2 -m offline -b dd
```
To run single-objective ```energy``` debugging for ```Deesptream``` in ```JETSON Xavier``` in the ```offline``` mode using encore please use the following command:
```
python run_baseline_debug  -o total_energy_consumption -s Deepstream -k Xavier -m offline -b encore
```
To run single-objective ```energy``` debugging for ```x264``` in ```JETSON Xavier``` in the ```offline``` mode using bugdoc please use the following command:
```
python run_baseline_debug  -o total_energy_consumption -s x264 -k Xavier -m offline -b bugdoc
```
## Optimization baselines
Unicorn supports two optimization baselines: SMAC and PESMO. SMAC is used for single-objective optimization while PESMO is used for multi-objective optimization. To run the baselines use the following commands:
```
python run_baseline_optimization.py  -o objective -s softwaresystem -k hardwaresystem -m mode -b baseline
```
#### Example
To run single-objective ```latency``` optimization for ```Xception``` in ```JETSON TX2``` in the ```offline``` mode using SMAC please use the following command:
```
python run_baseline_optimization  -o inference_time -s Image -k TX2 -m offline -b smac
```
To run multi-objective optimizaiton for ```Xception``` in ```JETSON TX2``` in the ```offline``` mode using PESMO please use the following command:
```
python run_baseline_optimization  -o inference_time -o total_energy_consumption -s Image -k TX2 -m offline -b pesmo
```

## Data generation
To run experiments on ```NVIDIA Jetson Xavier```, ```NVIDIA Jetson TX2```, and ```NVIDIA Jetson TX1``` devices for a particular software a flask app is required to be launched. Please use the following command to start the app in the ```localhost```.


```
python run_service.py softwaresystem
```

For example to initialize a flask app with ```Xception``` software system please use:
```
python run_service.py Image
```

Once the flask app is running and modelserver is ready then please use the following command to collect performance measurements for different configurations:
```
python run_params.py softwaresystem
```

## Unicorn usage on a different dataset
To run Unicorn on your a different dataset you will only need ```unicorn_debugging.py``` and ```unicorn_optimization.py```. In the online mode, to perform interventions using the recommended configuration you need to develop your own utilities (similar to ```run_params.py```). Additionally, you need to make some changes in the ```etc/config.yml``` to use the configuration options and their values accordingly. The necessary steps are the following:

**Step 1**: Update ```init_dir```in ```config.yml``` with the directory where initial data is stored.

**Step 2**: Update ```bug_dir``` in ```config.yml``` with the directory where bug data is stored.

**Step 3**: Update ```output_dir``` variable in the ```config.yml``` file where you want to save the output data.

**Step 4**: Update ```hardware_columns``` in the ```config.yml``` with the hardware configuration options you want to use.

**Step 5**: Update ```kernel_columns``` in the ```config.yml``` with the kernel configuration options you want to use.

**Step 6**: Update ```perf_columns``` in the ```config.yml``` with the events you want to track using perf. If you use any other monitoring tool you need to update it accordingly.

**Step 7**: Update ```measurement_colums``` in the ```config.yml``` based on the performance objectives you want to use for bug resolve.

**Step 8**: Update ```is_intervenable``` variables in the ```config.yml``` with the configuration options you want to use and based on your application change their values to True or False. True indicates the configuration options can be intervened upon and vice-versa for False.

**Step 9**: Update the ```option_values``` variables in the ```config.yml``` based on the allowable values your option can take.

At this stage you can run ```unicorn_debugging.py``` and ```unicorn_optimization.py``` with your own specification. Please notice that you also need to update the directories according to your software and hardware name in data directory. If you change the name of the variables in the config file or use a new config fille you need to make changes accordingly from in ```unicorn_debugging.py``` and ```unicorn_optimization.py```.

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
Unicorn is released under the under terms of the [MIT License](LICENSE).
