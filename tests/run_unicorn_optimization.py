import os
import sys
import pandas as pd
import json
import yaml
from ananke.graphs import ADMG
from networkx import DiGraph
from optparse import OptionParser


sys.path.append('/root')

from src.causal_model import CausalModel
from src.generate_params import GenerateParams


def config_option_parser():
    """This function is used to configure option parser 
    @returns:
        options: option parser handle"""
    usage = """USAGE: %python3 unicorn_debugging.py -o [objectives] -d [init_data] -s [software] -k [hardware]
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
    #_, notears_edges = CM.learn_entropy(df, tabu_edges, 0.75)
    # get bayesian network from DAG obtained by NOTEARS
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

    NUM_PATHS = 25
    query = "best"
    options = config_option_parser()
    # Initialization
    with open(os.path.join(os.getcwd(), "etc/config.yml")) as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)
    with open(os.path.join(os.getcwd(), cfg["opt_dir"], "measurement.json")) as mfl:
        m = json.load(mfl)

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
    else:

        init_dir = os.path.join(os.getcwd(), cfg["init_dir"], "single",
                                options.hardware, options.software, options.hardware + "_" + options.software + "_" + "initial.csv")

    # get init data
    df = pd.read_csv(init_dir)
    df = df[columns]
    # initialize causal model object
    CM = CausalModel(columns)
    g = DiGraph()
    g.add_nodes_from(columns)
    # edge constraints
    tabu_edges = CM.get_tabu_edges(columns, conf_opt, options.obj)

    G, di_edges, bi_edges = run_unicorn_loop(CM, df, tabu_edges,
                                             columns, options, NUM_PATHS)

    g.add_edges_from(di_edges + bi_edges)

    var_types = {}
    for col in columns:
        var_types[col] = "c"

    ref_index = df[[options.obj[0]]].idxmin()
    ref_df = df.loc[ref_index]
    ref = ref_df.iloc[0]
    for it in range(68):
        # identify causal paths
        previous_config = ref[conf_opt].copy()
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
                                                            query, options, ref[options.obj[0]],
                                                            previous_config, cfg, var_types)

        else:
            # multi objective
            paths = paths[options.obj[0]]
            # compute individual treatment effect in a path
            config = CM.compute_individual_treatment_effect(df, paths, g,
                                                            query, options, ref[options.obj],
                                                            previous_config, cfg, var_types)

        # perform intervention. This updates the init_data
        if config is not None:
            if options.mode == "offline":

                curm = m[options.hardware][options.software][options.obj[0]][str(
                    it)]["measurement"]
                curc = m[options.hardware][options.software][options.obj[0]][str(
                    it)]["conf"]

                # update initial
                config = config.tolist()
                config.extend(curc)
                config.extend([curm])
                config = pd.DataFrame([config])
                config.columns = columns
                df = pd.concat([df, config], axis=0)
                df = df[columns]
                previous_config = config.squeeze()[conf_opt]
                run_unicorn_loop(CM, df, tabu_edges,
                                 columns, options, NUM_PATHS)

            elif options.mode == "online":
                gprm = GenerateParams(cfg, options.software, "unicorn")
                output = gprm.run_unicorn_experiment(config)
                output.extend(curc)
                output.extend([curm])
                output = pd.DataFrame([output])
                output.columns = columns
                df = pd.concat([df, config], axis=0)
                df = df[columns]
                previous_config = output.squeeze()[conf_opt]
                run_unicorn_loop(CM, df, tabu_edges,
                                 columns, options, NUM_PATHS)
            else:
                print("[ERROR]: invalid mode")
        else:
            print("[ERROR]: no config recommended")
    print("---------------------------------------------------------------")
    print("Optimal value obtained by Unicorn is:", df[options.obj[0]].min())
    print("---------------------------------------------------------------")
