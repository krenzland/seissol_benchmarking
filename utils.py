import itertools
from pathlib import Path

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
        
def format_timedelta(delta):
    s = int(delta.total_seconds())
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)


def find_file_in_path(filename, dirs):
    print([Path(dir).resolve() for dir in dirs])
    first_found = Path()
    all_paths = []
    num_found = 0
    for dir in dirs:
        dir = Path(dir)
        if not dir.exists():
            raise FileNotFoundError(filename)
        path = (dir / filename).resolve()
        if path.exists():
            if num_found == 0:
                first_found = path
            num_found += 1
            all_paths += [path]
    
    if num_found > 1:
        print("Warning: More than one version of {} found! Namely:".format(filename))
        for path in all_paths:
            print(path)
        print()

    if num_found > 0:
        print("Returning, found:")
        print(first_found)
        return first_found
    else:
        raise FileNotFoundError(filename)
