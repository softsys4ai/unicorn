# Unicorn functionality
In this section, we introduce the Uniocorn with a walkthrough example. Initially we will get to familiarize with the directory structure used in this repository. 

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

## Functionality testing
