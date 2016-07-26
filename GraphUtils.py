from graph_tool.all import *
import hashlib
from collections import OrderedDict
import json

def hash_graph(graph):
	"""
		Takes a graph_tool Graph() or GraphView() object, concatenates vertex and edge IDs
		to a string and returns an md5 hash of said string.
	"""
	#return graph # Override the hashing -- useful for testing by passing string straight through
	graph_ids_string = " ".join([graph.vp["_graphml_vertex_id"][v] for v in graph.vertices()] + 
		[graph.ep["_graphml_edge_id"][e] for e in graph.edges()])
	graph_hash = hashlib.md5(graph_ids_string.encode('utf-8')).hexdigest()
	return graph_hash


def join_graphs(main, sub):

	# Generate id_to_vertex_map for main graph
	id_to_vertex_map = {main.vp["_graphml_vertex_id"][v]: v for v in main.vertices()}
	missing_props = [k for k, _ in sub.vp.items() if k not in [j for j, _ in main.vp.items()]]
	
	for prop in missing_props:
		new_prop = main.new_vertex_property("string")
		main.vp[prop] = new_prop

	# Iterate sub_graph vertices
	for sub_vertex in sub.vertices():
		
		# Add node to graph if not already there
		if sub.vp["_graphml_vertex_id"][sub_vertex] not in id_to_vertex_map:
			print('adding new node:', sub.vp["_graphml_vertex_id"][sub_vertex])
			main_vertex = main.add_vertex()

			# Add vertex properties to map
			for prop in [k for k, _ in sub.vp.items()]:
				
				main.vp[prop][main_vertex] = sub.vp[prop][sub_vertex]

		###### ADD MORE DATA TO EXISTING NODES??? Useful for adding KWIC info.

		## This for some reason not being run...!
		if sub.vp["_graphml_vertex_id"][sub_vertex] in id_to_vertex_map:
			main_vertex = id_to_vertex_map[sub.vp["_graphml_vertex_id"][sub_vertex]]	
			print('already node:', sub.vp["_graphml_vertex_id"][sub_vertex])
			# Does a join of search_kwic rather than overwriting!
			if 'search_kwic' in sub.vp and sub.vp['search_kwic'][sub_vertex]:
				print('kwic there', sub.vp["_graphml_vertex_id"][sub_vertex])
				if main.vp['search_kwic'][main_vertex]:
					main_kwic_str = main.vp['search_kwic'][main_vertex]
				else:
					main_kwic_str = ''
				main.vp['search_kwic'][main_vertex] = main_kwic_str + '<p class="kwic">' + sub.vp['search_kwic'][sub_vertex]
				

			
			for prop in missing_props:
				main.vp[prop][main_vertex] = sub.vp[prop][sub_vertex]
				
		
			
		

	# Regenerate id_to_vertex_map to included added vertices -- make into function
	id_to_vertex_map = {main.vp["_graphml_vertex_id"][v]: v for v in main.vertices()}
	
	for sub_edge in sub.edges():
		# THE LINE BELOW NOT ADDING THE *ACTUAL* MAIN EDGE, BUT A SUBEDGE REF... Another fucking lookup??

		sub_edge_source_id = sub.vp["_graphml_vertex_id"][sub_edge.source()]
		sub_edge_source = id_to_vertex_map[sub_edge_source_id]

		sub_edge_target_id = sub.vp["_graphml_vertex_id"][sub_edge.target()]
		sub_edge_target = id_to_vertex_map[sub_edge_target_id]

		main_edge = main.add_edge(sub_edge_source, sub_edge_target)
		for prop in [k for k, _ in sub.ep.items()]:
			try:
				main.ep[prop][main_edge] = sub.ep[prop][sub_edge]
			except KeyError:
				pass
	return main


def initial_pos(graph):
	vprop = graph.new_vertex_property("vector<double>")
	for n, v in enumerate(graph.vertices()):
		vprop[v] = n, n
	return vprop


def build_vertices_list(graph, layout):
	vertices = []
	for v in graph.vertices():
		vertex = {"id": graph.vp["_graphml_vertex_id"][v]}
		try:
			vertex["label"] = graph.vp["node_label"][v]
		except KeyError:
			pass
		try:
			vertex["color"] = graph.vp["color"][v]
			vertex["originalColor"] = graph.vp["color"][v]
			vertex["lighten_color"] = graph.vp["lighten_color"][v]
		except KeyError:
			pass

		# Shape of node
		vertex['size'] = 0.5
		vertex["data"] = {
						"type": graph.vp["type"][v],
						 "title": graph.vp["title"][v],
						 "label": graph.vp["node_label"][v],
						}
		try:
			vertex["data"]["letterId"] = graph.vp["letterId"][v]
			vertex["data"]["search_kwic"] = graph.vp["search_kwic"][v]
		except KeyError:
			pass
		vertex["x"], vertex["y"] = layout[v]
		vertices.append(vertex)
	return vertices


def build_edge_list(graph, edges_omit_list=None):
	edges = []
	for e in graph.edges():
		edge = {"id": graph.edge_properties["_graphml_edge_id"][e]}
		edge["source"], edge["target"] = graph.vp["_graphml_vertex_id"][e.source()], graph.vp["_graphml_vertex_id"][e.target()]
		edge["type"] = 'arrow'
		edges.append(edge)
	return edges


def graph_to_linkurious_json(graph, layout, edges_omit_list=None):
	json_graph = OrderedDict()
	json_graph['nodes'] = build_vertices_list(graph, layout)
	json_graph['edges'] = build_edge_list(graph, edges_omit_list)
	return json.dumps(json_graph)
