from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound


class BaseAPIView(APIView):
    """
    Abstract base view to support CRUD operations for models.
    Handles core DRF APIView responsibilities and delegates extended behavior to subclasses.
    """

    model_class = None  # Set in subclass
    serializer_class = None  # Set in subclass
    service_class = None  # Set in subclass

    def get_object(self, pk):
        return self.service_class.get_by_id(pk)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk:
            instance = self.get_object(pk)
            if not instance:
                return Response(
                    {"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND
                )

            return Response(
                {"data": self.serializer_class(instance).data, "message": "Retrieved"}
            )
        else:
            queryset = self.service_class.get_all()
            serializer = self.serializer_class(queryset, many=True)
            return Response({"data": serializer.data, "message": "Retrieved"})

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            instance = self.service_class.create(serializer.validated_data)
            return Response(
                self.serializer_class(instance).data, status=status.HTTP_201_CREATED
            )

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        instance = self.get_object(pk)
        if not instance:
            raise NotFound("Object not found")

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            instance = self.service_class.update(instance, serializer.validated_data)
            return Response(self.serializer_class(instance).data)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        instance = self.get_object(pk)
        if not instance:
            raise NotFound("Object not found")

        self.service_class.delete(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
