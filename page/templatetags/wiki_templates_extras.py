from django import template

register = template.Library()

@register.filter(name='tags_to_string')
def tags_to_string(tag_query_set):
	return ", ".join([str(x) for x in tag_query_set.all().values_list('name', flat=True)])
