#!/usr/bin/python
import os 
import sys
import commands
import subprocess
from Configuration import Config as cfg

class ConfigParams(object):
    """This class is used to create different confiuration space for jetson  tx1
    """
    def __init__(self,
                 logger,
                 cur_config,
                 cur_sys,
                 big_cores):
        
        self.logger=logger
        self.logger.info("[STATUS]: Initializing ConfigParams Class")
        self.cur_config=cur_config
        self.cur_sys=cur_sys
        self.big_cores=big_cores
        self.logger.info ("++Current Config: " + str(self.cur_config)+ "++")
        # define constant variables
        self.ENABLE="1"
        self.DISABLE="0"
        # set specific configuration
        
        
        self.set_big_core_status(cfg.systems[self.cur_sys]["cpu"]["cores"]["core1"],self.cur_config[1])
        self.set_big_core_status(cfg.systems[self.cur_sys]["cpu"]["cores"]["core2"],self.cur_config[2])
        self.set_big_core_status(cfg.systems[self.cur_sys]["cpu"]["cores"]["core3"],self.cur_config[3])
        self.set_big_core_freq(cfg.systems[self.cur_sys]["cpu"]["cores"]["core0"],self.cur_config[4])
        self.set_gpu_status(self.cur_config[5])
        self.set_gpu_freq(self.cur_config[6])
        self.set_emc_status(self.cur_config[7])
        self.set_emc_freq(self.cur_config[8])
                  
    def set_big_core_status(self,
                            cpu_name,
                            status):
        """This function is used set core status (enable or disable)
        @input:
             cpu_name: cpu that will be enabled or disabled
        @returns:
        boolean: whether the operation was successful or not  
        """
        #print("cpu status")
        if cpu_name!="cpu0":
            filename="{0}{1}{2}".format("/sys/devices/system/cpu/",
                                       cpu_name,
                                       "/online"
                                       )
            cur_status=commands.getstatusoutput("cat {0}".format(filename))[1]   
            if cur_status!=status:
                res=subprocess.call(["sudo","sh","./Utils/change_core_status.sh",str(cpu_name),str(status)])
                if res!=0:
                    err="subprocess command failed"
                    self.logger.error("[CPU STATUS ERROR]: {0}".format(err))
                    return False
                # check if the operation is successful
                new_status= commands.getstatusoutput("cat {0}".format(filename))[1]
                if new_status!=status:
                    self.logger.error ("[CPU STATUS ERROR]: "+cpu_name+ "\n"
                                       "expected: " + str(status) + "\n"
                                       "actual: "+ str(new_status))
                    return False
                return True
        else:
            self.logger.error("invalid cpu_name argument")

    def set_big_core_freq(self,
                          cpu_name,
                          frequency):
        """This function is used to set core frequency of one or more cores
        @input:
            frequency: clockspeed at what the cpu will be set 
            cpu_name: cpu number which will be set
        @returns:
            @returns:
            boolean: status of operation
        """
        #print ("cpu frequency")
        if frequency is not None:
            filename="{0}{1}{2}".format("/sys/devices/system/cpu/",
                                        cpu_name,
                                        "/cpufreq/scaling_cur_freq")
            
            cur_freq=commands.getstatusoutput("cat {0}".format(filename))[1]
            res=subprocess.call(["sudo","sh","./Utils/change_core_frequency.sh",str(self.cur_sys),str(frequency),str(cur_freq)])
            if res!=0:
                    err="subprocess command failed"
                    self.logger.error("[CPU FREQUENCY ERROR]: {0}".format(err))
                    return False
            
            new_freq=commands.getstatusoutput("cat {0}".format(filename))[1]
            if str(new_freq)!=str(frequency):
                self.logger.error ("[CPU FREQUENCY ERROR]: "+cpu_name+ "\n"
                                   "expected: " + str(frequency) + "\n"
                                   "actual: "+ str(new_freq))
                return False 

            return True  
       
    def set_gpu_status(self,
                       status):
        """This function is used to change gpu status
        @input:
            status: the status for gpu
        @returns:
            boolean: status of operation 
        """
        #print ("gpu status")
        filename=cfg.systems[self.cur_sys]["gpu"]["status"]
        try:
            cur_status=commands.getstatusoutput("cat {0}".format(filename))[1]
            if cur_status!=status:
                res=subprocess.call(["sudo","sh","./Utils/change_gpu_status.sh",str(self.cur_sys),str(status)])
                if res!=0:
                    err="subprocess command failed"
                    self.logger.error("[GPU STATUS ERROR]: {0}".format(err))
                    return False
            
                # check if the operation is successful 
                new_status=commands.getstatusoutput("cat {0}".format(filename))[1]
                if new_status!=status:
                    self.logger.error ("[GPU STATUS ERROR]: \n"
                                       "expected: " + str(status) + "\n"
                                       "actual: "+ str(new_status))
                    return False

                return True
        except AttributeError as e:
                self.logger.error("[GPU STATUS ERROR: {0}]".format(e)) 
    
        

    def set_gpu_freq(self,
                     frequency):
        """This function is used to change gpu clockspeeds
        @input:
           frequency: the clockspeed at which the gpu will be set
        @returns:
            boolean: status of operation
        """
        #print("gpu frequency")
        if frequency is not None:
            filename=cfg.systems[self.cur_sys]["gpu"]["frequency"]["current"]
            try:
                if frequency is not None:
                    cur_freq=commands.getstatusoutput("cat {0}".format(filename))[1]
                    res=subprocess.call(["sudo","sh","./Utils/change_gpu_frequency.sh",str(self.cur_sys),str(frequency),str(cur_freq)])
                    if res!=0:
                        err="subprocess command failed"
                        self.logger.error("[GPU FREQUENCY ERROR]: {0}".format(err))
                        return False
                           
                    # check if the operation is successful 
                    new_freq=commands.getstatusoutput("cat {0}".format(filename))[1]
                    if new_freq!=frequency:
                        self.logger.error ("[GPU FREQUENCY ERROR]: \n"
                                           "expected: " + str(frequency) + "\n"
                                           "actual: "+ str(new_freq))
                        return False

                    return True
            except AttributeError as e:
                self.logger.error("[GPU FREQUENCY ERROR: {0}]".format(e)) 
    
    def set_emc_status(self,
                       status):
        """This function is used to change emmc status
        @input:
            status: the status for emc
        @returns:
            boolean: status of operation 
        """
        #print ("emc status")
        filename=cfg.systems[self.cur_sys]["emc"]["status"]
        try:
            cur_status=commands.getstatusoutput("cat {0}".format(filename))[1]
            if cur_status!=status:
                res=subprocess.call(["sudo","sh","./Utils/change_emc_status.sh",str(self.cur_sys),str(status)])
                if res!=0:
                    err="subprocess command failed"
                    self.logger.error("[EMC STATUS ERROR]: {0}".format(err))
                    return False
            
                
                # check if the operation is successful 
                new_status=commands.getstatusoutput("cat "+filename)[1]
                if new_status!=status:
                    self.logger.error ("[EMC STATUS ERROR]: \n"
                                       "expected: " + str(status) + "\n"
                                       "actual: "+ str(status))
                    return False
   
                return True
        except AttributeError as e:
                self.logger.error("[EMC STATUS ERROR: {0}]".format(e))     

    def set_emc_freq(self,
                     frequency):
        """This function is used to change emmc clockspeeds
        @input:
            frequency: the clockspeed at which the emmc will be set
        @returns:
            boolean: status of operation
        """
        #print ("emc frequency")
        if frequency is not None:
            filename=cfg.systems[self.cur_sys]["emc"]["frequency"]["current"]
            try:
                if frequency is not None:
                    cur_freq=commands.getstatusoutput("cat {0}".format(filename))[1]
                    
                    res=subprocess.call(["sudo","sh","./Utils/change_emc_frequency.sh",str(self.cur_sys),str(frequency)])
                    if res!=0:
                        err="subprocess command failed"
                        self.logger.error("[EMC FREQUENCY ERROR]: {0}".format(err))
                        return False
            
                    # check if the operation is successful 
                    new_freq=commands.getstatusoutput("cat {0}".format(filename))[1]
                    if new_freq!=frequency:
                        self.logger.error ("[EMC FREQUENCY ERROR]: \n"
                                           "expected: " + str(frequency) + "\n"
                                           "actual: "+ str(new_freq))
                        return False

                    return True
            except AttributeError as e:
                self.logger.error("[EMC FREQUENCY ERROR: {0}]".format(e))

