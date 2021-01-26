from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):  # returns None if key does not exist
    return dictionary.get(key)
