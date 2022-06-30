import sys
sys.path.append("..") 

from settings import Cluster

class Fugaku(Cluster):
    def get_partition(self, num_nodes):
        return 'small'
        raise ValueError('Unsupported number of nodes')
    
    def get_cores_per_node(self):
        return 48
    
    def get_hyperthreading_factor(self):
        return 1
