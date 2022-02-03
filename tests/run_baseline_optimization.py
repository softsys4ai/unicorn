import os
import sys
import yaml
import pandas as pd
from optparse import OptionParser

sys.path.append('/root')
from src.optimization_baselines import OptimizationBaselines

def config_option_parser():
    """This function is used to configure option parser
    @returns:
        options: option parser handle"""
    usage="""USAGE: %python3 baselines.py -o [objectives] -s [software] -k [hardware] -m [mode]
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
    parser.add_option('-b', "--baseline", action="store",
                      type="string", dest="baseline", help="baseline")
    (options, args)=parser.parse_args()
    return options


if __name__=="__main__":
    options = config_option_parser()
    # Initialization
   
    # baseline optimization
    
    OB = OptimizationBaselines()
    if options.baseline == "smac":
        OB.smac(options.obj, options.software, options.hardware)  
    else:
        print ("[ERROR]: baseline not implemented")
