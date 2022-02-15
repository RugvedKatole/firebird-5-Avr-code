from scipy import stats
import pandas as pd
import numpy as np
import glob
import rospkg
import random as rn
import yaml
import pingouin as pg
import networkx as nx

dirname = rospkg.RosPack().get_path('mrpp_sumo')
k="through_modified_basic_5"
# config_files = glob.glob(dir_name + '/config/{}/*.yaml'.format(k))
samples = pd.Series(rn.sample(range(1,37),10))

algos=['tpbp_final', 'tpbp_util', 'through_basic_1', 'through_basic_3', 'through_basic_5', 'through_FHUM_1', 'through_FHUM_3', 'through_FHUM_5', 'through_modified_basic_1', 'through_modified_basic_3', 'through_modified_basic_5', 'through_modified_FHUM_1', 'through_modified_FHUM_3', 'through_modified_FHUM_5']
algos.extend(['sample_no'])

df = pd.DataFrame(columns=algos)
df['sample_no'] = samples
# adding average idleness values to df for each algo
for a in algos[:-1]:
    graph_avg_idle=[]
    for i in samples:
        name_list = a.split('_')
        if len(name_list) == 2:
            with open('{}/config/{}/{}_{}.yaml'.format(dirname, a, a, i), 'r') as f:
                config = yaml.load(f, yaml.FullLoader)
            sim_dir = dirname + '/post_process/' + a + "_" + str(i)
            df1 = pd.read_csv(sim_dir + '/{}_{}_node.csv'.format(a,str(i)))
        elif len(name_list) == 3:
            with open('{}/config/{}/{}_{}_{}.yaml'.format(dirname, a, "_".join(name_list[:-1]), str(i), name_list[-1] ), 'r') as f:
                config = yaml.load(f, yaml.FullLoader)
            sim_dir = dirname + '/post_process/{}_{}_{}'.format("_".join(name_list[:-1]), str(i), name_list[-1])
            df1 = pd.read_csv(sim_dir + '/{}_{}_{}_node.csv'.format("_".join(name_list[:-1]), str(i), name_list[-1]))
        else:
            with open('{}/config/{}/{}_{}.yaml'.format(dirname, a, a, i), 'r') as f:
                config = yaml.load(f, yaml.FullLoader)
            sim_dir = dirname + '/post_process/' + a + "_" + str(i)
            df1 = pd.read_csv(sim_dir + '/{}_{}_node.csv'.format(a,str(i)))
        #reading parameters
        graph = nx.read_graphml(dirname + '/graph_ml/{}.graphml'.format(config['graph']))
        nodes = list(graph.nodes())
        priority_nodes = config['priority_nodes'].split(' ')
        non_priority_nodes = [u for u in graph.nodes if u not in priority_nodes]
        time_period = config['time_periods'].split(' ')
        # calculating mean and appendind
        # print(df.loc[::].mean())
        graph_avg_idle.append(df1.loc[::].mean(axis = 1).mean())
    df[a] = graph_avg_idle

#df contains graph idleness values for all algorithms for a given sample
#now we will perform one way ANOVA to find if there is a significant difference in them

Annova_result = pg.rm_anova(df.iloc[:,:-1])
         
ttest_df = pd.DataFrame(columns=algos[:-1],index=algos[:-1])
ttest_df.fillna(1)
for i in algos[:-1]:
    values = []
    for j in algos[:-1]:
        s,p = stats.ttest_rel(df.loc[:,i],df.loc[:,j])
        values.append(p)
    ttest_df[i] = values

ttest_df.to_csv(dirname + "/ttest_results.csv",index=True)

wilcoxon_df = pd.DataFrame(columns=algos[:-1],index=algos[:-1])
wilcoxon_df.fillna(1)
for i in algos[:-1]:
    values = []
    for j in algos[:-1]:
        if i == j:
            values.append(0)
        else:
            s,p = stats.wilcoxon(df.loc[:,i],df.loc[:,j])
            values.append(p)
    wilcoxon_df[i] = values

wilcoxon_df.to_csv(dirname + "/wilcoxon_results.csv",index=True)



