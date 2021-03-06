import datetime
from haystack import indexes
from .models import Activity, Problem, Sequence


class ActivityIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    #topic = indexes.CharField(model_attr='topics')
    #equipment = indexes.CharField(model_attr='equipment_required')

    def get_model(self):
        return Activity

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class ProblemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    #topic = indexes.CharField(model_attr='topics')
    #equipment = indexes.CharField(model_attr='equipment_required')

    def get_model(self):
        return Problem

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class SequenceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    #topic = indexes.CharField(model_attr='topics')
    #equipment = indexes.CharField(model_attr='equipment_required')

    def get_model(self):
        return Sequence

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()