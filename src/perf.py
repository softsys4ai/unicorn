import os
import sys
import re
import json
import pandas as pd 

class Perf:
    """This class is used to perform Perf parsing"""
    def __init__(self, cfg, options):
        print ('[STATUS]: Initializing Perf Class')
        self.VALUE = 0
        self.EVENT = 1
        self.cfg = cfg
        self.options = options
        if len(self.options.obj) < 2:
            with open(os.path.join(os.getcwd(), cfg["debug_dir"], "single", options.hardware,
                      options.software, "measurement.json")) as mfl:
                self.m = json.load(mfl)
            self.f = os.path.join(os.getcwd(),"data","measurement","current","measurement.json")
        # events with name change
        self.map = {"sched_sched_wakeup_new": "sched:sched_wakeup_new", 
                    "sched_sched_wakeup": "sched:sched_wakeup", 
                    "sched_sched_switch": "sched:sched_switch", 
                    "sched_sched_stat_runtime": "sched:sched_stat_runtime", 
                    "sched_sched_process_wait": "sched:sched_process_wait",
                    "sched_sched_load_avg_cpu": "sched:sched_load_avg_cpu",
                    "sched_sched_overutilized": "sched:sched_overutilized",
                    "raw_syscalls_sys_enter": "raw_syscalls:sys_enter",
                    "raw_syscalls_sys_exit": "raw_syscalls:sys_exit",
                    }
    
    def parse_perf(self, dev_trg, count):
        """This function is used to parse perf line by line"""       
        output=list()
        with open ('cur','r') as f:
            for line in f:
                output.append(line.split(' '))
        output=output[5:]
        output.pop()
        output.pop()
        output.pop()
        processed_output=[[] for _ in range(len(output))]
        perf_output={}
        for line in range(len(output)):
            for elem in output[line]:
                if elem!='':
                    processed_output[line].append(elem)
        for line in processed_output:
            if len(line) > 2:
                perf_output[line[self.EVENT]]=[line[self.VALUE]]
             
        pdf = pd.DataFrame(perf_output)
        # process perf df 
        columns = list(pdf)
        pdf[columns] = pdf[columns].replace({',':''}, regex = True)
        pdf[columns] = pdf[columns].astype(float)
        # convert columns to json readable format
        perf_columns = self.cfg["perf_columns"]
        df = pd.DataFrame(columns = perf_columns)
        with open(self.f,'r') as f:
                        data = json.load(f)

        curm = self.m[self.options.hardware][self.options.software][self.options.obj[0]][str(dev_trg)][str(count)]["measurement"]
        curc = self.m[self.options.hardware][self.options.software][self.options.obj[0]][str(dev_trg)][str(count)]["conf"]
        for col in perf_columns:
            try:
                df[col]=pdf[col]
            except KeyError:
                df[col]=pdf[self.map[col]]
         
        return curc, curm 



       
