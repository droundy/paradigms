from django.contrib import admin
from .models import Problem, Activity, Sequence, ProblemSet, ProblemSetItems, SequenceItems, Pages, Course, CourseLearningOutcome, CourseAsTaught, CourseDay, DayActivity, DayProblem

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

class CourseLearningOutcomeInline(admin.TabularInline):
    model = CourseLearningOutcome
    extra = 1
class CourseAdmin(admin.ModelAdmin):
    inlines = (CourseLearningOutcomeInline,)
admin.site.register(Course, CourseAdmin)

admin.site.register(CourseAsTaught)

class DayActivityInline(admin.TabularInline):
    model = DayActivity
    extra = 1
class DayProblemInline(admin.TabularInline):
    model = DayProblem
    fk_name = 'day'
    extra = 1
class DayAdmin(admin.ModelAdmin):
    inlines = (DayActivityInline, DayProblemInline,)

admin.site.register(CourseDay, DayAdmin)
