import os
import sys
import pandas as pd 
import yaml
import json 
from src.causal_model import CausalModel
from src.generate_params import GenerateParams
from ananke.graphs import ADMG
from causalnex.structure.notears import from_pandas
from causalnex.network import BayesianNetwork
from networkx import DiGraph
from optparse import OptionParser
from pycausal.pycausal import pycausal 

def config_option_parser():
    """This function is used to configure option parser 
    @returns:
        options: option parser handle"""
    usage="""USAGE: %python3 run_unicorn_debug.py -o [objectives] -d [init_data] -s [software] -k [hardware] -m [mode] -i [bug_index]
    """
    parser=OptionParser(usage=usage)
    parser.add_option('-o', '--objective', dest='obj', 
                      default=[], nargs=1, type='choice', 
                      choices=('inference_time', 'total_energy_consumption', 'total_temp'), action='append', help="objective type")
    parser.add_option('-s', "--software", action="store",
                      type="string", dest="software", help="software")
    parser.add_option('-k', "--hardware", action="store",
                      type="string", dest="hardware", help="hardware")
    parser.add_option('-m', "--mode", action="store",
                      type="string", dest="mode", help="mode")
    parser.add_option('-i', "--bug_index", action="store",
                      type="string", dest="bug_index", help="bug_index")
    (options, args)=parser.parse_args()
    return options

def run_unicorn_loop(CM, df, 
                   tabu_edges, columns, options, 
                   NUM_PATHS):
    """This function is used to run unicorn in a loop"""
    # NOTEARS causal model hyperparmas
    #_, notears_edges = CM.learn_entropy(df, tabu_edges, 0.75)
    # get bayesian network from DAG obtained 
    # bn = BayesianNetwork(sm)
    
    fci_edges = CM.learn_fci(df, tabu_edges)
    edges = []
    # resolve notears_edges and fci_edges and update 
    di_edges, bi_edges = CM.resolve_edges(edges, fci_edges, columns, 
                                          tabu_edges, NUM_PATHS, options.obj)
    # construct mixed graph ADMG
    
    G = ADMG(columns, di_edges = di_edges, bi_edges = bi_edges)
    return G, di_edges, bi_edges

