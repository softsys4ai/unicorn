import sys
import pandas as pd
import pydot
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
    try:
        graph=CausalGraphicalModel(nodes=nodes, edges=edges)
        graph.draw().render(filename=fname)
    except AssertionError:
        print ("[ERROR]: cycles in NOTEARS dag")
        print("Edges: {0}".format(edges))

def learn_tetrad(df, fname):
    """This function is used to learn model using tetrad runner"""
    from pycausal.pycausal import pycausal as pc
    from pycausal import search as s
    pc=pc()
    pc.start_vm()
    tetrad=s.tetradrunner()
    tetrad.getAlgorithmParameters(algoId = 'fci', testId = 'fisher-z-test')
    tetrad.run(algoId = 'fci', dfs = df, testId = 'fisher-z-test', 
               depth = -1, maxPathLength = -1, completeRuleSetUsed = False, 
               verbose = True)
    
    dot_str = pc.tetradGraphToDot(tetrad.getTetradGraph())
    graph = pydot.graph_from_dot_data(dot_str)
    graph[0].write_pdf(fname) 

if __name__=="__main__":
   
    # get data 
    df=pd.read_csv(sys.argv[1])
    columns = ["core_freq", "gpu_freq", "emc_freq","inference_time",
               "scheduler.policy","vm.swappiness","total_energy_consumption", 
               "cpu_utilization","migrations","context-switches",
               "cache-misses","cache-references","branch-misses",
               "branch-load-misses"]
    print (df.columns)
    df=df[columns]
    
    options = ["core_freq", "gpu_freq", "emc_freq",
               "scheduler.policy", "vm.swappiness"] 
    objectives = ["total_energy_consumption", "inference_time"]
    # edge constraints
    tabu_edges = get_tabu_edges(columns, options, objectives)
    # causal model hyperparmas
    thres = 0.05 # between 0 and 1
    sm=from_pandas(df,tabu_edges=tabu_edges,w_threshold=thres)
    #bn = BayesianNetwork(sm)
    # save causal graph 
    fname = str(sys.argv[2])+ "_" + str(sys.argv[3])
    visualize (columns, sm.edges, fname+"_nt.pdf")
    learn_tetrad(df, fname+"_t.pdf")
    
    






    
