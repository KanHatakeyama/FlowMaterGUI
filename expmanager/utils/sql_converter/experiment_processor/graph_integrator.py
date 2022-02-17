import copy
import networkx as nx


MAX_NESTING = 10
MAX_NODES = 1000

# integrate different experiments


def connect_experiments(
        raw_experiment_dict,
        parent_graph,
        parent_node_id,
        additional_experiment_id,
        inner_count,
        mode="fusion_experiment"):
    # prepare copies
    parent_graph = copy.copy(parent_graph)
    additional_graph = copy.copy(
        raw_experiment_dict[additional_experiment_id]["graph"])

    num_parent_nodes = max(list(parent_graph.nodes))
    if len(list(parent_graph.nodes)) > MAX_NODES:
        raise ValueError(
            "too many nodes in a graph! related graph ID: ", additional_experiment_id)

    # for nesting graphs, add unique node IDs
    def update_node_id(k):
        # return num_parent_nodes+k+1
        if k < MAX_NODES:
            return k+MAX_NODES*(MAX_NESTING-inner_count)*10
        else:
            return k-MAX_NODES*(1)

    mapping = {k: update_node_id(k) for k in additional_graph.nodes}
    additional_graph = nx.relabel_nodes(additional_graph, mapping)

    # connect
    parent_graph = nx.compose(parent_graph, additional_graph)

    last_id = max(list(additional_graph.nodes))
    # first_id=min(list(additional_graph.nodes))
    first_id = last_id-last_id % MAX_NODES

    # fusion mode
    if mode == "fusion_experiment":
        parent_graph.add_edge(last_id, parent_node_id)
        parent_graph.nodes[parent_node_id].pop("fusion_experiment")
    # insert mode
    else:
        parent_graph.add_edge(parent_node_id, first_id)
        parent_graph.add_edge(last_id, parent_node_id+1)
        try:
            parent_graph.remove_edge(parent_node_id, parent_node_id+1)
        except:
            raise ValueError(
                "failed insertion, check the insersion graph", parent_graph.nodes)
        parent_graph.nodes[parent_node_id].pop("insert_experiment")

    return parent_graph


# search for fusion or insert experiment keywords

def auto_integrate_graphs(raw_experiment_dict, target_graph, current_id, inner_count=0):
    inner_count += 1

    if inner_count > MAX_NESTING:
        raise ValueError("Too many insersion/fusions!", target_graph.nodes[0])

    for node_id in target_graph.nodes:
        for key in target_graph.nodes[node_id].keys():
            if key in ["fusion_experiment", "insert_experiment"]:
                # raise error with a self-referencing case
                if key == current_id:
                    raise ValueError(
                        f"parent (={current_id}) and additional (={key}) ids should not match")

                target_graph = connect_experiments(
                    raw_experiment_dict, target_graph, node_id, target_graph.nodes[node_id][key], inner_count, mode=key)
                target_graph = auto_integrate_graphs(
                    raw_experiment_dict, target_graph, current_id, inner_count)

    return target_graph

# load fusion and insert graph data


def prepare_integrated_experiment_dict(raw_experiment_dict):
    integrated_experiment_dict = copy.copy(raw_experiment_dict)

    for i in raw_experiment_dict.keys():
        target_graph = integrated_experiment_dict[i]["graph"]
        target_graph = copy.copy(target_graph)

        try:
            target_graph = auto_integrate_graphs(
                raw_experiment_dict, target_graph, i)
        except:
            target_graph = create_broken_graph()

        integrated_experiment_dict[i]["graph"] = target_graph
    return integrated_experiment_dict


def create_broken_graph(comment="Error! \n check for self insersion or fusion"):
    g = nx.DiGraph()

    # header node
    g.add_node(0)
    g.nodes[0]["label"] = comment
    return g
