# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import igraph as ig




print('GENERATING TERRESTRIAL AND FLUVIAL NETWORKS')

# CSV gerado a partir do arquivo "Base_de_dados_ligacoes_rodoviarias_e_hidroviarias_2016.xlsx"
data = pd.read_csv('data/Base_de_dados_ligacoes_rodoviarias_e_hidroviarias_2016.csv', delimiter=';')

# Concatenar os geocódigos das colunas de origem e destino e considerar apenas valores únicos.
# Importante: o método "unique" também ordena os valores, do menor para o maior.
geocodes_ori = np.unique(np.concatenate((data['CODMUNDV_A'],data['CODMUNDV_B'])))




#VAR05 is the fluvial flow
#VAR06 is the terrestrial flow 
for var_flow in ['VAR05', 'VAR06']:
	geocodes = geocodes_ori

	if var_flow == 'VAR05':
		net_name = 'fluvial'
	else:
		net_name = 'terrestrial'

	# Montar a matriz dos fluxos
	N = len(geocodes)
	flow_matrix = np.zeros((N,N))

	# inserindo os fluxos nas respectivas linhas e colunas
	for i in range(len(data)):
		lin = np.where(geocodes == data['CODMUNDV_A'][i])[0][0]
		col = np.where(geocodes == data['CODMUNDV_B'][i])[0][0]

		flow_matrix[lin,col] = data[var_flow][i]


	# Remover nós com geocódigo maior do que 5300108 (Brasília), pois eles pertencem a cidades estrangeiras
	# Indices do array com os geocódigos a serem removidos
	idx_to_remove = [idx for idx in range(len(geocodes)) if geocodes[idx] > 5300108]

	# Remover linhas de colunas da matrix de fluxo e no array de geocodigos, nestes índices
	geocodes = np.delete(geocodes, idx_to_remove)
	flow_matrix = np.delete(flow_matrix, idx_to_remove, axis=0) # rows
	flow_matrix = np.delete(flow_matrix, idx_to_remove, axis=1) # cols
	N = len(geocodes)


	# Dados das cidades brasileiras: geocódigo, nome do município, coordenadas geográficas
	cities_data = pd.read_csv('data/cities_data.csv', delimiter=',')

	# Considerando apenas os geocodigos presentes na rede
	cities_data = cities_data[cities_data.CODMUNDV.isin(geocodes)]

	# Garantindo que os geocodigos estão ordenados neste dataframe
	cities_data = cities_data.sort_values(['CODMUNDV'],ascending=True)
	cities_data = cities_data.reset_index(drop=True)


	# Criar Rede. 
	#g = ig.Graph.Adjacency((flow_matrix > 0).tolist())
	#g.to_undirected()
	g = ig.Graph.Weighted_Adjacency(flow_matrix.tolist(), attr="weight", mode=ig.ADJ_MAX) 
	g.to_undirected()

	# Add edge weights, node labels and coordinates.
	#g.es['weight'] = flow_matrix[flow_matrix.nonzero()]
	g.vs['geocode'] = geocodes
	# Se não quiser que os nomes dos municípios apareçam nos nós, basta comentar a linha abaixo.
	g.vs['label'] = np.array(cities_data['NOMEMUN'])
	g.vs['X'] = np.array(cities_data['X'])
	g.vs['Y'] = np.array(cities_data['Y'])


	# Remover singletons (nós de grau zero)
	# Se quiser manter os singletons, basta comentar as próximas 7 linhas desta célula
	singletons_idx = [v.index for v in g.vs if v.degree() == 0]
	g.delete_vertices(singletons_idx)
	geocodes = np.delete(geocodes, singletons_idx)
	flow_matrix = np.delete(flow_matrix, singletons_idx, axis=0) # rows
	flow_matrix = np.delete(flow_matrix, singletons_idx, axis=1) # cols
	N = len(geocodes)
	print("  " + net_name + " - N =",N)


	# Tamanho do nó dependendo do grau
	node_size = g.degree()

	# normalization
	node_size = np.array(node_size)
	max_size = max(node_size)
	min_size = min(node_size)

	# Tamanhos mínimo e máximo dos nós no plot
	T_min = 2
	T_max = 15
	node_size = T_min + ( (node_size - min_size) / (max_size - min_size) ) * (T_max - T_min) # normalizacao dos valores
	# Salvando novos tamanhos
	g.vs["size"] = node_size.tolist()


	# Plotting the network
	layout = []
	for i in range(g.vcount()):
		layout.append( (g.vs[i]["X"],g.vs[i]["Y"]*(-1)) )


	g.vs["label_size"] = 2


	# create plotting styles
	visual_style = {}
	visual_style["vertex_size"] = g.vs["size"]
	visual_style["edge_width"] = 0.5
	visual_style["layout"] = layout
	visual_style["bbox"] = (500, 500)
	visual_style["margin"] = 30


	ig.plot(g, "output/" + net_name + ".pdf", **visual_style)
	ig.plot(g, "output/" + net_name + ".png", **visual_style)

	g.write_graphml("output/" + net_name + ".GraphML")