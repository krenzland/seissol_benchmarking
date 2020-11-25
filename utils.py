import itertools

def product_dict(**kwargs):
    # From https://stackoverflow.com/a/5228294
    keys = kwargs.keys()
    vals = kwargs.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))

def dict_subset_eq(a, b):
    for k, v in a.items():
        #print(k, a[k], b[k])
        if (a[k] != b[k]):
            return False
    return True

def dict_subset_idx_in_list(dictionary, l):
    for i, e in enumerate(l):
        if dict_subset_eq(dictionary, e):
            return i
    return -1
        
