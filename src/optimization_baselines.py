import yaml
import os
from operator import itemgetter
import random
from bayes_opt import BayesianOptimization
import json
<<<<<<< HEAD
import pandas as pd
=======

>>>>>>> f67624787a3a63b3a3484c8aeb1b72d1673d6321
class OptimizationBaselines:
    def __init__(self):
        print ("initializing OptimizationBaselines class")
        with open(os.path.join(os.getcwd(),"etc/bo_config.yml")) as file:
            self.cfg = yaml.load(file, Loader=yaml.FullLoader)
        with open(os.path.join(os.getcwd(),self.cfg["opt_dir"],"measurement_b.json")) as mfl:    
            self.m = json.load(mfl)
        self.iteration = 0
    
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
        an internal translation is performed to map to the nearest configuration."""
        
        curm = self.m[self.hw][self.soft][self.objective][str(self.iteration)]["measurement"]
        self.iteration += 1
        return -curm
    
    def get_configs(self, configs, columns):
        for i in range(len(configs)):
           cur = configs[i]['params']
           value = configs[i]['target']
           for col in columns:
                min_distance = 20000000000000000
                vals = self.cfg["option_values"][self.hw][col]
                
<<<<<<< HEAD
                cur_val = cur[col]
                
                for val in vals:
                    if abs(val-cur_val) < min_distance:
                        
=======
                print (vals)
                cur_val = cur[col]
                print (cur_val)
                for val in vals:
                    if abs(val-cur_val) < min_distance:
                        print (min_distance)
>>>>>>> f67624787a3a63b3a3484c8aeb1b72d1673d6321
                        min_distance = abs(val-cur_val)
                configs[i]['params'][col]=val
               
        return configs  
              
           
    def smac(self, objective, soft, 
             hw):
        """This function is used to implement smac"""
        
        # initialization requires reading from a separate config file as the 
        # config option names are passed as argument and dot conflicts with the
        # keyword and are removed by replacing with underscore. . 
        
        soft_columns = self.cfg["software_columns"][soft]
        hw_columns = self.cfg["hardware_columns"][hw]
        kernel_columns = self.cfg["kernel_columns"]
        columns = soft_columns + hw_columns + kernel_columns 
        option_values = self.cfg["option_values"][hw]
        
            
        # define bounded configuration space 
        self.objective = objective[0]
        self.hw = hw
        self.soft = soft
        pbounds={}

        for col in columns:
            pbounds[col] = [option_values[col][0], option_values[col][-1]]

        # define optimizer
        optimizer = BayesianOptimization(
        f = self.measure_config,
        pbounds = pbounds,
        random_state=1)

        # optimize for 200 iterations
        optimizer.maximize(
<<<<<<< HEAD
        init_points=25,
        n_iter=175)
        
        configs = self.get_configs(optimizer.res, columns)
        dfl = []
        for conf in configs:
           cur = []
           for col in columns:
              cur.append(conf['params'][col])
           cur.append(-conf['target'])
           dfl.append(cur)
        df = pd.DataFrame(dfl)
        columns.append(self.objective) 
        df.columns = columns
        df["Iteration"] = [i for i in range(len(df))]
        print ("Optimal value obtained by SMAC: ", df[self.objective].min())
               
        
=======
        init_points=5,
        n_iter=5)
        
        print(self.get_configs(optimizer.res, columns))

        
        #for i, res in enumerate(optimizer.res):
        #    print("Iteration {}: \n\t{}".format(i, res))
    
    
    def pesmo(self, data):
        """This function is used to implement pesmo"""
        if data:
            print ("data format is valid")
        
        else:
            print ("no data found")
            return
    
>>>>>>> f67624787a3a63b3a3484c8aeb1b72d1673d6321
    


