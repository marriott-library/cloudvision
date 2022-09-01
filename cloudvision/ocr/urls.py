from django.urls import path
from django.contrib import admin
from django.urls import include, re_path
from django.views import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.oai, name='oai'),
    path('ocr/', views.oai, name='oai'),
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),

    path('results/', views.results, name='results'),
    path('results/<int:job_id>', views.results, name='results'),
    path('results/ocr_download/<str:uuid>', views.ocr_download, name='ocr_download'),
    path('ajax/load-sets/', views.load_sets, name='ajax_load_sets'),  # <-- url for loading sets
    path('ajax/load-records/', views.load_records, name='ajax_load_records'),  # <-- url for loading records
    path('import/', views.import_tsv, name='import'),
    path('oai/', views.oai, name='oai'),
    path('download/<str:filename>', views.template_tsv, name='template_tsv'),
    path('redirect/', views.redirect_page, name='redirect'),


    # DB Operation URL
    path('get/', views.get_all, name='read'),  # <-- read all Log records,
    path('get/<job_id>', views.get, name='get'),  # <-- read Log record by id,

    # File Access
    re_path(r'^data/(?P<path>.*)$', static.serve, {'document_root': settings.DATA_DIR + "/"}),
]
