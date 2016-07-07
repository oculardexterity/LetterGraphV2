from collections import OrderedDict
from flask import Flask, render_template, request
from graph_tool.all import *
import hashlib
import json
import io
import numpy
import time

from config import Config
from eXistWrapper.wrapper import ExistWrapper
from GraphUtils import join_graphs
from LayoutCache import LayoutCache



# Initialise app
app = Flask(__name__)

numpy.random.seed(42)
graph_tool.seed_rng(42) 

exist = ExistWrapper(Config().existURI)
graphData = exist.buildGraphML("buildGraphGt.xql")
initialGraph = graph_tool.load_graph(io.StringIO(graphData), fmt='graphml')
layoutCache = LayoutCache('graph_data/')
print(layoutCache[initialGraph])


@app.route("/")
def index():
	return render_template('testLinkurious.html')

@app.route("/testgraph")
def testgraph():
	return render_template('testtest.html')



@app.route('/ajax/letter/<int:letterId>/')
def letterAjax(letterId):
	try:
		if request.args.get('searchTerm'):
			print('getting letter with searchterm ')
			return exist.letter(letterId, request.args.get('searchTerm'))
		else:
			print('getting letter without searchterm')
			return exist.letter(letterId)
	except:
		return "NO LETTER OF THAT ID"


@app.route('/ajax/defaultGraph')
def defaultGraph():
	start = time.clock()
	# Need to rebuild initial graph otherwise fails to reset...
	initialGraph = graph_tool.load_graph(io.StringIO(graphData), fmt='graphml')
	
	# Rewrite this caching balls --- actually plan a better plan!!!
	# Load and cache graph -- ??
	graph = initialGraph
	print(request.args)
	
	'''	
		Ok, so here we need some form of graph dispatch-y bugger


	'''
	if request.args.get('graphIncludes'):
		includes = request.args.get('graphIncludes').split(',')

		if 'repo' in includes:
			print('repo in includes')

			# Use some naming convention here::: i.e. make a script in eXist matching this name
			# and then iterate over the `includes` list (with a try-except for missing scripts)
			addData = exist.buildGraphML('repo' + '.xql')
			addGraph = graph_tool.load_graph(io.StringIO(addData), fmt='graphml')
			graph = join_graphs(graph, addGraph)
	
	if request.args.get('searchTerm'):
		searchTerms = request.args.get('searchTerm').split(';')

		for searchTerm in searchTerms:
			print(searchTerm)

			addData = exist.buildGraphML('searchTerm.xql?searchString=' + searchTerm)
			addGraph = graph_tool.load_graph(io.StringIO(addData), fmt='graphml')
			graph = join_graphs(graph, addGraph)
	
	#l = graph_tool.draw.sfdp_layout(g, mu=0.1, mu_p=4.0, C=0.9, init_step=1, verbose=True, pos=initial_pos(g))
	end = time.clock()
	print('buiding graph time', end-start)


	return graph_to_linkurious_json(graph, layoutCache[graph])


@app.route('/ajax/graph')
def graph():
	pass
	# Build some shitting arg parser and format------!!!!


# Graph function





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


if __name__ == '__main__':
    app.run(debug=True)

    
