import glob
import hashlib
import pickle
import os

class LayoutCache:
	def __init__(self, graph_dir):
		self.layout_dir = graph_dir + 'layouts/'
		try:
			os.makedirs(self.layout_dir)
		except FileExistsError:
			pass


	def __getitem__(self, graph):
		# So we are going to have to make the thing...

		# THIS GETITEM WILL TAKE A GRAPH, HASH IT, and check the cache...!
		return "You wanted the " + str(attr) + " but we haven't got one yet"

	def __contains__(self, graph):
		if self._hash_graph(graph) in self.cached_layouts:
			return True
		return False


	def _hash_graph(self, graph):
		graph_ids_string = " ".join([view.vp["_graphml_vertex_id"][v] for v in view.vertices()] + 
			[view.ep["_graphml_edge_id"][e] for e in view.edges()])
		graph_hash = hashlib.md5(graph_ids_string.encode('utf-8')).hexdigest()
		return graph_hash

	@property
	def cached_layouts(self):
		return [f.replace(self.layout_dir, "").replace(".layout", "") 
									for f in glob.glob(self.layout_dir + "*.layout")]



layoutCache = LayoutCache('graph_data/')
print(type(layoutCache))