from django.urls import path
from . import views
from django.conf.urls import url, static

urlpatterns=[
    path("graph/<str:graph_id>",views.view_experiment_graph,name="graph"),
    path("duplicate_experiment/<int:original_experiment_id>",views.duplicate_experiment,name="duplicate_experiment"),
    path("media/files/<str:media_name>",views.show_media,name="media_name"),
    path("",views.index,name="index"),
]

