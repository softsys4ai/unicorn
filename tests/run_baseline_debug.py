import os
import sys
import yaml
import pandas as pd
from optparse import OptionParser

sys.path.append('/root')

from src.causal_model import CausalModel
from src.generate_params import GenerateParams
from src.debugging_baselines import DebuggingBaselines


def config_option_parser():
    """This function is used to configure option parser
    @returns:
        options: option parser handle"""
    usage = """USAGE: %python3 run_baseline_debug.py -o [objectives] -s [software] -k [hardware] -m [mode] -b [baseline]
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
    parser.add_option('-b', "--baseline", action="store",
                      type="string", dest="baseline", help="baseline")
    (options, args) = parser.parse_args()
    return options


if __name__ == "__main__":
    options = config_option_parser()
    # Initialization
    with open(os.path.join(os.getcwd(), "etc/config.yml")) as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)

    soft_columns = cfg["software_columns"][options.software]
    hw_columns = cfg["hardware_columns"][options.hardware]
    kernel_columns = cfg["kernel_columns"]
    perf_columns = cfg["perf_columns"]

    obj_columns = options.obj
    columns = soft_columns + hw_columns + kernel_columns + obj_columns

    if len(options.obj) > 1:
        init_dir = os.path.join(os.getcwd(), cfg["init_dir"], "multi",
                                options.hardware, options.software, options.hardware + "_" + options.software + "_" + "initial.csv")
        baseline_init_dir = os.path.join(os.getcwd(), cfg["init_dir"], "multi",
                                         options.hardware, options.software, options.hardware + "_" + options.software + "_" + "baseline_initial.csv")
        bug_dir = os.path.join(os.getcwd(), cfg["bug_dir"], "multi", options.hardware,
                               options.software, options.hardware + "_" + options.software + "_" + "multi.csv")

    else:
        init_dir = os.path.join(os.getcwd(), cfg["init_dir"], "multi",
                                options.hardware, options.software, options.hardware + "_" + options.software + "_" + "initial.csv")
        baseline_init_dir = os.path.join(os.getcwd(), cfg["init_dir"], "single",
                                         options.hardware, options.software, options.hardware + "_" + options.software + "_" + "baseline_initial.csv")
        bug_dir = os.path.join(os.getcwd(), cfg["bug_dir"], "single",
                               options.hardware, options.software, options.hardware + "_" + options.software + "_" + options.obj[0] + ".csv")
    sampled_dir = os.path.join(os.getcwd(), cfg["sampled_dir"], options.hardware,
                               options.software, options.hardware + "_" + options.software + "_" + "baseline.csv")

    # get bug data
    bug_df = pd.read_csv(bug_dir)
    # get init data
    df = pd.read_csv(baseline_init_dir)
    sampled_df = pd.read_csv(sampled_dir)
    df = pd.concat([df, sampled_df], axis=0)
    # baseline debugging
    for _, bug in bug_df.iterrows():
        DB = DebuggingBaselines()
        if options.baseline == "cbi":
            DB.cbi(cfg, df, options.obj,
                   bug, options.software, options.hardware)
        elif options.baseline == "encore":
            DB.encore(cfg, df, options.obj,
                      bug, options.software, options.hardware)
        elif options.baseline == "dd":
            DB.dd(cfg, df, options.obj,
                  bug, df.columns, options.software,
                  options.hardware)
        elif options.baseline == "bugdoc":
            bdf = pd.read_csv(init_dir)
            bdf = bdf[columns]
            DB.bugdoc(cfg, bdf, options.obj,
                      bug, options.software, options.hardware)
        else:
            print("[ERROR]: baseline not implemented")
