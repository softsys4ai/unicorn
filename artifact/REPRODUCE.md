# Unicorn reproducibility
In this section, we discuss the steps required to reproduce our key findings reported in the paper. Please check the hardware section in [functionality](./FUNCTIONALITY.md). We will use Unicorn offline to for reproducibility.

## How to use Unicorn
Unicorn is used for performing tasks such as performance optimization and performance debugging in offline and online modes. 

- **Offline mode:** In the offline mode, Unicorn can be run on any device that uses previously measured configurations. 
- **Offline mode:** In the online mode, the measurements are performed from ```NVIDIA Jetson Xavier```, ```NVIDIA Jetson TX2```, and ```NVIDIA Jetson TX1``` devices directly while the experiments are running. To collect measurements from these devices ```sudo``` privilege is required as it requires setting a device to a new configuration before measurement. 

In both offline and online modes, Unicorn can be used for debugging and optimization for objectives such as latency (```inference_time```) and energy (```total_energy_consumption```). Unicorn has been implemented on six software systems such as DEEPSTREAM (```Deepstream```), XCEPTION (```Image```), BERT (```NLP```), DEEPSPEECH (```Speech```), X264 (```x264```), and SQLITE (```sqlite```). 

__Note: In this artifact, we will be using offline mode. Contact [Md Shahriar Iqbal](mailto:miqbal@email.sc.edu?subject=Testing%20UNICORN%20in%20online%20mode) for instructions if you are running UNICORN in online mode.__

## Setup

To get started, you'll need to have `docker` and `docker-compose`.
On desktop systems like Docker Desktop for Mac and Windows, Docker Compose is included as part of those desktop installs.
You can get them here: <https://docs.docker.com/desktop/mac/install/>.

**NOTE: We'll be using `docker-compose` and all `docker-compose` commands must be run from withtin the root folder of the repository.**

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
   $ docker-compose up --build --detach
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

##  Key claims

We reproduce results for the following three key claims reported in our paper:

- Unicorn can be used to detect root causes of non-functional performance (```latency``` and ```energy```) faults with higher accuracy and gain. To support this claim we will reproduce partial results from Table 2. In Table 2 we reported our findings for 243/494 faults discovered in this study. For reproducibility, we will reproduce results for 29/243 energy faults reported in Table 2 for ```Xception``` on ```NVIDIA Jetson Xavier```.

- Unicorn can be used as a central tool and can support performing tasks such as performance optimization. To support this claim we will reproduce single-objective latency and energy optimization results reported in Figure 16 (a).

- Unicorn can be effeciciently re-used when the deployment environment changes. To support this claim we will reproduce our findings reported in Figure 18.

For each of the above claims, we will compare our results with the baselines reported in the paper. Instructions to run the baselines can be found in [baselines](./BASELINES.md).

## Steps to reproduce Table 2 energy results for ```Xception``` (Experiment time ~90mins)
Here, the reported energy faults, initial data and ground truths are stored in the corresponding directories. The complete experiment on all 29 of the energy faults can be run with the following commands:

```
docker-compose exec unicorn python ./tests/run_unicorn_debug.py -o total_energy_consumption -s Image -k Xavier -m offline
docker-compose exec unicorn python ./tests/run_unicorn_debug.py -o total_energy_consumption -s Image -k Xavier -m offline -b cbi
docker-compose exec unicorn python ./tests/run_unicorn_debug.py -o total_energy_consumption -s Image -k Xavier -m offline -b encore
docker-compose exec unicorn python ./tests/run_unicorn_debug.py -o total_energy_consumption -s Image -k Xavier -m offline -b bugdoc
docker-compose exec unicorn python ./tests/run_debug_metrics.py -o total_energy_consumption -s Image -k Xavier -e debug
```
Debugging output will be saved to the ```./data/measurement/output/debug_exp.csv``` and the final script will generate plots for gain and number of samples required to achieve that gain that will be saved as ```./data/measurement/output/debug_gain.pdf``` and  ```./data/measurement/output/debug_num_samples.pdf```, respectively.

