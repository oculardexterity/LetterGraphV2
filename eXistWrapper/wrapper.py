import json
import requests


class ExistWrapper:
	def __init__(self, existURI):
		self.connection = existURI

	def run(self, suff):
		run_string = self.connection + suff
		r = requests.get(run_string)
		if "<null></null>" not in r.text:
			return r.text
		else:
			raise(Exception)

	def letter(self, req, searchTerm=None):
		if searchTerm:
			print('calling with searchterm')
			letter = self.run("letterPlusSearchTerm.xql?letter=" + str(req) + '&searchTerm=' + searchTerm)
			print(letter)
			return letter
		else:
			print('calling without searchterm')
			return self.run("letter.xql?letter=" + str(req))
	def buildGraphML(self, eXistScript):
		return self.run(eXistScript)