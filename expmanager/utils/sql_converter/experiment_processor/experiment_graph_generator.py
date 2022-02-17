from .json_to_graph_experiment import json_experiment_to_graph_dict
from .graph_integrator import prepare_integrated_experiment_dict
from .graph_duplicator import duplicate_experiment_with_variables, obtain_global_variable_dict
from .FlowchartFP import FlowchartFP


def generate_experiment_dict(json_dict, fp_mode=True):

    integrated_experiment_dict, global_variable_dict = json_experiment_to_dict_graph(
        json_dict)

    # integrate info
    for exp_id in integrated_experiment_dict:
        integrated_experiment_dict[exp_id].update(global_variable_dict[exp_id])

    if not fp_mode:
        return integrated_experiment_dict

    # add fingerprint
    fingerprinted_experiment_dict, ffp_calculator = add_fingerprint(
        integrated_experiment_dict)

    return fingerprinted_experiment_dict, ffp_calculator


def json_experiment_to_dict_graph(json_dict):

    # json to networkX graph data
    raw_experiment_dict = json_experiment_to_graph_dict(json_dict)

    # integrated fragmented graphs
    integrated_experiment_dict = prepare_integrated_experiment_dict(
        raw_experiment_dict)

    # duplicate graphs with variables
    duplicate_experiment_with_variables(integrated_experiment_dict)

    global_variable_dict = obtain_global_variable_dict(
        integrated_experiment_dict)

    return integrated_experiment_dict, global_variable_dict


def add_fingerprint(integrated_experiment_dict):
    graph_list = [integrated_experiment_dict[k]["graph"]
                  for k in integrated_experiment_dict]
    ffp_calculator = FlowchartFP(graph_list, dict_mode=True)

    # fingerprinted_experiment_dict=copy.deepcopy(integrated_experiment_dict)
    fingerprinted_experiment_dict = integrated_experiment_dict

    for i, exp_id in enumerate(fingerprinted_experiment_dict):
        fp_dict = ffp_calculator(graph_list[i])
        for k in fp_dict:
            fingerprinted_experiment_dict[exp_id][f"FP_{k}"] = fp_dict[k]
    return fingerprinted_experiment_dict, ffp_calculator
