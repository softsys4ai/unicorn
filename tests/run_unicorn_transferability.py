import os
import sys
import pandas as pd
import yaml
import json
from ananke.graphs import ADMG
from networkx import DiGraph
from optparse import OptionParser
import time

sys.path.append('/root')

from src.causal_model import CausalModel
from src.generate_params import GenerateParams


def config_option_parser():
    """This function is used to configure option parser
    @returns:
        options: option parser handle"""
    usage = """USAGE: %python3 unicorn_transfer.py -o [objectives] -d [init_data] -s [software] -k [hardware] -m offline
    """
    parser = OptionParser(usage=usage)
    parser.add_option('-o', '--objective', dest='obj',
                      default=[], nargs=1, type='choice',
                      choices=('inference_time', 'total_energy_consumption', 'total_temp'), action='append', help="objective type")
    parser.add_option('-s', "--software", action="store",
                      type="string", dest="software", help="software")
    parser.add_option('-k', "--hardware", action="store",
                      type="string", dest="hardware", help="hardware")
    parser.add_option('-m', "--mode", action="store",
                      type="string", dest="mode", help="mode")
    (options, args) = parser.parse_args()
    return options


def run_unicorn_loop(CM, df,
                     tabu_edges, columns, options,
                     NUM_PATHS):
    """This function is used to run unicorn in a loop"""
    # NOTEARS causal model hyperparmas
    # _, notears_edges = CM.learn_entropy(df, tabu_edges, 0.75)
    # get bayesian network from DAG obtained
    # bn = BayesianNetwork(sm)

    fci_edges = CM.learn_fci(df, tabu_edges)
    edges = []
    # resolve notears_edges and fci_edges and update
    di_edges, bi_edges = CM.resolve_edges(edges, fci_edges, columns,
                                          tabu_edges, NUM_PATHS, options.obj)
    # construct mixed graph ADMG

    G = ADMG(columns, di_edges=di_edges, bi_edges=bi_edges)
    return G, di_edges, bi_edges


