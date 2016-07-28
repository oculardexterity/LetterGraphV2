
from graph_tool.all import *
import io
import numpy
import os
import time

from config import Config
from eXistWrapper.wrapper import ExistWrapper
import GraphUtils
from LayoutCache import LayoutCache

import jinja2

import tornado.concurrent
import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.template
import tornado.web

from tornado_jinja2 import Jinja2Loader


from memory_profiler import profile


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
			print("searchterm:", searchTerm)
			self.write(exist.letter(letterId, searchTerm))
		except:
			raise tornado.web.HTTPError(404)
		self.finish()


class GraphHandler(tornado.web.RequestHandler):
	@profile
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
				print('\n\n#####################\n JOINING REPO GRAPH\n#######################')
				graph = GraphUtils.join_graphs(graph, addGraph)
		
		# Add in search terms
		searchString = self.get_argument('searchTerm', default=None)
		if searchString:
			searchTerms = searchString.split('|')
			for st in searchTerms:
				addData = exist.buildGraphML('searchTerm.xql?searchString=' + st)
				print('\n\n#####################\n JOINING ST', st, 'GRAPH\n#######################')
				addGraph = graph_tool.load_graph(io.StringIO(addData), fmt='graphml')
				graph = GraphUtils.join_graphs(graph, addGraph)

		layout = yield executor.submit(self.get_layout, graph)

		###########
		self.write(GraphUtils.graph_to_linkurious_json(graph, layout))
		self.finish()

	# Layout wrapper function to run in some other thread

	def get_layout(self, graph):
		return layoutCache.getLayout(graph)



"""
Bump off these functions into GraphUtils!!!
"""



def main():
	server = tornado.httpserver.HTTPServer(make_app())
	server.bind(5000)
	print("Tornado server started\nCPU count:", tornado.process.cpu_count())
	server.start(0)  # autodetect number of cores and fork a process for each
	tornado.ioloop.IOLoop.current().start()
	print(os.getpid())


if __name__ == '__main__':
    main()

    
