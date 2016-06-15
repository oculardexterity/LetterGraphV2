from bunch import Bunch
import yaml

class Config(Bunch):
	'''Config class: loads config.yaml into bunch dict for dot-notation access'''
	def __init__(self):
		with open("config.yaml") as f:
			super().__init__(yaml.load(f.read()))