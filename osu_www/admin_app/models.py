from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.urls import reverse
from autoslug import AutoSlugField
from django.utils.safestring import mark_safe
import os
import latex_snippet
import cairosvg
import re
import admin_app.choices as choices
# from admin_app.choices import *


class PageMedia(models.Model):
    title = models.CharField(max_length=255, blank=True)
    media_category = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='page_media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension


class Pages(models.Model):
    title = models.CharField(max_length=255, blank=True)
    slug = AutoSlugField(populate_from='title')
    page_content = models.TextField(blank=True, null=True)
    keywords = models.TextField(
        blank=True, null=True, help_text="Comma-separated list of topics or keywords: adiabatic susceptibility,entropy")
    published_date = models.DateTimeField(blank=True, null=True)
    media = models.ManyToManyField(
        PageMedia, through='PageMediaAssociation', related_name='pagemedias')
    whitepaper = models.BooleanField(
        blank=False, default=False, help_text="Is this a whitepaper?", verbose_name="Whitepaper")
    whitepaper_category = models.CharField(max_length=255, blank=True, null=True,
                                           help_text="If this page is meant to be a whitepaper, please select a category. The category list is maintained by system administrators and can not be dynamic.")
    publication = models.BooleanField(
        blank=False, default=False, help_text="Whitepaper is ready for public viewing.", verbose_name="Publish Whitepaper")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        permissions = (
            ("can_edit_pages", "Edit Pages"),
            ("can_add_pages", "Add Pages"),)

    def get_absolute_url(self):
        return reverse('page_display', kwargs={'slug': self.slug})


class PageMediaAssociation(models.Model):
    media = models.ForeignKey(PageMedia, on_delete=models.CASCADE)
    page = models.ForeignKey(Pages, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)
    media_position = models.PositiveIntegerField(blank=True, null=True)
    media_title = models.CharField(max_length=255, blank=True, null=True)

# Create your models here.


