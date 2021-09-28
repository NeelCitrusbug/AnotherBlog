from rest_framework.response import Response
from rest_framework.permissions import  AllowAny
from core.api.serializers import ContactUsSerializer
from core.api.apiviews import MyAPIView

# .................................................................................
# contact us API
# .................................................................................


class ContactUsCreateAPI(MyAPIView):

    """API View to create contact us"""

    permission_classes = (AllowAny,)
    serializer_class = ContactUsSerializer

    def post(self, request, format=None):

        request.data._mutable = True
        request.data['user']=request.user.id
        serializer = self.serializer_class(data=request.data,  context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "OK", "message": "Successfully submitted details", "data": serializer.data})

        else:
            return Response({"status": "FAIL", "message": "Cannot submit contact us", "data": serializer.errors})

       