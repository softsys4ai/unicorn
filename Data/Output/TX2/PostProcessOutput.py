import pandas as pd

def read_data(fn):
    """This function is used to read data as a dataframe
    """
    return pd.read_csv(fn)

def find_dup(df):
    """This function is used to find duplicates and process them for averaging
    """
    dup=df[df.duplicated(['core0_status',
                         'core1_status',
                         'core2_status',
                         'core3_status',
                         'core_freq',
                         'gpu_freq',
                         'emc_freq',
                         'scheduler.policy',
                         'vm.swappiness',
                         'vm.vfs_cache_pressure']
                        )]
    cur=0
    ind=[x[0] for x in dup.values]
    fpr={}
    for i in xrange(len(ind)-1):
        if ind[i+1]-ind[i]==1:
            try:
                fpr[cur].append(ind[i])
            except KeyError:
                fpr[cur]=[ind[i]]
        else:
            fpr[cur].append(ind[i])
            if i<len(ind)-1:
                cur=ind[i+1]-1
                fpr[cur]=[ind[i+1]]
    print fpr, ind    
            
        
    
def save_file(fn,
              df):
    """This file is used to save file
    """
    df.to_csv('post_processed_'+fn)

if __name__=="__main__":
   #fn=raw_input("Enter file name: ")
   fn='processed_output_no_intervention.csv'
   df=read_data(fn)
   df.dropna()
   find_dup(df)
   
   #save_file(fn,df)
   
   
