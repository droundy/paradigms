from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from admin_app.choices import *
from admin_app.models import Activity, ActivityMedia, MediaAssociation, Sequence, SequenceItems

register = template.Library()

@register.filter(name='trimtob')


# topic_list = activity.topics.strip().rstrip(",").split(",")
# topic_list = map(str.strip, topic_list)


# def cut(value, arg):
#     """Removes all values of arg from the given string"""
#     return value.replace(arg, '')

# Used to repair type_of_beast formatting
# {{ activity.type_of_beast|trimtob }}
def trimtob(value):
    if value:
        tob = value.strip("('")
        tob = tob.strip("'),")
        # iterate through possible choices for type of beast
        for beast in BEASTICONS:
            if tob == beast[0]:
                tob = '<span class="oi oi-' + beast[1] + '"></span> ' + tob
        return mark_safe(tob)
    else:
        return value

@register.filter(needs_autoescape=True)
def tagbuttons(value, autoescape=True):
    if value:
        topic_list = value.strip().rstrip(",").split(",")
        topic_list = map(str.strip, topic_list)
        buttons = ''
        for topic in topic_list:
            buttons += '<a class="badge badge-secondary" href="/search/keyword/' + topic + '">' + topic + '</a> '
        return mark_safe(buttons)
    else:
        return value

# The following "filter" takes an Activity ID and builds a mini navigational system showing which sequences contain this activity and a previous / next link to next items in that sequence
@register.filter(needs_autoescape=True)
def activitysequencepager(sequenceid, activityid, autoescape=True):

    if sequenceid and activityid:
        
        return_html = ""
        bigger_html = ""
        smaller_html = ""

        # create a query that at least finds the name of the sequence if no position is available
        sequence_name_sql = 'SELECT s.id, s.title as sequence_title FROM admin_app_sequence s WHERE s.id = "' + str(sequenceid) + '"'

        for sequence in Sequence.objects.raw(sequence_name_sql): 
            sequence_html = ' <strong><a href="/sequences/' + str(sequenceid) + '"/>' + str(sequence.sequence_title) + '</a></strong>'

            # print(sequence_html)
        
        item_position_sql = 'SELECT id, item_position FROM admin_app_sequenceitems WHERE sequence_id = "' + str(sequenceid) + '" AND activity_id = "' + str(activityid) + '"'
        
        #  Given a known position for this item in the sequence, find the next biggest and smallest items
        for position in SequenceItems.objects.raw(item_position_sql):
            # print(position.item_position)

            smaller_item_sql = 'SELECT s.title AS sequence_title, i.id, i.item_position, i.problem_id, i.activity_id, a.title AS activity_title, p.problem_title FROM admin_app_sequence s, admin_app_sequenceitems i LEFT JOIN admin_app_problem p ON i.problem_id = p.id LEFT JOIN admin_app_activity a ON i.activity_id = a.id WHERE s.id = "' + str(sequenceid) + '" AND sequence_id = "' + str(sequenceid) + '" AND item_position < "' + str(position.item_position) + '" ORDER BY item_position DESC  LIMIT 1;'
            
            print("SMALLER: " + smaller_item_sql)
        
            smaller_item_records = SequenceItems.objects.raw(smaller_item_sql)

            # print(smaller_item_records)

            # Collect information about the smaller item
            for item in smaller_item_records:
                
                if item.problem_id:
                    smaller_html += '&lt; &lt; <a href="/problem/' + str(item.problem_id) + '">' + str(item.problem_title) + '</a>'
                
                if item.activity_id:
                    smaller_html = '&lt; &lt; <a href="/activities/' + str(item.activity_id) + '">' + str(item.activity_title) + '</a>'

                sequence_html = ' <a href="/sequences/' + str(sequenceid) + '"/>' + str(item.sequence_title) + '</a>'

                return_html = str(smaller_html) + ' <a href="/sequence/' + str(sequenceid) + '"/>' + str(item.sequence_title) + '</a>'

            bigger_item_sql = 'SELECT s.title AS sequence_title, i.id, i.item_position, i.problem_id, i.activity_id, a.title AS activity_title, p.problem_title FROM admin_app_sequence s, admin_app_sequenceitems i LEFT JOIN admin_app_problem p ON i.problem_id = p.id LEFT JOIN admin_app_activity a ON i.activity_id = a.id WHERE s.id = "' + str(sequenceid) + '" AND sequence_id = "' + str(sequenceid) + '" AND item_position > "' + str(position.item_position) + '" ORDER BY item_position ASC LIMIT 1;'
            
            print('BIGGER: ' + bigger_item_sql)
        
            bigger_item_records = SequenceItems.objects.raw(bigger_item_sql)

            # print(bigger_item_records)

            # Collect information about the bigger item
            for item in bigger_item_records:
                
                if item.problem_id:
                    bigger_html += '<a href="/problem/' + str(item.problem_id) + '">' + str(item.problem_title) + '</a> &gt; &gt;'
                
                if item.activity_id:
                    bigger_html += '<a href="/activities/' + str(item.activity_id) + '">' + str(item.activity_title) + '</a>  &gt; &gt; '
                
                sequence_html = ' <a href="/sequences/' + str(sequenceid) + '"/>' + str(item.sequence_title) + '</a>'

            
            if smaller_html and bigger_html:
                return_html = smaller_html + ' | <strong>' + sequence_html + '</strong> | ' + bigger_html

            if smaller_html and not bigger_html:
                return_html = smaller_html + ' | <strong>' + sequence_html + '</strong> | ' + bigger_html

            if bigger_html and not smaller_html:
                return_html = '<strong>' + sequence_html + '</strong> | ' + bigger_html


            if not bigger_html and not smaller_html: 
                return_html = sequence_html

        return mark_safe(return_html)
    

    else:
        return "This Activity is not associated with any sequences."