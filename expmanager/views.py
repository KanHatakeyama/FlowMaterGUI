#from msilib.schema import ListView
#from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . utils.sql_converter import sql_receiver
from . utils.sql_converter.experiment_processor import experiment_graph_generator
from . utils.sql_converter.experiment_processor import draw_experiment_graph
from . utils import experiment_duplicator
from . models import Experiment
from django.http import FileResponse
# Create your views here.


def index(request):
    return render(request, "expmanager/index.html")


# show experiment graph
@login_required
def view_experiment_graph(request, graph_id):

    # get all experiments in the same project
    # TODO: not all experiments are needed
    current_experiment = Experiment.objects.get(pk=graph_id)
    project_id = current_experiment.project_id
    queryset = Experiment.objects.filter(project_id=project_id)

    dict_data = sql_receiver.generate_experiment_json(queryset, dict_mode=True)
    experiment_dict = experiment_graph_generator.generate_experiment_dict(
        dict_data, fp_mode=False)

    try:
        img = draw_experiment_graph.draw_selected_graph(
            experiment_dict, graph_id)
        tag = "<img src='data:image/png;base64,{}'/>".format(img)
    except:
        tag = "error occured during drawing of a graph!"
    return HttpResponse(tag)


# duplicate experiment
@login_required
def duplicate_experiment(request, original_experiment_id):
    try:
        experiment_duplicator.duplicate_experiment(original_experiment_id)
    except:
        return HttpResponse("Failed!")
    return HttpResponse("Success!\n reload admin page to update view")


# show media file
@login_required
def show_media(request, media_name):
    return FileResponse(open(f"media/files/{media_name}", "rb"), as_attachment=True, filename=media_name)