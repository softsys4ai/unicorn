#!/usr/bin/python
import os 
import sys
import commands
import itertools 
import subprocess
import numpy as np
import pandas as pd

from Perf import Perf
from interruptingcow import timeout
from ConfigParams import ConfigParams 
from Configuration import Config as cfg
from TuneKernelParameters import TuneKernelParameters
from ComputePerformance import ComputePerformance

class GenerateParams(object):
    """This class is used to generate parameters for running inference
    """
    def __init__(self, 
                 logger,
                 exp_id):
        self.logger=logger
        self.logger.info("[STATUS]: Initializing GenerateParams Class")
        self.perf_obj=Perf()
        self.tkp=TuneKernelParameters()
        self.KERNEL_PARAMS=self.tkp.get_kernel_params()
        print self.KERNEL_PARAMS
        # constants
        self.ENABLE="1"
        self.DISABLE="0"
        self.NUM_TEST=5
        self.invalid_configs=[]
        # determine current system
        self.sys_name=self.get_sys_name()
        self.logger.info("[SYSTEM ID]: {0}".format(self.sys_name))
        
        # get list of big cores 
        self.big_cores=cfg.systems[self.sys_name]["cpu"]["cores"]
        try:
            if self.sys_name=="TX1":
                from TX1.Params import params
                self.params=params
                self.output_file=os.getcwd()+cfg.tx1_output_dir
                self.file_name_output=self.output_file+"output_"+".csv"
                self.file_name_conf=self.output_file+"output_conf_"+exp_id+".csv"
                self.file_name_invalid=self.output_file+"invalid_config_"+exp_id+".csv"
            
            elif self.sys_name=="TX2":
                from TX2.Params import params
                self.params=params
                self.output_file=os.getcwd()+cfg.tx2_output_dir
                self.file_name_output=self.output_file+"output_"+".csv"
                self.file_name_conf=self.output_file+"output_conf_"+exp_id+".csv"
                self.file_name_invalid=self.output_file+"invalid_config_"+exp_id+".csv"
             
            else:
                return
        
        except ImportError:
            # get big core frequencies 
            self.big_core_freqs=self.get_big_core_freqs()
            self.big_core_freqs = filter(None, self.big_core_freqs)
        
            # get gpu frequencies
            self.gpu_freqs=self.get_gpu_freqs()
            self.gpu_freqs=self.freq_conversion(self.gpu_freqs)
        
            # get emmc frequencies
            self.emc_freqs=self.get_emc_freqs()
            self.emc_freqs=self.freq_conversion(self.emc_freqs)
        
            # generate all possible combinations 
            self.generate_params_combination()
            self.get_valid_params()
        
            
        # output data for single config
        self.df=pd.DataFrame(columns=(
                                      "model_name",
                                      "sample",
                                      "size",
                                      "system_name",
                                      "config_name",
                                      "core0_status",
                                      "core1_status",
                                      "core2_status",
                                      "core3_status",
                                      "core_freq",
                                      "gpu_status",
                                      "gpu_freq",
                                      "emc_status",
                                      "emc_freq",              
                                      "inference_time",
                                      "power_consumption"))
        
        # output data for single config
        self.dfc=pd.DataFrame(columns=(
                                      "model_name",
                                      "sample",
                                      "size",
                                      "system_name",
                                      "config_name",
                                      "core0_status",
                                      "core1_status",
                                      "core2_status",
                                      "core3_status",
                                      "core_freq",
                                      "gpu_status",
                                      "gpu_freq",
                                      "emc_status",
                                      "emc_freq",   
                                      "mean_inference_time",
                                      "mean_power_consumption"))       
        # set config 
        for conf in xrange(0,len(self.params)):                             
            cur_conf=self.params[conf]
            cur_conf_name="{0}{1}".format("Config",conf)
            """
            ConfigParams(self.logger,
                         cur_conf,
                         self.sys_name,
                         self.big_cores)
            """
            # output param initialization
            cur_conf_inference_time=[ _ for _ in xrange(self.NUM_TEST)]
            cur_conf_power=[ _ for _ in xrange(self.NUM_TEST)]                            
            for iteration in xrange(self.NUM_TEST):
                os.system('/usr/src/linux-headers-4.4.38-tegra/tools/perf/perf stat -e block:*,ext4:*,sched:* -o cur python /home/nvidia/Shahriar/ASE2019/KernelConfig/Src/ComputePerformance.py')
                perf_output=self.perf_obj.parse_perf()    
                print perf_output   
            # build output dataframe
           
            break
                                  
        self.df.to_csv(self.file_name_output, header=False,mode="a")
        self.dfc.to_csv(self.file_name_conf, header=False, mode="a")
 
    def get_sys_name(self):
        """This function is used to determine the system id
        @returns: 
            sys_name: TX1/TX2/TK1
        """
        sys_id=commands.getstatusoutput("cat {}".format(str(cfg.sys_id_file)))[1]
        sys_name=cfg.sys_id_dict[sys_id]
        return sys_name
    
    def freq_conversion(self,array):
        """This function is is used to convert frequency from KHz to Hz
        @returns: 
            array: array where each element is converted to Hz from KHz 
        """
        if not array[-1].isdigit():
            array.pop()
            array=["{0}{1}".format(i,"000") for i in array]
        return array

    def get_big_core_freqs(self):
        """This function is used to get available frequencies for all the big cores
        @returns:
            freq: list of available frequencies for big cores
        """
        try:
            filename=cfg.systems[self.sys_name]["cpu"]["frequency"]["available"]
            freq=commands.getstatusoutput("cat {0}".format(filename))[1]
            if freq:
                freq=freq.split(" ")
                return freq
        except AttributeError:
            self.logger.error ("[ERROR]: big core frequency file does not exist")

    def get_gpu_freqs(self):
        """This function is used to get available gpu frequencies
        @returns:
            freq: list of available frequencies for gpus
        """
        try:
            filename=cfg.systems[self.sys_name]["gpu"]["frequency"]["available"]
            freq=commands.getstatusoutput("cat {0}".format(filename))[1]
            if freq:
                freq=freq.split(" ")
                return freq
        except AttributeError:
            self.logger.error ("[ERROR]: gbus frequency file does not exist")

    def get_emc_freqs(self):
        """This function is used to get available emmc frequencies
        @returns:
            freq: list of available frequencies for emmc controller
        """
        try:
            filename=cfg.systems[self.sys_name]["emc"]["frequency"]["available"]
            freq=commands.getstatusoutput("cat {0}".format(filename))[1]
            if freq:
                freq=freq.split(" ")
                return freq
        except AttributeError:
            self.logger.error ("[ERROR]: emc frequency file does not exist")
    
    def get_indices(self,l):
        """This function is used to generate indices for emc and gpu freqs
        """
        if l:
            n=len(l)
            x=n/3
            y=(2*n)/3
            return [0,x,y,n-1]
    
    def generate_params_combination(self):
        """This function is used to generate parameter combination. It assumes there are
        four cores from 0-3 and generates params accordingly. 
        """
        # cpu frequency and status
   
        core_status=dict()
        for key in self.big_cores.iterkeys():
            if key=="core0":
               core_status[key]=[self.ENABLE]
            else:
               core_status[key]=[self.ENABLE,self.DISABLE]
        core_frequency=self.big_core_freqs[:]
               
        # gpu status
        gpu_status=[self.ENABLE]    
        # emmc status 
        emc_status=[self.ENABLE]  
        # gpu max frequency
        #[a,b,c,d]=self.get_indices(self.gpu_freqs)
        gpu_freq=self.gpu_freqs[:]    
        #emc max frequency
        
        emc_freq=self.emc_freqs[:]
        
        """
        create configurable paramters set before permutation in a varibale named var
        index 0: core0 status
        index 1: core1 status 
        index 2: core2 status 
        index 3: core3 status 
        index 4: core frequency
        index 5,6: gpu status, gpu frequency 
        index 7,8: emc status, emc frequency  
        """
        status_var=[(self.ENABLE,self.DISABLE,self.DISABLE,self.DISABLE),
                    (self.ENABLE,self.DISABLE,self.DISABLE,self.ENABLE),
                    (self.ENABLE,self.DISABLE,self.ENABLE,self.DISABLE),
                    (self.ENABLE,self.DISABLE,self.ENABLE,self.ENABLE),
                    (self.ENABLE,self.ENABLE,self.DISABLE,self.DISABLE),
                    (self.ENABLE,self.ENABLE,self.DISABLE,self.ENABLE),
                    (self.ENABLE,self.ENABLE,self.ENABLE,self.DISABLE),
                    (self.ENABLE,self.ENABLE,self.ENABLE,self.ENABLE)
                    ]
        var=[
             core_frequency,
             gpu_status, 
             gpu_freq,
             emc_status, 
             emc_freq
        ]
        
        self.params=list(itertools.product(*var))
        self.params=list(itertools.product(status_var,self.params))
        for i in range(len(self.params)):
            self.params[i]=self.params[i][0]+self.params[i][1]
        print (self.params)
        
    def get_valid_params(self):
        """This function is used to extract the valid params from all the combination of params
        """
        # set frequency values to null when cpu/gpu/emmc is disabled
        for i in xrange(len(self.params)):
            self.params[i]=list(self.params[i])
            for j in range(5,len(self.params[i]),2):
                if self.params[i][j]==self.DISABLE:
                    self.params[i][j+1]=None

        # remove duplicates
        self.params.sort()
        self.params=list(self.params for self.params,_ in itertools.groupby(self.params))
        # save to a file for temporary use
        if self.sys_name=="TX1":
            params_file=cfg.tx1_config_file
        elif self.sys_name=="TX2":
            params_file=cfg.tx2_config_file
        else:
            self.logger.error("[ERROR]: invalid system name")
            return    
        filename=os.getcwd()+params_file
        with open(filename, "w") as f:
            f.write('params = %s' %self.params)
       
