"""
"""

import os
from pathlib import Path

from oemof.solph import EnergySystem, Model, processing

# DONT REMOVE THIS LINE!
from oemof.tabular import datapackage  # noqa
from oemof.tabular.constraint_facades import CONSTRAINT_TYPE_MAP
from oemof.tabular.facades import TYPEMAP
from oemof.tabular.postprocessing import calculations, core

# scenario definition
SCENARIO = "eprom"
DATAPACKAGES_PATH = Path(__file__).parent
SCENARIO_DATAPACKAGE = DATAPACKAGES_PATH / SCENARIO / "datapackage.json"
RESULTS_PATH = Path(__file__).parent / "oemof-results"

# create energy system object
es = EnergySystem.from_datapackage(
    str(SCENARIO_DATAPACKAGE),
    attributemap={},
    typemap=TYPEMAP,
)

# create model from energy system (this is just oemof.solph)
m = Model(es)

# add constraints from datapackage to the model
m.add_constraints_from_datapackage(
    str(SCENARIO_DATAPACKAGE),
    constraint_type_map=CONSTRAINT_TYPE_MAP,
)

# if you want dual variables / shadow prices uncomment line below
# m.receive_duals()

# select solver 'gurobi', 'cplex', 'glpk' etc
m.solve("cbc")

es.params = processing.parameter_as_dict(es)
es.results = m.results()
# now we use the write results method to write the results in oemof-tabular
# format
postprocessed_results = calculations.run_postprocessing(es)
postprocessed_results.to_csv(str(RESULTS_PATH / "results.csv"))


#calculator = core.Calculator(es.params, es.results)
#aggregated_flows = calculations.AggregatedFlows(calculator, from_nodes=["heat-pump", "solar-thermal"], resample_mode="1min").result
#aggregated_flows.to_csv('test.csv')
#print(aggregated_flows)