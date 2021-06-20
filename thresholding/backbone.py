# Author: Iuri Diniz (UFOP)
# Date: 03/2021


import igraph as ig
import sys







# input: g, alpha
# output: g

# pij = (1 - (wij/si))**(ki - 1), where:
# w --> weight
# s --> strength
# k --> degree

def backbone(g,alpha):
    p={}
    adj = g.get_adjacency()
    n_nodes = g.vcount()
    s = g.strength(weights=g.es['weight']) # calcula o strength de toda a rede
    for i in range(n_nodes):
        for j in range(n_nodes):
            if (adj[i,j] == 1): # verificando se há conexão entre o par i,j
                w = g.es[g.get_eid(i,j)]['weight']
                k = g.vs[i].degree()
                pij = (1 - (w/s[i]))**(k-1)
                if (pij < alpha): # aplicando a relação com o alpha
                    p[i,j] = pij

    # Pegando os pares simétricos e atribuindo -99 ao par com maior valor de probabilidade
    for i in p:
        if ((i[0],i[1]) and (i[1],i[0])) in p.keys():
            if p[i[0],i[1]] <= p[i[1],i[0]]:
                p[i[1],i[0]] = -99
            else:
                p[i[0],i[1]] = -99

    # Criando dicionário com os pares válidos
    pij = {}
    for i in p:
        if not (p[i] == -99):
            pij[i] = p[i]

    return(pij)



# MAIN CODE


# The network name comes from command line. 
net_name = sys.argv[1]


g = ig.Graph.Read_GraphML('../networks/' + net_name + '.GraphML')

# Set parameter alpha
alpha = 0.04
prob=(backbone(g,alpha))

new_g = ig.Graph()
new_g.add_vertices(g.vcount())
new_g.add_edges(list(prob.keys()))
# Nomes das zonas
#new_g.vs['label'] = g.vs['label']

# coordendas
new_g.vs["X"] =  g.vs["X"] 
new_g.vs["Y"] = g.vs["Y"] 

# tamanho dos nós dependendo do grau
new_g.vs["size"] = g.vs["size"]


new_g.write_graphml('output/' + net_name + '_backbone.GraphML')