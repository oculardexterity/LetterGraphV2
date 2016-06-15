from graph_tool.all import *
import hashlib

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
	'''
	This function is going to be REALLY slow...(no it's not slow) which means can't cache graphs based on hash
	-> Can't cache graphs based on graph hash anyway, because it's well stupid...
	- have to create the whole graph to be able to hash it.
	ie.. HASH query params...
	....... I wonder if FLASK will do this? -- no it won't do this; query params not cached...
	'''
	#print('old graph and sub')
	#print(main)
	#print(sub)

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
			main_vertex = main.add_vertex()

			# Add vertex properties to map
			for prop in [k for k, _ in sub.vp.items()]:
				main.vp[prop][main_vertex] = sub.vp[prop][sub_vertex]

		###### ADD MORE DATA TO EXISTING NODES??? Useful for adding KWIC info.

		## This for some reason not being run...!
		if sub.vp["_graphml_vertex_id"][sub_vertex] in id_to_vertex_map:
			for prop in missing_props:
				
				main_vertex = id_to_vertex_map[sub.vp["_graphml_vertex_id"][sub_vertex]]
				
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
	#print("new graph...")
	#print(main)
	return main
