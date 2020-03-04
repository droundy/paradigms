from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from admin_app.choices import *
from admin_app.models import Pages
from django.db.models import Q

register = template.Library()

# The following tag will display a list of hrefs for inclusion in a 
# standard bootstrap nav dropdown list
# The list is populated by querying the boolean field whitepaper for "1", and the choice field
# whitepaper_category using the value passed from the tag

@register.filter(needs_autoescape=True)
def whitepaperdropdownlist(value, autoescape=True):
    if value:
        links = Pages.objects.filter(Q(whitepaper__exact=1) and Q(whitepaper_category__exact=value)).order_by('title')
        link_list = ''
        for link in links:
            link_list += '<a class="dropdown-item" href="/whitepaper/' + link.slug + '">' + link.title + '</a>'
        return mark_safe(link_list)
    else:
        return value

@register.filter(needs_autoescape=True)
def pagelist(value, authorization, autoescape=True):
    if value:
        page_links = ''
        whitepaper_links = ''
        #  Return a list of all records, whitepapers and pages
        if value == 'all':
            # Queries for user with permissions
            if authorization == 1:
                # Exclude whitepapers for the page links
                page_links = Pages.objects.exclude(Q(whitepaper__exact=1)).order_by('title')
                # Include whitepapers for the whitepaper links
                whitepaper_links = Pages.objects.filter(Q(whitepaper__exact=1)).order_by('title') 
                # Queries for the user without permissions
            else:
                # Exclude whitepapers and unpublished pages
                page_links = Pages.objects.exclude(Q(whitepaper__exact=1)).filter(Q(publication__exact=1)).order_by('title')
                # Include published whitepapers only
                whitepaper_links = Pages.objects.filter(Q(whitepaper__exact=1) and Q(publication__exact=1)).order_by('title')
                    
        else:
            # return list of only whitepapers
            # Queries for user with permissions
            if authorization == 1:
                # Find all whitepapers for this category
                whitepaper_links = Pages.objects.filter(Q(whitepaper__exact=1) and Q(whitepaper_category__exact=value)).order_by('title')            
            else:
                # Exclude unpublished whitepapers for this category
                whitepaper_links = Pages.objects.filter(Q(whitepaper__exact=1) and Q(whitepaper_category__exact=value) and Q(publication__exact=1)).order_by('title')

        if page_links:
            page_link_list = '<div class="list-group"><h5 class="list-group-item">Pages</h5>'
            for link in page_links:                
                if link.publication == True:
                    page_link_list += '<a href="/' + str(link.slug) + '" class="list-group-item list-group-item-action"><div class="d-flex w-100 justify-content-between"><h6  class="mb-1"><span class="oi oi-link-intact"></span></span> ' + str(link.title) + '</h6></div></a>'
                else:
                    page_link_list += '<a href="/' + str(link.slug) + '" class="list-group-item list-group-item-action"><div class="d-flex w-100 justify-content-between"><h6  class="mb-1"><span class="oi oi-link-intact"></span></span> ' + str(link.title) + '</h6> <span class="badge badge-danger"><span class="oi oi-warning"></span> Draft</span></div></a>'
            page_link_list = page_link_list + '</div>'

        if whitepaper_links:
            whitepaper_link_list = '<div class="list-group" style="margin-top: 1.5em;"><h5 class="list-group-item list-group-item-action">Whitepapers</h5>'
            for link in whitepaper_links:
                if link.publication == True:
                    whitepaper_link_list += '<a href="/whitepaper/' + str(link.slug) + '" class="list-group-item list-group-item-action"><div class="d-flex w-100 justify-content-between"><h6  class="mb-1"><span class="oi oi-document"></span></span> ' + str(link.title) + '</h6></div> <small>' + str(link.whitepaper_category) + '</small></a>'
                else:
                    whitepaper_link_list += '<a href="/whitepaper/' + str(link.slug) + '" class="list-group-item list-group-item-action"><div class="d-flex w-100 justify-content-between"><h6  class="mb-1"><span class="oi oi-document"></span></span> ' + str(link.title) + '</h6> <span class="badge badge-danger"><span class="oi oi-warning"></span> Draft</span></div><small>' + str(link.whitepaper_category) + '</small></a>'
            whitepaper_link_list = whitepaper_link_list + '</div>'
        
        if whitepaper_links and page_links:
            return mark_safe(page_link_list + whitepaper_link_list)

        if whitepaper_links and not page_links:
            return mark_safe(whitepaper_link_list)

        if page_links and not whitepaper_links:
            return mark_safe(page_link_list)
    else:
        return value