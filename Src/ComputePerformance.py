#!/usr/bin/python

from Configuration import Config as cfg
from multiprocessing import Process
from apscheduler.schedulers.background import BackgroundScheduler

import os 
import sys
import commands
import time
import json
import logging
import requests
import numpy as np

class ComputePerformance(object):
    """This function is used to compute cpu,gpu and total power and measure inference time
    """
    def __init__(self):
        print ("[STATUS]: Initializing Compute Performance Class")
        logging.basicConfig()
        logging.getLogger("apscheduler").setLevel(logging.ERROR)
        self.cur_sys=self.get_sys_name()
        self.url='http://localhost:5000/api'
        self.total_power=list()
        
        # create scheduler
        job_defaults= {"coalesce":False,
                       "max_instances":1
        }
        self.sched=BackgroundScheduler(job_defaults=job_defaults)
        # add background job
        self.sched.start()
        self.sched.add_job(self.compute_power,"interval",seconds=.01)       
        # start        
        self.inference_time=self.compute_inference_time()
        # end
        self.sched.shutdown()
        self.store_output_metrics()
    
    def get_sys_name(self):
        """This function is used to determine the system id
        @returns: 
            sys_name: TX1/TX2/TK1
        """
        sys_id=commands.getstatusoutput("cat {}".format(str(cfg.sys_id_file)))[1]
        sys_name=cfg.sys_id_dict[sys_id]
        return sys_name         
    
    def compute_power(self):
        """This function is used to read power consumption using from INA monitor 
        """
        filename=cfg.systems[self.cur_sys]["power"]["total"]
        try:
            
            self.total_power.append(commands.getstatusoutput("cat {0}".format(filename))[1])
        except AttributeError:
            self.logger.error("[ERROR]: invalid power file ")
    
    def compute_inference_time(self):
        """This function is used to compute inference time
        """
        
        r=requests.post(self.url,json={'connect':'yes',})             
        duration= json.loads(r.json())     
        return duration["time"]         
        
    
    def store_output_metrics(self):
        """This file is used to return output data 
        """
        
        self.total_power=[int(i) if i is not None else 0 for i in self.total_power ]    
        self.total_power=np.sum(self.total_power)
        output={'cur_power':self.total_power,
                'cur_inferenece':self.inference_time}
        
        with open('measurement','w') as f:
            json.dump(output,f)

if __name__=="__main__":
    ComputePerformance()
        
        
          
