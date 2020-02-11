from django.contrib import admin
from .models import Problem, Activity, Sequence, ProblemSet, ProblemSetItems, SequenceItems

# Register your models here.
admin.site.register(Problem)
admin.site.register(Activity)
admin.site.register(ProblemSet)
admin.site.register(ProblemSetItems)
admin.site.register(Sequence)
admin.site.register(SequenceItems)
