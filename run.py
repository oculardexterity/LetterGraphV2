from collections import OrderedDict
from graph_tool.all import *
import json
import io
import numpy
import time

from config import Config
from eXistWrapper.wrapper import ExistWrapper
from GraphUtils import join_graphs
from LayoutCache import LayoutCache

import jinja2

import tornado.concurrent
import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.template
import tornado.web

from tornado_jinja2 import Jinja2Loader





numpy.random.seed(42)
graph_tool.seed_rng(42) 

exist = ExistWrapper(Config().existURI)
graphData = exist.buildGraphML("buildGraphGt.xql")
initialGraph = graph_tool.load_graph(io.StringIO(graphData), fmt='graphml')
layoutCache = LayoutCache('graph_data/')


executor = tornado.concurrent.futures.ThreadPoolExecutor(8)



# Make app function; called from __main__
def make_app():
	jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates/'), autoescape=False)
	jinja2_loader = Jinja2Loader(jinja2_env)
	settings = {'template_loader': jinja2_loader,
				'static_path': 'static/',
				'static_url_prefix': '/static/'

				}
	return tornado.web.Application(
    	[
        (r"/", SinglePageAppHandler),
        (r"/ajax/letter/(\d*)", LetterHandler),
        (r"/ajax/defaultGraph", GraphHandler)
    ], debug=False, **settings)





class SinglePageAppHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('testLinkurious.html')

# Get letter html from exist -- synchronous
class LetterHandler(tornado.web.RequestHandler):
	@tornado.gen.coroutine
	def get(self, letterId):
		searchTerm = self.get_argument('searchTerm', default=None)
		try:
			self.write(exist.letter(letterId, searchTerm))
		except:
			raise tornado.web.HTTPError(404)
		self.finish()


class GraphHandler(tornado.web.RequestHandler):
	@tornado.gen.coroutine
	def get(self):

		# Grab initial graph
		initialGraph = graph_tool.load_graph(io.StringIO(graphData), fmt='graphml')
		graph = initialGraph

		# Add in graphincludes
		graphIncludes = self.get_argument('graphIncludes', default=None)
		if graphIncludes:
			includes = graphIncludes.split('|')
			#### Turn this into a for-loop, with appropriately named exist queries??
			if 'repo' in includes:
				addData = exist.buildGraphML('repo' + '.xql')
				addGraph = graph_tool.load_graph(io.StringIO(addData), fmt='graphml')
				graph = join_graphs(graph, addGraph)
		
		# Add in search terms
		searchTerm = self.get_argument('searchTerm', default=None)
		if searchTerm:
			searchTerms = searchTerm.split('|')
			for st in searchTerms:
				print(st)
				addData = exist.buildGraphML('searchTerm.xql?searchString=' + st)
				addGraph = graph_tool.load_graph(io.StringIO(addData), fmt='graphml')
				graph = join_graphs(graph, addGraph)

		layout = yield executor.submit(self.get_layout, graph)

		###########
		self.write(graph_to_linkurious_json(graph, layout))
		self.finish()

	# Layout wrapper function to run in some other thread
	def get_layout(self, graph):
		return layoutCache.getLayout(graph)



"""
Bump off these functions into GraphUtils!!!
"""
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


def main():
	server = tornado.httpserver.HTTPServer(make_app())
	server.bind(5000)
	print("Tornado server started\nCPU count:", tornado.process.cpu_count())
	server.start(0)  # autodetect number of cores and fork a process for each
	tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()

    
