import os
import sys
import json
import yaml
import pandas as pd
from optparse import OptionParser
import matplotlib.pyplot as plt
import seaborn as sns
sys.path.append(os.getcwd())
sys.path.append('/root')


def config_option_parser():
    """This function is used to configure option parser 
    @returns:
        options: option parser handle"""
    usage = """USAGE: %python3 run_debug_metrics.py -o [objective] -e [experiment] 
    """
    parser = OptionParser(usage=usage)
    parser.add_option('-o', '--objective', dest='obj',
                      default=[], nargs=1, type='choice',
                      choices=('inference_time', 'total_energy_consumption', 'total_temp'), action='append', help="objective type")
    parser.add_option('-e', "--experiment", action="store",
                      type="string", dest="experiment", help="experiment")
    parser.add_option('-s', "--software", action="store",
                      type="string", dest="software", help="software")
    parser.add_option('-k', "--hardware", action="store",
                      type="string", dest="hardware", help="hardware")
    (options, args) = parser.parse_args()
    return options

def plot_bar(df, column, experiment):
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(x="method", y=column, data=df)
    plt.xlabel = "method"
    plt.savefig(os.path.join(os.getcwd(),"data","measurement","output",experiment+"_"+column+".pdf"))

if __name__ == "__main__":
   
    options = config_option_parser()
    # Initialization
    with open(os.path.join(os.getcwd(), "etc/config.yml")) as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)

    # nodes for causal graph
    soft_columns = cfg["software_columns"][options.software]
    hw_columns = cfg["hardware_columns"][options.hardware]
    kernel_columns = cfg["kernel_columns"]
    obj_columns = options.obj
    columns = soft_columns + hw_columns + kernel_columns + obj_columns
    
    bug_dir = os.path.join(os.getcwd(), cfg["bug_dir"], "single",
                           options.hardware, options.software, options.hardware + "_" + options.software + "_" + options.obj[0] + ".csv")
    
    if options.experiment == "debug":
         measurement_dir = measurement_dir = os.path.join(os.getcwd(),"data","measurement","output","debug_exp.csv")
    elif options.experiment == "transfer":
         measurement_dir = measurement_dir = os.path.join(os.getcwd(),"data","measurement","output","transfer_exp.csv")
    else:
        print ("[ERROR]: automatic metrics computation not supported")

    df = pd.read_csv(measurement_dir)
    bug_df = pd.read_csv(bug_dir)
    bug_df["bug_id"]=[i for i in range(len(bug_df))]
    
    plot_bar(df, "gain", options.experiment)
    plot_bar(df, "num_samples", options.experiment)
         
    
   

    
    
    
    
    
    
