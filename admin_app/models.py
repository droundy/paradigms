from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from autoslug import AutoSlugField
import os
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
    keywords = models.TextField(blank=True, null=True, help_text="Comma-separated list of topics or keywords: adiabatic susceptibility,entropy")
    published_date = models.DateTimeField(blank=True, null=True)
    media = models.ManyToManyField(PageMedia, through='PageMediaAssociation', related_name='pagemedias')
    whitepaper = models.BooleanField(blank=False, default=False, help_text="Is this a whitepaper?", verbose_name="Whitepaper")
    whitepaper_category = models.CharField(max_length=255,blank=True, null=True, help_text="If this page is meant to be a whitepaper, please select a category. The category list is maintained by system administrators and can not be dynamic.")
    publication = models.BooleanField(blank=False, default=False, help_text="Whitepaper is ready for public viewing.", verbose_name="Publish Whitepaper")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        permissions = (
            ("can_edit_pages", "Edit Pages"),
            ("can_add_pages","Add Pages"),)

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

class Problem(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problem_title = models.CharField(max_length=255)
    problem_latex = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    attribution = models.CharField(max_length=255, help_text="Original source information.", blank=True, null=True)
    old_name = models.CharField(max_length=255, help_text="Name from original homework archive.", blank=True, null=True)
    topics = models.TextField(blank=True, null=True, help_text="Comma-separated list of topics: adiabatic susceptibility,entropy")
    figures = models.ManyToManyField(Figure, through='FigureAssociations', related_name='problems')
    course = models.CharField(max_length=255, blank=True, null=True)
    publication = models.BooleanField(blank=False, default=False, help_text="Problem is ready for public viewing", verbose_name="Publish Problem")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.problem_title

    class Meta:
        permissions = (
            ("can_edit_problem", "Edit Problem"),
            ("can_add_problem","Add Problem"),
            ("can_view_solution","View Solution"))

class ProblemSet(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    author = author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author_info = models.CharField(max_length=4096, blank=True, null=True)
    publication = models.BooleanField(blank=False, default=False, help_text="Problem Set is ready for public viewing. Takes 5-10 seconds to generate new problem set PDFs", verbose_name="Publish Problem Set")
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
            ("can_add_problem_set","Add Problem Set"),
            ("can_view_solution","View Solution"))

class ProblemSetItems(models.Model):
    problem = models.ForeignKey(Problem, blank=True, null=True, on_delete=models.CASCADE, related_name='itemProblem')
    problem_set = models.ForeignKey(ProblemSet, blank=True, null=True, on_delete=models.CASCADE, related_name='set_problems')
    item_position = models.DecimalField(max_digits=5, decimal_places=2, default=1, blank=True, null=True)
    item_instructions = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['item_position']
    # def __str__(self):
    #     return self.problem

class ProblemSetPDFs(models.Model):
    pdf = models.FileField(upload_to='problem_set_pdfs/')
    problem_set = models.ForeignKey(ProblemSet, on_delete=models.CASCADE, related_name="problem_set_pdfs")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    solution = models.BooleanField(blank=False, default=False, help_text="Does this include the solution?", verbose_name="Solution Included")

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
    activity_image = models.ImageField(blank=True, null=True, upload_to='activity_images/')
    keywords = models.TextField(blank=True, null=True)
    author = author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    associated_paper_links = models.TextField(blank=True, null=True)
    program_learning_outcomes = models.TextField(blank=True, null=True)
    course_learning_outcomes = models.TextField(blank=True, null=True)
    learning_progression_concepts = models.TextField(blank=True, null=True)
    course = models.CharField(max_length=255, blank=True, null=True)
    author_info = models.CharField(max_length=4096, blank=True, null=True)
    media = models.ManyToManyField(ActivityMedia, through='MediaAssociation', related_name='medias')
    old_name = models.CharField(max_length=255, blank=True, null=True)

    def publish(self):
        self.publication_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        permissions = (
            ("can_edit_activity", "Edit Activity"),
            ("can_add_activity","Add Activity"),
            ("can_view_solution","View Solution"))

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
    problems = models.ManyToManyField(Problem, through='SequenceItems', related_name='problems')
    activities = models.ManyToManyField(Activity, through='SequenceItems', related_name='activities')
    author = author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author_info = models.CharField(max_length=4096, blank=True, null=True)
    publication = models.BooleanField(blank=False, default=False, help_text="Sequence is ready for public viewing", verbose_name="Publish Sequence")

    def __str__(self):
        return self.title

    class Meta:
        permissions = (
            ("can_edit_sequence", "Edit Sequence"),
            ("can_add_sequence","Add Sequence"),
            ("can_view_solution","View Solution"))

class SequenceItems(models.Model):
    sequence = models.ForeignKey(Sequence, blank=True, null=True, on_delete=models.CASCADE, related_name='itemSequences')
    problem = models.ForeignKey(Problem, blank=True, null=True, on_delete=models.CASCADE, related_name='itemProblems')
    activity = models.ForeignKey(Activity, blank=True, null=True, on_delete=models.CASCADE, related_name='itemActivities')
    item_position = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    role_in_sequence = models.TextField(blank=True, null=True)
    required = models.CharField(max_length=255, blank=True)

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
