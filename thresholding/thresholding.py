# Author: Aurelienne Jorge (INPE)
# Date: 03/2021


import igraph as ig
import sys


# Aim: Remove links whose weights are below a certain threshold
# Input: g, w_threshold
# Output: g
def remove_edges(g, w_threshold):
  del_edges = []
  for e in g.es():
    if e['weight'] < w_threshold:
      del_edges.append(e)
  g.delete_edges(del_edges)
  return g




# MAIN CODE

# The network name comes from command line. 
net_name = sys.argv[1]


g = ig.Graph.Read_GraphML('../networks/' + net_name + '.GraphML')


# Set the threshold
w_threshold = 12
ng = remove_edges(g, w_threshold)

ng.write_graphml('output/' + net_name + '_global_thresholding.GraphML')