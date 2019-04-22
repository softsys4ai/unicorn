#!/usr/bin/python
import os
import sys 
import commands
import subprocess

class TuneKernelParameters(object):
    """This class is used to tune linux kernel parameters
    """
    def __init__(self):
        print ("Initializing Tune Kernel Parameter Class")
    
    def get_kernel_params(self):
        """This function is used to get all kernel parameters include in experimental design
        """
        kernel_params={'kernel.cpu_time_max_percent':25,
                       'kernel.random.read_wakeup_threshold':64,
                       'kernel.random.write_wakeup_threshold':896,
                       'kernel.sched_cfs_bandwith_slice_us':5000,
                       'kernel.sched_child_runs_first':0,
                       'kernel.sched_rr_timeslice_ms':25,
                       'kernel.sched_rt_period_us':1000000,
                       'kernel.sched_rt_runtime_us':950000,
                       'kernel.timer_migration':1,
                       'vm.block_dump':0,
                       'vm.compact_unevictable_allowed':1,
                       'vm.dirty_background_bytes':0,
                       'vm.dirty_background_ratio':10,
                       'vm.dirty_bytes':0,
                       'vm.dirty_expire_centisecs':3000,
                       'vm.dirty_ratio':20,
                       'vm.dirty_writeback_centisecs': 500,
                       'vm.dirtytime_expire_seconds': 43200,
                       'vm.drop_caches':0,
                       'vm.extfrag_threshold':500,
                       'vm.extra_free_kbytes':0,
                       'vm.lazy_vfree_pages':8192,
                       'vm.lazy_vfree_tlb_flush_all_threshold':536870912,               
                       'vm.max_map_count':65530,
                       'vm.min_free_kbytes':11337,
                       'vm.mmap_min_addr':32768,
                       'vm.nr_pdflush_threads':0,
                       'vm.oom_dump_tasks':1,
                       'vm.oom_kill_allocating_task':0,
                       'vm.overcommit_kbytes':0,
                       'vm.overcommit_memory':0,
                       'vm.overcommit_ratio':50,
                       'vm.page-cluster':3,
                       'vm.percpu_pagelist_fraction':0,
                       'vm.stat_interval':1,
                       'vm.swappiness': 60,
                       'vm.user_reserve_kbytes':1310,
                       'vm.vfs_cache_pressure':100                    
                       }
       
        return kernel_params
        
    def tune_io_scheduler_parameters(io_sched_param):
        """This function is used to tune io scheduler kernel parameters
        Parameters:
        ---------------------------------------------------------------
        | IO Scheduler:                                               |
        --------------------------------------------------------------- 
        1. CFQ
        2. NOOP           
        """
        if io_sched_param=="cfq":
            os.system ("echo cfq > /sys/block/mmcblk0/queue/scheduler")
        if io_sched_param=="noop":
            os.system ("echo cfq > /sys/block/mmcblk0/queue/scheduler")
    
    def tune_task_scheduler_parameters():
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
    
    def tune_block_device_parameters():
        """This function is used to tune block device kernel parameters
        """
        print "tune block device params"
    
    def tune_network_parameters():
        """This function is used to tune io network kernel parameters
        """
        print "tune network params"
    
    def tune_memory_subsystem_parameters():
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
        print "tune memory subsystem params"





























