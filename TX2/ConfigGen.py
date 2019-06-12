from Params import params

def random_config_select():
    """This function is to select 400 configurations randomly
    """
    from random import randint
    from operator import itemgetter
    index=[randint(0,len(params)) for p in range(0,400)]
    return itemgetter(*index)(params)

if __name__=="__main__":
    configs=list(random_config_select())
    print len(configs)
    with open('CausalConfig.py', "w") as f:
            f.write('configs = %s' %configs)
