#!/usr/bin/python
import os
import sys 
import commands
import subprocess
import pandas as pd

class TuneKernelParameters(object):
    """This class is used to tune linux kernel parameters
    """
    def __init__(self,
                counter):
        print ("Initializing Tune Kernel Parameter Class")
        self.counter=counter
        self.kernel_params={}
        self.tune_io_scheduler_parameters()
        self.tune_memory_subsystem_parameters()
    def get_kernel_params(self):
        """This function is used to get all kernel parameters include in experimental design
        """
        return pd.DataFrame(self.kernel_params)
        
    def tune_io_scheduler_parameters(self):
        """This function is used to tune io scheduler kernel parameters
        Parameters:
        ---------------------------------------------------------------
        | IO Scheduler:                                               |
        --------------------------------------------------------------- 
        1. CFQ
        2. NOOP           
        """
        if self.counter % 2==0:
            os.system ("echo cfq > /sys/block/mmcblk0/queue/scheduler")
        else:
            os.system ("echo noop > /sys/block/mmcblk0/queue/scheduler")
    
    def tune_task_scheduler_parameters(self):
        """This function is used to tune task scheduler kernel parameters
        ---------------------------------------------------------------
        | Task Scheduler:                                             |
        --------------------------------------------------------------- 
        1.  SCHED_FIFO
        2.  SCHED_BATCH
        3.  SCHED_IDLE
        4.  SCHED_OTHER
        5.  SCHED_RR
        6.  sched_cfs_bandwith_slice_us
        7.  sched_child_runs_first
        8.  sched_compat_yield
        9.  sched_migration_cost_ns
        10. sched_latency_ns
        11. sched_min_granularity_ns
        12. sched_wakeup_granualarity_ns
        13. sched_rr_timeslice_ms
        14. sched_rt_period_us
        15. sched_rt_runtime_us 
        16. sched_nr_migrate
        17. sched_time_avg_ms     
        """
    
    def tune_block_device_parameters(self):
        """This function is used to tune block device kernel parameters
        """
        print "tune block device params"
    
    def tune_network_parameters(self):
        """This function is used to tune io network kernel parameters
        """
        print "tune network params"
    
    def tune_memory_subsystem_parameters(self):
        """This function is used to tune io memory kernel parameters
         ---------------------------------------------------------------
        | Memory Subsystem:                                            |
        --------------------------------------------------------------- 
        1. vm.swappiness
        2. vm.vfs_cache_pressure
        3. vm.min_free_kbytes
        4. vm.watermark_scale_factor
        5. vm.dirty_background_ratio
        6. vm.dirty_background_bytes
        7. vm.dirty_ratio
        8. vm.dirty_bytes
        9. vm.dirty_expire_centisecs
        """
        ## 0-100 | 0-500
        if self.counter==0:
            os.system ("sysctl vm.swappiness=0")
            self.kernel_params['vm.swappiness']=[0]
            os.system ("sysctl vm.vfs_cache_pressure=100")
            self.kernel_params['vm.vfs_cache_pressure']=[100]
        if self.counter==1:
            os.system ("sysctl vm.swappiness=0")
            self.kernel_params['vm.swappiness']=[0]
            os.system ("sysctl vm.vfs_cache_pressure=100")
            self.kernel_params['vm.vfs_cache_pressure']=[100]
        if self.counter==2:
            os.system ("sysctl vm.swappiness=0")
            self.kernel_params['vm.swappiness']=[0]
            os.system ("sysctl vm.vfs_cache_pressure=500")
            self.kernel_params['vm.vfs_cache_pressure']=[500]
        if self.counter==3:
            os.system ("sysctl vm.swappiness=0")
            self.kernel_params['vm.swappiness']=[0]
            os.system ("sysctl vm.vfs_cache_pressure=500")
            self.kernel_params['vm.vfs_cache_pressure']=[500]
        ## 60-100 | 60-500
        if self.counter==4:
            os.system ("sysctl vm.swappiness=60")
            self.kernel_params['vm.swappiness']=[60]
            os.system ("sysctl vm.vfs_cache_pressure=100")
            self.kernel_params['vm.vfs_cache_pressure']=[100]
        if self.counter==5:
            os.system ("sysctl vm.swappiness=60")
            self.kernel_params['vm.swappiness']=[60]
            os.system ("sysctl vm.vfs_cache_pressure=100")
            self.kernel_params['vm.vfs_cache_pressure']=[100]
        if self.counter==6:
            os.system ("sysctl vm.swappiness=60")
            self.kernel_params['vm.swappiness']=[60]
            os.system ("sysctl vm.vfs_cache_pressure=500")
            self.kernel_params['vm.vfs_cache_pressure']=[500]
        if self.counter==7:
            os.system ("sysctl vm.swappiness=60")
            self.kernel_params['vm.swappiness']=[60]
            os.system ("sysctl vm.vfs_cache_pressure=500")
            self.kernel_params['vm.vfs_cache_pressure']=[500]
        ## 100-100 | 100-500
        if self.counter==4:
            os.system ("sysctl vm.swappiness=100")
            self.kernel_params['vm.swappiness']=[100]
            os.system ("sysctl vm.vfs_cache_pressure=100")
            self.kernel_params['vm.vfs_cache_pressure']=[100]
        if self.counter==5:
            os.system ("sysctl vm.swappiness=1000")
            self.kernel_params['vm.swappiness']=[100]
            os.system ("sysctl vm.vfs_cache_pressure=100")
            self.kernel_params['vm.vfs_cache_pressure']=[100]
        if self.counter==6:
            os.system ("sysctl vm.swappiness=100")
            self.kernel_params['vm.swappiness']=[100]
            os.system ("sysctl vm.vfs_cache_pressure=500")
            self.kernel_params['vm.vfs_cache_pressure']=[500]
        if self.counter==7:
            os.system ("sysctl vm.swappiness==100")
            self.kernel_params['vm.swappiness']=[100]
            os.system ("sysctl vm.vfs_cache_pressure=500")
            self.kernel_params['vm.vfs_cache_pressure']=[500]
        
        self.kernel_params['kernel.cpu_time_max_percent']=[25]
        self.kernel_params['kernel.random.read_wakeup_threshold']=[64]
        self.kernel_params['kernel.random.write_wakeup_threshold']=[896]
        self.kernel_params['kernel.sched_cfs_bandwith_slice_us']=[5000]
        self.kernel_params['kernel.sched_child_runs_first']=[0]
        self.kernel_params['kernel.sched_rr_timeslice_ms']=[25]
        self.kernel_params['kernel.sched_rt_period_us']=[1000000]
        self.kernel_params['kernel.sched_rt_runtime_us']=[950000]
        self.kernel_params['kernel.timer_migration']=[1]
        self.kernel_params['scheduler.policy']=[self.counter % 2]
        self.kernel_params['vm.dirty_background_bytes']=[0]
        self.kernel_params['vm.dirty_background_ratio']=[10]
        self.kernel_params['vm.dirty_bytes']=[0]
        self.kernel_params['vm.drop_caches']=[0]                    
                       
        





























