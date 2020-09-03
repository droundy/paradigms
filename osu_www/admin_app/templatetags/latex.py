from django import template
from django import urls
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import bs4
import os
import latex_snippet

from admin_app.models import Activity, Problem, Pages, Sequence, Course

register = template.Library()

os.environ['RUST_BACKTRACE'] = '1'


@register.filter()
def latex_with_solution(value):
    if value:
        return mark_safe(modify_html(latex_snippet.html_with_solution(value)))
    else:
        return value


@register.filter()
def latex_omit_solution(value):
    if value:
        return mark_safe(modify_html(latex_snippet.html_omit_solution(value)))
    else:
        return value


def append_class(tag, c):
    tag['class'] = tag.get('class', []) + [c]


def modify_html(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    for a in soup.find_all('a'):
        # print('href:', a['href'])
        # print('contents:', a.contents)
        href = a['href']
        if len(href) > 0 and href[0] == '/' and [href] == a.contents:
            try:
                try:
                    match = urls.resolve(href)
                except:
                    match = urls.resolve(href+'/')
                if match.view_name == 'activity_detail' and 'pk' in match.kwargs:
                    for activity in Activity.objects.filter(pk=match.kwargs['pk']):
                        new = soup.new_tag('a', href=href)
                        new.string = latex_snippet.html_omit_solution(
                            activity.title)
                        a.replaceWith(new)
                elif match.view_name == 'problem_display_html' and 'pk' in match.kwargs:
                    for problem in Problem.objects.filter(pk=match.kwargs['pk']):
                        new = soup.new_tag('a', href=href)
                        new.string = latex_snippet.html_omit_solution(
                            problem.problem_title)
                        a.replaceWith(new)
                elif match.view_name == 'page_display' and 'pagename' in match.kwargs:
                    for page in Pages.objects.filter(slug=match.kwargs['pagename']):
                        new = soup.new_tag('a', href=href)
                        new.string = latex_snippet.html_omit_solution(
                            page.title)
                        a.replaceWith(new)
                elif match.view_name == 'sequence_detail' and 'pk' in match.kwargs:
                    for sequence in Sequence.objects.filter(pk=match.kwargs['pk']):
                        new = soup.new_tag('a', href=href)
                        new.string = latex_snippet.html_omit_solution(
                            sequence.title)
                        a.replaceWith(new)
                elif match.view_name == 'course_view' and 'number' in match.kwargs:
                    for course in Course.objects.filter(number=match.kwargs['number']):
                        new = soup.new_tag('a', href=href)
                        new.string = latex_snippet.html_omit_solution(
                            course.short_name)
                        a.replaceWith(new)
            except:
                print('unable to resolve', href)
                pass
    # Apply the bootstrap classes to semantic elements.
    for t in soup.find_all('img'):
        append_class(t, 'img-fluid')
        # get any figures with no path from the /media/figures/
        # directory.
        if '/' not in t['src']:
            t['src'] = '/media/figures/' + t['src']
    for t in soup.find_all('figure'):
        append_class(t, 'figure')
        if 'wrapfigure' in t['class']:
            append_class(t, 'float-sm-right')
            append_class(t, 'mw-100')
        for i in t.find_all('img'):
            append_class(i, 'figure-img')
    for t in soup.find_all('figcaption'):
        append_class(t, 'figure-caption')
    return str(soup)
