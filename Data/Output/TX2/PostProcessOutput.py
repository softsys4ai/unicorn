import pandas as pd
import math

def read_data(fn):
    """This function is used to read data as a dataframe
    """
    return pd.read_csv(fn)

def process_df(df):
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
    # find duplicates
    for i in xrange(len(ind)-1):
        if ind[i+1]-ind[i]==1:
            try:
                fpr[cur].append(ind[i])
            except KeyError:
                fpr[cur]=[ind[i]]
        else:
            fpr[cur].append(ind[i])
            cur=ind[i+1]-1
    
    # perform average            
    new_df_val=[]
    df_val=list(df.values)
    for k,v in fpr.iteritems():
        cur=df_val[int(k)]
        counter=1
        for i in xrange(len(v)):
            cur=[sum(x) for x in zip(cur,df_val[int(v[i])])]
            counter=counter+1
        final=[x/counter for x in cur]
        new_df_val.append(final)   
    
    cols=df.columns
    new_df=pd.DataFrame(new_df_val)
    new_df.columns=cols
    return new_df
               
def save_file(fn,
              df):
    """This file is used to save file
    """
    df.to_csv('post_'+fn)

if __name__=="__main__":
   
   fn=raw_input("Enter file name: ")
   df=read_data(fn)
   df.dropna()
   new_df=process_df(df) 
   save_file(fn,new_df)
   
   
