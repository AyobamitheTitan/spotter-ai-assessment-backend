from rest_framework.exceptions import NotFound


class BaseApiService:
    repository_class = None  # Must be set by child classes

    @classmethod
    def get_all(cls, page: int = 10, size: int = 0, filters: dict = {}):
        return cls.repository_class.get_all(page, size, filters)

    @classmethod
    def get_by_id(cls, pk):
        """Retrieve an object by its primary key."""
        instance = cls.repository_class.get_by_id(pk)
        if not instance:
            raise NotFound("Object not found")
        return instance

    @classmethod
    def create(cls, validated_data):
        return cls.repository_class.create(**validated_data)

    @classmethod
    def update(cls, instance, validated_data):
        return cls.repository_class.update(instance, **validated_data)

    @classmethod
    def delete(cls, instance):
        return cls.repository_class.delete(instance)
