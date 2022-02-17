# preparing dataframe for dtale
import pandas as pd
import json
import dtale
from django.shortcuts import redirect
import numpy as np
from . dict_util import change_dict_key
from . import sql_receiver, json_integrator, dict_util
from .experiment_processor import experiment_graph_generator


NAN_STRING="____n/a___not_available___"

# IP of the server. this is needed to use dtale
DTALE_SERVER_HOST_IP="133.9.195.84"


def df_to_dtale(df, pandas_mode=False):
    # drop all nan column
    df = df.dropna(how='all', axis=1)

    # drop same variable column
    df=df.fillna(NAN_STRING)
    df=df.loc[:,~(df.nunique()==1)]

    df=df.replace(NAN_STRING,np.nan)

    if pandas_mode:
        return df


    #set host ip of the server
    d = dtale.show(df, host=DTALE_SERVER_HOST_IP)
    response = redirect(d._main_url)
    return response

# prepare chemicals database as df


def generate_chemical_dtale(queryset, pandas_mode=False):
    chem_dict = sql_receiver.generate_chemical_json(
        queryset, dict_mode=True)["Chemical"]

    for compound in chem_dict:
        parse_property_and_tag(compound)

    df = pd.DataFrame.from_dict(chem_dict)
    return df_to_dtale(df, pandas_mode=pandas_mode)


def generate_mixture_dtale(queryset, pandas_mode=False):
    dict_data = sql_receiver.generate_mixture_json(queryset, dict_mode=True)
    json_integrator.param_sort(dict_data, "Mixture", "chemicals")
    mixture_list = dict_data["Mixture"]
    modif_mixture_list = []

    for mixture in mixture_list:
        # parse tags and props
        parse_property_and_tag(mixture)

        # parse inner chemicals
        if "chemicals" in mixture.keys():
            for component in mixture["chemicals"]:
                parse_property_and_tag(component["chemical"])

        # nested to plain dict
        modif_mixture = dict_util.nested_to_plain_dict(mixture)
        modif_mixture = clean_mixture_dict(modif_mixture)
        modif_mixture_list.append(modif_mixture)

    df = pd.DataFrame.from_dict(modif_mixture_list)
    return df_to_dtale(df, pandas_mode=pandas_mode)


def generate_experiment_dtale(queryset, pandas_mode=False):
    dict_data = sql_receiver.generate_experiment_json(queryset, dict_mode=True)
    parsed_data = experiment_graph_generator.generate_experiment_dict(
        dict_data, fp_mode=False)
    df = pd.DataFrame.from_dict(parsed_data).T
    return df_to_dtale(df, pandas_mode=pandas_mode)


def generate_experiment_fp_dtale(queryset, pandas_mode=False):
    dict_data = sql_receiver.generate_experiment_json(queryset, dict_mode=True)
    parsed_data, _ = experiment_graph_generator.generate_experiment_dict(
        dict_data)
    df = pd.DataFrame.from_dict(parsed_data).T
    return df_to_dtale(df, pandas_mode=pandas_mode)


# ------- util funcs  --------------

def parse_property_and_tag(compound):
    # parse properties
    if "property" in compound.keys():
        for prop_dict in compound["property"]:
            for key, value in prop_dict.items():
                if key not in ["pk", "level"]:
                    compound[f"property_{key}"] = value

        compound.pop("property")

    # parse tags
    if "tags" in compound.keys():
        tag_list = json.loads(compound["tags"].replace("'", '"'))

        for tag_dict in tag_list:
            name = tag_dict["name"]
            compound[f"tag_{name}"] = True

        compound.pop("tags")


def clean_mixture_dict(modif_mixture):
    del_list = [
        "_pk",
        "_level",
        "order",
    ]

    for key in list(modif_mixture.keys()):
        # delete unnecessary keys
        for del_name in del_list:
            if key.find(del_name) > 0:
                modif_mixture.pop(key)
        # rename
        target_name = "chemicals_"
        if key.find(target_name) == 0:
            new_key = key.replace(target_name, "C")
            new_key = new_key.replace("chemical_", "")
            change_dict_key(modif_mixture, key, new_key)
    return modif_mixture
