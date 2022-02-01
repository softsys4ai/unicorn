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
The offline version can be run from any devices while the online version needs to be run from ```NVIDIA Jetson TX2``` and ```NVIDIA Jetson Xavier```. However, we believe testing the offline version is sufficient to determine Unicorn's functionality. 

We used the following hardware specifications for offline mode.
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
Jetpack: 4.3
OS: Ubuntu 20.04 64-bit 85.3 GB/s

**NVIDIA Jetson TX2**
-----------------------------------------------------------------------------------------
Processor: Dual-core NVIDIA Denver 2 64-bit CPU and quad-core Arm Cortex-A57 
GPU: NVIDIA Pascal architecture with 256 NVIDIA CUDA cores
Memory: 4 GB 128-bit LPDDR4 51.2 GB/s
Jetpack: 4.3
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
memory_growth                    5.000000e-01
logical_devices                  2.000000e+00
core_freq                        2.188800e+06
gpu_freq                         2.688000e+05
emc_freq                         6.000000e+08
num_cores                        2.000000e+00
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
The reported ```energy``` value for the performance fault is over ```150000 millijoules```. To resolve the fault, the developer queries Unicorn to determine the root cause and expects to achieve a ```80% or more``` improvement as a fix to this fault. The developer is also interested to know the root causes of failure. The developer's query is hardcoded in ```line 58``` in ```./tests/run_unicorn_debug.py```  as the following:
```
query = 0.8
``` 
The fault must be in the appropriate bug directory to run Unicorn for this fault with the current version. Therefore, we put the fault in ```./data/bug/single/Xavier/Image/Xavier_Image_total_energy_consumption.csv``` in the beginning. Unicorn needs to be passed  the ```index``` of the bug (row number) before running. To see what arguments are needed to run debugging with Unicorn please use the following:

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
Here, objective type is ```total_energy_consumption```, software is ```Image```, hardware is ```Xavier```, mode is ```offline```, and bug_index is ```0```. Therefore, we need to use the following command.
```
python3 ./test/run_unicorn_debug.py -o total_energy_consumption -s Image -k Xavier -m offline -i 0
``` 
Let us look into different steps involved in Unicorn for resolving the fault. 

### Learn causal performance model
Once the above command is run we should see similar output while Unicorn is running. We have an warning as we have 25 samples at this point and the number of features (configuration options and system events) are higher than 25. At this point we can safely ignore this warning.
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
Unicorn initially builds a causal graph with the initial samples located in ```./data/initial/Xavier/Image/Xavier_Image_initial.csv``` usingthe causal graph discovery algorithm FCI (indicated by ```Finishing Fast Adjacency Search```). Then, Unicorn imposes constraints on the discovered causal structure as background knowledge (BK) to remove incoming edges to any configuration options node and outgoing edges from any performance objective node to any other nodes indicated by the ```BK Orientation``` messages.  

At this stage the causal graph has some undecided edges which are later resolved and the following causal graph is discovered in the first iteration. 

