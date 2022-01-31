import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, recall_score
class Metrics:
      def __init__(self):
          print ("[STATUS]: initializing Metrics class")
      
      def compute_accuracy(self, list1, list2):
          
          intersection = len(list(set(list1).intersection(list2)))
          union = (len(list1) + len(list2)) - intersection
          return float(intersection) / union
      
      def compute_precision(self, recommended_fix, true_cause):
          return precision_score(recommended_fix, true_cause)

      def compute_recall(self, recommended_fix, true_cause):
          return recall_score(recommended_fix, true_cause)
      
      def compute_gain(self, recommended_val, bug_val):
          return ((recommended_val - bug_val)/bug_val)*100


class Plotting:
      def __init__(self):
          print ("[STATUS]: initializing Plotting class")
      
      def plot_histogram(self):
          """This class is used to plot histograms"""
          print ("TODO")


      def plot_line(self):
          """This class is used for line plotting"""
          print ("TODO")

class Preprocessing:
      
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

      def save_file(fn, df):
          """This file is used to save file
          """
          df.to_csv('processed_'+fn)


   
          
         
 
