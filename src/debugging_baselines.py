import sys
import math
import yaml
import copy
import random
import itertools
import numpy as np
from math import e
import pandas as pd
from sklearn.tree import _tree
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
        threshold = 0.7 * bug_val
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
                Increase_P=Failure_P - Context_P + 0.1
                        
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
        # convert the fix to a dataframe
        cur_df = [col_dict[cur_col] for cur_col in columns]
        cur_df = pd.Series(cur_df, index = columns)
        
        return cur_df, 0

    def cbi(self, cfg, data,
            objective, bug, soft,
            hw, bug_id, dfm,
            measurement_dir):
        """This function is used to run CBI"""
        if not data.empty:
            print ("[STATUS]: Starting CBI")
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
            fix = self.detect_cbi_fix(importance, columns)
            
            cdf = dfm[dfm["baseline"] == "cbi"]
            cdf = cdf[cdf["bug_id"] == bug_id]
            fix_val = cdf[objective[0]]
            
            print ("++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("Recommended Fix")
            print (fix)
            print ("Recommended Fix value", fix_val)
            print ("++++++++++++++++++++++++++++++++++++++++++++++++++")
            print ("++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("Bug")
            print (bug)
            print ("++++++++++++++++++++++++++++++++++++++++++++++++++")
            
        else:
            print ("[ERROR]: no data found")
            return
        
    def process_bug(self, cfg, bug,
                    baseline_columns, columns):
       
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
           soft, hw, bug_id):
        """This function is used to implement dd"""

        if not data.empty:
            print ("[STATUS]: Starting Delta Debugging")

            if len(objective) > 1:
                no_bug_subset_df = data.loc[data[objective[0]] < 0.7 * bug[objective[0]]]
                no_bug_subset_df = no_bug_subset_df.loc[data[objective[0]] < 0.7 * bug[objective[0]]]
            else:
                no_bug_subset_df = data.loc[data[objective[0]] < 0.7 * bug[objective[0]]]
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
        selected_H = [h for h in H if h>0.325]
        max_H = np.max(H)
        max_H_index = H.index(max_H)
        selected_config = configs[max_H_index]
        return selected_config

    def encore(self, cfg, data,
              objective, bug, soft,
              hw, bug_id, dfm, measurement_dir):
        """This function is used to implement encore"""
        from mlxtend.frequent_patterns import apriori, association_rules
        if not data.empty:
            print ("[STATUS]: Starting Encore")

            columns = data.columns
            if len(objective) > 1:
                no_bug_subset_df = data.loc[data[objective[0]] < 0.7* bug[objective[0]]]
                no_bug_subset_df = data.loc[data[objective[1]] < 0.7 * bug[objective[1]]]
            else:
                no_bug_subset_df = data.loc[data[objective[0]] < 0.7 * bug[objective[0]]]
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
                dict_col[col] = bug[col]
                
            for col in columns:
                for option in fix:
                    if col in option:
                        opt, val = option.split("@")
                        dict_col[opt] = val
            
            # convert the fix to a dataframe
            fix = [dict_col[col] for col in columns]
            fix = pd.Series(fix, index = columns)
            cdf = dfm[dfm["baseline"] == "encore"]
            cdf = cdf[cdf["bug_id"] == bug_id]
            fix_val = cdf[objective[0]]
            print ("++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("Recommended Fix")
            print (fix)
            print("Recommended Fix value", fix_val)
            print ("++++++++++++++++++++++++++++++++++++++++++++++++++")
            print ("++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("Bug")
            print (bug)
            print ("++++++++++++++++++++++++++++++++++++++++++++++++++")
        else:
            print ("[ERROR]: no data found")
            return
    
    def get_rules(self, tree, feature_names, class_names):
        tree_ = tree.tree_
        feature_name = [feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!" for i in tree_.feature]

        paths = []
        path = []
    
        def recurse(node, path, paths):
        
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                p1, p2 = list(path), list(path)
                p1 += [f"({name} <= {np.round(threshold, 3)})"]
                recurse(tree_.children_left[node], p1, paths)
                p2 += [f"({name} > {np.round(threshold, 3)})"]
                recurse(tree_.children_right[node], p2, paths)
            else:
                path += [(tree_.value[node], tree_.n_node_samples[node])]
                paths += [path]
            
        recurse(0, path, paths)

        # sort by samples count
        samples_count = [p[-1][1] for p in paths]
        ii = list(np.argsort(samples_count))
        paths = [paths[i] for i in reversed(ii)]
    
        rules = []
        for path in paths:
            rule = "if "
        
            for p in path[:-1]:
                if rule != "if ":
                    rule += " and "
                rule += str(p)
            rule += " then "
            if class_names is None:
                rule += "response: "+str(np.round(path[-1][0][0][0],3))
            else:
                classes = path[-1][0][0]
                l = np.argmax(classes)
                rule += f"class: {class_names[l]} (proba: {np.round(100.0*classes[l]/np.sum(classes),2)}%)"
            rule += f" | based on {path[-1][1]:,} samples"
            rules += [rule]
        
        return rules
    
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
             
            for node in recurse(left, right, child):
                print (node) 
               
            return struct
    
    def parse(self, cur_rule, cfg, columns, hw):
        if " <= " in cur_rule:
            cur_rule = cur_rule.split( " <= ")
            opt_s, val_s = cur_rule[0], cur_rule[1]
            for col in columns:
                if col in opt_s:
                    val_s = float(val_s.split(")")[0])
                    for val in cfg["option_values"][hw][col]:
                        if val <= val_s:
                            val_s = val
                            break
              
                    break 
        if " < " in cur_rule:
            cur_rule = cur_rule.split( " < ")
            opt_s, val_s = cur_rule[0], cur_rule[1]
            for col in columns:
                if col in opt_s:
                    val_s = float(val_s.split(")")[0])
                    for val in cfg["option_values"][hw][col]:
                        if val < val_s:
                            val_s = val
                            break
                    break 
        if " > " in cur_rule:
            cur_rule = cur_rule.split( " > ")
            opt_s, val_s = cur_rule[0], cur_rule[1]
            for col in columns:
                if col in opt_s:
                    val_s = float(val_s.split(")")[0])
                    for val in cfg["option_values"][hw][col]:
                        if val > val_s:
                            val_s = val
                            break
                    break 
        if " => " in cur_rule:
            cur_rule = cur_rule.split( " => ")
            opt_s, val_s = cur_rule[0], cur_rule[1]
            for col in columns:
                if col in opt_s:
                    val_s = float(val_s.split(")")[0])
                    for val in cfg["option_values"][hw][col]:
                        if val >= val_s:
                            val_s = val
                            break
                    break
        return col, val_s                          
                       
    def bugdoc(self, cfg, df, 
               objective, bug, soft, 
               hw, bug_id, dfm, measurement_dir):
        """This function is used to implement bugdoc"""
        if not df.empty:
            print ("[STATUS]: Starting BugDoc")
            # create label for training
            if len(objective) > 1:
                maximum_obj_0 = df[objective[0]].max()
                maximum_obj_1 = df[objective[1]].max()
            else:
                threshold = 0.6* bug[objective[0]]
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
            print ("Rules", r)
            # get debug rules
            rules = self.get_rules(decision_tree,columns,[0,1])
            # process rules to extract
            config = []
            for rule in rules:
                print ("++++++++++++++++++++++++++++++++")
                print ("Rule")
                print (rule)
                if "class: 1" in rule:
                    cur_conf = {}                   
                    cur = rule.split("then")[0]
                    cur = cur.split("if ")[1]
                    cur = cur.split(" and ")
                    for cur_rule in cur:                   
                        col, val_s = self.parse(cur_rule, cfg, columns, hw)
                        cur_conf[col] = val_s 
                        print (cur_conf)    
                    config.append(cur_conf)                    
                print ("++++++++++++++++++++++++++++++++")        
           
            for i in range(len(config)):
                for col in columns: 
                   if col not in config[i].keys():
                       config[i][col]=bug[col]
            
            recommended_fixes =[]
            for fix in config:
                fix = [fix[col] for col in columns]
                fix = pd.Series(fix, index = columns)              
                recommended_fixes.append(fix)
            
            cdf = dfm[dfm["baseline"] == "bugdoc"]
            cdf = cdf[cdf["bug_id"] == bug_id]
            fix_val = cdf[objective[0]].values.tolist()
                       
            for ifix in range(len(recommended_fixes)):
                

                print ("++++++++++++++++++++++++++++++++++++++++++++++++++")
                print ("BUGDOC")
                print ("++++++++++++++++++++++++++++++++++++++++++++++++++")
                print("Recommended Fix")
                print (recommended_fixes[ifix])
                print ("Recommended Fix Value", fix_val[ifix])
                print ("++++++++++++++++++++++++++++++++++++++++++++++++++")
                print ("++++++++++++++++++++++++++++++++++++++++++++++++++")
                print("Bug")
                print (bug)
                print ("++++++++++++++++++++++++++++++++++++++++++++++++++")
            print ("Number of Samples required:", len(df))            

