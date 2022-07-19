# TODO Fix
import sys
sys.path.append("..") 

from settings import Cluster

class Mahti(Cluster):
    def get_partition(self, num_nodes):
        # Never use test!
        if 1 <= num_nodes <= 20:
            return 'medium'
        if 20 < num_nodes <= 200:
            return 'large'
        if 200 < num_nodes <= 700:
            return 'gc'
        raise ValueError('Unsupported number of nodes')
    
    def get_cores_per_node(self):
        return 128
    
    def get_hyperthreading_factor(self):
        return 2
