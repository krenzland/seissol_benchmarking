# TODO Fix
import sys
sys.path.append("..") 

from settings import Cluster

class Frontera(Cluster):
    def get_partition(self, num_nodes):
        if 1 <= num_nodes <= 2:
            return 'development'
        if 3 <= num_nodes <= 512:
            return 'normal'
        if 513 <= num_nodes <= 2048:
            return 'large'
        raise ValueError('Unsupported number of nodes')
    
    def get_cores_per_node(self):
        return 56
    
    def get_hyperthreading_factor(self):
        return 1

    def is_slurm_array_supported(self):
        return False
