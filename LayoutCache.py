from GraphUtils import hash_graph

from graph_tool.all import *
import glob
import pickle
import os
import time

class LayoutCache:
	def __init__(self, graph_dir, purge=False):
		self.layout_dir = graph_dir + 'layouts/'
		try:
			os.makedirs(self.layout_dir)
		except FileExistsError:
			pass




	def __getitem__(self, graph):
		start = time.clock()
		# Maybe make it possible to throw a graph or a hash to this?
		# No idea how to do it... typecheck?? If type(str) and len(graph) == md5-hash-length??
		graph_hash = hash_graph(graph)
		end = time.clock()
		print('graph hash time ', end-start)
		if graph_hash in self.cached_layouts:
			print('Loading layout ' +  graph_hash + ' from cache')
			layout = pickle.load(open(self.layout_dir + graph_hash + ".layout", "rb"))
			return layout
		else:
			print('Building new layout for ' + graph_hash)

			# Don't like this layout being here... but then again, all I'd do is subclass my own layout...
			# which would just pass data onwards...

			# BUT BUT this needs to be called asynchronously, right?
			layout = graph_tool.draw.sfdp_layout(graph, gamma=4.0, mu=20.0, mu_p=10.0, C=2, verbose=True)
			
			try:
				pickle.dump(layout, open(self.layout_dir + graph_hash + ".layout", "wb" ))
			except Exception as e:
				print(e, 'ERROR THROWING HERE....!!!')
			return layout


	def __contains__(self, graph):
		if hash_graph(graph) in self.cached_layouts:
			return True
		return False


	@property
	def cached_layouts(self):
		return [f.replace(self.layout_dir, "").replace(".layout", "") 
									for f in glob.glob(self.layout_dir + "*.layout")]




	

if __name__ == "__main__":
	# some testing stuff here
	layoutCache = LayoutCache('graph_data/')
	print('test' in layoutCache)
	print(layoutCache['test'])