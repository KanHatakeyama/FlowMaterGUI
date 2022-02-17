
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import base64
import io


def draw_selected_graph(
    graph_dict,
    graph_id,
):

    # some keys are string, some are int
    try:
        graph_id = int(graph_id)
    except:
        pass

    # try checking duplicated graphs
    if graph_id not in graph_dict.keys():
        graph_id = f"{graph_id}_1"

    g = graph_dict[graph_id]["graph"]
    return draw_graph(g, buffer_mode=True)


def draw_graph(g, buffer_mode=False):
    label_dict = get_label_dict(g)
    pos_dict, size_list = get_node_pos(g, label_dict)

    sx = max(pos_dict[k][0] for k in pos_dict)
    sy = -min(pos_dict[k][1] for k in pos_dict)
    sx = max(sx, 0.1)
    sy = max(sy, 0.05)

    const_x = 80
    const_y = 200

    plt.figure(figsize=(sx*const_x, sy*const_y), dpi=100)

    nx.draw_networkx_labels(g, pos_dict, labels=label_dict)
    nx.draw(g, pos_dict, node_color="orange",
            node_size=size_list, node_shape="s")

    plt.axis('off')
    axis = plt.gca()
    axis.set_xlim((-0.03, axis.get_xlim()[1]*1.2+0.01))
    # print(axis.get_xlim())
    #axis.set_xlim([1.2*x for x in axis.get_xlim()])
    axis.set_ylim([1.2*y for y in axis.get_ylim()])

    # print(axis.get_xlim())
    plt.tight_layout()

    if not buffer_mode:
        plt.show()
    if buffer_mode:
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        base64Img = base64.b64encode(
            buffer.getvalue()).decode().replace("'", "")
        return base64Img


def get_node_pos(g,
                 label_dict,
                 scale_x=0.05,
                 scale_y=0.001,
                 node_size_scale=1500,
                 ):

    global_y = 0
    global_x = 0

    pos_dict = {}
    size_list = []
    for node in g.nodes:
        num_props = label_dict[node].count("\n")+1
        pos = np.array([global_x, -global_y])
        pos_dict[node] = pos

        # update global pos
        global_y += (num_props+10)*scale_y

        # node size
        size_list.append(node_size_scale*num_props)

        # check for branches
        next_node = list(g.neighbors(node))

        # in the directed graph, the number of next node should be 1 (normal) or 0 (end of graph)
        shift_flag = False
        if len(next_node) == 0:
            shift_flag = True
        else:
            next_node = next_node[0]
            # in the case of branch
            # if next_node<node:
            if abs(next_node-node) > 800:
                shift_flag = True

        if shift_flag:
            global_y = 0
            global_x += scale_x
    return pos_dict, size_list


def check_non_use_label(target_label):
    remove_list = ["created_at", "updated_at", "tags"]

    if target_label in remove_list:
        return False

    if target_label.find("Mixture_title") >= 0:
        return True

    if target_label.find("Mixture_") >= 0:
        return False

    if target_label.find("chemical_title") >= 0:
        return True

    if target_label.find("chemical_") >= 0:
        return False

    return True


def get_label_dict(g):
    label_dict = {}
    for node in g.nodes:
        note_list = []
        for k, v in g.nodes[node].items():
            if k == "label":
                note_list.append(f"0000[{v}]")
            elif v is not None and v != "[]":
                if check_non_use_label(k):
                    key = k.replace("_title", "")
                    note_list.append(f"{key}: {v}")

        note_list = sorted(note_list)
        note_list[0] = note_list[0].replace("0000", "")
        note = "\n".join(note_list)
        label_dict[node] = note
    return label_dict
