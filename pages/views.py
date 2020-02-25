#from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from admin_app.models import Pages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from pages.forms import PageForm

# class Home(TemplateView):
#         template_name = 'home.html'
def home(request):
        return render(request, 'pages/home.html', {})

class Loggedout(TemplateView):
        template_name = 'logout.html'

def white_papers(request):
        return render(request, 'pages/white_papers.html', {})

def about(request):
        return render(request, 'pages/about.html', {})

def history(request):
        return render(request, 'pages/history.html', {})

def courses(request):
        return render(request, 'pages/courses.html', {})

# class renderpage(DetailView):
#     model = Pages
#     template_name = 'pages/render.html'

def renderpage(request, pagename):
        this_page = get_object_or_404(Pages, slug=pagename)
        context = {
                'pagename': pagename,
                'this_page': this_page,
        }
        if this_page.keywords:
                keyword_list = this_page.keywords.strip().rstrip(",").split(",")
                keyword_list = map(str.strip, keyword_list)
                context = {
                        'pagename': this_page.title,
                        'this_page': this_page,
                        'keyword_list': keyword_list,
                }
        return render(request, 'pages/render.html', context)

def page_title(request, pagename):
        page = get_object_or_404(Pages, slug=pagename)
        return HttpResponse(page.title)

# Url for home page is handled slightly differently because it doesn't use a slug/pagename to identify itself
def renderhomepage(request):
        this_page = get_object_or_404(Pages, slug='home')
        thisPrimaryKey = this_page.pk
        figures_list = Pages.objects.get(id=thisPrimaryKey).media.all()
        context = {
                'pagename': this_page.title,
                'this_page': this_page,
                'thisPrimaryKey': thisPrimaryKey,
                'figures_list': figures_list,
        }
        if this_page.keywords:
                keyword_list = this_page.keywords.strip().rstrip(",").split(",")
                keyword_list = map(str.strip, keyword_list)
                context = {
                        'pagename': this_page.title,
                        'this_page': this_page,
                        'thisPrimaryKey': thisPrimaryKey,
                        'keyword_list': keyword_list,
                        'figures_list': figures_list,
                }

        return render(request, 'pages/render.html', context)

@permission_required('admin_app.can_edit_pages',login_url='/')
def editpage(request, pagename):
        this_page = get_object_or_404(Pages, slug=pagename)
        thisPrimaryKey = this_page.pk
        figures_list = Pages.objects.get(id=thisPrimaryKey).media.all()
        if request.method == "POST":
                form = PageForm(request.POST, instance=this_page)
                if form.is_valid():
                        this_page = form.save(commit=False)
                        this_page.save()
                        return redirect('page_edit', pagename=this_page.slug)
                else:
                        messages.error(request, form.errors)
        else:
                form = PageForm(instance=this_page)
                context = {
                        'pagename': pagename,
                        'this_page': this_page,
                        'thisPrimaryKey': thisPrimaryKey,
                        'form': form,
                        'figures_list': figures_list,
                }
        return render(request, 'pages/edit.html', context)

def editpagebyid(request, pk):
        # this_page = get_object_or_404(Pages, slug=pagename)
        this_page = get_object_or_404(Pages, pk=pk)
        thisPrimaryKey = this_page.pk
        figures_list = Pages.objects.get(id=thisPrimaryKey).media.all()
        if request.method == "POST":
                form = PageForm(request.POST, instance=this_page)
                if form.is_valid():
                        this_page = form.save(commit=False)
                        this_page.save()
                        return redirect('page_edit_by_id', pk=this_page.pk)
                else:
                        messages.error(request, form.errors)
        else:
                form = PageForm(instance=this_page)
                context = {
                        'pk': pk,
                        'this_page': this_page,
                        'thisPrimaryKey': thisPrimaryKey,
                        'form': form,
                        'figures_list': figures_list,
                }
        return render(request, 'pages/edit.html', context)
