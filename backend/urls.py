from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib import admin

from core import admin_views
from core import yönetici_views



urlpatterns = [


    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('yonetici/', yönetici_views.yindex, name='yhome'),



    # Diğer tablolar (istersen bunları da benzer şekilde RESTful URL'lere çekebilirsin)
    path('ytablesDevamB.html', yönetici_views.devam_eden_basvurular, name='ytablesDevamB'),
    path('ytablesYeniB.html', yönetici_views.yeni_basvurular,   name='ytablesYeniB'),
    path('ytablesBitenB.html', yönetici_views.biten_basvurular, name='ytablesBitenB'),

    path('ytables.html', yönetici_views.tables,   name='tables'),

    path('yyeniKullanici.html', yönetici_views.yeni_juri,   name='yeni_juri'),

        path('juri/yeni/', yönetici_views.yeni_juri_olustur, name='yeni_juri_olustur'),
     
         path('ytablesDevamB.html', yönetici_views.devam_eden_basvurular, name='tablesDevamB'),
    path('ilan/<int:ilan_id>/edit/', yönetici_views.ilan_duzenle, name='ilan_duzenle'),
    path('ilan/<int:ilan_id>/delete/', yönetici_views.ilan_sil,    name='ilan_sil'),
    

    # Sonuçlanan başvurular listesi (sadece bir tane olmalı, fazlasını sildik)
    path('ytablesSonuclananB.html',
         yönetici_views.sonuclanan_basvurular,
         name='ysonuclanan_basvurular'),

    # Bir ilanın altındaki tüm başvuruları gösteren detay sayfası
    # (template’te kullanacağın {% url 'basvurudetay' ilan_id=ilan.id %})
    path('basvurudetay/<int:ilan_id>/',
         yönetici_views.basvurudetay,
         name='basvurudetay'),

    # Tek bir başvuruya ait tüm bilgileri gösteren sayfa
    # (template’te kullanacağın {% url 'detailapplication' basvuru_id=basvuru.id %})
    path('detailapplication/<int:basvuru_id>/',
         yönetici_views.detail_application,
         name='detailapplication'),

    path('kullanicilar/',
         yönetici_views.kayitli_kullanicilar,
         name='kayitli_kullanicilar'),

   path('kullanici-kaydet', admin_views.kullanici_kaydet, name='kullanici_kaydet'),
   path('tablesSonuclananB.html', admin_views.sonuclanan_basvurular, name='tablesSonuclanan_basvurular'),
   path('admin/', admin.site.urls),
   path('', TemplateView.as_view(template_name='index.html'), name='home'),
    
    # Diğer tablolar (istersen bunları da benzer şekilde RESTful URL'lere çekebilirsin)
    path('tablesDevamB.html', admin_views.devam_eden_basvurular, name='tablesDevamB'),
    path('tablesYeniB.html', admin_views.yeni_basvurular,   name='tablesYeniB'),
    path('tablesBitenB.html', admin_views.biten_basvurular, name='tablesBitenB'),
    path('yeniKullanici.html', admin_views.yeni_kullanici,   name='yeniKullanici'),
    path('kayıtlıKullanicilar.html', admin_views.kayitli_kullanicilar, name='kayitli_kullanicilar'),
    path('tablesSonuclananB.html', admin_views.sonuclanan_basvurular, name='sonuclanan_basvurular'),
    path('basvurudetay/<int:ilan_id>/', admin_views.basvurudetay, name='basvurudetay'),
    path('detailapplication/<int:basvuru_id>/', admin_views.detail_application, name='detailapplication'),
    path('tables.html', admin_views.tables,   name='tables'),
    path('kullanici-kaydet', admin_views.kullanici_kaydet, name='kullanici_kaydet'),

    
    path('kayit/', views.kayit, name='kayit'),
    path('basvurudegerlendirme/', views.basvuru_degerlendirme, name='basvuru_degerlendirme'),
    # "Başvur" butonunun yönlendirdiği basvuruform.html sayfası

    path('basvuru/<int:pk>/', views.basvuru_form, name='basvuru_form'),
    # … diğer URL’ler …

    path('kisisel_bilgiler/', views.kisisel_bilgiler, name='kisisel_bilgiler'),

    # 1) /basvuru/ GET→form, POST→kayıt+PDF
    
    path('basvuru/create/<int:ilanID>/', views.basvuru_create, name='basvuru_create'),

     path('ilanlar/', views.ilanlar, name='ilanlar'),
    # 2) /basvuru/<pk>/ → kayıt sonrası modal ile detay gösterimi
    path(
        'basvuru/<int:pk>/',
        views.basvuru_form,
        name='basvuru_form'
    ),

   path(
      'ilan/<int:ilanID>/indir/',
      views.download_bilgilendirme,
      name='ilan-bilgilendirme'
    ),
    path('basvuru/<int:pk>/onayla/', views.basvuru_onayla, name='basvuru_onayla'),
    path('basvuru/<int:pk>/reddet/', views.basvuru_reddet, name='basvuru_reddet'),

    path(
        'basvuru/<int:pk>',       # URL örneği: /basvuru/5/indir/
        views.basvuru_pdf_indir,         # bu, basvuru_pdf_indir adında view’unuz olmalı
        name='basvuru_pdf_indir'
    ),

   
    path('giris/', views.giris, name='giris'),
    # 3) /basvuru/<pk>/pdf/ → PDF indirme
    path(
        'basvuru/<int:pk>/pdf/',
        views.basvuru_pdf_indir,
        name='basvuru_pdf'
    ),

    path('basvurudegerlendirme/', views.basvuru_degerlendirme, name='basvurudegerlendirme'),

    path('juri-degerlendirme/', views.juri_degerlendirme_kaydet, name='juri_degerlendirme_kaydet'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
