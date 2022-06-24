"""File Model."""
from masoniteorm.models import Model
from masoniteorm.scopes import SoftDeletesMixin


class File(Model, SoftDeletesMixin):
    __fillable__ = ['id', 'name', 'size', 'type', 'user_email']
