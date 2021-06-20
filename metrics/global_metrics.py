# Author: Aurelienne Jorge (INPE)
# Date: 03/2021

import numpy as np
import matplotlib.pyplot as plt
import igraph as ig
import networkx as nx
import math 
import sys


def get_average_degree(g):
  return ig.mean(g.degree())

def get_shortest_path_mean(g):
  paths = g.shortest_paths()
  nodes = len(paths)
  mean = np.zeros(nodes)
  for i in range(nodes):
    count = 0
    path_length = len(paths[i])
    for j in range(path_length):
      if (paths[i][j] == np.inf):
        paths[i][j] = 0
      else:
        # Contabiliza elementos da componente conexa
        count += 1

    if (count - 1) <= 0:
      mean[i] = 0
    else:
      mean[i] = np.sum(paths[i]) / (count - 1)

  return mean

def get_average_shortest_path_mean(g):
  sh_paths_mean = get_shortest_path_mean(g)
  sh_paths_mean = sh_paths_mean[sh_paths_mean>0]
  if len(sh_paths_mean) == 0:
    avg_sh_paths_mean = np.inf
  else:
    avg_sh_paths_mean = sum(sh_paths_mean)/len(sh_paths_mean)
  return avg_sh_paths_mean

def statistically_small_world(N, L, avg_shortest_path, avg_cluster_coef):
  p = 2*L/(N*(N-1))
  avg_degree_rand = (p*(N-1))
  avg_clust_rand = p
  avg_shortpath_rand = math.log(N)/math.log(avg_degree_rand)
  if avg_cluster_coef > avg_clust_rand and avg_shortest_path < avg_shortpath_rand:
    return True
  return False

def plot_network_hierarchy(g):
  degrees = g.degree()
  cluster_coefs = g.transitivity_local_undirected()
  plt.plot(degrees, cluster_coefs, 'b.')
  plt.xlabel('Degree')
  plt.ylabel('Clustering Coefficient')
  plt.show()

def heterogeneity(g):
  degrees = g.degree()
  acc = 0
  for k in degrees:
    acc = acc + k**2
  avg = acc/len(degrees)
  het = avg/(get_average_degree(g)**2)
  return het



# MAIN CODE

# The network name comes from command line. 
net_name = sys.argv[1]


# igraph
g = ig.Graph.Read_GraphML('../networks/' + net_name + '.GraphML')

# networkx
g_nx = nx.readwrite.graphml.read_graphml('../networks/' + net_name + '.GraphML')


N = g.vcount()
L = g.ecount()
avg_degree = get_average_degree(g)
avg_cluster_coef = g.transitivity_avglocal_undirected()
avg_shortest_path = get_average_shortest_path_mean(g)
diameter = g.diameter(directed=False)
density = g.density()
plot_network_hierarchy(g)
dg_assort_coef = nx.degree_assortativity_coefficient(g_nx)
print(statistically_small_world(N, L, avg_shortest_path, avg_cluster_coef))
print('degree_assortativity_coefficient: ', dg_assort_coef)
print('avg_degree: ', avg_degree)
print('avg_shortest_path: ', avg_shortest_path)
print('avg_cluster_coef: ', avg_cluster_coef)
print('density: ', density)
print('heterogeneity: ', heterogeneity(g))