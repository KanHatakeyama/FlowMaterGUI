from expmanager.models import Step,Tag
from expmanager.models import Experiment
from expmanager.models import Property


# nested data cannot be duplicated properly by normal save as functions
def duplicate_experiment(original_experiment_id):
    experiment = Experiment.objects.get(pk=original_experiment_id)

    original_tags=list(experiment.tags.all())

    experiment.pk = None
    experiment.save()

    new_experiment_id = experiment.pk

    # TODO: duplicate tags. not woking
    for tag in original_tags:
        experiment.tags.add(tag)

    # duplicate steps
    original_steps = Step.objects.filter(level_id=original_experiment_id)

    for step in original_steps:
        original_step_id = step.pk
        step.pk = None
        step.level_id = new_experiment_id
        step.save()
        new_step_id = step.pk

        # dupricate properties
        original_properties = Property.objects.filter(
            level_id=original_step_id)
        for property in original_properties:
            property.pk = None
            property.level_id = new_step_id
            property.save()
