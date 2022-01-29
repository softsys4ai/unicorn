import random 
import json
import pandas as pd
import numpy as np
import json
import yaml
import copy
random.seed(28)
en_df=pd.read_csv("Xavier_Image_total_energy_consumption.csv")
ref_df = pd.read_csv("Xavier_ref.csv")

with open("config.yml") as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)
curd={}
curd["Xavier"]={}
curd["Xavier"]["Image"]={}
curd["Xavier"]["Image"]["total_energy_consumption"]={}
perf_configs=cfg["perf_columns"]

bug_id = 0
for _,bug in en_df.iterrows():
    samples = random.randint(21,36)
    curd["Xavier"]["Image"]["total_energy_consumption"][bug_id]={}
    val = [int(random.uniform(0.28,0.6)*bug["total_energy_consumption"]) for j in range(samples-1)]
    val.append(int(random.uniform(0.13,0.2)*bug["total_energy_consumption"]))
    for i in range(samples):  
            
            curd["Xavier"]["Image"]["total_energy_consumption"][bug_id][i]={}
            curd["Xavier"]["Image"]["total_energy_consumption"][bug_id][i]["measurement"] =val[i]
            cur_l=[]
            for col in perf_configs:
                max_cur = ref_df[col].max()
                if val[i] < 0.35*bug["total_energy_consumption"]:
                    cur_l.append (int(random.uniform(0.2*max_cur, 0.4*max_cur)))
                else:
                    cur_l.append (int(random.uniform(0.35*max_cur, 0.7*max_cur)))
            curd["Xavier"]["Image"]["total_energy_consumption"][bug_id][i]["conf"]=copy.deepcopy(cur_l)
    """
    print ("+++++")
    print (val)
    print (len(val))
    print (bug_id)  
    print ((bug["total_energy_consumption"]-val[-1])/bug["total_energy_consumption"])
    """
    bug_id+=1
      
    print (curd["Xavier"]["Image"]["total_energy_consumption"][0])
    #bug_id +=1
with open("measurement.json", "w") as outfile:
    json.dump(curd, outfile)


                
        
