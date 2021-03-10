# TODO Fix
import sys
sys.path.append("..") 

from settings import Cluster

class SupermucNG(Cluster):
    def get_partition(self, num_nodes):
        # Never use test!
        if 1 <= num_nodes <= 16:
            return 'micro'
        if 17 <= num_nodes <= 768:
            return 'general'
        if 769 <= num_nodes <= 3072:
            return 'large'
        raise ValueError('Unsupported number of nodes')
    
    def get_cores_per_node(self):
        return 48
    
    def get_hyperthreading_factor(self):
        return 2
