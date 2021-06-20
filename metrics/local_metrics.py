# Author: Vander Freitas (UFOP)
# Date: 06/2021



# WARNING:
# If the network is weighted, one should take care about
# the notion of distance. For example, 
# 1) if you are dealing with mobility networks,
# the distance could be something like 1/flow, because neighbors
# with higher flows could be considered closer. The same concept
# holds for networks where the weights are a certain correlation coefficient,
# where higher coefficients represent closer nodes.
# 2) Otherwise, if your weights have a direct relation with distance, 
# just keep it, without any concern.
# THIS CODE IS CONSIDERING THE FIRST CASE, then refer to line 114 and
# the following, where we create the edge attribute w_inv to be used in some metrics.



import sys
import igraph as ig
import networkx as nx
import numpy as np
import vulnerability as vn



# The network name comes from command line. 
net_name = sys.argv[1]



# Aim: export the computed metrics
# Input: network (g), computed metric (data), name of the metric (stat)
# Output: 
def export_data(g, data, metric_name):
    file_out = open('output/' + net_name + '_' + metric_name + '.csv', 'w')
    for i in range(g.vcount()):
        file_out.write(str(g.vs[i]['geocode']) + ';' + str(data[i]) + '\n')
    file_out.close()

    # ordered version
    stat_array = []
    for i in range(len(data)):
        stat_array.append( ( g.vs[i]['geocode'], float(data[i]) ) )

    dtype = [('label', int), ('stat', float)]
    stat_array = np.array(stat_array, dtype=dtype)
    stat_array = np.sort(stat_array, order='stat')
    stat_array = np.flip(stat_array)
    
    file_stat = open('output/' + net_name + '_ordered_' + metric_name + '.csv', 'w')
    for i in range(len(stat_array)):
        file_stat.write(str(stat_array[i][0]) + ';' + str(stat_array[i][1]) + '\n')
    file_stat.close()



# MAIN CODE




# reading the network from file
g = ig.Graph.Read_GraphML('../networks/' + net_name + '.GraphML')

# There are some metrics implemented in Networkx and not in igraph
# This is why we use Networkx below
g_nx = nx.readwrite.graphml.read_graphml('../networks/' + net_name + '.GraphML')





########## UNWEIGHTED METRICS ##########
print('  Degree')
degrees = g.degree()
export_data(g, degrees, 'degree')
#print(f'degrees: {degrees}')

print('  Betweenness')
betweenness = g.betweenness(vertices=None, directed=False, cutoff=None) #normalized_betweenness(g)
export_data(g, betweenness, 'betweenness')
#print(f'betweenness: {betweenness}')

print('  Closeness')
closeness = g.closeness(vertices=None, mode='all', cutoff=None, weights=None, normalized=True)
export_data(g, closeness, 'closeness')
#print(f'closeness: {closeness}')

print('  Vulnerability')
vuln = vn.vulnerability(g, weights=None)
export_data(g, vuln, 'vulnerability')
#print(f'vuln: {vuln}')


print('  Eigenvector centrality')
eignv = g.evcent(directed=False, scale=True, weights=None, return_eigenvalue=False)
export_data(g, eignv, 'eigenvector')


print('  Pagerank')
prank = nx.pagerank(g_nx, alpha=0.85, weight=1)
dictlist = []
for key, value in prank.items():
    dictlist.append(value)
export_data(g, dictlist, 'pagerank')


########## WEIGHTED METRICS ##########

if g.is_weighted():

    # strength (flows are the weights)
    print('  Strength')
    strength = g.strength(weights='weight')
    export_data(g, strength, 'strength')
    #print(f'Strength: {strength}')

    # Inverse of the flow 
    # This is a valid notion of distance in mobility networks, 
    # since the higher the flows between neighbors, the closer they are.
    g.es['w_inv'] = 1.0 / np.array(g.es['weight'])

    print('  Weighted Betweenness')
    betweenness_w = g.betweenness(vertices=None, directed=False, cutoff=None, weights='w_inv') 
    export_data(g, betweenness_w, 'betweenness_weight')
    #print(f'betweenness_w: {betweenness_w}')

    print('  Weighted Closeness')
    closeness_w = g.closeness(vertices=None, mode='all', cutoff=None, weights='w_inv', normalized=True)
    export_data(g, closeness_w, 'closeness_weight')
    #print(f'closeness_w: {closeness_w}')

    print('  Weighted Vulnerability')
    vuln_w = vn.vulnerability(g, weights='w_inv')
    export_data(g, vuln_w, 'vulnerability_weight')
    #print(f'vuln_w: {vuln_w}')

    print('  Weighted eigenvector centrality')
    eignv_w = g.evcent(directed=False, scale=True, weights='w_inv', return_eigenvalue=False)
    export_data(g, eignv_w, 'eigenvector_weight')


    print('  Weighted Pagerank')
    prank_w = nx.pagerank(g_nx, alpha=0.85, weight='weight')
    dictlist = []
    for key, value in prank_w.items():
        dictlist.append(value)
    export_data(g, dictlist, 'pagerank_weight')


'''
# OTHER METRICS:
katz, bonacich, damage


g_nx = nx.readwrite.graphml.read_graphml("../../input_data/" + net_name + ".GraphML")

L = nx.normalized_laplacian_matrix(g_nx)
e = np.linalg.eigvals(L.A)
largest_e = float(max(abs(e)))
print(f'largest e = {largest_e}')



katz = nx.katz_centrality(g_nx, alpha=1/largest_e - 0.1)
export_data(g, katz, 'katz', 0)
'''

# Metrics
# Bonacich (with negative values of beta)
# Damage: defined in Latora e Marchiori (2005). Basically how the removal of such node affects the network through some metric (eg. giant component size)