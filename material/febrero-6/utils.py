from rich import print, pretty
pretty.install()

import polars as pl
from bw2io.importers import EcoinventLCIAImporter
from pathlib import Path
from typing import List, Union
import re
import bw2data as bd
import bw2calc as bc
import bw2io as bi
import logging
from rich.console import Console
import polars as pl
from pathlib import Path
from bw2io.importers import EcoinventLCIAImporter
from bw2io.strategies import (
    drop_unspecified_subcategories,
    link_iterable_by_fields,
    normalize_units,
    rationalize_method_names,
    set_biosphere_type,
)
import functools
from bw2data import Database
console = Console()

def parse_lcia_ei_excel(lcia_file:Union[str,Path]):
    """Parses LCIA data from excel file downloaded from ecoinvent website

    Right now only works with ecoinvent 3.8

    Args:
        lcia_file: Path to the excel file containing the LCIA data
    """
    lcia_file = Path(lcia_file)
    cf_data = pl.read_excel(lcia_file, sheet_name="CFs").select(
        pl.concat_list(['Method','Category','Indicator']).alias("method"),
        pl.col('Name').alias('name'),
        pl.col(['Compartment','Subcompartment']),
        # pl.concat_list(["Compartment", "Subcompartment"]).alias("categories"),
        pl.col("CF").alias("amount")
                ).to_dicts()
    biosphere_nodes = []
    
    for row in cf_data:
        if row['Subcompartment'] in [None, 'unspecified']:
            category = (row['Compartment'], )
        else:
            category = (row['Compartment'],row['Subcompartment'])
        
        row['categories']= category
        biosphere_nodes.append((row["name"],category)) 
    biosphere_nodes = set(biosphere_nodes)

    for row in cf_data:
        row['method'] = tuple(row['method'])
        row['categories'] = tuple(row["categories"])

    units = pl.read_excel(lcia_file,sheet_name="Indicators").select(
        pl.concat_list(['Method','Category','Indicator']).alias("method"),
        pl.col("Indicator Unit"),
                    ).to_dict(as_series=False)
    units['method'] = [tuple(i) for i in units["method"]]
    units = dict(zip(units['method'],units["Indicator Unit"]))
    return cf_data, units, biosphere_nodes

from typing import Tuple, List
from bw2data.errors import UnknownObject
def biosphere_node_creator(biosphere_name:str, nodes: List[Tuple[str,Tuple[str, Union[None,str]]]]):
    """Creates a new biosphere node without much details, node looks like this:
    (<name>, (<category_1>,<category_2>))    
    """
    for node in nodes:
        try:
            bd.get_node(
                database=biosphere_name,
                name=node[0],
                categories=node[1]
                    )
            console.print(f"[green] :white_check_mark: Node {node[0]} already exists, passing [/]")
        except UnknownObject:
            bd.Database(biosphere_name).new_activity(
                    name=node[0],
                    unit='kilogram',
                    code=(node[0]+"-"+str(node[1])),
                    categories=node[1],
                    type='emission'
                    ).save()
            console.print(f"[dark_orange] :warning: Node `{node[0]}` does not exist, creating new one... [/]")

class myEcoinventLCIAImporter(EcoinventLCIAImporter):

    def __init__(self, cf_data:List[dict], units:dict,file_name:str, biosphere_database:Union[str, None]):
            """Initialize a customized instance of EcoinventLCIAImporter.
            """
            self.strategies = [
                normalize_units,
                set_biosphere_type,
                drop_unspecified_subcategories,
                functools.partial(
                    link_iterable_by_fields,
                    other=Database(biosphere_database),
                    fields=("name", "categories"),
                ),
            ]
            self.applied_strategies = []
            self.cf_data = cf_data
            self.units = units
            self.file = file_name
            self.separate_methods()

def custom_methods_importer(lcia_file:Union[str,Path],biosphere_name:str,overwrite:bool=False):
    """Imports methods and required biosphere node for custom list of methods from excel file"""
    lcia_file = Path(lcia_file)
    cf_data, units, biosphere_nodes = parse_lcia_ei_excel(lcia_file)
    biosphere_node_creator(biosphere_name, biosphere_nodes)
    methods = myEcoinventLCIAImporter(cf_data=cf_data, units=units,
                        file_name=lcia_file.name,
                        biosphere_database=biosphere_name)
    methods.apply_strategies()
    methods.statistics()
    methods.write_excel('errors_custom_lcia')
    methods.write_methods(overwrite=overwrite)

# TODO: This is a custom biosphere installer
# def setup_biosphere(filepath, lcia_file):
#     biosphere_name = f"biosphere3"
#     if biosphere_name in bd.databases:
#         print('biosphere already installed, removing and installing again')
#         del bd.databases[biosphere_name]
#     ei_bio = bi.importers.Ecospold2BiosphereImporter(
#         name = f"{biosphere_name}",
#     )
#     filepath=Path(filepath)
#     ei_bio.apply_strategies()
#     ei_bio.write_database(overwrite=False)
#     lcia_file = Path(lcia_file)
    
#     cf_data, units, biosphere_nodes = parse_lcia_ei_excel(lcia_file)
    
#     ei = myEcoinventLCIAImporter(cf_data=cf_data, units=units,
#                                  file_name=lcia_file.name,
#                                  biosphere_database=biosphere_name)

#     if rationalize_method_names:
#         ei.add_rationalize_method_names_strategy()
#     ei.apply_strategies()
#     ei.drop_unlinked()
#     ei.write_methods(overwrite=True)

