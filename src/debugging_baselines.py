import sys
import math
import yaml
import copy
import random
import itertools
import numpy as np
from math import e
import pandas as pd
from operator import itemgetter
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_text
random.seed(288)

class DebuggingBaselines:
    def __init__(self):
        print ("initializing DebuggingBaselines class")

    def measure_cbi_importance(self, cfg, data, objective,
                   bug_val):
        """This function is used to measure importance"""
        Importance = {}

        adjustment = 4
        threshold = 0.5 * bug_val
        for col in data.columns:
            if col != objective:
                # compute F (P_true)
                P_true_df = data.loc[data[col] == 1]
                F_P_true_df = P_true_df.loc[P_true_df[objective] > threshold]
                F_P_true = len(F_P_true_df) + adjustment

                # compute S (P_true)
                S_P_true_df = P_true_df.loc[P_true_df[objective] < threshold]
                S_P_true = len(S_P_true_df) + adjustment

                # compute F (P_observed)
                F_P_observed_df = data.loc[data[objective] > threshold]
                F_P_observed=len(F_P_observed_df)
                # compute S (P_observed)
                S_P_observed_df = data.loc[data[objective] < threshold]
                S_P_observed=len(S_P_observed_df)
                # compute Failure
                Failure_P = F_P_true / (S_P_true + F_P_true)

                # compute Context
                Context_P = F_P_observed/ (S_P_observed + F_P_observed)

                # compute Increase
                Increase_P=Failure_P - Context_P

                #compute Importance
                Importance_P = 2/(1/Increase_P) + (1/(math.log(F_P_true)/math.log(F_P_observed)))
                Importance[col] = Importance_P

        return Importance

    def detect_cbi_fix(self, importance, columns):
        """This function is used to detect a fix"""

        col_dict={}

        for col in columns:
            cur = []
            for item in importance.items():
                if col in item[0]:
                    cur.append(item)
                    cur = sorted(cur,key=itemgetter(1), reverse=True)
                    selected = cur[0][0].split("@")
                    col_dict[selected[0]] = selected[1]
        print (col_dict)
        return col_dict, 0

    def cbi(self, cfg, data,
            objective, bug, soft,
            hw):
        """This function is used to run CBI"""
        if not data.empty:
            print ("[STATUS]: data format is valid")
            soft_configs = cfg["software_columns"][soft]
            hw_configs=cfg["hardware_columns"][hw]
            kernel_configs=cfg["kernel_columns"]
            columns = []
            columns.extend(soft_configs)
            columns.extend(hw_configs)
            columns.extend(kernel_configs)

            # measure importance
            if len(objective) > 1:
                importance_1 = self.measure_cbi_importance(cfg, data,
                                                     objective[0], bug[objective[0]])
                importance_2 = self.measure_cbi_importance(cfg, data,
                                                     objective[1], bug[objective[1]])
            else:
                importance = self.measure_cbi_importance(cfg, data,
                                                     objective[0], bug[objective[0]])
                fix, fix_val = self.detect_cbi_fix(importance, columns)

        else:
            print ("[ERROR]: no data found")
            return
        
    def process_bug(self, cfg, bug,
                    baseline_columns, columns):
       # Hardcoded
       bug["kernel.max_pids"]=65536
       col_index ={}
       index = 0
       for col in baseline_columns:
           col_index[col] = index
           index += 1
       bug_data = [0 for col in baseline_columns if col!="inference_time" or "total_energy_consumption"]
       
       for col in columns:
           cur = bug[col]
           try:
               cur_index= col_index[col+"@"+str(cur)]
           except KeyError:
               cur_index= col_index[col+"@"+str(int(cur))]                  
           bug_data[cur_index] = 1
        
       return bug_data, col_index
    
    def debug(self, possible_fix, bug_conf,
             threshold):
        if len(possible_fix) > 1:
            mid = int(len(possible_fix)/2)
            left, right = possible_fix[:mid], possible_fix[mid:]
            # generate configurations
            cur_conf = copy.deepcopy(bug_conf)
            for i in range(len(l)):
                if cur_conf[i] == 1:
                    cur_conf[i] = 0
                else:
                    cur_conf[i] = 1
            measurement = random.uniform(0.5 * threshold, 1.5*threshold)
            if measurement < threshold:
                possible_fix = [i for i in range(len(cur_conf)) if cur_conf[i]!=bug_conf[i]]
                self.debug(left, bug_conf, threshold)
            else:
                for i in range(len(right)):
                    if cur_conf[i] == 1:
                        cur_conf[i] = 0
                    else:
                        cur_conf[i] = 1
                possible_fix = [i for i in range(len(cur_conf)) if cur_conf[i]!=bug_conf[i]]
                self.debug(right, bug_conf, threshold)
            return possible_fix

    def dd(self, cfg, data,
           objective, bug, baseline_columns,
           soft, hw):
        """This function is used to implement dd"""

        if not data.empty:
            print ("[STATUS]: data format is valid")

            if len(objective) > 1:
                no_bug_subset_df = data.loc[data[objective[0]] < 0.5 * bug[objective[0]]]
                no_bug_subset_df = no_bug_subset_df.loc[data[objective[0]] < 0.5 * bug[objective[0]]]
            else:
                no_bug_subset_df = data.loc[data[objective[0]] < 0.5 * bug[objective[0]]]
                threshold = 0.5 * bug[objective[0]]
            # randomly select a fix
            pass_conf = no_bug_subset_df.sample(n=1)
            pass_conf = pass_conf.values.tolist()
            # process bug to compute delta
            soft_configs = cfg["software_columns"][soft]
            hw_configs=cfg["hardware_columns"][hw]
            kernel_configs=cfg["kernel_columns"]
            columns = []
            columns.extend(soft_configs)
            columns.extend(hw_configs)
            columns.extend(kernel_configs)
            bug_conf, conf_index = self.process_bug(cfg, bug, baseline_columns, columns)
            
            possible_fix = [i for i in range(len(pass_conf)) if pass_conf[i]!=bug_conf[i]]
            fix = self.debug(possible_fix, bug_conf, threshold)
            if not fix:
                fix = possible_fix
            print (fix)

            
    def compute_entropy(self, antecedents, df):
        """This function is used to compute entropy for encore"""
        configs = antecedents.values.tolist()
        configs=[list(conf) for conf in configs]
        H = [0 for i in configs]
        ln = np.log
        for i in range(len(configs)):
            cur_entropy = 0
            try:
                for option in configs[i]:
                    N = len(df)
                    N_i = len(df.loc[df[option] == 1])
                    p_i = N_i/N
                    cur_entropy += -(p_i *ln(p_i))

            except KeyError:
                print ("[ERROR]: possible adjustmens need to be made")
                H[i] = -1
            H[i] = cur_entropy
        max_H = np.max(H)
        max_H_index = H.index(max_H)
        selected_config = configs[max_H_index]
        return selected_config

    def encore(self, cfg, data,
              objective, bug, soft,
              hw):
        """This function is used to implement encore"""
        from mlxtend.frequent_patterns import apriori, association_rules
        if not data.empty:
            print ("[STATUS]: data format is valid")

            columns = data.columns
            if len(objective) > 1:
                no_bug_subset_df = data.loc[data[objective[0]] < 0.25 * bug[objective[0]]]
                no_bug_subset_df = data.loc[data[objective[1]] < 0.25 * bug[objective[1]]]
            else:
                no_bug_subset_df = data.loc[data[objective[0]] < 0.5 * bug[objective[0]]]
            no_bug_subset_df = no_bug_subset_df.drop(columns=['inference_time', 'total_energy_consumption'])
            no_bug_df = no_bug_subset_df

            no_bug_subset_df = apriori(no_bug_subset_df, min_support=0.2, use_colnames=True, verbose=1)
            df_ar = association_rules(no_bug_subset_df, metric= "confidence", min_threshold=0.6)

            # compute entropy
            fix = self.compute_entropy(df_ar["antecedents"],no_bug_df)
            # encode config
            soft_configs = cfg["software_columns"][soft]
            hw_configs=cfg["hardware_columns"][hw]
            kernel_configs=cfg["kernel_columns"]
            columns = []
            columns.extend(soft_configs)
            columns.extend(hw_configs)
            columns.extend(kernel_configs)
            dict_col={}
            for col in columns:
                for option in fix:
                    if col in option:
                        opt, val = option.split("@")
                        dict_col[opt] = val

        else:
            print ("[ERROR]: no data found")
            return
    
    def get_bugdoc_rules(self, tree, feature_names):
        left      = tree.tree_.children_left
        right     = tree.tree_.children_right
        threshold = tree.tree_.threshold
        features  = [feature_names[i] for i in tree.tree_.feature]

        # get ids of child nodes
        idx = np.argwhere(left == -1)[:,0]     

        def recurse(left, right, child, lineage=None):          
            if lineage is None:
                lineage = [child]
            if child in left:
                parent = np.where(left == child)[0].item()
                split = 'l'
            else:
                parent = np.where(right == child)[0].item()
                split = 'r'
            
            lineage.append((parent, split, threshold[parent], features[parent]))

            if parent == 0:
                lineage.reverse()
                return lineage
            else:
                return recurse(left, right, parent, lineage)
        struct = []
        for child in idx:
            cur=[]
            for node in recurse(left, right, child):
                
                if isinstance(node,int):
                    print (node)
                else:
                    cur.append(node)
                    struct.append(cur)
            return struct
    
    def bugdoc(self, cfg, df, 
               objective, bug, soft, 
               hw):
        """This function is used to implement bugdoc"""
        if not df.empty:
            print ("[STATUS]: data format is valid")
            # create label for training
            if len(objective) > 1:
                maximum_obj_0 = df[objective[0]].max()
                maximum_obj_1 = df[objective[1]].max()
            else:
                threshold = 0.5 * bug[objective[0]]
                obj = df[objective[0]].values.tolist()
                y = [0 for i in obj]
                for i in range(len(obj)):
                    if obj[i] < threshold:
                        y[i] = 1
            
            # drop unnecessary columns at this stage
            df = df.drop(columns=objective[0])
            columns = df.columns.to_list()
            
            X = df.values.tolist()
            # debugging decision tree
            decision_tree = DecisionTreeClassifier(random_state=0, max_depth=5)
            decision_tree = decision_tree.fit(X, y)
            r = export_text(decision_tree, feature_names=columns)
            
            # get debug rules
            rules = self.get_bugdoc_rules(decision_tree,columns)
            
            # parse the rules to generate config
            configs = []
            rules.sort()
            rules=list(rules for rules,_ in itertools.groupby(rules))
            col_dict={}
            for col in columns:
                col_dict[col]=bug[col]
            for rule in rules:
                for i in range(len(rule)-1):      
                    col_dict[rule[i][3]] = rule[i][2]

            print (col_dict)
              
