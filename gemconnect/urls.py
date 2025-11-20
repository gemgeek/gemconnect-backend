from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from django.conf import settings
from django.conf.urls.static import static

# SIMPLE FUNCTION
@csrf_exempt
def ping_view(request):
    return JsonResponse({"message": "pong"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ping/', ping_view),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)