# Author: Vander Freitas (UFOP)
# Date: 03/2021



import igraph as ig

# Obter a subrede formada pelo estado cujo geocódigo é uf_geocode. Exemplo: 35 é o código para São Paulo


# Aim: produce a network having only the nodes that belong to a given state uf_geocode
# Input: network (g), state (uf_geocode)
# Output: a network
def subnet_from_a_given_state(g,uf_geocode):
  codes_from_list_geocodes = []

  # encontrar os índices dos vértices que tenham os geocodes da lista passada por parâmetro
  for i in range(len(g.vs['geocode'])):
    gc = int(g.vs['geocode'][i])

    uf = gc / 1000000
    gc /= 10
    uf = int(10*uf + gc / 1000000)

    if(uf == uf_geocode):
      try:
        codes_from_list_geocodes.append(np.where(geocodes == int(g.vs['geocode'][i]))[0][0])
      except:
        pass

  if len(codes_from_list_geocodes) > 0:
    # Criar uma lista de índices válidos e remover os índices desejados
    idx_to_remove = np.zeros(g.vcount(), dtype=int)
    for i in range(g.vcount()):
      idx_to_remove[i] = int(i)
    idx_to_remove = np.delete(idx_to_remove, np.array(codes_from_list_geocodes))

    # Deletar os vértices com os índices selecionados
    g.delete_vertices(idx_to_remove.tolist())
  
    return g
  
  else:
    return None


# Aim: Produce a network containing only a desired subset of geocodes (nodes)
# Input: network (g), list of geocodes that represent cities (list_geocodes)
# Output: a network
def subnet_from_list_of_geocodes(g,list_geocodes):
  codes_from_list_geocodes = []

  # encontrar os índices dos vértices que tenham os geocodes da lista passada por parâmetro
  for i in range(len(list_geocodes)):
    try:
      codes_from_list_geocodes.append(np.where(geocodes == list_geocodes[i])[0][0])
    except:
      pass

  if len(codes_from_list_geocodes) > 0:
    # Criar uma lista de índices válidos e remover os índices desejados
    idx_to_remove = np.zeros(g.vcount(), dtype=int)
    for i in range(g.vcount()):
      idx_to_remove[i] = int(i)
    idx_to_remove = np.delete(idx_to_remove, np.array(codes_from_list_geocodes))

    # Deletar os vértices com os índices selecionados
    g.delete_vertices(idx_to_remove.tolist())
    
    return g

  else:
    return None



# MAIN CODE

# The network name comes from command line. 
net_name = sys.argv[1]

# reading the network from file
g = ig.Graph.Read_GraphML('output/' + net_name + '.GraphML')

# Test: Brasilia, São Paulo, Rio de Janeiro, Salvador
g_filtered = subnet_from_list_of_geocodes(g,[5300108,3550308,3304557,2927408])

# Test: Amazon state
#g_filtered = subnet_from_a_given_state(g,13)


g_filtered.write_graphml('output/' + net_name + '_filtered.GraphML")