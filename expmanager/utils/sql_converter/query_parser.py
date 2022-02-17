from expmanager.models import Step
from expmanager.models import Experiment, ExperimentFile
from expmanager.models import Property, PropertyChem, PropertyMixture
from expmanager.models import Chemical, ChemicalFile
from expmanager.models import Mixture, MixtureComponent, MixtureFile
from django.core import serializers
import json


def get_serialized_str(queryset):
    return serializers.serialize("json", queryset)


def append_serialized_str(queryset, model_name, master_dict={}):
    if model_name not in master_dict.keys():
        master_dict[model_name] = []

    # get inline queries
    for query in queryset:
        additional_query = get_serialized_str([query])
        master_dict[model_name].append(additional_query)


def parse_inline_query(queryset,
                       master_dict={},
                       son_model=Step,
                       ):
    son_model_name = get_model_name(son_model)

    if son_model_name not in master_dict.keys():
        master_dict[son_model_name] = []

    # get inline queries
    for query in queryset:
        query_pk = query.pk
        son_queryset = son_model.objects.filter(level_id=query_pk)
        append_serialized_str(
            son_queryset, get_model_name(son_model), master_dict)
        # son_additional_queries=get_serialized_str(son_queryset)
        # master_dict[son_model_name].append(son_additional_queries)

    return master_dict


def generate_chemical_dict(queryset, master_dict={}):
    append_serialized_str(queryset, "Chemical", master_dict)
    parse_inline_query(queryset, master_dict, son_model=PropertyChem)
    parse_inline_query(queryset, master_dict, son_model=ChemicalFile)

    return master_dict


def generate_mixture_dict(queryset, master_dict={}):
    # master_dict["Mixture"]=get_serialized_str(queryset)
    append_serialized_str(queryset, "Mixture", master_dict)

    # get inner data
    parse_inline_query(queryset, master_dict, son_model=MixtureComponent)
    parse_inline_query(queryset, master_dict, son_model=MixtureFile)
    parse_inline_query(queryset, master_dict, son_model=PropertyMixture)
    # get chemical data
    chemical_queryset = get_grandson_queryset(
        master_dict, "MixtureComponent", Chemical, "chemical")
    generate_chemical_dict(chemical_queryset, master_dict)

    return master_dict


def generate_step_dict(queryset, master_dict={}):
    append_serialized_str(queryset, "Step", master_dict)
    parse_inline_query(queryset, master_dict, son_model=Property)

    # get inner data
    chemical_queryset = get_grandson_queryset(
        master_dict, "Step", Chemical, "chemical")
    generate_chemical_dict(chemical_queryset, master_dict)
    mixture_queryset = get_grandson_queryset(
        master_dict, "Step", Mixture, "Mixture")
    generate_mixture_dict(mixture_queryset, master_dict)

    return master_dict


def generate_experiment_dict(queryset, master_dict={}):
    append_serialized_str(queryset, "Experiment", master_dict)
    parse_inline_query(queryset, master_dict, son_model=Step)
    parse_inline_query(queryset, master_dict, son_model=ExperimentFile)
    step_queryset = get_grandson_queryset(master_dict, "Step", Step, "pk")
    generate_step_dict(step_queryset, master_dict)

    return master_dict

# utils


def get_grandson_queryset(master_dict, son_name, grandson_model, search_key):
    # temporaliry comvert string-type dict into normal dict
    son_dict_list = master_dict[son_name]
    son_dict_list = [json.loads(record)[0] for record in son_dict_list]

    grandson_pks = []
    for d in son_dict_list:
        try:
            grandson_pks.append(d["fields"][search_key])
        except:
            grandson_pks.append(d[search_key])

    grandson_queryset = grandson_model.objects.filter(pk__in=grandson_pks)
    return grandson_queryset


def partial_string_to_complete_dict(master_dict):
    for k in list(master_dict):
        list_data = master_dict[k]

        # for already formatted string json
        if type(list_data) is str:
            dict_component = json.loads(list_data)
            master_dict[k] = dict_component
            continue

        if len(list_data) < 1:
            continue
        if type(list_data[0]) is dict:
            continue

        # drop duplicated records
        list_data = list(set(list_data))

        dict_record = []
        for str_record in list_data:
            dict_component = json.loads(str_record)
            dict_record.append(dict_component[0])

        master_dict[k] = dict_record


def get_model_name(obj):
    name = str(obj)
    name = name.replace("<class 'expmanager.models.", "")
    name = name.replace("'>", "")
    return name
