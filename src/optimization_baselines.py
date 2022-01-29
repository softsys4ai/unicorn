import yaml
import os
from operator import itemgetter
import random
from bayes_opt import BayesianOptimization

class OptimizationBaselines:
    def __init__(self):
        print ("initializing OptimizationBaselines class")
    
    def measure_config(self, memory_growth, logical_devices, core_freq, 
                   gpu_freq, emc_freq, num_cores, 
                   scheduler_policy, vm_swappiness, vm_vfs_cache_pressure,
                   vm_dirty_background_ratio, vm_drop_caches, vm_nr_hugepages,           
                   vm_overcommit_ratio, vm_overcommit_memory, vm_overcommit_hugepages,  
                   kernel_sched_child_runs_first, kernel_sched_rt_runtime_us, vm_dirty_bytes, 
                   vm_dirty_background_bytes, vm_dirty_ratio, swap_memory, 
                   kernel_max_pids, kernel_sched_latency_ns, kernel_sched_nr_migrate,
                   kernel_cpu_time_max_percent, kernel_sched_time_avg_ms):
        """This function is used to measure the recommended configuration by BO. Here, 
        an internal traslation is performed to map to the nearest configuration."""
        
        return -random.uniform(100,200)
    
    def smac(self, objective, soft, 
             hw):
        """This function is used to implement smac"""
        
        # initialization requires reading from a separate config file as the 
        # config option names are passed as argument and dot conflicts with the
        # keyword and are removed by replacing with underscore. . 
        with open(os.path.join(os.getcwd(),"etc/bo_config.yml")) as file:
            cfg = yaml.load(file, Loader=yaml.FullLoader)
    
            soft_columns = cfg["software_columns"]["Image"]
            hw_columns = cfg["hardware_columns"]["TX2"]
            kernel_columns = cfg["kernel_columns"]
            columns = soft_columns + hw_columns + kernel_columns 
            option_values = cfg["option_values"]["TX2"]
            
            # define bounded configuration space 

            pbounds={}

            for col in columns:
                pbounds[col] = [option_values[col][0], option_values[col][1]]

            # define optimizer
            optimizer = BayesianOptimization(
            f = self.measure_config,
            pbounds = pbounds,
            random_state=1)

            # optimize for 200 iterations
            optimizer.maximize(
            init_points=25,
            n_iter=200)

            # output
            for i, res in enumerate(optimizer.res):
                print("Iteration {}: \n\t{}".format(i, res))
    
    
    def pesmo(self, data):
        """This function is used to implement pesmo"""
        if data:
            print ("data format is valid")
        
        else:
            print ("no data found")
            return
    
    