class Figure(models.Model):
    title = models.CharField(max_length=255, blank=True)
    # file = models.FileField(upload_to='figures/')
    file = models.FileField(upload_to='figures/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    media_category = models.CharField(max_length=255, blank=True)

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension


def convert_latex_for_pdf(latex, imagedir='/media/figures/'):
    if latex is None:
        return None
    # The following splits up the latex on any includegraphics, so we can
    # adjust the paths to any files, and also change svg files to pdf.
    splitup = re.split(r'\\includegraphics(\[[^\]]*\])?{([^\}]+)}', latex)
    latex = ''
    for a, b, c in zip(*[splitup[i::3] for i in range(3)]):
        latex += a

        print('b is', b)
        if len(c) > 0:
            if b is None:
                b = ''
            if c[0] == '/' or c.startswith('https://'):
                if c.startswith('https://'):
                    c = c[len('https:/'):]
                c = '/var/www/osu_production_env/osu_www'+c
            else:
                c = '/var/www/osu_production_env/osu_www'+imagedir+c
            if c[-4:] == '.svg':
                # use PDF files rather than SVG files.
                path = c[:-4] + '.pdf'
                if not os.path.isfile(path) and os.path.isfile(c):
                    cairosvg.svg2pdf(url=c, write_to=path)
            else:
                path = c
            if os.path.isfile(path):
                latex += r'\includegraphics'+b+'{'+path+'}'
            else:
                latex += r'{\tiny Missing \verb!%s!}' % path
    latex += splitup[-1]
    return latex


class Problem(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problem_title = models.CharField(max_length=255)
    problem_latex = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    attribution = models.CharField(
        max_length=255, help_text="Original source information.", blank=True, null=True)
    old_name = models.CharField(
        max_length=255, help_text="Name from original homework archive.", blank=True, null=True)
    topics = models.TextField(
        blank=True, null=True, help_text="Comma-separated list of topics: adiabatic susceptibility,entropy")
    figures = models.ManyToManyField(
        Figure, through='FigureAssociations', related_name='problems')
    course = models.CharField(max_length=255, blank=True, null=True)
    learning_outcomes = models.ManyToManyField('CourseLearningOutcome', related_name='problems')
    publication = models.BooleanField(
        blank=False, default=False, help_text="Problem is ready for public viewing", verbose_name="Publish Problem")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.problem_title

    @property
    def icon(self):
        return mark_safe('<i class="material-icons">assignment</i>')
        return mark_safe('<span class="oi oi-pencil"></span>')

    @property
    def beast(self):
        return mark_safe(self.icon + ' Homework')

    @property
    def title(self):
        return self.problem_title

    @property
    def pdf_latex(self):
        ''' return the latex content, modified for pdf generation by making image paths
          absolute, removing image paths that don't correspond to actual files, and converting
          SVG files to PDF, and removing solutions. '''
        return latex_snippet.omit_solutions(self.pdf_solution_latex)

    @property
    def pdf_solution_latex(self):
        ''' return the latex content, modified for pdf generation by making image paths
          absolute, removing image paths that don't correspond to actual files, and converting
          SVG files to PDF, and including the solutions. '''
        return convert_latex_for_pdf(latex_snippet.physics_macros(self.problem_latex))

    @property
    def split_topics(self):
        if self.topics is not None:
            return [t.strip() for t in self.topics.split(',') if t.strip() != '']
        else:
            return []

    class Meta:
        ordering = ['problem_title']
        permissions = (
            ("can_edit_problem", "Edit Problem"),
            ("can_add_problem", "Add Problem"),
            ("can_view_solution", "View Solution"))


class ProblemSet(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    author = author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author_info = models.CharField(max_length=4096, blank=True, null=True)
    publication = models.BooleanField(
        blank=False, default=False, help_text="Problem Set is ready for public viewing. Takes 5-10 seconds to generate new problem set PDFs", verbose_name="Publish Problem Set")
    items = models.ManyToManyField(Problem, through="ProblemSetItems")
    course = models.CharField(max_length=255, blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return '%s %s' % (self.title, self.instructions)

    class Meta:
        permissions = (
            ("can_edit_problem_set", "Edit Problem Set"),
            ("can_add_problem_set", "Add Problem Set"),
            ("can_view_solution", "View Solution"))


class ProblemSetItems(models.Model):
    problem = models.ForeignKey(
        Problem, blank=True, null=True, on_delete=models.CASCADE, related_name='itemProblem')
    problem_set = models.ForeignKey(
        ProblemSet, blank=True, null=True, on_delete=models.CASCADE, related_name='set_problems')
    item_position = models.DecimalField(
        max_digits=5, decimal_places=2, default=1, blank=True, null=True)
    item_instructions = models.TextField(blank=True, null=True)
    required = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['item_position']
    # def __str__(self):
    #     return self.problem


class ProblemSetPDFs(models.Model):
    pdf = models.FileField(upload_to='problem_set_pdfs/')
    problem_set = models.ForeignKey(
        ProblemSet, on_delete=models.CASCADE, related_name="problem_set_pdfs")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    solution = models.BooleanField(
        blank=False, default=False, help_text="Does this include the solution?", verbose_name="Solution Included")


class FigureAssociations(models.Model):
    figure = models.ForeignKey(Figure, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)
    figure_position = models.PositiveIntegerField(blank=True, null=True)
    figure_title = models.CharField(max_length=255, blank=True, null=True)


class ActivityMedia(models.Model):
    title = models.CharField(max_length=255, blank=True)
    media_category = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='activity_media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension


class Activity(models.Model):
    title = models.CharField(max_length=255, blank=True)
    overview_paragraph = models.TextField(blank=True, null=True)
    # time_estimate = models.IntegerField()
    time_estimate = models.IntegerField(blank=True, null=True)
    what_students_learn = models.TextField(blank=True, null=True)
    type_of_beast = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    equipment_required = models.TextField(blank=True, null=True)
    topics = models.TextField(blank=True, null=True)
    instructor_guide = models.TextField(blank=True, null=True)
    publication_status = models.TextField(blank=True, null=True)
    publication_date = models.DateTimeField(blank=True, null=True)
    prerequisite_knowledge = models.TextField(blank=True, null=True)
    readings = models.TextField(blank=True)
    activity_image = models.ImageField(
        blank=True, null=True, upload_to='activity_images/')
    keywords = models.TextField(blank=True, null=True)
    author = author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    associated_paper_links = models.TextField(blank=True, null=True)
    learning_outcomes = models.ManyToManyField('CourseLearningOutcome', related_name='activities')
    course = models.CharField(max_length=255, blank=True, null=True)
    author_info = models.CharField(max_length=4096, blank=True, null=True)
    media = models.ManyToManyField(
        ActivityMedia, through='MediaAssociation', related_name='medias')
    old_name = models.CharField(max_length=255, blank=True, null=True)

    def publish(self):
        self.publication_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    @property
    def is_activity(self):
        return True

    @property
    def icon(self):
        # iterate through possible choices for type of beast
        BEASTICONS = {
            # choices.TBCSMALLGROUP: "puzzle-piece",
            # choices.TBCSMALLBOARD: "person",
            # choices.TBCMATHEMATICA: "code",
            # choices.TBCKINESTHETIC: "bolt",
            # choices.TBCQUIZ: "question-mark",
            # choices.TBCWHOLECLASS: "people",
            # choices.TBCEXPERIMENT: "beaker",
            # choices.TBCCOMPUTERSIM: "laptop",
            # choices.TBCLECTURE: "microphone",
        }
        if self.type_of_beast in BEASTICONS:
            return mark_safe('<span class="oi oi-' + BEASTICONS[self.type_of_beast] + '"></span> ')
        ICONS = {
            choices.TBCSMALLGROUP: '<i class="material-icons">group_work</i>',
            choices.TBCSMALLBOARD: '<i class="material-icons">assignment_ind</i>',
            choices.TBCMATHEMATICA: '<i class="material-icons">insights</i>',
            choices.TBCKINESTHETIC: '<i class="material-icons">accessibility_new</i>',
            choices.TBCQUIZ: '<i class="material-icons">grading</i>',
            choices.TBCWHOLECLASS: '<i class="material-icons">forum</i>',
            choices.TBCEXPERIMENT: '<i class="material-icons">biotech</i>',
            choices.TBCCOMPUTERSIM: '<i class="material-icons">computer</i>',
            choices.TBCLECTURE: '<i class="material-icons">face</i>',
        }
        if self.type_of_beast in ICONS:
            return mark_safe(ICONS[self.type_of_beast])
        return ''

    @property
    def beast(self):
        if self.icon is not None and self.type_of_beast is not None:
            return mark_safe(str(self.icon) + ' ' + str(self.type_of_beast))
        else:
            return "???"

    @property
    def has_solution(self):
        if r'\begin{handout}' in self.instructor_guide:
            h = latex_snippet.only_handout(self.instructor_guide)
        elif r'\begin{guide}' in self.instructor_guide:
            h = latex_snippet.omit_guide(self.instructor_guide)
        else:
            return False
        return r'\begin{solution}' in h

    @property
    def solution_latex(self):
        ''' return the latex content for the student solutions '''
        if r'\begin{handout}' in self.instructor_guide:
            h = latex_snippet.only_handout(self.instructor_guide)
        elif r'\begin{guide}' in self.instructor_guide:
            h = latex_snippet.omit_guide(self.instructor_guide)
        else:
            return None
        if r'\begin{solution}' not in h:
            return None
        return latex_snippet.physics_macros(h)

    @property
    def has_handout(self):
        return r'\begin{handout}' in self.instructor_guide or r'\begin{guide}' in self.instructor_guide

    @property
    def handout_latex(self):
        ''' return the latex content for the student handout '''
        if r'\begin{handout}' in self.instructor_guide:
            h = latex_snippet.only_handout(self.instructor_guide)
        elif r'\begin{guide}' in self.instructor_guide:
            h = latex_snippet.omit_guide(self.instructor_guide)
        else:
            return None
        return latex_snippet.omit_solutions(latex_snippet.physics_macros(h))

    @property
    def guide_latex(self):
        ''' return the latex content for the instructor guide '''
        return latex_snippet.omit_solutions(latex_snippet.physics_macros(self.instructor_guide))

    @property
    def pdf_guide_latex(self):
        ''' return the latex content for the instructor guide, modified for pdf generation by making image paths
          absolute, removing image paths that don't correspond to actual files, and converting
          SVG files to PDF '''
        return convert_latex_for_pdf(self.guide_latex, imagedir='/media/activity_media/')

    @property
    def pdf_handout_latex(self):
        ''' return the latex content for the student, modified for pdf generation by making image paths
          absolute, removing image paths that don't correspond to actual files, and converting
          SVG files to PDF '''
        return convert_latex_for_pdf(self.handout_latex, imagedir='/media/activity_media/')

    @property
    def pdf_solution_latex(self):
        ''' return the latex content for the student solution, modified for pdf generation by making image paths
          absolute, removing image paths that don't correspond to actual files, and converting
          SVG files to PDF '''
        return convert_latex_for_pdf(self.solution_latex, imagedir='/media/activity_media/')

    @property
    def split_topics(self):
        if self.topics is not None:
            return [t.strip() for t in self.topics.split(',') if t.strip() != '']
        else:
            return []

    @property
    def split_keywords(self):
        if self.keywords is not None:
            return [t.strip() for t in self.keywords.split(',') if t.strip() != '']
        else:
            return []

    class Meta:
        verbose_name_plural = "activities"
        permissions = (
            ("can_edit_activity", "Edit Activity"),
            ("can_add_activity", "Add Activity"),
            ("can_view_solution", "View Solution"))


class MediaAssociation(models.Model):
    media = models.ForeignKey(ActivityMedia, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)
    media_position = models.PositiveIntegerField(blank=True, null=True)
    media_title = models.CharField(max_length=255, blank=True, null=True)


class Sequence(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    overview_paragraph = models.TextField(blank=True, null=True)
    problems = models.ManyToManyField(
        Problem, through='SequenceItems', related_name='problems')
    activities = models.ManyToManyField(
        Activity, through='SequenceItems', related_name='activities')
    author = author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author_info = models.CharField(max_length=4096, blank=True, null=True)
    publication = models.BooleanField(
        blank=False, default=False, help_text="Sequence is ready for public viewing", verbose_name="Publish Sequence")

    def __str__(self):
        return self.title

    @property
    def is_sequence(self):
        return True

    @property
    def icon(self):
        return mark_safe('<i class="material-icons">format_list_numbered</i>')
        return mark_safe('<span class="oi oi-sort-ascending"></span>')

    @property
    def beast(self):
        return mark_safe(self.icon + ' Sequence')

    class Meta:
        permissions = (
            ("can_edit_sequence", "Edit Sequence"),
            ("can_add_sequence", "Add Sequence"),
            ("can_view_solution", "View Solution"))


class SequenceItems(models.Model):
    sequence = models.ForeignKey(
        Sequence, blank=True, null=True, on_delete=models.CASCADE, related_name='itemSequences')
    problem = models.ForeignKey(
        Problem, blank=True, null=True, on_delete=models.CASCADE, related_name='itemProblems')
    activity = models.ForeignKey(
        Activity, blank=True, null=True, on_delete=models.CASCADE, related_name='itemActivities')
    item_position = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    role_in_sequence = models.TextField(blank=True, null=True)
    required = models.CharField(max_length=255, blank=True)


course_number_validator = RegexValidator(
    regex=r'^ph\d+$', message='Enter a value of form ph123')


class Course(models.Model):
    catalog_name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Course name in catalog")
    short_name = models.CharField(
        max_length=255, blank=True, null=True, help_text="A human-friendly short name of course")
    number = models.CharField(max_length=255, blank=True, null=True,
                              help_text='include ph e.g. "ph425"',
                              validators=[course_number_validator])
    quarter_numbers = models.CharField(max_length=255, blank=True, null=True,
                                       help_text='e.g. Fall of Junior year = 7, comma delimit if taught at multiple stages')
    description = models.TextField(
        blank=True, null=True, verbose_name='Description in catalog')
    learning_resources = models.TextField(
        blank=True, verbose_name='Syllabus learning resources')
    prereq = models.TextField(blank=True, null=True,
                              verbose_name='Prerequisites')
    publication = models.BooleanField(
        blank=False, default=False, help_text="Course is ready for public viewing", verbose_name="Publish course")
    credits = models.PositiveIntegerField(default=3)

    def __str__(self):
        if self.short_name is not None:
            return self.short_name
        if self.catalog_name is not None:
            return self.catalog_name
        if self.number is not None:
            return self.number
        return 'Course<{}>'.format(self.id)

    @property
    def pretty_number(self):
        ''' like PH 365 '''
        if 'ph' == self.number[:2]:
            return 'PH ' + self.number[2:]
        return self.number

    @property
    def quarter_integer(self):
        ''' gives an integer that is the first quarter listed in its quarter_numbers '''
        n = self.quarter_numbers
        idx = self.quarter_numbers.find(',')
        if idx > 0:
            n = n[:idx]
        n = n.strip()
        try:
            return int(n)
        except:
            return 13


class CourseLearningOutcome(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    outcome = models.CharField(max_length=255, blank=True, null=True,
                               help_text="A human-friendly short name of course")

    def __str__(self):
        if self.course.number is not None:
            return self.course.number+': ' + str(self.number)+') ' + self.outcome
        return str(self.course)+': ' + str(self.number)+') ' + self.outcome

class CourseAsTaught(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='year')
    instructor = models.CharField(max_length=255, blank=True, null=True)
    office_hours = models.TextField(blank=True)

    evaluation = models.TextField(blank=True)
    modification_version = models.PositiveIntegerField(default=0)

    def __str__(self):
        if self.course.number is not None:
            return self.course.number+' ' + self.year
        return str(self.course)+' ' + self.year
    
    class Meta:
        verbose_name = 'Course as taught'
        verbose_name_plural = 'Courses as taught'

    @property
    def possible_topics(self):
        keys = set()
        for d in self.courseday_set.all():
            for a in d.activities.all():
                keys.update(a.split_topics)
            for a in d.problems.all():
                keys.update(a.split_topics)
            keys.update([t.strip() for t in d.topic.replace('\\', ' ').split(' ') if t.strip() != ''])
        return keys

    @property
    def possible_activities(self):
        ''' a list of activities that could be added '''
        query = models.Q(title='This should never happen')
        for t in self.possible_topics:
            query |= models.Q(topics__icontains=t)

        return Activity.objects.filter(query).exclude(day__taught=self)


    @property
    def possible_problems(self):
        ''' a list of problems that could be added '''
        query = models.Q(problem_title='This should never happen')
        for t in self.possible_topics:
            query |= models.Q(topics__icontains=t)
        return Problem.objects.filter(query).exclude(day__taught=self)
    @property
    def has_activities(self):
        ''' are there any activities in this course? '''
        return True
    @property
    def has_topics(self):
        ''' are there any topics in this course? '''
        return CourseDay.objects.filter(taught=self).exclude(topic='')
    @property
    def has_resources(self):
        ''' are there any resources in this course? '''
        return CourseDay.objects.filter(taught=self).exclude(resources='')

class CourseDay(models.Model):
    taught = models.ForeignKey(CourseAsTaught, on_delete=models.CASCADE)
    order = models.CharField(max_length=255, default='')
    day = models.CharField(max_length=255)
    topic = models.TextField(blank=True, default='')
    resources = models.TextField(blank=True, default='')
    problemsetname = models.CharField(max_length=255, blank=True)
    show_solution = models.BooleanField(blank=False, default=False, help_text="Show problem set solution to students.")
    show_problemset = models.BooleanField(blank=False, default=False, help_text="Show problem set to students.")

    activities = models.ManyToManyField(Activity, through='DayActivity', related_name='day')
    problems = models.ManyToManyField(Problem, through='DayProblem',
                                      through_fields=('day', 'problem'), related_name='day')

    problemset = models.ManyToManyField(Problem, through='DayProblem',
                                        through_fields=('due', 'problem'), related_name='due')

    def __str__(self):
        return str(self.taught)+' day ' + self.day

    @property
    def possible_due(self):
        ''' a list of days things could be due '''
        return self.taught.courseday_set.filter(order__gte=self.order).exclude(problemsetname='').order_by('order')

    @property
    def problemset_data(self):
        ''' problem set data due today '''
        return DayProblem.objects.filter(due=self).order_by('order')

    @property
    def problemset_slug(self):
        return slugify(self.problemsetname)

def slugify(x):
    s = x.replace(' ', '').lower()
    if s == '':
        return 'none'
    return s

class DayActivity(models.Model):
    day = models.ForeignKey(CourseDay, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    order = models.CharField(max_length=8, blank=True)
    show_handout = models.BooleanField(blank=False, default=False, help_text="Show handout to students.")
    show_solution = models.BooleanField(blank=False, default=False, help_text="Show solution to students.")

    class Meta:
        ordering = ['day__order', 'order']

class DayProblem(models.Model):
    day = models.ForeignKey(CourseDay, on_delete=models.CASCADE, related_name='dayproblem')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    order = models.CharField(max_length=8, blank=True)
    instructions = models.CharField(max_length=255, blank=True, default='')
    due = models.ForeignKey(CourseDay, on_delete=models.CASCADE, related_name='problem_due')

    class Meta:
        ordering = ['due__order', 'order']

# class Pages(models.Model):
#     title = models.TextField(blank=True, null=True)
#     contents = models.TextField(blank=True, null=True)
#
# class PageImage(models.Model):
#     page = models.ForeignKey(Pages, on_delete=models.CASCADE)
#     image = models.ImageField(blank=True, null=True, upload_to='page_images/')
#     title = models.TimeField(blank=True, null=True)
#     caption = models.TextField(blank=True, null=True)
#     uploaded_at = models.DateTimeField(auto_now_add=True)
