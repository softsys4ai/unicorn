import pandas as pd
from causalnex.structure.notears import from_pandas
from causalnex.network import BayesianNetwork
df=pd.read_csv("ir_tx1.csv")
df=df[["core_freq", "gpu_freq", "emc_freq","inference_time",
       "scheduler.policy","vm.swappiness","cpu_energy_consumption", 
       "cpu_utilization","migrations","context-switches",
       "cache-misses","cache-references","branch-misses",
       "branch-load-misses"]]
if __name__=="__main__":

   sm=from_pandas(df,w_threshold=0.2)
   sm=sm.get_largest_subgraph()
   bn = BayesianNetwork(sm)
    
