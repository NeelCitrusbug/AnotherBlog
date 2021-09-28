from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.api.serializers import EventScriptSerializer
from core.api.apiviews import MyAPIView
from core.models import EventScript

# .................................................................................
# Event Script API
# ..................................................................................


class ScriptCreateAPI(MyAPIView):
    """API View to create Event script"""

    permission_classes = (IsAuthenticated,)
    serializer_class = EventScriptSerializer

    def post(self, request):

        check = EventScript.objects.filter(event__id=request.data['event']).exists()

        if check:
            check = EventScript.objects.filter(event__id=request.data['event']).delete()


        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "OK",
                    "message": "Successfully submitted event script details",
                    "data": serializer.data,
                }
            )
        else:
            return Response(
                {
                    "status": "FAIL",
                    "message": "Cannot submit script",
                    "data": serializer.errors,
                }
            )



class ScriptListAPIView(MyAPIView):
    """
    API View for Event script  listing
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = EventScriptSerializer

    def get(self, request, pk):

        try:
            script = EventScript.objects.filter(event__id=pk).order_by("-created_at").latest("created_at")

            serializer = self.serializer_class(
                script, context={"request": request}
            )
            return Response(
                {
                    "status": "OK",
                    "message": "Successfully fetched script list",
                    "data": serializer.data,
                }
            )

        except EventScript.DoesNotExist:
                return Response(
                    {"status": "FAIL", "message": "Event script not found", "data": []}
                )    



class ScriptUpdateAPI(MyAPIView):
    """API View to update Event script """

    permission_classes = (IsAuthenticated,)
    serializer_class = EventScriptSerializer

    def put(self, request, pk):
        """ PUT method to offer the data"""
        if request.user.is_authenticated:
            try:
                event_script = EventScript.objects.get(pk=pk)
                serializer = self.serializer_class(
                    event_script, data=request.data, context={"request": request}
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {
                            "status": "OK",
                            "message": "Successfully updated  event script.",
                            "data": serializer.data,
                        }
                    )
                else:
                    return Response(
                        {
                            "status": "FAIL",
                            "message": "Cannot update event script",
                            "data": serializer.errors,
                        }
                    )
            except EventScript.DoesNotExist:
                return Response(
                    {"status": "FAIL", "message": "Event script not found", "data": []}
                )
        else:
            return Response(
                {"status": "FAIL", "message": "Unauthorised User", "data": []}
            )



class ScriptDeleteAPI(MyAPIView):
    """API View to update Event script"""

    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        """ PUT method to script the data"""
        if request.user.is_authenticated:
            try:
                EventScript.objects.get(pk=pk).delete()
                return Response(
                    {
                        "status": "OK",
                        "message": "Successfully deleted  event script.",
                        "data": [],
                    }
                )
            except EventScript.DoesNotExist:
                return Response(
                    {"status": "FAIL", "message": "Event script not found", "data": []}
                )
        else:
            return Response(
                {"status": "FAIL", "message": "Unauthorised User", "data": []}
            )
