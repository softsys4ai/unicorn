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
An example run of Unicorn for an ```energy``` fault is recorded in this 
[trial run](https://user-images.githubusercontent.com/12802456/151889655-63efb22e-be37-480c-9f21-dc4d25f77335.mp4). Let us walkthorugh the example in more detail to understand the steps better. 
