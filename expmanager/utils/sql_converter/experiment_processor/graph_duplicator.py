import copy
from . graph_integrator import create_broken_graph


def duplicate_experiment_with_variables(integrated_experiment_dict):

    duplicated_experiment_dict = integrated_experiment_dict
    for key in list(duplicated_experiment_dict):
        graph_list = duplicate_graphs_with_variables(
            duplicated_experiment_dict[key]["graph"])

        if len(graph_list) > 1:
            for dup_number in range(len(graph_list)):
                new_key = f"{key}_{dup_number+1}"
                duplicated_experiment_dict[new_key] = copy.copy(
                    duplicated_experiment_dict[key])
                duplicated_experiment_dict[new_key]["graph"] = graph_list[dup_number]

            # delete original
            duplicated_experiment_dict.pop(key)


# if a graph has comma separated variable, duplicate graphs
def duplicate_graphs_with_variables(target_graph):

    # search for comma separated variables. e.g., [10,5,2,1]
    comma_val_list = []

    exception_list = ["chemical_tags", "Mixture_tags", "tags","SMILES",
                      "chemical_title", "Mixture_title","special_content"]

    # search for comma separated variables
    for node_id in target_graph.nodes:
        for property_key, value in target_graph.nodes[node_id].items():
            exception_flag = False

            if type(value) is not str:
                exception_flag = True

            for ex in exception_list:
                if property_key.find(ex) >= 0:
                    exception_flag = True

            #print(property_key,exception_flag)
            if exception_flag:
                continue

            if value.find(",") > 0:
                comma_val_list.append(
                    (node_id, property_key, value.split(",")))

    new_graph_list = []

    # if commas are not used, just appen the original graph
    if len(comma_val_list) == 0:
        new_graph_list.append(target_graph)
        return new_graph_list

    # duplicate graphs
    else:
        # check variable length
        comma_variable_length_list = [len(i[2]) for i in comma_val_list]
        #print(comma_val_list)
        if len(list(set(comma_variable_length_list))) != 1:
            comment = f"Error! \n number of variables must be the same! \n {comma_val_list}"
            caution_graph = create_broken_graph(comment=comment)
            new_graph_list = [caution_graph]*2
            #raise ValueError("number of variables should be the same!",comma_val_list)
            return new_graph_list

        # duplicate
        number_of_duplicates = comma_variable_length_list[0]

        for dup_number in range(number_of_duplicates):
            new_graph = copy.deepcopy(target_graph)

            for command in comma_val_list:
                node_id, property_key, values = command[0], command[1], command[2]
                value = values[dup_number]
                # print(node_id,property_key,value)
                new_graph.nodes[node_id][property_key] = value

            new_graph_list.append(new_graph)

    return new_graph_list


def obtain_global_variable_dict(integrated_experiment_dict):
    """
    collect global variables marked by "ID" steps
    NOTE: this will change original dict (delete "ID" nodes)

    """

    globalized_experiment_dict = integrated_experiment_dict
    global_variable_dict = {}

    for experiment_id in list(globalized_experiment_dict.keys()):
        current_record_dict = {}
        project_name = globalized_experiment_dict[experiment_id]["project"]
        target_graph = globalized_experiment_dict[experiment_id]["graph"]

        # check each node
        for node_id in target_graph.nodes:
            # search for "ID"
            if "ID" not in target_graph.nodes[node_id]:
                continue

            # if "ID" is blank, just delete the key
            if target_graph.nodes[node_id]["ID"] is None:
                target_graph.nodes[node_id].pop("ID")
                continue

            # if "ID" is available, add features to global variables
            for node_key, value in list(target_graph.nodes[node_id].items()):
                if node_key in ["ID", "label"]:
                    continue

                current_record_dict[f"{project_name}_{node_key}"] = value
                target_graph.nodes[node_id].pop(node_key)

        global_variable_dict[experiment_id] = current_record_dict

    """
    for exp_id in integrated_experiment_dict:
        for k in integrated_experiment_dict[exp_id]:
            if k!="graph":
                global_variable_dict[exp_id][k]=integrated_experiment_dict[exp_id][k]
    """
    return global_variable_dict
