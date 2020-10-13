from Configuration import Config as cfg
from multiprocessing import Process
from apscheduler.schedulers.background import BackgroundScheduler

import os 
import sys
import subprocess
import time
import json
import requests
import numpy as np

class ComputePerformance(object):
    """This function is used to compute cpu, gpu and total power and measure inference time"""
    def __init__(self):
        print ("[STATUS]: Initializing Compute Performance Class")
        self.cur_sys = self.get_sys_name()
        self.url = 'http://localhost:5000/api'
        self.total_power = list()
        self.gpu_power = list()
        self.cpu_power = list()
        self.total_temp = list()
        self.gpu_temp = list()
        self.cpu_temp = list()
        
        # create scheduler
        job_defaults = {"coalesce":False,
                         "max_instances":2
        }
        self.sched=BackgroundScheduler(job_defaults=job_defaults)
        # add background job
        self.sched.start()
        self.sched.add_job(self.compute_power,"interval",seconds=0.5)
        self.sched.add_job(self.compute_temp,"interval",seconds=0.5)        
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
        sys_id=subprocess.getstatusoutput("cat {}".format(str(cfg.sys_id_file)))[1]
        sys_name=cfg.sys_id_dict[sys_id]
        return sys_name         
    
    def compute_power(self):
        """This function is used to read power consumption using from INA monitor 
        """
        tot=cfg.systems[self.cur_sys]["power"]["total"]
        gpu=cfg.systems[self.cur_sys]["power"]["gpu"]
        cpu=cfg.systems[self.cur_sys]["power"]["cpu"]
        try:
            
            self.total_power.append(subprocess.getstatusoutput("cat {0}".format(tot))[1])
            self.gpu_power.append(subprocess.getstatusoutput("cat {0}".format(gpu))[1])
            self.cpu_power.append(subprocess.getstatusoutput("cat {0}".format(cpu))[1])
        except AttributeError:
            print("[ERROR]: invalid power file ")
    
    def compute_temp(self):
        """This function is used to read power consumption using from INA monitor 
        """
        tot=cfg.systems[self.cur_sys]["temperature"]["total"]
        gpu=cfg.systems[self.cur_sys]["temperature"]["gpu"]
        cpu=cfg.systems[self.cur_sys]["temperature"]["cpu"]
        #try:
            
        self.total_temp.append(subprocess.getstatusoutput("cat {0}".format(tot))[1])
        self.gpu_temp.append(subprocess.getstatusoutput("cat {0}".format(gpu))[1])
        self.cpu_temp.append(subprocess.getstatusoutput("cat {0}".format(cpu))[1])
            
        #except AttributeError:
        #    print("[ERROR]: invalid temperature file ")
    
    def compute_inference_time(self):
        """This function is used to compute inference time
        """
        
        r=requests.post(self.url,json={'connect':'yes',})             
        duration= json.loads(r.json())     
        return duration["time"]         
        
    
    def store_output_metrics(self):
        """This file is used to return output data 
        """
        # total power
        self.total_power=[int(i) if i is not None else 0 for i in self.total_power]    
        self.total_power=np.sum(self.total_power)
        # gpu power
        self.gpu_power=[int(i) if i is not None else 0 for i in self.gpu_power]    
        self.gpu_power=np.sum(self.gpu_power)
        # cpu power
        self.cpu_power=[int(i) if i is not None else 0 for i in self.cpu_power]    
        self.cpu_power=np.sum(self.cpu_power)
        
        # total temp
        self.total_temp=[int(i) if i is not None else 0 for i in self.total_temp]    
        self.total_temp=np.mean(self.total_temp)
        # gpu temp
        self.gpu_temp=[int(i) if i is not None else 0 for i in self.gpu_temp]    
        self.gpu_temp=np.mean(self.gpu_temp)
        # cpu temp
        self.cpu_temp=[int(i) if i is not None else 0 for i in self.cpu_temp]    
        self.cpu_temp=np.mean(self.cpu_temp)
        
        # output
        output={'cur_total_power' : int(self.total_power),
                'cur_gpu_power' :  int(self.gpu_power),
                'cur_cpu_power' : int(self.cpu_power),
                'cur_inference' : float(self.inference_time),
                'cur_total_temp' : float(self.total_temp),
                'cur_gpu_temp' : float(self.gpu_temp),
                'cur_cpu_temp' : float(self.cpu_temp)}
        with open('measurement','w') as f:
            json.dump(output, f)

if __name__=="__main__":
    ComputePerformance()
        
        
          
