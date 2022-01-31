import sys
import os
import socket 
from datetime import datetime
from src.set_workload import SetWorkload

def process_input():
    '''This function is used to process input passed by user to select experiment.
    @returns:
        options: options dictionary
    '''
    options={}
    options['software_system']=sys.argv[1]
    # Deep Neural Network Systems1
    if options['software_system']=='Image':
       options['properties']={}
           
    return options
                             
if __name__=='__main__':
    options=process_input()
    if options['software_system']=='Image':
            SWL=SetWorkload(options)
            
    
   
              
