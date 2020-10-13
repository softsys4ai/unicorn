import sys
import pandas as pd 
from cadet.utils.config_parser import Config
from cadet.causal_model import CausalModel
from cadet.generate_params import GenerateParams
from ananke.graphs import ADMG
from causalnex.structure.notears import from_pandas
from causalnex.network import BayesianNetwork
from optparse import OptionParser

def config_option_parser():
    """
    This function is used to configure option parser 
    Returns
    -------
        options: option parser handle
    """
    
    usage = """
    USAGE: %python3 RunCausalModel.py -o [objectives] -d [init_data] -s [software] -k [hardware]
    """
    parser=OptionParser(usage=usage)
    parser.add_option('-o', '--objective', dest='obj', 
                      default=[], nargs=1, type='choice', 
                      choices=('inference_time', 'total_energy_consumption', 'total_temp'), action='append', help="objective type")
    parser.add_option('-d', "--data", action="store",
                      type="string", dest="init_data", help="init_data")
    parser.add_option('-s', "--software", action="store",
                      type="string", dest="software", help="software")
    parser.add_option('-k', "--hardware", action="store",
                      type="string", dest="hardware", help="hardware")
    (options, args)=parser.parse_args()
    return options

def run_cadet_loop(CM, df, tabu_edges, 
                   columns, options, NUM_PATHS):
    """
    This function is used to run cadet in a loop
    """
    # NOTEARS causal model hyperparmas
    _, notears_edges = CM.learn_notears(df, tabu_edges, 0.75)
    # get bayesian etowrk from DAG obtained by NOTEARS
    # bn = BayesianNetwork(sm)
    fci_edges = CM.learn_fci(df, tabu_edges)
    # resolve notears_edges and fci_edges and update 
    di_edges, bi_edges = CM.resolve_edges(notears_edges, fci_edges, columns, 
                                          tabu_edges)
    # construct mixed graph ADMG
    G = ADMG(columns, di_edges = di_edges, bi_edges = bi_edges)
    
if __name__=="__main__":
    cfg = Config("./etc/config.yml")
    cfg = cfg.load_config()
    NUM_PATHS =  cfg.num_paths
    query = cfg.query
    options = config_option_parser()
    # Initialization
    init_dir = cfg.init_dir 
    df = pd.read_csv(options.init_data)
    columns = ["core_freq", "gpu_freq", "emc_freq",
               "inference_time", "total_energy_consumption",
               "scheduler.policy","vm.swappiness", "cpu_utilization", 
               "migrations","context-switches", "cache-misses",
               "cache-references","branch-misses", "branch-load-misses", 
               "vm.vfs_cache_pressure", "vm.dirty_background_ratio"
               ]
    df = df[columns]
    
    conf_opt = ["core_freq", "gpu_freq", "emc_freq",
               "scheduler.policy", "vm.swappiness", "vm.vfs_cache_pressure",
               "vm.dirty_background_ratio"] 
    objectives = ["total_energy_consumption", "inference_time"]
    
    # initialize causal model object
    CM = CausalModel()
    # edge constraints
    tabu_edges = CM.get_tabu_edges(columns, conf_opt, objectives)
    # initialize
    run_cadet_loop(CM, df, tabu_edges, 
                    columns, options, NUM_PATHS)
    # Get Bug and update df 
    bug_dir = cfg.bug_dir
    bug_exists = True
    for bug in bug_dir
        while bug_exists:
            # identify causal paths 
            paths = CM.get_causal_paths(columns, di_edges, bi_edges, 
                                        options.obj)
            # compute causal paths
            for key, val in paths.items():
                if len(paths[key]) > NUM_PATHS:
                    paths = CM.compute_path_causal_effect(df, paths[key], G, 
                                                          NUM_PATHS)
            # compute individual treatment effect in a path 
            config = CM.compute_individual_treatment_effect(df, paths, G, 
                                            query, options.obj, bug_val, 
                                            bug)
            # perform intervention. This updates the init_data 
            _, obj_val = GenerateParams(config) 
            if obj_val < (1-query)*bug_val  
                bug_exists = False
            else: 
                # run loop
                run_cadet_loop(CM, df, tabu_edges, 
                                columns, options, NUM_PATHS) 

        
       
        
