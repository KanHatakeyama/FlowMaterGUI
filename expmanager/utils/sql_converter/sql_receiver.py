import json
from django.core import serializers
from datetime import date, datetime
from ... import models
from . import query_parser
from . import json_integrator


def generate_general_json(queryset, dict_func, dict_mode=False):
    parsed_dict = get_mutual_dict()
    dict_func(queryset, parsed_dict)
    query_parser.partial_string_to_complete_dict(parsed_dict)
    parsed_dict = json_integrator.auto_json_to_graph_experiment(parsed_dict)
    if dict_mode:
        return parsed_dict
    return json.dumps(parsed_dict, default=json_serial)


def generate_chemical_json(queryset, dict_mode=False):
    return generate_general_json(queryset, query_parser.generate_chemical_dict, dict_mode=dict_mode)


def generate_mixture_json(queryset, dict_mode=False):
    return generate_general_json(queryset, query_parser.generate_mixture_dict, dict_mode=dict_mode)


def generate_experiment_json(queryset, dict_mode=False):
    return generate_general_json(queryset, query_parser.generate_experiment_dict, dict_mode=dict_mode)


# utils
def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def get_mutual_dict():
    parsed_dict = {}
    obj_list = [
        "MutualKey", "Project", "Tag",
        "PropertyName",
    ]

    for obj_name in obj_list:
        obj = getattr(models, obj_name)
        obj = obj.objects.filter().order_by()
        str_content = serializers.serialize("json", obj)
        parsed_dict[obj_name] = str_content

    return parsed_dict
