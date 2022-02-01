# Unicorn functionality
In this section, we introduce Unicorn with a walkthrough example. Initially we will get to familiarize with the directory structure used in this repository. 

## Structure

```
unicorn
   |-- artifact (contains documentations)
   |-- causallearn (contains third party code to recover causal structure)
   |-- data 
      |--bug (contains bugs, ground truths and measurements)
         |--multi (contains multi-objective bugs for software in different hardware)
         |--single (contains single-objective bugs for software in different hardware)
      |--ground_truth
         |--multi (contains multi-objective ground truth fixes for reported bugs)
         |--single (contains single-objective ground truth fixes for reported bugs)
      |--initial (contains initial data for Unicorn and baselines)
      |--measurement (contains configuration measurements data)
      |--sampled
    |-- etc (contains configuration meatadata )
    |-- services (contains scripts for data generation)
    |--src (contains necessary code to implement unicorn and other baselines)
    |--tests (contains necessary code to run and test unicorn)
    |--utils (contains necessary scripts to set hardware configuration)
```
## Hardware 
The offline version can be run from any devices while the online version needs to be run from ```NVIDIA Jetson TX2``` and ```NVIDIA Jetson Xavier```. For this evaluation, we believe testing the offline version would be sufficient for Unicorn functionality. We used the following specifications for offline mode.
``` 
**offline mode**
-----------------------------------------------------------------------------------------
Processor: Intel Core i7-8700 CPU @ 3.20GHz × 12 
Memory: 31.2 GB
OS: Ubuntu 18.04 LTS 64-bit
```
For online mode we used the following setup.
``` 
**NVIDIA Jetson Xavier**
-----------------------------------------------------------------------------------------
Processor: 6-core Carmel ARM v8.2 64-bit CPU, 8MB L2 + 4MB L3
GPU: 384-core Volta GPU with 48 Tensor cores
Memory: 8 GB 256-bit LPDDR4x 1333MHz
OS: Ubuntu 20.04 64-bit 85.3 GB/s

**NVIDIA Jetson TX2**
-----------------------------------------------------------------------------------------
Processor: Dual-core NVIDIA Denver 2 64-bit CPU and quad-core Arm Cortex-A57 
GPU: NVIDIA Pascal architecture with 256 NVIDIA CUDA cores
Memory: 4 GB 128-bit LPDDR4 51.2 GB/s
OS: Ubuntu 20.04 64-bit
```


## Functionality testing
Once the pre-requisites are installed clone the repo and navigate to the root directory using the following:
```
git clone https://github.com/softsys4ai/unicorn.git
cd unicorn
```
Consider a performance developer encounters a non-functional ```energy``` fault for ```Xception``` in ```NVIDIA Jetson Xavier``` as the following:
```
**Example Bug** (Bug ID: 0)
------------------------------------------------------------------------------------------
core_freq                        2.188800e+06
gpu_freq                         2.688000e+05
emc_freq                         6.000000e+08
num_cores                        2.000000e+00
memory_growth                    5.000000e-01
logical_devices                  2.000000e+00
scheduler.policy                 0.000000e+00
vm.swappiness                    1.000000e+02
vm.vfs_cache_pressure            5.000000e+02
vm.dirty_background_ratio        8.000000e+01
vm.drop_caches                   0.000000e+00
vm.nr_hugepages                  1.000000e+00
vm.overcommit_ratio              5.000000e+01
vm.overcommit_memory             1.000000e+00
vm.overcommit_hugepages          2.000000e+00
kernel.sched_child_runs_first    1.000000e+00
kernel.sched_rt_runtime_us       9.500000e+05
vm.dirty_bytes                   3.000000e+01
vm.dirty_background_bytes        6.000000e+01
vm.dirty_ratio                   5.000000e+01
swap_memory                      1.000000e+00
kernel.max_pids                  3.276800e+04
kernel.sched_latency_ns          2.400000e+07
kernel.sched_nr_migrate          1.280000e+02
kernel.cpu_time_max_percent      1.000000e+02
kernel.sched_time_avg_ms         1.000000e+03
total_energy_consumption         1.500357e+05
```
The reported ```energy``` value for the performance fault is over ```150000 millijoules```. To resolve the fault, the developer queries Unicorn to determine the root cause and expects to achieve a ```80% or more``` improvement as a fix to this fault. The developer's query is hardcoded in ```line 58``` in ```./tests/run_unicorn_debug.py```  as the following:
```
query = 0.8
``` 
The fault must be in the appropriate bug directory to run Unicorn for this fault with the current version. We put the fault in ```.data/bug/single/Xavier/Image/Xavier_Image_total_energy_consumption.csv``` in the beginning. Unicorn needs to be passed  the ```index``` of the bug (row number) before running. To see what arguments are needed to run debugging with Unicorn use the following:

