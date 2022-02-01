# Unicorn reproducibility
In this section, we discuss the steps required to reproduce our key findings reported in the paper. Please check the hardware section in [functionality](./FUNCTIONALITY.md). We will use Unicorn offline to for reproducibility.


## Installation
Please install the pre-requisites, clone the repo and navigate to the root directory using the following:

```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.6
pip install json
pip install numpy
pip install scipy
pip install pandas
pip install matplotlib
pip install seaborn
pip install networkx
pip install pydot
pip install causalgraphicalmodels
pip install causalnex
pip install graphviz
pip install py-causal
pip install causality
pip install statsmodels
pip install tqdm
pip install mlxtend
pip install -U scikit-learn
pip install basyesian-optimization
git clone https://github.com/softsys4ai/unicorn.git
cd unicorn
```
##  Key claims

We reproduce results for the following three key claims reported in our paper:

- Unicorn can be used to detect root causes of non-functional performance (```latency``` and ```energy```) faults with higher accuracy and gain. To support this claim we will reproduce partial results from Table 2. In Table 2 we reported our findings for 243/494 faults discovered in this study. For reproducibility, we will reproduce results for 44/243 faults reported in Table 2 for ```Xception``` in ```NVIDIA Jetson TX2``` and  ```NVIDIA Jetson Xavier```.

- Unicorn can be used as a central tool and can support performing tasks such as performance optimization. To support this claim we will reproduce single-objective latency and energy optimization results reported in Figure 16 (a) and 16 (b).

- Unicorn can be effeciciently re-used when the deployment environment changes. To support this claim we will reproduce our findings reported in Figure 18.

For each of the above claims, we will compare our results with the baselines reported in the paper. Instructions to run the baselines can be found in [baselines](./BASELINES.md).

## Steps to reproduce Table 2 results for ```Xception```
Here, the reported energy and latency faults, initial data and ground truths are stored in the corresponding directories. Please run the following command to run Unicorn and baselines one by one.
```
python3 ./tests/run_unicorn_debug.py -o inference_time -s Image -k TX2 -m offline
python3 ./tests/run_baseline_debug.py -o inference_time -s Image -k TX2 -m offline -b cbi
python3 ./tests/run_baseline_debug.py -o inference_time -s Image -k TX2 -m offline -b dd
python3 ./tests/run_baseline_debug.py -o inference_time -s Image -k TX2 -m offline -b encore
python3 ./tests/run_baseline_debug.py -o inference_time -s Image -k TX2 -m offline -b bugdoc
python3 ./tests/run_unicorn_debug.py -o total_energy_consumption -s Image -k Xavier -m offline
python3 ./tests/run_unicorn_debug.py -o total_energy_consumption -s Image -k Xavier -m offline -b cbi
python3 ./tests/run_unicorn_debug.py -o total_energy_consumption -s Image -k Xavier -m offline -b dd
python3 ./tests/run_unicorn_debug.py -o total_energy_consumption -s Image -k Xavier -m offline -b encore
python3 ./tests/run_unicorn_debug.py -o total_energy_consumption -s Image -k Xavier -m offline -b bugdoc
```
## Steps to reproduce Figure 16 (a) and 16 (b) results 
Please use the following commands to reproduce this step:
```
python3 ./tests/run_unicorn_optimization.py -o inference_time -s Image -k TX2 -m offline
python3 ./tests/run_baseline_optimization.py -o inference_time -s Image -k TX2 -m offline -b smac
python3 ./tests/run_unicorn_optimization.py -o total_energy_consumption -s Image -k TX2 -m offline
python3 ./tests/run_baseline_optimization.py -o total_energy_consumption -s Image -k TX2 -m offline -b smac
```

## Steps to reproduce Figure 18 results 
Please use the following commands to reproduce this step:
```
python3 ./tests/run_unicorn_transferability.py -o inference_time -s Image -k Xavier -m offline
```