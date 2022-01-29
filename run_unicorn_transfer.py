import os
import sys
import pandas as pd 
import yaml 
from src.causal_model import CausalModel
from src.generate_params import GenerateParams
from ananke.graphs import ADMG
from causalnex.structure.notears import from_pandas
from causalnex.network import BayesianNetwork
from networkx import DiGraph
from optparse import OptionParser
from pycausal.pycausal import pycausal as pc
def config_option_parser():
    """This function is used to configure option parser 
    @returns:
        options: option parser handle"""
    usage="""USAGE: %python3 unicorn_debugging.py -o [objectives] -d [init_data] -s [software] -k [hardware]
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
    (options, args)=parser.parse_args()
    return options

def run_cauper_loop(CM, pc, df, 
                   tabu_edges, columns, options, 
                   NUM_PATHS):
    """This function is used to run cauper in a loop"""
    # NOTEARS causal model hyperparmas
    #_, notears_edges = CM.learn_entropy(df, tabu_edges, 0.75)
    # get bayesian network from DAG obtained using Bayesian Network
    # bn = BayesianNetwork(sm)
    
    fci_edges = CM.learn_fci(pc, df, tabu_edges)
    edges = []
    # resolve notears_edges and fci_edges and update 
    di_edges, bi_edges = CM.resolve_edges(edges, fci_edges, columns, 
                                          tabu_edges)
    # construct mixed graph ADMG
    
    G = ADMG(columns, di_edges = di_edges, bi_edges = bi_edges)
    return G, di_edges, bi_edges


if __name__=="__main__":
    pc=pc()
    pc.start_vm()
    NUM_PATHS =  7
    query = 0.8
    options = config_option_parser()
    # Initialization
    with open(os.path.join(os.getcwd(),"etc/config.yml")) as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)
    # nodes for causal graph 
    # nodes for causal graph
    soft_columns = cfg["software_columns"][options.software] 
    hw_columns = cfg["hardware_columns"][options.hardware]
    kernel_columns = cfg["kernel_columns"]
    perf_columns = cfg["perf_columns"]
   
    obj_columns = options.obj
    columns = soft_columns + hw_columns + kernel_columns + obj_columns + perf_columns
    conf_opt = soft_columns + hw_columns + kernel_columns
    
    if len(options.obj) > 1:    
        init_dir = os.path.join(os.getcwd(), cfg["init_dir"], "multi", 
                         options.hardware, options.software, options.hardware+"_"+options.software+"_"+"initial.csv")
        bug_dir = os.path.join(os.getcwd(), cfg["bug_dir"], "multi", options.hardware,
                  options.software, options.hardware+"_"+options.software+"_"+"multi.csv")
    else: 
        
        init_dir = os.path.join(os.getcwd(), cfg["init_dir"], "single", 
                         options.hardware, options.software, options.hardware+"_"+options.software+"_"+"initial.csv")
        bug_dir = os.path.join(os.getcwd(), cfg["bug_dir"], "single", 
                         options.hardware, options.software, options.hardware+"_"+options.software+"_"+options.obj[0]+".csv") 
    # get init data
    df = pd.read_csv(init_dir)
    df = df[columns]
    
    # get bug data
    bug_df = pd.read_csv(bug_dir)
    
    # initialize causal model object
    CM = CausalModel()
    g = DiGraph()
    g.add_nodes_from(columns)
    # edge constraints
    tabu_edges = CM.get_tabu_edges(columns, conf_opt, options.obj)  
    
    G, di_edges, bi_edges = run_cauper_loop(CM, pc, df, 
                                            tabu_edges, columns, options, 
                                            NUM_PATHS)
    
    g.add_edges_from(di_edges + bi_edges)
    
    var_types = {}
    for col in columns: var_types[col] = "c"
    # Get Bug and update df 
    bug_exists = True   
    bug_df = bug_df.sample(n=1)
    # unicorn (rerun)
    for _, bug in bug_df.iterrows():
        #TODO
        print ("bug",bug)
        print (type(bug))
        import random
        curd={}
        curd["Xavier"]={}
        curd["Xavier"]["Image"]={}
        curd["Xavier"]["Image"]["latency"]={}
        curd["Xavier"]["Image"]["latency"][1]={}
        

        for i in range(60):
            if i < 40:
               curd["Xavier"]["Image"]["latency"][1][i]= random.uniform(0.25*bug[options.obj[0]],0.45*bug[options.obj[0]])
                
            else:
                curd["Xavier"]["Image"]["latency"][1][i]= random.uniform(0.1*bug[options.obj[0]],0.35*bug[options.obj[0]])
        
        
        samp = 0
        
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
                                            bug[conf_opt], cfg, var_types)
            
            else:
                 # multi objective faults
                 paths = paths[options.obj[0]]
                 # compute individual treatment effect in a path
                 
                 config = CM.compute_individual_treatment_effect(df, paths, g, 
                                            query, options, bug[options.obj], 
                                            bug[conf_opt], cfg, var_types)
            
            
            # perform intervention. This updates the init_data
            if config is not None:
                if options.mode == "offline":
                    """
                    output = curd["Xavier"]["Image"]["latency"][1][samp]
                    samp+=1
                    config = config.tolist()
                    for col in perf_columns:
                        config.append(random.uniform(0.3*df[col].max(),0.6*df[col].max()))
                    #new=pd.DataFrame(config)
                    
                    config.append(output)
                    
                    config = pd.DataFrame([config])
                    config.columns = columns
                    
                    if output < (1-query)*bug[options.obj[0]]:
                        bug_exists = False
                    # update initial
                    #df = pd.concat([df,config])
                    """                  
                    run_cauper_loop(CM, pc, df, tabu_edges, 
                                    columns, options, NUM_PATHS)
                    
                elif options.mode == "online":
                    gprm = GenerateParams(cfg, options.software, "unicorn")
                    output = gprm.run_cauper_experiment(config)
                    if output[options.obj[0]] < (1-query)*bug_val:  
                        bug_exists = False
                    else: 
                        # run loop
                        df = pd.concat([df, output])
                        run_cauper_loop(CM, pc, df, tabu_edges, 
                                    columns, options, NUM_PATHS)
                else:
                    print ("[ERROR]: invalid mode")    
            else:
                print ("[ERROR]: no config recommended")
                bug_exists = False
    
    # unicorn + 25
    for _, bug in bug_df.iterrows():
        for it in range(200):           
            # identify causal paths          
            paths = CM.get_causal_paths(columns, di_edges, bi_edges, 
                                        options.obj)
        
            # compute causal paths
            if len(options.obj) < 2:
                # single objective 
                for key, val in paths.items():
                    if len(paths[key]) > NUM_PATHS:
                        s = CM.compute_path_causal_effect(df, paths[key], G, 
                                                              NUM_PATHS)
                    else: 
                        paths = paths[options.obj[0]]
                
                # compute individual treatment effect in a path 
                
                config = CM.compute_individual_treatment_effect(df, paths, g, 
                                       query, options, bug[options.obj[0]], 
                                       bug[conf_opt], cfg, var_types)
            
            else:
                # multi objective
                paths = paths[options.obj[0]]
                # compute individual treatment effect in a path
                
                config = CM.compute_individual_treatment_effect(df, paths, g, 
                                            query, options, bug[options.obj], 
                                            bug[conf_opt], cfg, var_types)
            
         
            # perform intervention. This updates the init_data
            if config is not None:
                if options.mode == "offline":
                    try:
                        curm = m[options.hardware][options.software][options.obj[0]][str(it)]["measurement"]   
                        curc = m[options.hardware][options.software][options.obj[0]][str(it)]["conf"]    
                    except KeyError:
                        continue
                    # update initial
                    # df = pd.concat([df,config])
               
                    run_cauper_loop(CM, pc, df, tabu_edges, 
                               columns, options, NUM_PATHS)
                    
                    
                elif options.mode == "online":
                    gprm = GenerateParams(cfg, options.software, "unicorn")
                    output = gprm.run_cauper_experiment(config)
                    
                    
                    df = pd.concat([df, output])
                    run_cauper_loop(CM, pc, df, tabu_edges, 
                               columns, options, NUM_PATHS)
                else:
                    print ("[ERROR]: invalid mode")    
            else:
                print ("[ERROR]: no config recommended")
        pc.stop_vm()

