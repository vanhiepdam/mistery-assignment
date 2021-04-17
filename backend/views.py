import os
import logging
from django.conf import settings
from django.http import HttpResponse
from django.views import View

index_file_path = os.path.join(settings.REACT_APP_DIR, "build", "index.html")


class ReactAppView(View):

    def get(self, request):
        try:
            with open(index_file_path) as file:
                return HttpResponse(file.read())
        except :
            return HttpResponse(
                """
                index.html not found ! build your React app !!
                """,
                status=501,
            )
