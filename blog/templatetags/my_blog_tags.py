import datetime

from django import template
from django.db.models.fields.files import FieldFile

register = template.Library()


@register.simple_tag
@register.filter()
def mediapath(data: FieldFile) -> str:
    """
    Make url path to media
    """
    return data.url if data else '#'


@register.simple_tag
@register.filter()
def formatted_data(data_time_obj: datetime) -> datetime:
    """
    change datetime format
    """
    return data_time_obj.strftime("%d-%m-%Y %H:%M")
