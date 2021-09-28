from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from core.models import Banner
from core.api.apiviews import MyAPIView
from core.api.serializers import BannerSerializer

# .................................................................................
# Banner list API
# .................................................................................


class BannerListAPIView(MyAPIView):
    """
    API View for banner  listing
    """

    permission_classes = (AllowAny,)
    serializer_class = BannerSerializer

    def get(self, request):
        banner = Banner.objects.all().order_by("-created_at")
        serializer = self.serializer_class(
            banner, many=True, context={"request": request}
        )
        return Response(
            {
                "status": "OK",
                "message": "Successfully fetched banner list",
                "data": serializer.data,
            }
        )
