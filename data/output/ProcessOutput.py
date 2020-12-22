import pandas as pd

def read_data(fn):
    """This function is used to read data as a dataframe
    """
    return pd.read_csv(fn)

def strip_commas(df):
    """This function is used to strip commas
    """
    # get all the columns
    cols=list(df)
    df[cols]=df[cols].replace({',':''},regex=True)
    df[cols]=df[cols].astype(float)
    return df

def save_file(fn,
              df):
    """This file is used to save file
    """
    df.to_csv('processed_'+fn)

if __name__=="__main__":
   fn=raw_input("Enter file name: ")
   
   df=read_data(fn)
   df=strip_commas(df)
   save_file(fn,df)
   
   
