from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import bs4
import latex_snippet

register = template.Library()

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
        print('href:', a['href'])
        print('contents:', a.contents)
        if len(a['href']) > 0 and a['href'][0] == '/' and [a['href']] == a.contents:
            # FIXME we could now look this up on the server rather
            # than asking the client to look up the title...
            iframe = soup.new_tag('iframe', src=a['href']+'/title',
                                  onload = "this.before(this.contentDocument.body.innerHTML);this.remove()")
            a.clear()
            a.append(iframe)
    # Apply the bootstrap classes to semantic elements.
    for t in soup.find_all('img'):
        append_class(t, 'img-fluid')
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