![graph_iter_1 png](https://user-images.githubusercontent.com/12802456/151999773-bce9cc41-bb4f-4d99-bfca-5fbda2b07b57.png)

### Iterative sampling
After the causal graph is discovered we identify the causal paths. A causal path starts from a performance objective node and ends in a configuration option. For example, the causal paths for ```total_energy_consumption``` from the causal graph obatined in the first iteration are below.
```
[['total_energy_consumption', 'core_freq'], ['total_energy_consumption', 'num_cores'], ['total_energy_consumption', 'kernel.max_pids'], ['total_energy_consumption', 'vm.drop_caches'], ['total_energy_consumption', 'kernel.sched_nr_migrate'], ['total_energy_consumption', 'emc_freq']]
```
Once the causal paths are identified we select the top K paths using their average causal effect. For this software system we set ```K=25```. Since, the number of causal paths obtained from the causal graph is less than 25 we select all the paths to consider in the later stages. Now, we compute the individual treatment effect for each path by setting each option in the path to its allowable values and determine for what value of an option provides the maximum treatment effect to resolve this bug. In this case, we observe that ```emc_freq = 2.133000e+09``` has the highest individual treatment effect in the path ```['total_energy_consumption', 'emc_freq']```. Therefore, we perform an intervention by changing ```emc_freq = 2.133000e+09``` in the performance fault configuration and select for measurement. 

```
memory_growth                    5.000000e-01
logical_devices                  2.000000e+00
core_freq                        2.188800e+06
gpu_freq                         2.688000e+05
emc_freq                         2.133000e+09
num_cores                        2.000000e+00
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
```
### Update causal performance model
In this stage, we measure the recommended configuration to determine whether it resolves the fault. Here,
```
Recommended Config Objective Value 65084
```
Since, this configuration does not resolve developers query to improve ```energy``` by ```80% or more``` we proceed to the next iteration and update the causal graph with the new configuration.
```
--------------------------------------------------
/home/pjamshid/unicorn/causallearn/search/ConstraintBased/FCI.py:792: UserWarning: The number of features is much larger than the sample size!
  warnings.warn("The number of features is much larger than the sample size!")
Starting Fast Adjacency Search.
Working on node 48: 100%|████████████████████| 49/49 [00:00<00:00, 12084.49it/s]
Finishing Fast Adjacency Search.
/home/pjamshid/unicorn/causallearn/search/ConstraintBased/FCI.py:792: UserWarning: The number of features is much larger than the sample size!
  warnings.warn("The number of features is much larger than the sample size!")
Starting Fast Adjacency Search.
Working on node 2:   6%|█▍                     | 3/49 [00:00<00:00, 3306.07it/s]X3 --- X5 because it was forbidden by background background_knowledge.
Working on node 3:   8%|█▉                     | 4/49 [00:00<00:00, 2441.39it/s]X4 --- X7 because it was forbidden by background background_knowledge.
X4 --- X12 because it was forbidden by background background_knowledge.
X4 --- X17 because it was forbidden by background background_knowledge.
X4 --- X19 because it was forbidden by background background_knowledge.
X4 --- X26 because it was forbidden by background background_knowledge.
Working on node 4:  10%|██▎                    | 5/49 [00:00<00:00, 1183.69it/s]X5 --- X11 because it was forbidden by background background_knowledge.
X5 --- X25 because it was forbidden by background background_knowledge.
Working on node 5:  12%|██▊                    | 6/49 [00:00<00:00, 1054.42it/s]X6 --- X10 because it was forbidden by background background_knowledge.
Working on node 6:  14%|███▍                    | 7/49 [00:00<00:00, 994.75it/s]X7 --- X14 because it was forbidden by background background_knowledge.
Working on node 8:  18%|████▍                   | 9/49 [00:00<00:00, 990.44it/s]X9 --- X15 because it was forbidden by background background_knowledge.
X9 --- X18 because it was forbidden by background background_knowledge.
Working on node 9:  20%|████▍                 | 10/49 [00:00<00:00, 1010.89it/s]X10 --- X20 because it was forbidden by background background_knowledge.
X10 --- X21 because it was forbidden by background background_knowledge.
Working on node 10:  22%|████▉                 | 11/49 [00:00<00:00, 931.94it/s]X11 --- X14 because it was forbidden by background background_knowledge.
Working on node 11:  24%|█████▍                | 12/49 [00:00<00:00, 938.25it/s]X12 --- X17 because it was forbidden by background background_knowledge.
X12 --- X19 because it was forbidden by background background_knowledge.
X12 --- X24 because it was forbidden by background background_knowledge.
X12 --- X26 because it was forbidden by background background_knowledge.
Working on node 12:  27%|█████▊                | 13/49 [00:00<00:00, 911.04it/s]X13 --- X23 because it was forbidden by background background_knowledge.
Working on node 13:  29%|██████▎               | 14/49 [00:00<00:00, 908.39it/s]X14 --- X26 because it was forbidden by background background_knowledge.
Working on node 15:  33%|██████▊              | 16/49 [00:00<00:00, 1017.08it/s]X16 --- X23 because it was forbidden by background background_knowledge.
Working on node 16:  35%|███████▎             | 17/49 [00:00<00:00, 1050.63it/s]X17 --- X19 because it was forbidden by background background_knowledge.
Working on node 17:  37%|███████▋             | 18/49 [00:00<00:00, 1083.66it/s]X18 --- X20 because it was forbidden by background background_knowledge.
Working on node 18:  39%|████████▏            | 19/49 [00:00<00:00, 1115.80it/s]X19 --- X22 because it was forbidden by background background_knowledge.
X19 --- X24 because it was forbidden by background background_knowledge.
Working on node 48: 100%|█████████████████████| 49/49 [00:00<00:00, 6552.35it/s]
Finishing Fast Adjacency Search.
Starting BK Orientation.
Finishing BK Orientation.
Starting BK Orientation.
Finishing BK Orientation.
X45 --> X49

``` 
Causal graph discovered in iteration 2 is updated after adding the recommended configuration. Here, we see an impact of adding the recommended confiuration that changes the causal graph in previous iteration. 
![graph_iter_2 png](https://user-images.githubusercontent.com/12802456/151996491-ddca8174-6e08-4d12-a5ce-0c2fba0e002d.png)
After the graph is obtained we repeat the steps of causal path discovery, computing path causal effects and iterative sampling until the fault is resolved.

Finally, we find a fix after 23 iteration.

```
+++++++++++++++Recommended Fix++++++++++++++++++++
memory_growth                    5.000000e-01
logical_devices                  2.000000e+00
core_freq                        2.265600e+06
gpu_freq                         2.688000e+05
emc_freq                         2.133000e+09
num_cores                        4.000000e+00
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
kernel.max_pids                  6.553600e+04
kernel.sched_latency_ns          2.400000e+07
kernel.sched_nr_migrate          1.280000e+02
kernel.cpu_time_max_percent      1.000000e+02
kernel.sched_time_avg_ms         1.000000e+03
Name: 0, dtype: float64
Unicorn Fix Value 24748
Number of Samples Required 23
```

### Evaluation
Here, the gain is ```((150035 - 24748)/150035) * 100% = 83%```. Therefore, it satisfies the user query to improve performance fault by ```80%```. Unicorn required 23 additional samples to resolve the fault. 

We also measure accuracy, precision and recall of the recommended fix by comparison with the ground truth fix that is given below:

```
memory_growth                    5.000000e-01          
logical_devices                  2.000000e+00
core_freq                        2.265600e+06
gpu_freq                         2.688000e+05
emc_freq                         2.133000e+09
num_cores                        4.000000e+00
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
kernel.max_pids                  6.553600e+04
kernel.sched_latency_ns          2.400000e+07
kernel.sched_nr_migrate          1.280000e+02
kernel.cpu_time_max_percent      1.000000e+02
kernel.sched_time_avg_ms         1.000000e+03
total_energy_consumption         2.474800e+04
```

Let us compare them side by side to see what options are changed and what are the root causes of this fault.

```
                                  Bug        Ground truth     Unicorn
--------------------------------------------------------------------------
memory_growth                 5.000000e-01   5.000000e-01   5.000000e-01      
logical_devices               2.000000e+00   2.000000e+00   2.000000e+00
core_freq*                    2.188800e+06   2.265600e+06   2.265600e+06
gpu_freq                      2.688000e+05   2.688000e+05   2.688000e+05
emc_freq*                     6.000000e+08   2.133000e+09   2.133000e+09
num_cores*                    2.000000e+00   4.000000e+00   4.000000e+00
scheduler.policy              0.000000e+00   0.000000e+00   0.000000e+00
vm.swappiness                 1.000000e+02   1.000000e+02   1.000000e+02
vm.vfs_cache_pressure         5.000000e+02   5.000000e+02   5.000000e+02
vm.dirty_background_ratio     8.000000e+01   8.000000e+01   8.000000e+01
vm.drop_caches                0.000000e+00   0.000000e+00   0.000000e+00
vm.nr_hugepages               1.000000e+00   1.000000e+00   1.000000e+00
vm.overcommit_ratio           5.000000e+01   5.000000e+01   5.000000e+01
vm.overcommit_memory          1.000000e+00   1.000000e+00   1.000000e+00
vm.overcommit_hugepages       2.000000e+00   2.000000e+00   2.000000e+00
kernel.sched_child_runs_first 1.000000e+00   1.000000e+00   1.000000e+00
kernel.sched_rt_runtime_us    9.500000e+05   9.500000e+05   9.500000e+05
vm.dirty_bytes                3.000000e+01   3.000000e+01   3.000000e+01
vm.dirty_background_bytes     6.000000e+01   6.000000e+01   6.000000e+01
vm.dirty_ratio                5.000000e+01   5.000000e+01   5.000000e+01
swap_memory                   1.000000e+00   1.000000e+00   1.000000e+00
kernel.max_pids*              3.276800e+04   6.553600e+04   6.553600e+04
kernel.sched_latency_ns       2.400000e+07   2.400000e+07   2.400000e+07
kernel.sched_nr_migrate       1.280000e+02   1.280000e+02   1.280000e+02
kernel.cpu_time_max_percent   1.000000e+02   1.000000e+02   1.000000e+02
kernel.sched_time_avg_ms      1.000000e+03   1.000000e+03   1.000000e+03
total_energy_consumption*     1.500357e+05   2.474800e+04   2.474800e+04
```
Here, the root causes are ```core_freq```, ```emc_freq```, ```num_cores```, and ```kernel.max_pids``` (indicated by ```*```). Here, Unicorn is able to find each of the root causes. Therefore, Unicorn achieves ```100%``` accuracy, precision and recall for this non-functional energy fault.

An example run of Unicorn for an ```energy``` fault is recorded in this 
[trial run](https://user-images.githubusercontent.com/12802456/151889655-63efb22e-be37-480c-9f21-dc4d25f77335.mp4). Printing graph outputs are disabled in the trial run video (only connections are printed in the standard output.)



