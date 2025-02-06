import polars as pl
from bw2io.importers import EcoinventLCIAImporter
from pathlib import Path
from typing import List, Union


def parse_lcia_ei_excel(lcia_file:Path):
    """Parses LCIA data from excel file downloaded from ecoinvent website

    Right now only works with ecoinvent 3.8

    Args:
        lcia_file: Path to the excel file containing the LCIA data
    """
    cf_data = pl.read_excel(lcia_file, sheet_name="CFs").select(
        pl.concat_list(['Method','Category','Indicator']).alias("method"),
        pl.col('Name').alias('name'),
        pl.concat_list(["Compartment", "Subcompartment"]).alias("categories"),
        pl.col("CF").alias("amount")
                ).to_dicts()

    for row in cf_data:
        row['method'] = tuple(row['method'])
        row['categories'] = tuple(row["categories"])

    units = pl.read_excel(lcia_file,sheet_name="Indicators").select(
        pl.concat_list(['Method','Category','Indicator']).alias("method"),
        pl.col("Unit"),
                    ).to_dict(as_series=False)
    units['method'] = [tuple(i) for i in units["method"]]
    units = dict(zip(units['method'],units["Unit"]))
    return cf_data, units


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

# ei = myEcoinventLCIAImporter(cf_data=cf_data, units=units,
#                              file_name=lcia_file.name,
#                              biosphere_database=biosphere_name)

# if rationalize_method_names:
#     ei.add_rationalize_method_names_strategy()
# ei.apply_strategies()
# ei.drop_unlinked()
# ei.write_methods(overwrite=False)

