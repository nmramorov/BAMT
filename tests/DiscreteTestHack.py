import time

start = time.time()

# FIX IT
import sys
import os
path = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.insert(0, path)
#---------

from bamt.Preprocessors import Preprocessor
import pandas as pd
from sklearn import preprocessing as pp
from bamt import Networks
from pgmpy.estimators import K2Score
from bamt.utils import GraphUtils as gru

p1 = time.time()
print(f"Time elapsed for importing: {p1 - start}")

data = pd.read_csv(r"../data/hack_processed_with_rf.csv")[['Tectonic regime', 'Period', 'Lithology', 'Structural setting']]

p2 = time.time()
print(f"Time elapsed for uploading data: {p2 - p1}")

encoder = pp.LabelEncoder()
discretizer = pp.KBinsDiscretizer(n_bins=5, encode='ordinal', strategy='uniform')

p = Preprocessor([('encoder', encoder), ('discretizer', discretizer)])

nodes_type_mixed = gru.nodes_types(data)

discretized_data, est = p.apply(data)  # info
info = p.info

bn = Networks.DiscreteBN()
bn.add_nodes(descriptor=info)

params = {'init_nodes': None,
          'bl_add': None}
bn.add_edges(data=discretized_data, optimizer='HC', scoring_function=('K2', K2Score), params=params)
bn.get_info()
t1 = time.time()
bn.fit_parameters(data=data)
t2 = time.time()
print(f'PL elaspsed: {t2 - t1}')

# for num, el in enumerate(bn.sample(20), 1):
#     print(f"{num: <5}", [el[key] for key in list(bn.distributions.keys())[0:8]])

# for num, el in enumerate(bn.sample(10), 1):
#     print('\n', num)
#     for name, val in el.items():
#         print(f"{name: <15}", val)

bn.plot('Discrete')