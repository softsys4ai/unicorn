[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6360540.svg)](https://doi.org/10.5281/zenodo.6360540)
# Artifact evaluation (EuroSys 2022)
This artifact was awarded the [Available, Functional, and Reproducible Badges](https://sysartifacts.github.io/eurosys2022/badges).

For detailed instructions, please use [functionality](./artifact/FUNCTIONALITY.md) and [reproducibility](./artifact/REPRODUCE.md). 

# Reviews and Rebuttal
**EuroSys'21 (first submission, rejected) -> FSE'21 (second submission, rejected) -> EuroSys'22 (thisr submission, accepted)**

We benefited a lot by learning from previous rejections of this work, and therefore, to help other researchers in the Systems community, we release all reviews and rebuttal for the Unicorn paper and its associated artifact: 
* [EuroSys'22 reviews and rebuttal](https://github.com/softsys4ai/unicorn/wiki/Paper-Reviews-and-Rebuttal) 
* [EuroSys'22 artifact evaluation reviews](https://github.com/softsys4ai/unicorn/wiki/EuroSys-Artifact-Evaluation) 
* [EuroSys'22 communications with artifact reviewers](https://github.com/softsys4ai/unicorn/wiki/EuroSys-Artifact-Evaluation-Comments)
* [FSE'21 reviews and rebuttal](https://github.com/softsys4ai/unicorn/wiki/FSE'21-Reviews-and-Rebuttal)
* [EuroSys'21 reviews and rebuttal](https://github.com/softsys4ai/unicorn/wiki/EuroSys'21-Reviews-and-Rebuttal)

# Unicorn ([paper](https://arxiv.org/pdf/2201.08413.pdf))
```
EuroSys 2022 Title: Reasoning about Configurable System Performance through the lens of Causality
Md Shahriar Iqbal, Rahul Krishna, Mohammad Ali Javidian, Baishakhi Ray, and Pooyan Jamshidi
``` 
Unicorn is a performance analysis, debugging, and optimization tool designed for highly configurable systems with causal reasoning and inference. Users or developers can query Unicorn to resolve a performance issue or optimize performance.

## Overview
![overview](https://user-images.githubusercontent.com/12802456/151218680-5456bcdc-27c0-4736-b54c-7483bc394b8c.png)
## Abstract
Modern computer systems are highly configurable, with the total variability space sometimes larger than the number of atoms in the universe. Understanding and reasoning about the performance behavior of highly configurable systems due to a vast variability space is challenging. State-of-the-art methods for performance modeling and analyses rely on predictive machine learning models; therefore, they become (i) unreliable in unseen environments (e.g., different hardware, workloads) and (ii) produce incorrect explanations. To this end, we propose a new method, called Unicorn, which (i) captures intricate interactions between configuration options across the software-hardware stack and (ii) describes how such interactions impact performance variations via causal inference. We evaluated Unicorn on six highly configurable systems, including three on-device machine learning systems, a video encoder, a database management system, and a data analytics pipeline. The experimental results indicate that Unicorn outperforms state-of-the-art performance optimization and debugging methods. Furthermore, unlike the existing methods, the learned causal performance models reliably predict performance for new environments.

# How to use Unicorn
Unicorn is used for performing tasks such as performance optimization and performance debugging in offline and online modes. 

- **Offline mode:** Unicorn can be run on any device that uses previously measured configurations in offline mode. 
- **Online mode:** In the online mode, the measurements are performed from ```NVIDIA Jetson Xavier```, ```NVIDIA Jetson TX2```, and ```NVIDIA Jetson TX1``` devices directly while the experiments are running. To collect measurements from these devices ```sudo``` privilege is required to set a device to a new configuration before measurement. 

Unicorn can be used for debugging and optimization for objectives such as latency (```inference_time```) and energy (```total_energy_consumption```) in both offline and online modes. Unicorn has been implemented on six software systems such as DEEPSTREAM (```Deepstream```), XCEPTION (```Image```), BERT (```NLP```), DEEPSPEECH (```Speech```), X264 (```x264```), and SQLITE (```sqlite```). 

## Setup

To get started, you'll need to have `docker` and `docker-compose`.
On desktop systems like Docker Desktop for Mac and Windows, Docker Compose is included as part of those desktop installs.
You can get them here: <https://docs.docker.com/desktop/mac/install/>.

**NOTE: We'll be using `docker-compose`, and all `docker-compose` commands must be run from withtin the repository's root folder.**

1. First clone this repository, and `cd` into the repository:

    ```sh
    git clone git@github.com:softsys4ai/unicorn.git
    cd unicorn
    ```

2. Next, build the artifact with `docker-compose`. From the repository root, run:
   
   ```sh
   docker-compose up --build --detach
   ```

   You'll see the following output:

   ```
   ❯ docker-compose up --build --detach
    Building unicorn
    [+] Building 1.6s (16/16) FINISHED
    => [internal] load build definition from Dockerfile                                                          0.0s
    => => transferring dockerfile: 609B                                                                          0.0s
    => [internal] load .dockerignore                                                                             0.0s
    => => transferring context: 2B                                                                               0.0s
    => [internal] load metadata for docker.io/library/python:3.6.2                                               0.0s
    => [ 1/12] FROM docker.io/library/python:3.6.2                                                               0.0s
    => CACHED [ 2/12] RUN pip install --upgrade pip                                                              0.0s
    => CACHED [ 3/12] RUN pip install -U numpy                                                                   0.0s
    => CACHED [ 4/12] RUN pip install -U pandas                                                                  0.0s
    => CACHED [ 5/12] RUN pip install -U javabridge                                                              0.0s
    => CACHED [ 6/12] RUN pip install -U pydot                                                                   0.0s
    => CACHED [ 7/12] RUN pip install -U graphviz                                                                0.0s
    => CACHED [ 8/12] RUN pip install git+git://github.com/bd2kccd/py-causal                                     0.0s
    => CACHED [ 9/12] RUN pip install git+git://github.com/fmfn/BayesianOptimization                             0.0s
    => CACHED [10/12] RUN pip install scipy matplotlib     seaborn networkx causalgraphicalmodels     causalnex  0.0s
    => [11/12] RUN pip install pyyaml                                                                            1.4s
    => [12/12] WORKDIR /root                                                                                     0.0s
    => exporting to image                                                                                        0.1s
    => => exporting layers                                                                                       0.0s
    => => writing image sha256:6c803cd540fc03ac0535a24571769063651c6c0ddd0e1f24fb1241fb9277dc56                  0.0s
    => => naming to docker.io/library/unicorn_unicorn                                                            0.0s

    Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
    Creating unicorn ... done
   ```



## Debugging
Unicorn supports debugging and fixing single-objective and multi-objective performance faults in offline and online modes. It also supports root cause analysis of these fixes using metrics such as accuracy, precision, recall, and gain. 

### Single-objective debugging
To debug single-objective faults in using Unicorn, please use the following command:
```
docker-compose exec unicorn python ./tests/run_unicorn_debug.py  -o objective -s softwaresystem -k hardwaresystem -m mode
```

#### Example
To debug single-objective ```latency``` faults for ```Xception``` in ```JETSON TX2``` in the ```offline``` mode using Unicorn, please use the following command:
```
docker-compose exec unicorn python ./tests/run_unicorn_debug.py  -o inference_time -s Image -k TX2 -m offline
```
To debug single-objective ```energy``` faults for ```Bert``` in ```JETSON Xavier``` in the ```online``` mode using Unicorn please use the following command:
```
docker-compose exec unicorn python ./tests/run_unicorn_debug.py  -o total_energy_consumption -s NLP -k Xavier -m online
```

### Multi-objective debugging
To debug multi-objective faults using Unicorn, please use the following command:
```
docker-compose exec unicorn python ./tests/run_unicorn_debug.py  -o objective1 -o objective2 -s softwaresystem -k hardwaresystem -m mode
```
#### Example
To debug multi-objective ```latency``` and ```energy``` faults for ```Deepspeech``` in ```JETSON TX2``` in the ```offline``` mode using Unicorn, please use the following command:
```
docker-compose exec unicorn python ./tests/run_unicorn_debug.py  -o inference_time -o total_energy_consumption -s Speech  -k TX2 -m offline
```

## Optimization
Unicorn supports single-objective and multi-objective optimization in offline and online modes.

### Single-objective optimization
To run single-objective optimization using Unicorn, please use the following command:
```
docker-compose exec unicorn python ./tests/run_unicorn_optimization.py  -o objective -s softwaresystem -k hardwaresystem -m mode
```
#### Example
To run single-objective ```latency``` optimization for ```Xception``` in ```JETSON TX2``` in the ```offline``` mode using Unicorn, please use the following command:
```
docker-compose exec unicorn python ./tests/run_unicorn_optimization.py  -o inference_time -s Image -k TX2 -m offline
```
To run single-objective ```energy``` optimization for ```Bert``` in ```JETSON Xavier``` in the ```online``` mode using Unicorn, please use the following command:
```
docker-compose exec unicorn python ./tests/run_unicorn_optimization.py  -o total_energy_consumption -s NLP -k Xavier -m online
```

### Multi-objective debugging
To run multi-objective optimization in the using Unicorn, please use the following command:
```
docker-compose exec unicorn python ./tests/run_unicorn_optimization.py  -o objective1 -o objective2 -s softwaresystem -k hardwaresystem -m mode
```
#### Example
To run multi-objective ```latency``` and ```energy``` optimization for ```Deepspeech``` in ```JETSON TX2``` in the ```offline``` mode using Unicorn, please use the following command:
```
docker-compose exec unicorn python ./tests/run_unicorn_optimization.py  -o inference_time -o total_energy_consumption -s Deepspeech  -k TX2 -m offline
```

## Transferability
Unicorn supports both single and multi-objective transferability in online and offline modes. However, the current version is not tested for multi-objective transferability. To determine the single-objective transferability of Unicorn, please use the following command:
```
docker-compose exec unicorn python ./tests/run_unicorn_transferability.py  -o objective -s softwaresystem -k hardwaresystem -m offline
```
#### Example
To run single-objective ```latency``` transferability for ```Xception``` in ```JETSON TX2``` in the ```offline``` mode using Unicorn, please use the following command:
```
docker-compose exec unicorn python ./tests/run_unicorn_transferability.py  -o inference_time -s Image -k TX2 -m offline
```
To run single-objective ```energy``` transferability for ```Bert``` in ```JETSON Xavier``` in the ```offline``` mode using Unicorn, please use the following command:
```
docker-compose exec unicorn python ./tests/run_unicorn_transferability.py  -o total_energy_consumption -s NLP -k Xavier -m offline
```
## Data generation
To run experiments on ```NVIDIA Jetson Xavier```, ```NVIDIA Jetson TX2```, and ```NVIDIA Jetson TX1``` devices for a particular software a flask app is required to be launched. Please use the first command to start the app in the ```localhost```. Once the app is up and running, please use the second command to start measuring configurations.


```
docker-compose exec unicorn python ./services/run_service.py softwaresystem
docker-compose exec unicorn python ./services/run_params.py softwaresystem
```
#### Example
To initialize a flask app with ```Xception``` software system, please use:
```
docker-compose exec unicorn python ./services/run_service.py Image
```

Once the flask app is running and the modelserver is ready, then please use the following command to collect performance measurements for different configurations:
```
docker-compose exec unicorn python ./services/run_params.py Image
```
## Baselines 

Instructions to run the debugging and optimizations baselines used in Unicorn is described in [baselines](./artifact/BASELINES.md).

## Unicorn usage with different datasets

Instructions to use Unicorn with a different dataset are described in [others](./artifact/OTHERS.md).

## Docker teardown

After experimentation, consider stoping and removing any docker related caches.

```sh
echo "Stops any running docker compose services, and removes related caches"
docker-compose rm -fsv
```

## How to cite
If you use Unicorn in your research or the dataset in this repository please cite the following:
```
@inproceedings{iqbal2022unicorn,
  title={Unicorn: Reasoning about Configurable System Performance through the lens of Causality},
  author={Iqbal, Md Shahriar and Krishna, Rahul and Javidian, Mohammad Ali and Ray, Baishakhi and Jamshidi, Pooyan},
  booktitle={EuroSys '22: Proceedings of the Seventeen European Conference on Computer Systems},
  year={2022}
}
```

## Contacts
Please please feel free to contact via email if you find any issues or have any feedbacks. Thank you for using Unicorn.
|Name|Email|     
|---------------|------------------|      
|Md Shahriar Iqbal|miqbal@email.sc.edu|     
|Rahul Krishna|i.m.ralk@gmail.com|     
|Pooyan Jamshidi|pjamshid@cse.sc.edu|     

## 📘&nbsp; License
Unicorn is released under the terms of the [MIT License](./LICENSE).
