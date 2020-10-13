'''--------------------------------------------------------------------------------------
RUNSERVICE
Author: Shahriar Iqbal
Version: 0.1
-----------------------------------------------------------------------------------------
'''
import sys
import os
from datetime import datetime
from Src.Configuration import Config as cfg
from Src.GenerateParams import GenerateParams

def process_input():
    '''This function is used to process input passed by user to select experiment.
    @returns:
        options: options dictionary
    '''
    options={}
    options['software']=sys.argv[1] 
    return options
        
if __name__=='__main__':
    options=process_input()
    GP=GenerateParams(options['software'])
   
              
