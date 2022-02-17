"""
parse json type experiment to graph
"""
from ..dict_util import nested_to_plain_dict
import copy
import networkx as nx

ignore_list = [
    "ID", "step""title", "project",
    "bookmark", "machine_learning",
    "experimenter",
    "created_at", "updated_at", "step"
]


def json_experiment_to_graph_dict(json_dict):

    experiment_list = extract_experiment(json_dict)
    raw_experiment_dict = {}

    for experiment in experiment_list:
        inner_dict = {}

        # add experiment attributes
        # prepare graph
        step_list = experiment["step"]
        g = nx.DiGraph()

        # header node
        g.add_node(0)
        g.nodes[0]["label"] = "Start experiment"
        for k, v in experiment.items():
            if k in ignore_list:
                continue
            g.nodes[0][k] = v

        for i in range(len(step_list)):
            pos = i+1
            step = step_list[pos-1]
            g.add_node(pos)

            # nested to plain dict for each step
            plain_dict = nested_to_plain_dict(step)
            for k, v in plain_dict.items():
                # set step attributes
                g.nodes[pos][k] = v

            # connect nodes
            g.add_edge(pos-1, pos)

        inner_dict["title"] = experiment["title"]
        inner_dict["project"] = experiment["project"]["title"]
        inner_dict["graph"] = g
        raw_experiment_dict[experiment["ID"]] = inner_dict

    return raw_experiment_dict

# delete blank fields in dict


def clean_experiment(obj):
    if type(obj) is list:
        for i in obj:
            clean_experiment(i)

    if type(obj) is dict:
        for k, v in list(obj.items()):
            if type(k) is str:
                if k in ["pk", "level", "order"]:
                    obj.pop(k)
                elif k.find("special_memo") >= 0:
                    obj.pop(k)
                elif v is None or v == "":
                    obj.pop(k)
            if type(v) is dict or type(v) is list:
                clean_experiment(v)


def extract_experiment(json_dict):
    # clean
    experiment_list = copy.copy(json_dict["Experiment"])

    for experiment in experiment_list:
        experiment["ID"] = experiment["pk"]
        clean_experiment(experiment)

    return experiment_list