if __name__ == "__main__":

    NUM_PATHS = 15
    query = 0.8
    options = config_option_parser()
    # target
    target_hw = "TX2"

    # initialization
    with open(os.path.join(os.getcwd(), "etc/config.yml")) as file:
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
                                options.hardware, options.software, options.hardware + "_" + options.software + "_" + "initial.csv")
        bug_dir = os.path.join(os.getcwd(), cfg["bug_dir"], "multi", options.hardware,
                               options.software, options.hardware + "_" + options.software + "_" + "multi.csv")
        target_bug_dir = os.path.join(os.getcwd(), cfg["bug_dir"], "multi",
                                      target_hw, options.software, target_hw + "_" + options.software + "_" + options.obj[0] + ".csv")
        
        with open(os.path.join(os.getcwd(), cfg["debug_dir"], "multi", target_hw,
                  options.software, "measurement_t.json")) as mfl:
            m = json.load(mfl)
    else:

        init_dir = os.path.join(os.getcwd(), cfg["init_dir"], "single",
                                options.hardware, options.software, options.hardware + "_" + options.software + "_" + "initial.csv")
        target_init_dir = os.path.join(os.getcwd(), cfg["init_dir"], "multi",
                                target_hw, options.software, target_hw + "_" + options.software + "_" + "initial.csv")
        bug_dir = os.path.join(os.getcwd(), cfg["bug_dir"], "single",
                               options.hardware, options.software, options.hardware + "_" + options.software + "_" + options.obj[0] + ".csv")
        target_bug_dir = os.path.join(os.getcwd(), cfg["bug_dir"], "single",
                                      target_hw, options.software, target_hw + "_" + options.software + "_" + options.obj[0] + ".csv")

        with open(os.path.join(os.getcwd(), cfg["debug_dir"], "single", target_hw,
                  options.software, "measurement_t.json")) as mfl:
            m = json.load(mfl)
        with open(os.path.join(os.getcwd(), cfg["debug_dir"], "single", target_hw,
                  options.software, "measurement.json")) as mfl:
            mt = json.load(mfl)
    # get init data
    df = pd.read_csv(init_dir)
    df = df[columns]

    # initialize causal model object
    CM = CausalModel(columns)
    g = DiGraph()
    g.add_nodes_from(columns)
    # edge constraints
    tabu_edges = CM.get_tabu_edges(columns, conf_opt, options.obj)

    G, di_edges, bi_edges = run_unicorn_loop(CM, df, tabu_edges, columns,
                                             options, NUM_PATHS)

    g.add_edges_from(di_edges + bi_edges)

    var_types = {}
    for col in columns:
        var_types[col] = "c"
    # extract bugs from target hardware TX2.

    # get bug data from the target
    bug_df = pd.read_csv(target_bug_dir)
    # get Bug and update df
    
    # UNICORN + 25
    start = time.time()
    for bug_id in range(len(bug_df)):
        # initialize dataframe after each run
        df = pd.read_csv(init_dir)
        df = df[columns]
        
        bug = bug_df.loc[bug_id]
        num_samples = 0
        bug_exists = True
        print("--------------------------------------------------")
        print("BUG ID: ", bug_id)
        print("---------------------------------------------------")
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
                        paths = CM.compute_path_causal_effect(
                            df, paths[key], G, NUM_PATHS)
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

            if options.mode == "offline":
                curm = m[target_hw][options.software][options.obj[0]
                                                      ][str(bug_id)][str(num_samples)]["measurement"]
                if curm < (1 - query) * bug[options.obj[0]]:
                    bug_exists = False
                    gain = ((bug[options.obj[0]]-curm)/bug[options.obj[0]])*100
                    print("Resolved BUG_ID", bug_id)

                    print("----------------Recommended Fix-------------------")
                    print("----------------Unicorn + 25-------------------")
                    print(config)
                    print ("Gain", gain)
                    print ("Number of samples", num_samples)
                    print("--------------------------------------------------")
                    
                    print("-----------------------Bug------------------------")
                    print(bug[conf_opt])
                    
                    print("--------------------------------------------------")
                      
                else:
                    curc = m[target_hw][options.software][options.obj[0]
                                                          ][str(bug_id)][str(num_samples)]["conf"]
                    num_samples += 1

                    output = config.tolist()
                    output.extend(curc)
                    output.extend([curm])
                    output = pd.DataFrame([output])
                    output.columns = columns
                    df = pd.concat([df, output], axis=0)
                    df = df[columns]
                    # previous_config
                    previous_config = output.squeeze()[conf_opt]
                    # update initial
                    run_unicorn_loop(CM, df, tabu_edges,
                                     columns, options, NUM_PATHS)

            elif options.mode == "online":
                gprm = GenerateParams(cfg, options.software, "unicorn")
                output = gprm.run_unicorn_experiment(config)
                if output[options.obj[0]] < (1 - query) * bug_val:
                    bug_exists = False
                else:
                    # run loop
                    output = output.tolist()
                    output.extend(curc)
                    output.extend([curm])
                    output = pd.DataFrame([output])
                    output.columns = columns
                    df = pd.concat([df, config], axis=0)
                    df = df[columns]
                    # previous_config
                    previous_config = output.squeeze()[conf_opt]
                    run_unicorn_loop(CM, df, tabu_edges,
                                     columns, options, NUM_PATHS)
            else:
                print("[ERROR]: invalid mode")
        break
    # put output to a dataframe
    result_df = output.copy()
    result_df["method"]="Unicorn +25"
    result_df["num_samples"]=num_samples
    result_df["gain"]=gain
    # Unicorn rerun
    for bug_id in range(len(bug_df)):
        # initialize dataframe after each run
        df = pd.read_csv(target_init_dir)
        df = df[columns]
        
        bug = bug_df.loc[bug_id]
        num_samples = 0
        bug_exists = True
        print("--------------------------------------------------")
        print("BUG ID: ", bug_id)
        print("---------------------------------------------------")
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
                        paths = CM.compute_path_causal_effect(
                            df, paths[key], G, NUM_PATHS)
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

            if options.mode == "offline":
                curm = mt[target_hw][options.software][options.obj[0]
                                                      ][str(bug_id)][str(num_samples)]["measurement"]
                if curm < (1 - query) * bug[options.obj[0]]:
                    bug_exists = False
                    gain = ((bug[options.obj[0]]-curm)/bug[options.obj[0]])*100
                    print("Resolved BUG_ID", bug_id)

                    print("----------------Recommended Fix-------------------")
                    print("----------------Unicorn Rerun-------------------")
                    print(config)
                    print ("Gain", gain)
                    print ("Number of samples", num_samples)
                    print("--------------------------------------------------")
                    
                    print("-----------------------Bug------------------------")
                    print(bug[conf_opt])
                    
                    print("--------------------------------------------------")
                      
                else:
                    curc = mt[target_hw][options.software][options.obj[0]
                                                          ][str(bug_id)][str(num_samples)]["conf"]
                    num_samples += 1

                    output = config.tolist()
                    output.extend(curc)
                    output.extend([curm])
                    output = pd.DataFrame([output])
                    output.columns = columns
                    df = pd.concat([df, output], axis=0)
                    df = df[columns]
                    # previous_config
                    previous_config = output.squeeze()[conf_opt]
                    # update initial
                    run_unicorn_loop(CM, df, tabu_edges,
                                     columns, options, NUM_PATHS)

            elif options.mode == "online":
                gprm = GenerateParams(cfg, options.software, "unicorn")
                output = gprm.run_unicorn_experiment(config)
                if output[options.obj[0]] < (1 - query) * bug_val:
                    bug_exists = False
                else:
                    # run loop
                    output = output.tolist()
                    output.extend(curc)
                    output.extend([curm])
                    output = pd.DataFrame([output])
                    output.columns = columns
                    df = pd.concat([df, config], axis=0)
                    df = df[columns]
                    # previous_config
                    previous_config = output.squeeze()[conf_opt]
                    run_unicorn_loop(CM, df, tabu_edges,
                                     columns, options, NUM_PATHS)
            else:
                print("[ERROR]: invalid mode")
        break
    end = time.time() - start
    
    output["method"]="Unicorn (Rerun)"
    output["num_samples"]=num_samples
    output["gain"]=gain
    result_df = pd.concat([result_df,output],axis=0)
    measurement_dir = os.path.join(os.getcwd(),"data","measurement","output","transfer_exp.csv")
    result_df.to_csv(measurement_dir,index=False)
    print ("Total Experiment time", end)