if __name__=="__main__":
    query = 0.8
    NUM_PATHS =  25
    
    options = config_option_parser()
    # Initialization
    with open(os.path.join(os.getcwd(),"etc/config.yml")) as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)
    
    # nodes for causal graph
    soft_columns = cfg["software_columns"][options.software] 
    hw_columns = cfg["hardware_columns"][options.hardware]
    kernel_columns = cfg["kernel_columns"]
    perf_columns = cfg["perf_columns"]
   
    obj_columns = options.obj
    columns = soft_columns + hw_columns + kernel_columns + perf_columns + obj_columns
    conf_opt = soft_columns + hw_columns + kernel_columns
    
    if len(options.obj) > 1:    
        init_dir = os.path.join(os.getcwd(), cfg["init_dir"], "multi", 
                         options.hardware, options.software, options.hardware+"_"+options.software+"_"+"initial.csv")
        bug_dir = os.path.join(os.getcwd(), cfg["bug_dir"], "multi", options.hardware,
                  options.software, options.hardware+"_"+options.software+"_"+"multi.csv")
        with open(os.path.join(os.getcwd(),cfg["debug_dir"],"multi", options.hardware,
                  options.software,"measurement.json")) as mfl:    
            m = json.load(mfl)
    else: 
        
        init_dir = os.path.join(os.getcwd(), cfg["init_dir"], "single", 
                         options.hardware, options.software, options.hardware+"_"+options.software+"_"+"initial.csv")
        bug_dir = os.path.join(os.getcwd(), cfg["bug_dir"], "single", 
                         options.hardware, options.software, options.hardware+"_"+options.software+"_"+options.obj[0]+".csv") 
        with open(os.path.join(os.getcwd(),cfg["debug_dir"],"single", options.hardware,
                  options.software,"measurement.json")) as mfl:    
            m = json.load(mfl)
    # get init data
    df = pd.read_csv(init_dir)
    df = df[columns]
    
    # get bug data
    bug_df = pd.read_csv(bug_dir)
    
    # initialize causal model object
    CM = CausalModel(columns)
    g = DiGraph()
    g.add_nodes_from(columns)
    # edge constraints
    tabu_edges = CM.get_tabu_edges(columns, conf_opt, options.obj)  
    
    G, di_edges, bi_edges = run_unicorn_loop(CM, df, 
                                            tabu_edges, columns, options, 
                                            NUM_PATHS)
    
    g.add_edges_from(di_edges + bi_edges)
    
    var_types = {}
    for col in columns: var_types[col] = "c"
    # Get Bug and update df 
    bug_exists = True   
    if options.bug_index:
        bug_df = bug_df.iloc[int(options.bug_index):int(options.bug_index)+1]
     
    for bug_id in range(len(bug_df)):
        bug = bug_df.loc[bug_id]
        bug_exists = True
        print ("--------------------------------------------------")
        print ("BUG ID: ", bug_id)
        print ("--------------------------------------------------")
        it = 0 
        previous_config = bug[conf_opt].copy()  
         
        while bug_exists:
            # identify causal paths
            
            paths = CM.get_causal_paths(columns, di_edges, bi_edges, 
                                        options.obj)
            
            # compute causal paths
            if len(options.obj) < 2:
                # single objective faults
                for key, val in paths.items():
                    if len(paths[key]) > NUM_PATHS:
                        paths = CM.compute_path_causal_effect(df, paths[key], G, 
                                                              NUM_PATHS)
                    else: 
                        paths = paths[options.obj[0]]
                
                # compute individual treatment effect in a path
        
                config = CM.compute_individual_treatment_effect(df, paths, g, 
                                            query, options, bug[options.obj[0]], 
                                            previous_config, cfg, var_types)
                 
            else:
                 # multi objective faults
                 paths = paths[options.obj[0]]
                 # compute individual treatment effect in a path
                 
                 config = CM.compute_individual_treatment_effect(df, paths, g, 
                                            query, options, bug[options.obj], 
                                            previous_config, cfg, var_types)
            
            
            # perform intervention. This updates the init_data
            if config is not None:
                if options.mode == "offline":
                    
                    curm = m[options.hardware][options.software][options.obj[0]][str(bug_id)][str(it)]["measurement"]
                    if curm < (1-query)*bug[options.obj[0]]:
                        bug_exists = False
                        print ("--------------------------------------------------")
                        print ("+++++++++++++++Recommended Fix++++++++++++++++++++")
                        print (config)
                        print ("Unicorn Fix Value", curm)
                        print ("Number of Samples Required", str(it))
                        print ("--------------------------------------------------")
                        
                        print ("--------------------------------------------------")
                        print ("+++++++++++++++++++++Bug++++++++++++++++++++++++++")
                        print (bug[conf_opt])
                        print ("Bug Objective Value", bug[options.obj[0]])
                        print ("--------------------------------------------------")
                    else:
                        curc = m[options.hardware][options.software][options.obj[0]][str(bug_id)][str(it)]["conf"]
                        print ("--------------------------------------------------")
                        print ("+++++++++++++++++++++Bug++++++++++++++++++++++++++")
                        print ("Recommended Config Objective Value", curm)
                        print ("--------------------------------------------------")
                        it += 1 
                        config = config.tolist()       
                        config.extend(curc)
                        config.extend([curm])
                        config = pd.DataFrame([config])
                        config.columns = columns                         
                        df = pd.concat([df,config],axis=0)
                        df=df[columns]
                        # previous_config
                        previous_config=config.squeeze()[conf_opt]
                        # update initial
                        run_unicorn_loop(CM, df, tabu_edges, 
                                    columns, options, NUM_PATHS)
                    
                elif options.mode == "online":
                    gprm = GenerateParams(cfg, options.software, "unicorn")
                    m_config = gprm.run_unicorn_experiment(config)
                    if m_config[m_config.obj[0]] < (1-query)*bug_val:  
                        bug_exists = False
                        
                    else: 
                        # run loop
                        df = pd.concat([df, output], axis=0)
                        run_unicorn_loop(CM, df, tabu_edges, 
                                    columns, options, NUM_PATHS)
                else:
                    print ("[ERROR]: invalid mode")    
            else:
                print ("[ERROR]: no config recommended")
                bug_exists = False
        
            
        
