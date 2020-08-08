from django.contrib import admin
from .models import Problem, Activity, Sequence, ProblemSet, ProblemSetItems, SequenceItems, Pages, Course

# Register your models here.
# admin.site.register(Problem)
admin.site.register(Activity)
# admin.site.register(ProblemSet)
admin.site.register(ProblemSetItems)
admin.site.register(Sequence)
admin.site.register(SequenceItems)
admin.site.register(Pages)

class ProblemSetInline(admin.TabularInline):
    model = ProblemSetItems
    extra = 1

class ProblemAdmin(admin.ModelAdmin):
    inlines = (ProblemSetInline,)

class ProblemSetAdmin(admin.ModelAdmin):
    inlines = (ProblemSetInline,)

admin.site.register(Problem, ProblemAdmin)
admin.site.register(ProblemSet, ProblemSetAdmin)

admin.site.register(Course)
