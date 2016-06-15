from config import Config
import graph_tool.all as gt
from graph_tool.all import *

import hashlib
import json
import io
import os
import time

from eXistWrapper.wrapper import ExistWrapper
from LayoutCache import LayoutCache
from GraphUtils import hash_graph

exist = ExistWrapper(Config().existURI)




'''
{'_graphml_vertex_id': <PropertyMap object with key type 'Vertex' and value type 'string', for Graph 0x10f906940, at 0x10f86d828>, 
'type': <PropertyMap object with key type 'Vertex' and value type 'string', for Graph 0x10f906940, at 0x1252fc780>, 
'title': <PropertyMap object with key type 'Vertex' and value type 'string', for Graph 0x10f906940, at 0x1252fc7b8>, 
'node_label': <PropertyMap object with key type 'Vertex' and value type 'string', for Graph 0x10f906940, at 0x1252fc748>}


'''

'''
class GraphCache():
	def __init__(self):
		try:
			self = graph_tool.load_graph(Config().graphDataFolder + 'defaultGraph.gt', fmt='gt')
		except Exception:
			graph = exist.buildGraphML()
			self = graph_tool 

cache = GraphCache()

class GraphManager():
	def __init__(self, existDb):
		# Grab GraphML graph from exist
		graph = exist.buildGraphML()

		# Load into graph_tool
		self.g = graph_tool.load_graph(io.StringIO(graph), fmt='graphml')


	def graph():
		return self.g
'''

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
		except KeyError:
			pass
		vertex["data"] = {"type": graph.vp["type"][v],
						 "title": graph.vp["title"][v],
						 "label": graph.vp["node_label"][v],
						}
		#vertex["x"], vertex["y"] = layout[v]
		vertices.append(vertex)
	return vertices




def build_edge_list(graph):
	edges = []
	for e in graph.edges():
		edge = {"id": g.edge_properties["_graphml_edge_id"][e]}
		edge["source"], edge["target"] = graph.vp["_graphml_vertex_id"][e.source()], graph.vp["_graphml_vertex_id"][e.target()]
		edges.append(edge)
	return edges



def initial_pos(graph):
	vprop = graph.new_vertex_property("vector<double>")
	for n, v in enumerate(graph.vertices()):
		vprop[v] = n, n
	return vprop




graph = exist.buildGraphML("buildGraphGt.xql")
g = graph_tool.load_graph(io.StringIO(graph), fmt='graphml')
print(g)



verticesIds = [g.vp["_graphml_vertex_id"][v] for v in g.vertices()]
print(verticesIds)

'''
view = graph_tool.GraphView(g)



layoutCache = LayoutCache('graph_data/')
print(hash_graph(view))
print(layoutCache[view])












#view.save('graph_data.gt', fmt='gt')
#ip = initial_pos(g)


#l = 'none'

'''





