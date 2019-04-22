'''--------------------------------------------------------------------------------------
RUNSERVICE
Author: Shahriar Iqbal
Version: 0.1
-----------------------------------------------------------------------------------------
'''
import sys
import os
import socket
import logging 
from datetime import datetime

from Src.Configuration import Config as cfg
from Src.SetWorkload import SetWorkload

def process_input():
    '''This function is used to process input passed by user to select experiment.
    @returns:
        options: options dictionary
    '''
    options={}
    options['software_system']=raw_input('select software system: ')
    # Deep Neural Network Systems
    if options['software_system']=='DNN':
       options['properties']={}
       options['properties']['model']=raw_input('select model: ')
       options['properties']['height']=input('select image height: ')
       options['properties']['width']=input('select image height: ')
    
    return options

def config_logger():
    '''This function is used to configure logging information
    @returns: 
        logger: logging object
    '''
    # get log directory 
    log_dir=os.getcwd()+cfg.log_dir
    log_file_name='logfile_{0}'.format(str(datetime.now().date()))
    log_file=os.path.join(log_dir,log_file_name)
    
    # get logger object
    ip=socket.gethostbyname(socket.gethostname())
    extra={'ip_address':ip}
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logger=logging.getLogger(__name__)
    hdlr = logging.FileHandler(log_file)
    
    # define log format
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(ip_address)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    
    # define log level
    logger.setLevel(logging.INFO)
    logger = logging.LoggerAdapter(logger, extra)
    logger.info('[STATUS]: Start RunTest')
    return logger
                                
if __name__=='__main__':
    logger=config_logger()
    options=process_input()
    if options['software_system']=='DNN':
        # get input data 
        input_dir="{0}{1}".format(os.getcwd(), str(cfg.input_dir))
        input_data=[f for f in os.listdir(input_dir) 
                    if ((os.path.isfile(os.path.join(input_dir,f))) and 
                       (os.stat(os.path.join(input_dir,f)).st_size > 0))]
        for sample in input_data:
            sample=str(sample)
            data="{0}{1}".format(input_dir,sample)
            options['properties']['cur_input']=data
            SWL=SetWorkload(logger,
                            options)
            break
    
   
              
