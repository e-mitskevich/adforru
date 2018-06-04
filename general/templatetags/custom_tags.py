from django.template.defaulttags import register


@register.filter
def lookup(collection, key):
    return collection[key]
