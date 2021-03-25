from django.template.defaulttags import register

@register.filter
def get_object_list(paginator, page_obj):
    return list(paginator.page(page_obj.number).object_list)


@register.filter
def get_object_list_item_index(object_list, item):
    return object_list.index(item)
