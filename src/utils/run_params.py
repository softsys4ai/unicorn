import sys
import os
from datetime import datetime
from cadet.Configuration import Config as cfg
from cadet.generate_params import GenerateParams

def process_input():
    """
    This function is used to process input passed by user to select experiment.

    Returns
    -------
    options: dict
        options dictionary
    """
    options={}
    options['software']=sys.argv[1] 
    return options
        
if __name__=='__main__':
    options=process_input()
    GP=GenerateParams(options['software'])
   
              
