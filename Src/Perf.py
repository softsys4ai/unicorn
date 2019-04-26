import os
import sys
import pandas as pd 

class Perf:
    """This class is used to perform Perf parsing
    """
    def __init__(self):
        print ('Initializing Perf Class')
        self.VALUE=0
        self.EVENT=1
        
    
    def parse_perf(self):
        output=list()
        with open ('cur','r') as f:
            for line in f:
                output.append(line.split(' '))
        output=output[5:]
        output.pop()
        output.pop()
        output.pop()
        processed_output=[[] for _ in xrange(len(output))]
        perf_output={}
        for line in xrange(len(output)):
            for elem in output[line]:
                if elem!='':
                    processed_output[line].append(elem)
        
        for line in processed_output:
            perf_output[line[self.EVENT]]=[line[self.VALUE]]
            
        return pd.DataFrame(perf_output)
