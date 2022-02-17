#from importlib import resources
from django.contrib import admin
from django.http import HttpResponse
from . import models
from nested_inline.admin import NestedStackedInline, NestedModelAdmin, NestedTabularInline
from import_export.admin import ImportExportModelAdmin
from . utils.sql_converter import sql_receiver, table_generator
from django.forms import Textarea
# ----------experimental ----------
# class PropertyInline(NestedStackedInline):


class PropertyInline(NestedTabularInline):
    model = models.Property
    extra = 0
    fk_name = "level"

# class StepInline(NestedStackedInline):


class StepInline(NestedTabularInline):
    model = models.Step
    extra = 1
    ordering = ("order",)
    fk_name = "level"
    inlines = [PropertyInline]


class ExperimentFileInline(NestedStackedInline):
    model = models.ExperimentFile
    extra = 1
    fk_name = "level"


class ExperimentAdmin(NestedModelAdmin):
    model = models.Experiment
    inlines = [StepInline, ExperimentFileInline]
    list_display = ["title", "unique_name",
                    "tag_names", "project",
                    "duplicate_experiment",
                    "created_at", "updated_at", "pub_date",
                    ]
    list_filter = ["project", "tags__name", "created_at", "updated_at",
                   "experimenter", "pub_date", ]
    readonly_fields = ('graph_preview',)

    actions = ["show_table", "show_fp_table", 'show_json']
    #actions = ['show_json']

    # actions
    def show_json(self, request, queryset):
        str_json = sql_receiver.generate_experiment_json(queryset)
        return HttpResponse(str_json, content_type='application/json')
    show_json.short_description = "Export JSON"

    def show_table(self, request, queryset):
        return table_generator.generate_experiment_dtale(queryset)
    show_table.short_description = "Export table"

    def show_fp_table(self, request, queryset):
        return table_generator.generate_experiment_fp_dtale(queryset)
    show_fp_table.short_description = "Export fingerprinted table"

    # tags

    def tag_names(self, obj):
        return "\n".join([p.name for p in obj.tags.all()])

    def unique_name(self, obj):
        return obj.unique_name
    unique_name.short_description = 'unique_name'
    unique_name.allow_tags = True

    def graph_preview(self, obj):
        return obj.graph_preview
    graph_preview.short_description = 'graph_preview'
    graph_preview.allow_tags = True

    def duplicate_experiment(self, obj):
        return obj.duplicate_experiment
    duplicate_experiment.short_description = 'duplicate_experiment'
    duplicate_experiment.allow_tags = True


# ---------chemical ----------------

# admin
class PropertychemInline(NestedStackedInline):
    model = models.PropertyChem
    extra = 1
    fk_name = "level"


class ChemicalFileInline(NestedStackedInline):
    model = models.ChemicalFile
    extra = 1
    fk_name = "level"


# class ChemicalAdmin(NestedModelAdmin):
class ChemicalAdmin(NestedModelAdmin, ImportExportModelAdmin):

    list_display = ["title", "unique_name", "subtitle", "smiles_thumbnail",
                    "created_at", "updated_at",
                    "tag_names",
                    "commercial", "obtained_date", "made_by", ]
    list_filter = ["tags__name",  "commercial", "obtained_date", "made_by",
                   "created_at", "updated_at"]
    search_fields = ['title', "subtitle", "SMILES"]
    inlines = [PropertychemInline, ChemicalFileInline]

    readonly_fields = ('smiles_preview',"smiles_info",)
    ordering = ["title"]
    save_as = True

    actions = ["show_table", 'show_json']

    formfield_overrides = {
            models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':100})},
        }

    # actions
    def show_json(self, request, queryset):
        str_json = sql_receiver.generate_chemical_json(queryset)
        return HttpResponse(str_json, content_type='application/json')
    show_json.short_description = "Export JSON"

    def show_table(self, request, queryset):
        return table_generator.generate_chemical_dtale(queryset)
    show_table.short_description = "Export table"

    # show tags
    def tag_names(self, obj):
        return "\n".join([p.name for p in obj.tags.all()])

    # show chemical structure image
    def smiles_preview(self, obj):
        return obj.smiles_preview
    smiles_preview.short_description = 'Structure'
    smiles_preview.allow_tags = True

    def smiles_thumbnail(self, obj):
        return obj.smiles_thumbnail
    smiles_thumbnail.short_description = 'Structure'
    smiles_thumbnail.allow_tags = True

    # show unique name
    def unique_name(self, obj):
        return obj.unique_name
    unique_name.short_description = 'unique_name'
    unique_name.allow_tags = True

    def smiles_info(self, obj):
        return obj.smiles_info
    smiles_info.short_description = 'smiles_info'
    smiles_info.allow_tags = True



# -------Mixture---------
class MixtureComponentInline(admin.StackedInline):
    model = models.MixtureComponent
    extra = 1
    # fk_name="level"
    ordering = ("order",)


class MixtureFileInline(NestedStackedInline):
    model = models.MixtureFile
    extra = 1
    fk_name = "level"


class PropertyMixtureInline(NestedStackedInline):
    model = models.PropertyMixture
    extra = 1
    fk_name = "level"


class MixtureAdmin(admin.ModelAdmin):
    model = models.Mixture
    inlines = [MixtureComponentInline,
               PropertyMixtureInline, MixtureFileInline]
    list_display = ["title", "unique_name", "tag_names",
                    "made_by", "created_at", "updated_at"]
    list_filter = ["made_by", "tags__name", "created_at", "updated_at"]
    save_as = True

    actions = ["show_table", 'show_json']

    # actions
    def show_json(self, request, queryset):
        str_json = sql_receiver.generate_mixture_json(queryset)
        return HttpResponse(str_json, content_type='application/json')
    show_json.short_description = "Export JSON"

    def show_table(self, request, queryset):
        return table_generator.generate_mixture_dtale(queryset)
    show_table.short_description = "Export table"

    def tag_names(self, obj):
        return "\n".join([p.name for p in obj.tags.all()])

    def unique_name(self, obj):
        return obj.unique_name
    unique_name.short_description = 'unique_name'
    unique_name.allow_tags = True


# add
admin.site.register(models.Chemical, ChemicalAdmin)
admin.site.register(models.MutualKey)
admin.site.register(models.Project)
admin.site.register(models.PropertyName)
admin.site.register(models.Tag)
admin.site.register(models.Experiment, ExperimentAdmin)
admin.site.register(models.Mixture, MixtureAdmin)
