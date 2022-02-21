import os 
import sys
import subprocess
import traceback

class ConfigParams(object):
    """This class is used to create different confiuration space for jetson  tx1
    """
    def __init__(self, cfg, cur_config, cur_sys, 
                 big_cores, columns):     
        print("[STATUS]: Initializing ConfigParams Class")
        self.cfg = cfg
        self.cur_config = cur_config
        self.cur_sys = cur_sys
        self.big_cores = big_cores
        self.columns = columns 
        # define constant variables
        self.ENABLE = "1"
        self.DISABLE = "0"
        # set specific configuration    
        self.set_big_core_status(self.cfg["systems"][self.cur_sys]["cpu"]["cores"]["core1"],self.cur_config[self.columns.index("core1_status")])
        self.set_big_core_status(self.cfg["systems"][self.cur_sys]["cpu"]["cores"]["core2"],self.cur_config[self.columns.index("core2_status")])
        self.set_big_core_status(self.cfg["systems"][self.cur_sys]["cpu"]["cores"]["core3"],self.cur_config[self.columns.index("core3_status")])
        self.set_big_core_freq(self.cfg["systems"][self.cur_sys]["cpu"]["cores"]["core0"],self.cur_config[self.columns.index("core_freq")])   
        self.set_gpu_freq(self.cur_config[self.columns.index("gpu_freq")])     
        self.set_emc_freq(self.cur_config[self.columns.index("emc_freq")])
        self.set_scheduler_policy(self.cur_config[self.columns.index("scheduler.policy")])
        self.set_cache_pressure(self.cur_config[self.columns.index("vm.vfs_cache_pressure")])
        self.set_swappiness(self.cur_config[self.columns.index("vm.swappiness")])
        self.set_dirty_bg_ratio(self.cur_config[self.columns.index("vm.dirty_background_ratio")])
        self.set_dirty_ratio(self.cur_config[self.columns.index("vm.dirty_ratio")])
        self.set_drop_caches(self.cur_config[self.columns.index("vm.drop_caches")])
        self.set_sched_rt_runtime_us(self.cur_config[self.columns.index("kernel.sched_rt_runtime_us")])
        self.set_sched_child_runs_first(self.cur_config[self.columns.index("kernel.sched_child_runs_first")])
        self.set_overcommit_memory(self.cur_config[self.columns.index("vm.overcommit_memory")])
        self.set_overcommit_ratio(self.cur_config[self.columns.index("vm.overcommit_ratio")])
    
    def set_big_core_status(self, cpu_name, status):
        """This function is used set core status (enable or disable)
        @input:
             cpu_name: cpu that will be enabled or disabled
        @returns:
        boolean: whether the operation was successful or not  
        """
        if cpu_name!="cpu0":
            filename="{0}{1}{2}".format("/sys/devices/system/cpu/",
                                       cpu_name,
                                       "/online"
                                       )
            cur_status=subprocess.getstatusoutput("cat {0}".format(filename))[1]   
            if cur_status!=status:
                res=subprocess.call(["sudo","sh","./utils/change_core_status.sh",str(cpu_name),str(status)])
                if res!=0:
                    err="subprocess command failed"
                    print("[CPU STATUS ERROR]: {0}".format(err))
                    return False
                # check if the operation is successful
                new_status= subprocess.getstatusoutput("cat {0}".format(filename))[1]
                if new_status!=status:
                    print ("[CPU STATUS ERROR]: "+cpu_name+ "\n"
                                       "expected: " + str(status) + "\n"
                                       "actual: "+ str(new_status))
                    return False
                return True
        else:
            print("invalid cpu_name argument")

    def set_big_core_freq(self, cpu_name, frequency):
        """This function is used to set core frequency of one or more cores
        @input:
            frequency: clockspeed at what the cpu will be set 
            cpu_name: cpu number which will be set
        @returns:
            @returns:
            boolean: status of operation
        """
        frequency = int(frequency)
        if frequency is not None:
            filename="{0}{1}{2}".format("/sys/devices/system/cpu/",
                                        cpu_name,
                                        "/cpufreq/scaling_cur_freq")
            
            cur_freq=subprocess.getstatusoutput("cat {0}".format(filename))[1]
            res=subprocess.call(["sudo","sh","./utils/change_core_frequency.sh",str(self.cur_sys),str(frequency),str(cur_freq)])
            if res!=0:
                    err=traceback.print_exc()
                    print("[CPU FREQUENCY ERROR]: {0}".format(err))
                    return False
            
            new_freq=subprocess.getstatusoutput("cat {0}".format(filename))[1]
            if str(new_freq)!=str(frequency):
                print ("[CPU FREQUENCY ERROR]: "+cpu_name+ "\n"
                                   "expected: " + str(frequency) + "\n"
                                   "actual: "+ str(new_freq))
                return False 

            return True  
   
    def set_gpu_freq(self, frequency):
        """This function is used to change gpu clockspeeds
        @input:
           frequency: the clockspeed at which the gpu will be set
        @returns:
            boolean: status of operation
        """
        frequency = int(frequency)
        if frequency is not None:
            filename=self.cfg["systems"][self.cur_sys]["gpu"]["frequency"]["current"]
            try:
                if frequency is not None:
                    cur_freq=subprocess.getstatusoutput("cat {0}".format(filename))[1]
                    res=subprocess.call(["sudo","sh","./utils/change_gpu_frequency.sh",str(self.cur_sys),str(frequency),str(cur_freq)])
                    if res!=0:
                        err=traceback.print_exc()
                        print("[GPU FREQUENCY ERROR]: {0}".format(err))
                        return False
                           
                    # check if the operation is successful 
                    new_freq=subprocess.getstatusoutput("cat {0}".format(filename))[1]
                    if new_freq!=frequency:
                        print ("[GPU FREQUENCY ERROR]: \n"
                                           "expected: " + str(frequency) + "\n"
                                           "actual: "+ str(new_freq))
                        return False

                    return True
            except AttributeError as e:
                print("[GPU FREQUENCY ERROR: {0}]".format(e)) 
      
    def set_emc_freq(self, frequency):
        """This function is used to change emmc clockspeeds
        @input:
            frequency: the clockspeed at which the emmc will be set
        @returns:
            boolean: status of operation
        """
        #print ("emc frequency")
        frequency = int(frequency)
        if frequency is not None:
            filename=self.cfg["systems"][self.cur_sys]["emc"]["frequency"]["current"]
            try:
                if frequency is not None:
                    cur_freq=subprocess.getstatusoutput("cat {0}".format(filename))[1]
                    
                    res=subprocess.call(["sudo","sh","./utils/change_emc_frequency.sh",str(self.cur_sys),str(frequency)])
                    if res!=0:
                        err=traceback.print_exc()
                        print("[EMC FREQUENCY ERROR]: {0}".format(err))
                        return False
            
                    # check if the operation is successful 
                    new_freq=subprocess.getstatusoutput("cat {0}".format(filename))[1]
                    if new_freq!=frequency:
                        print ("[EMC FREQUENCY ERROR]: \n"
                                           "expected: " + str(frequency) + "\n"
                                           "actual: "+ str(new_freq))
                        return False

                    return True
            except AttributeError as e:
                print("[EMC FREQUENCY ERROR: {0}]".format(e))
        
    def set_scheduler_policy(self, val):

        """"This function is used to set scheduler policy"""
        if val==0: os.system ("echo cfq > /sys/block/mmcblk0/queue/scheduler")
        elif val==1: os.system ("echo noop > /sys/block/mmcblk0/queue/scheduler")
        else: print("[ERROR]: Invalid policy value")
    
    def set_cache_pressure(self, val):
        """This function is used to set cache pressure"""
        os.system ("sysctl vm.vfs_cache_pressure={0}".format(val))

    def set_swappiness(self, val):
        """This function is used to set swappiness value"""
        os.system ("sysctl vm.swappiness={0}".format(val))

    def set_dirty_bg_ratio(self, val):
        """This function is used to set dirty bg value"""
        os.system ("sysctl vm.dirty_background_ratio={0}".format(val))
    
    def set_dirty_ratio(self, val):
        """This function is used to set dirty ratio value"""
        os.system ("sysctl vm.dirty_ratio={0}".format(val))

    def set_drop_caches(self, val):
        """This function is used to set drop caches value"""
        os.system ("sysctl vm.drop_caches={0}".format(val))

    def set_sched_child_runs_first(self, val):
        """This function is used to set kernel.sched child runs first value"""
        os.system ("sysctl kernel.sched_child_runs_first={0}".format(val))
    
    def set_sched_rt_runtime_us(self, val):
        """This function is used to set sched rt runtime us value"""
        os.system ("sysctl kernel.sched_rt_runtime_us={0}".format(val))

    def set_nr_hugepages(self, val):
        """This function is used to set nr hugepages value"""
        os.system ("sysctl vm.nr_hugepages={0}".format(val))
    
    def set_overcommit_ratio(self, val):
        """This function is used to set overcommit ratio value"""
        os.system ("sysctl vm.overcommit_ratio={0}".format(val))

    def set_overcommit_memory(self, val):
        """This function is used to set overcommit memory value"""
        os.system ("sysctl vm.overcommit_memory={0}".format(val))

    def set_overcommit_hugepages(self, val):
        """This function is used to set overcommit hugepages value"""
        os.system ("sysctl vm.overcommit_hugepages={0}".format(val))

    def set_max_pids(self, val):
        """This function is used to set max pids value"""
        os.system ("sysctl user.max_pid_namespaces={0}".format(val))
    
    def set_sched_nr_migrate(self, val):
        """This function is used to set sched nr migrate value"""
        os.system ("sysctl kernel.sched_nr_migrate={0}".format(val))


    def set_sched_time_avg_ms(self, val):
        """This function is used to set sched nr migrate value"""
        os.system ("sysctl kernel.sched_time_avg_ms={0}".format(val))

    def set_cpu_time_max_percent(self, val):
        """This function is used to set cpu time max percent value"""
        os.system ("sysctl kernel.cpu_time_max_percent={0}".format(val))


    
    

