from django.db import models
from django.db.models import QuerySet
from typing import List, Optional
from django.core.paginator import Paginator


class BaseRepository:

    model: models.Model = None  # To be defined in subclasses

    @classmethod
    def get_all(cls, page: int, size: int, filters: dict) -> QuerySet:
        queryset = cls.model.objects.filter(**filters).all()
        paginator = Paginator(queryset, page)
        return paginator.object_list

    @classmethod
    def get_by_id(cls, object_id) -> Optional[models.Model]:
        return cls.model.objects.filter(id=object_id).first()

    @classmethod
    def create(cls, **kwargs) -> models.Model:
        instance = cls.model(**kwargs)
        instance.save()
        return instance

    @classmethod
    def get_by_filters(cls, filters: dict) -> Optional[List[models.Model]]:
        return cls.model.objects.filter(**filters).all()

    @classmethod
    def update(cls, instance: models.Model, **kwargs) -> models.Model:
        for attr, value in kwargs.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @classmethod
    def delete(cls, instance: models.Model):
        instance.delete()
