from django.db import models
from django.db.models import TextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.html import mark_safe
from .utils.chems import parse_smiles

import json
from django.core.exceptions import ValidationError


# set maximum file size
def file_size_validate(value):
    limit = 10 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 10 MiB.')

# treat chemical structure


# tag
class Tag(models.Model):
    name = models.CharField(max_length=32)
    special_memo = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name

# chemical
class Chemical(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    obtained_date = models.DateField(null=True, blank=True)
    made_by = models.CharField(max_length=400, null=True, blank=True)
    #SMILES = models.CharField(max_length=4000, null=True, blank=True)
    SMILES = models.TextField(max_length=4000, null=True, blank=True)
    commercial = models.BooleanField(default=True)
    disposed = models.BooleanField(default=False)
    company = models.CharField(max_length=200, null=True, blank=True)
    reference = models.CharField(max_length=400, null=True, blank=True)
    cris_id = models.CharField(max_length=200, null=True, blank=True)
    room = models.CharField(max_length=200, null=True, blank=True)
    special_memo = RichTextUploadingField(blank=True, null=True)

    class Meta:
        verbose_name = "Chemical"

    def __str__(self) -> str:
        return self.title

        # this somehow causes error during integrating graphs (utils/experiment_utilities)
        # return str(self.pk)+"_"+str(self.title)

    # show chemical structures
    def prepare_image(self, smiles, size=None):
        try:
            if size is None:
                img = parse_smiles.smiles_to_buffer_img(smiles)
            else:
                img = parse_smiles.smiles_to_buffer_img(smiles, size=size)
            tag = "<img src='data:image/png;base64,{}'/>".format(img)
        except:
            tag = "<p>error parsing smiles</p>"
        return tag

    # polymer data parsing
    @property
    def smiles_info(self):
        return parse_smiles.smiles_info(self.SMILES)

    @property
    def smiles_preview(self):
        if self.SMILES:
            return mark_safe(self.prepare_image(self.SMILES))
        return ""

    @property
    def smiles_thumbnail(self):
        if self.SMILES:
            return mark_safe(self.prepare_image(self.SMILES, size=100))
        return ""

    @property
    def unique_name(self):
        return str(self.pk)+"_"+str(self.title)


class ChemicalFile(models.Model):
    level = models.ForeignKey(
        Chemical, on_delete=models.CASCADE, related_name="chemical_file")
    file = models.FileField(
        upload_to="files", null=True, blank=True, validators=[file_size_validate])


# Mixture
class Mixture(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    obtained_date = models.DateField(null=True, blank=True)
    made_by = models.CharField(max_length=400, null=True, blank=True)
    commercial = models.BooleanField(default=False)
    disposed = models.BooleanField(default=False)
    company = models.CharField(max_length=200, null=True, blank=True)
    reference = models.CharField(max_length=400, null=True, blank=True)
    room = models.CharField(max_length=200, null=True, blank=True)
    special_memo = RichTextUploadingField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title
        return str(self.pk)+"_"+str(self.title)

    class Meta:
        verbose_name = "Mixture"

    @property
    def unique_name(self):
        return str(self.pk)+"_"+str(self.title)


# Mixture component
class MixtureComponent(models.Model):
    level = models.ForeignKey(
        Mixture, on_delete=models.CASCADE, related_name="Mixture_c")

    chemical = models.ForeignKey(
        Chemical, on_delete=models.CASCADE, related_name="chemical_c")

    order = models.IntegerField(default=0)
    mol_amount = models.CharField(max_length=200, null=True, blank=True)
    wt_amount = models.CharField(max_length=200, null=True, blank=True)
    vol_amount = models.CharField(max_length=200, null=True, blank=True)
    molar = models.CharField(max_length=200, null=True, blank=True)
    note = models.CharField(max_length=200, null=True, blank=True)


class MixtureFile(models.Model):
    level = models.ForeignKey(
        Mixture, on_delete=models.CASCADE, related_name="Mixture_file")
    file = models.FileField(
        upload_to="files", null=True, blank=True, validators=[file_size_validate])


# ------- about project ----------

# keyword to show a mutual step in different experiments
class MutualKey(models.Model):
    title = models.CharField(max_length=200)
    special_memo = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "MutualKey"

    def __str__(self) -> str:
        return self.title

# project name


class Project(models.Model):
    title = models.CharField(max_length=200)
    special_memo = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title


# experiment
class Experiment(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    experimenter = models.CharField(max_length=200)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="project_name")
    special_memo = models.CharField(max_length=200, null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    pub_date = models.DateTimeField("Experiment date", null=True, blank=True)
    #bookmark= models.BooleanField(default=False)
    #machine_learning= models.BooleanField(default=False)
    special_content = RichTextUploadingField(blank=True, null=True)
    reference = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self) -> str:
        return self.title
        return str(self.pk)+"_"+str(self.title)

    class Meta:
        verbose_name = "Experiment"

    @property
    def unique_name(self):
        return str(self.pk)+"_"+str(self.title)

    @property
    def graph_preview(self):
        number = str(self.pk)
        tag = f'<a href="../../../../../../graph/{number}" target="_blank" rel="noopener noreferrer">View graph (save experiment to show the latest graph)</a>'
        return mark_safe(tag)

    @property
    def duplicate_experiment(self):
        number = str(self.pk)
        tag = f'<a href="../../../../../../duplicate_experiment/{number}" target="_blank" rel="noopener noreferrer">Duplicate experiment</a>'
        return mark_safe(tag)


class ExperimentFile(models.Model):
    level = models.ForeignKey(
        Experiment, on_delete=models.CASCADE, related_name="experiment_file")
    file = models.FileField(
        upload_to="files", null=True, blank=True, validators=[file_size_validate])


class Step(models.Model):
    level = models.ForeignKey(
        Experiment, on_delete=models.CASCADE, related_name="step")
    order = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    special_memo = models.CharField(max_length=200, null=True, blank=True)
    mutual_key = models.ForeignKey(
        MutualKey, on_delete=models.CASCADE, null=True, blank=True, related_name="mutual_key")
    chemical = models.ForeignKey(
        Chemical, on_delete=models.CASCADE, null=True, blank=True)
    Mixture = models.ForeignKey(
        Mixture, on_delete=models.CASCADE, null=True, blank=True)
    fusion_experiment = models.ForeignKey(
        Experiment, on_delete=models.CASCADE, null=True, blank=True, related_name="fusion_experiment")
    insert_experiment = models.ForeignKey(
        Experiment, on_delete=models.CASCADE, null=True, blank=True, related_name="insert_experiment")
    file_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

# ----- properties--------


class PropertyName(models.Model):
    title = models.CharField(max_length=200)
    explanation= models.CharField(max_length=200,null=True,blank=True)

    def __str__(self) -> str:
        return str(self.title)


class Property(models.Model):
    level = models.ForeignKey(
        Step, on_delete=models.CASCADE, related_name="property")
    title = models.ForeignKey(
        PropertyName, on_delete=models.CASCADE, related_name="property_title")
    value = models.CharField(max_length=2000)
    special_memo = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.title)


class PropertyChem(models.Model):
    level = models.ForeignKey(
        Chemical, on_delete=models.CASCADE, related_name="property_chem")
    title = models.ForeignKey(
        PropertyName, on_delete=models.CASCADE, related_name="property_chem_title")
    value = models.CharField(max_length=200)
    special_memo = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "PropertyChem"

    def __str__(self) -> str:
        return str(self.title)


class PropertyMixture(models.Model):
    level = models.ForeignKey(
        Mixture, on_delete=models.CASCADE, related_name="property_Mixture")
    title = models.ForeignKey(
        PropertyName, on_delete=models.CASCADE, related_name="property_Mixture_title")
    value = models.CharField(max_length=200)
    special_memo = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.title)
