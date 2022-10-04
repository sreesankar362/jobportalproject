"""jobportalproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("home.urls")),
<<<<<<< HEAD
    path('employer/',include("companyaccount.urls")),

]
||||||| 1613bdc
    path('company/',include("companyaccount.urls"))
]
=======
    path('company/',include("companyaccount.urls"))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

>>>>>>> f41c6a974fcd56f57609f9cfd08ee6b068f9481a
