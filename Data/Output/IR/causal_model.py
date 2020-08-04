import pandas as pd
from causalnex.structure.notears import from_pandas
from causalnex.network import BayesianNetwork

def get_tabu_edges(columns, options, objectives):
   """This function is used exclude edges which are not possible"""
   tabu_edges=[]
   # constraint on configuration options
   for opt in options:
       for cur_elem in columns:
           if cur_elem != opt:
               tabu_edges.append((cur_elem, opt))
        
   # constraints on performance objetcives  
   for obj in objectives:
       for cur_elem in columns:
           if cur_elem != obj:
               tabu_edges.append((obj, cur_elem))

   return tabu_edges 

def visualize(nodes, edges, fname):
    """This function is used to visualize the causal model using graphviz"""
    from causalgraphicalmodels import CausalGraphicalModel
    import graphviz

    graph=CausalGraphicalModel(nodes=nodes, edges=edges)
    graph.draw().render(filename=fname)



if __name__=="__main__":
   
    # get data 
    df=pd.read_csv("ir_xavier.csv")
    columns = ["core_freq", "gpu_freq", "emc_freq","inference_time",
               "scheduler.policy","vm.swappiness","total_energy_consumption", 
               "cpu_utilization","migrations","context-switches",
               "cache-misses","cache-references","branch-misses",
               "branch-load-misses"]
    df=df[columns]
    options = ["core_freq", "gpu_freq", "emc_freq",
               "scheduler.policy", "vm.swappiness"] 
    objectives = ["total_energy_consumption", "inference_time"]
    # edge constraints
    tabu_edges = get_tabu_edges(columns, options, objectives)
    # causal model hyperparmas
    thres = 0.05 # between 0 and 1
    sm=from_pandas(df,tabu_edges=tabu_edges,w_threshold=thres)
    print (sm.edges)
    #bn = BayesianNetwork(sm)
    # save causal graph 
    fname = "g.pdf"
    visualize (columns, sm.edges, fname)
    
    