## Steps to reproduce Figure 16 (a) results (Experiment time ~90mins)
Please use the following commands to reproduce this step:
```
docker-compose exec unicorn python ./tests/run_unicorn_optimization.py -o inference_time -s Image -k TX2 -m offline
docker-compose exec unicorn python ./tests/run_baseline_optimization.py -o inference_time -s Image -k TX2 -m offline -b smac
```
Once the experiments are over, the output for Unicorn and SMAC will be directly saved to ```./data/measurement/output/unicorn_opt.pdf``` and ```./data/measurement/output/smac_opt.pdf```, respectively.

## Steps to reproduce Figure 18 results (Experiment time ~8mins)
Please use the following commands to reproduce this step:
```
docker-compose exec unicorn python ./tests/run_unicorn_transferability.py -o inference_time -s Image -k Xavier -m offline
docker-compose exec unicorn python ./tests/run_debug_metrics.py -o inference_time -s Image -k TX2 -e transfer
```
Transfer output will be saved to the ```./data/measurement/output/transfer_exp.csv``` and the final script will generate plots for gain and number of samples required to achieve that gain that will be saved as ```./data/measurement/output/transfer_gain.pdf``` and  ```./data/measurement/output/transfer_num_samples.pdf```, respectively.



## Video run of the example in the online mode
An example run of Unicorn for an ```energy``` fault in the online mode is shown here. 


https://user-images.githubusercontent.com/12802456/154901154-59c63033-722d-427b-bab1-42da7ab0c0a1.mp4


## Steps to reproduce Table 2 energy results for ```Xception``` (Experiment time ~11.6 hours (0.4 hours/Bug)) in online mode

Fro two terminals please use the following commands to access the ```Nvidia Jetson Xavier``` device:
```
ssh nvidia@10.173.131.123
```
Use the following credentials for the device:
```
user: nvidia
password: nvidia
```

Once logged in into the device please use the following commands to run the experiments from one terminal:
```
cd unicorn
python3 ./services/run_services.py Image
``` 
Please wait until the status shows the flask app is running on http://127.0.0.1/5000

Now run the following two commands to run the debugging experiment and plot the results from the other terminal:
```
sudo su
python3 ./tests/run_unicorn_debug.py -o total_energy_consumption -s Image -k Xavier -m online
python3 ./tests/run_debug_metrics.py -o total_energy_consumption -s Image -k Xavier -e debug
```
To avoid running 11.6 Hours (approx.) experiments, each bug can be run by passing the bug_id. There are 29 energy bugs of Image on Xavier. So, bug_id 0 - 28 can be passed. For example, to debug bug_id = 0, please use the following command:
```
python3 ./tests/run_unicorn_debug.py -o total_energy_consumption -s Image -k Xavier -m online -i 0
```
This will take roughly 0.4 hours/bug. If you wish to run optimization and transfer learning experiments in the online mode, please let us know. We need to allow access to ```Nvidia Jetson TX2``` device for that purpose.
## Optional (Additional) Experiments
We believe the above experiments are sufficient to support our claims. However, if you want to run additional experiments using Unicorn please use the following commands.

## Steps to reproduce Table 2 latency results for ```Xception```
For debugging ```latency``` faults in ```NVIDIA Jetson TX2``` please use the following commands:
```
docker-compose exec unicorn python ./tests/run_unicorn_debug.py -o inference_time -s Image -k TX2 -m offline
``` 
## Steps to reproduce Figure 16 (b) results 
For ```energy``` optimization in ```NVIDIA Jetson TX2``` please use the following commands.
```
docker-compose exec unicorn python ./tests/run_unicorn_optimization.py -o total_energy_consumption -s Image -k TX2 -m offline
docker-compose exec unicorn python ./tests/run_baseline_optimization.py -o total_energy_consumption -s Image -k TX2 -m offline -b smac
```