```
python3 ./tests/run_unicorn_debug.py -h
Usage: %python3 run_unicorn_debug.py -o [objectives] -d [init_data] -s [software] -k [hardware] -m [mode] -i [bug_index]
    

Options:
  -h, --help  show this help message and exit
  -o OBJ, --objective=OBJ objective type
  -s SOFTWARE, --software=SOFTWARE software
  -k HARDWARE, --hardware=HARDWARE hardware
  -m MODE, --mode=MODE  mode
  -i BUG_INDEX, --bug_index=BUG_INDEX bug_index

```
Therefore, we need to use the following command to run Unicorn to resolve this energy fault (```bug_index is 0```).
```
python3 ./test/run_unicorn_debug.py -o total_energy_consumption -s Image -k Xavier -m offline -i 0
``` 
### Learn causal performance model
We will see similar output while Unicorn is running.
```
initializing CausalModel class
/home/pjamshid/unicorn/causallearn/search/ConstraintBased/FCI.py:792: UserWarning: The number of features is much larger than the sample size!
  warnings.warn("The number of features is much larger than the sample size!")
Starting Fast Adjacency Search.
Working on node 48: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 49/49 [00:00<00:00, 426.24it/s]
Finishing Fast Adjacency Search.
/home/pjamshid/unicorn/causallearn/search/ConstraintBased/FCI.py:792: UserWarning: The number of features is much larger than the sample size!
  warnings.warn("The number of features is much larger than the sample size!")
Starting Fast Adjacency Search.
Working on node 1:   4%|█████▉                                                                                                                                            | 2/49 [00:00<00:00, 10446.59it/s]X2 --- X7 because it was forbidden by background background_knowledge.
X2 --- X26 because it was forbidden by background background_knowledge.
Working on node 2:   6%|█████████                                                                                                                                          | 3/49 [00:00<00:00, 1526.87it/s]X3 --- X4 because it was forbidden by background background_knowledge.
X3 --- X5 because it was forbidden by background background_knowledge.
X3 --- X17 because it was forbidden by background background_knowledge.
Working on node 3:   8%|███████████▉                                                                                                                                       | 4/49 [00:00<00:00, 1150.39it/s]X4 --- X12 because it was forbidden by background background_knowledge.
X4 --- X17 because it was forbidden by background background_knowledge.
Working on node 6:  14%|█████████████████████▏                                                                                                                              | 7/49 [00:00<00:00, 989.06it/s]X7 --- X14 because it was forbidden by background background_knowledge.
Working on node 8:  18%|███████████████████████████▏                                                                                                                        | 9/49 [00:00<00:00, 983.40it/s]X9 --- X15 because it was forbidden by background background_knowledge.
X9 --- X18 because it was forbidden by background background_knowledge.
X9 --- X20 because it was forbidden by background background_knowledge.
Working on node 9:  20%|██████████████████████████████                                                                                                                     | 10/49 [00:00<00:00, 957.28it/s]X10 --- X15 because it was forbidden by background background_knowledge.
X10 --- X20 because it was forbidden by background background_knowledge.
X10 --- X21 because it was forbidden by background background_knowledge.
Working on node 11:  24%|███████████████████████████████████▊                                                                                                              | 12/49 [00:00<00:00, 925.49it/s]X12 --- X26 because it was forbidden by background background_knowledge.
Working on node 12:  27%|██████████████████████████████████████▋                                                                                                           | 13/49 [00:00<00:00, 971.66it/s]X13 --- X16 because it was forbidden by background background_knowledge.
X13 --- X23 because it was forbidden by background background_knowledge.
Working on node 13:  29%|█████████████████████████████████████████▋                                                                                                        | 14/49 [00:00<00:00, 959.94it/s]X14 --- X26 because it was forbidden by background background_knowledge.
Working on node 14:  31%|████████████████████████████████████████████▋                                                                                                     | 15/49 [00:00<00:00, 991.51it/s]X15 --- X18 because it was forbidden by background background_knowledge.
Working on node 15:  33%|███████████████████████████████████████████████▎                                                                                                 | 16/49 [00:00<00:00, 1020.73it/s]X16 --- X23 because it was forbidden by background background_knowledge.
Working on node 16:  35%|██████████████████████████████████████████████████▎                                                                                              | 17/49 [00:00<00:00, 1060.13it/s]X17 --- X19 because it was forbidden by background background_knowledge.
Working on node 17:  37%|█████████████████████████████████████████████████████▎                                                                                           | 18/49 [00:00<00:00, 1103.91it/s]X18 --- X20 because it was forbidden by background background_knowledge.
Working on node 18:  39%|████████████████████████████████████████████████████████▏                                                                                        | 19/49 [00:00<00:00, 1102.77it/s]X19 --- X22 because it was forbidden by background background_knowledge.
Working on node 20:  43%|██████████████████████████████████████████████████████████████▏                                                                                  | 21/49 [00:00<00:00, 1160.83it/s]X21 --- X26 because it was forbidden by background background_knowledge.
Working on node 48: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 49/49 [00:00<00:00, 622.43it/s]
Finishing Fast Adjacency Search.
Starting BK Orientation.
Finishing BK Orientation.
Starting BK Orientation.
Finishing BK Orientation.
```
Unicorn initially builds a causal graph with 25 initial samples located in ```./data/initial/Xavier/Image/Xavier_Image_initial.csv``` usingthe causal graph discovery algorithm FCI (indicated by ```Finishing Fast Adjacency Search```). Then, Unicorn imposes constraints on the discovered causal structure as background knowledge (BK) to remove incoming edges to any configuration options node and outgoing edges from any performan objective node to any other node indicated by the ```BK Orientation``` messages.  

At this stage the causal graph has some undecided edges which are later resolved and the following causal graph is discovered in the first iteration. 

![graph_1](https://user-images.githubusercontent.com/12802456/151922460-efbd2a6e-119b-4ba6-8513-db255483891b.png)

An example run of Unicorn for an ```energy``` fault is recorded in this 
[trial run](https://user-images.githubusercontent.com/12802456/151889655-63efb22e-be37-480c-9f21-dc4d25f77335.mp4). Printing graph outputs are disabled 
in the trial run video (only connections are printed in the standard output.)

## Evaluation



