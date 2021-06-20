# Author: Aurelienne Jorge (INPE)
# Date: 03/2021


import igraph as ig
import numpy as np
import thresholding as thr
import sys


# Aim: Find the weight threshold for the maximum diameter
# Input: g
# Output: threshold
def max_diameter_threshold(g):
  max_threshold = max(g.es['weight'])
  max_diameter = 0
  for threshold in np.arange(0.1, max_threshold, 0.1):
    #print(threshold)
    ng = g.copy()
    ng = thr.remove_edges(ng, threshold)
    #print(ng)
    diameter = ng.diameter(directed=False)
    #print(diameter)
    if diameter > max_diameter:
      max_diameter = diameter
      threshold_max_diameter = threshold
  return threshold_max_diameter



# MAIN CODE

# The network name comes from command line. 
net_name = sys.argv[1]

g = ig.Graph.Read_GraphML('../networks/' + net_name + '.GraphML')
print('Obtained threshold: ', max_diameter_threshold(g))