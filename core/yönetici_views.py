# core/views.py
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import JuriAdaylari, Ilan, JuriDegerlendirme,Basvurular
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from .models import JuriAdaylari, Ilan, JuriDegerlendirme, Basvurular
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from .models import Ilanı
from .models import Basvurular

from django.shortcuts import render



def yindex(request):
    return render(request, 'yindex.html')


def yeni_basvurular(request):
    if request.method == 'POST':
        bolum      = request.POST.get('bolum')
        pozisyon   = request.POST.get('pozisyon')
        aciklama   = request.POST.get('aciklama')
        basl_tarih = request.POST.get('basl_tarih')
        bitis_tarih= request.POST.get('bitis_tarih')
        kadro_sayi = request.POST.get('kadro_sayi')

        # Dosya yükleme (ilk dosyayı alıyoruz, istersen hepsini kaydederiz)
        uploaded_files = request.FILES.getlist('dosyalar')
        file_urls = []
        if uploaded_files:
            fs = FileSystemStorage()
            for dosya in uploaded_files:
                filename = fs.save(dosya.name, dosya)
                file_urls.append(fs.url(filename))

        # Veritabanına kaydet
        Ilan.objects.create(
            bolum=bolum,
            pozisyon=pozisyon,
            aciklama=aciklama,
            bilgilendirme_dosya=file_urls,
            basl_tarih=basl_tarih,
            bitis_tarih=bitis_tarih,
            kadro_sayi=kadro_sayi,
        )
        # Başarılıysa anasayfaya veya liste sayfasına yönlendir
        return redirect('home')

    # GET ise formu göster
    return render(request, 'ytablesYeniB.html')

def devam_eden_basvurular(request):
    """Bitiş tarihi bugün veya sonrasında olan ilanları listeler"""
    bugun   = timezone.localdate()
    ilanlar = Ilan.objects.filter(bitis_tarih__gte=bugun).order_by('-basl_tarih')
    return render(request, 'ytablesDevamB.html', {'ilanlar': ilanlar})

def biten_basvurular(request):
    """Bitiş tarihi bugün veya sonrasında olan ilanları listeler"""
    bugun   = timezone.localdate()
    ilanlar = Ilan.objects.filter(basl_tarih__gte=bugun).order_by('-bitis_tarih')
    return render(request, 'ytablesBitenB.html', {
        'ilanlar': ilanlar
    })

def ilan_duzenle(request, ilan_id):
    ilan = get_object_or_404(Ilan, pk=ilan_id)
    if request.method == 'POST':
        try:
            ilan.bolum       = request.POST.get('bolum')
            ilan.pozisyon    = request.POST.get('pozisyon')
            ilan.aciklama    = request.POST.get('aciklama')
            ilan.basl_tarih  = request.POST.get('basl_tarih')
            ilan.bitis_tarih = request.POST.get('bitis_tarih')
            ilan.kadro_sayi  = request.POST.get('kadro_sayi')
            # (PDF güncellemesini istersen ekleyebilirsin)
            ilan.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Yalnızca POST desteklenir.'}, status=405)


def ilan_sil(request, ilan_id):
    ilan = get_object_or_404(Ilan, pk=ilan_id)

    # 1) Ona bağlı başvuruların fk alanını NULL yap
    Basvurular.objects.filter(ilan_id=ilan.pk).update(ilan_id=None)

    # 2) İlanı sil
    ilan.delete()

    return redirect('tablesDevamB')

#def yeni_basvurular(request):
#    """Yeni başvurular sayfası (henüz doldurulmadıysa statik)"""
#    return render(request, 'tablesYeniB.html')


def yeni_juri(request):
    """Yeni başvurular sayfası (henüz doldurulmadıysa statik)"""
    return render(request, 'yyeniKullanici.html')

def tables(request):
    """Yeni başvurular sayfası (henüz doldurulmadıysa statik)"""
    return render(request, 'ytables.html')


def basvurudetay(request, ilan_id):
    """
    Bir ilana ait başvuruları gösterir.
    URL parametresi ilan_id üzerinden çalışır.
    """
    ilan       = get_object_or_404(Ilanı, pk=ilan_id)
    basvurular = Basvurular.objects.filter(ilan=ilan) \
                                   .select_related('kullanici') \
                                   .order_by('-basvuru_tarihi')
    return render(request, 'ybasvurudetay.html', {
        'ilan': ilan,
        'basvurular': basvurular
    })

def sonuclanan_basvurular(request):
    # Artık hiçbir tarih filtresi yok; tüm kayıtlar listelenecek
    basvurular = (
        Basvurular.objects
        .select_related('ilan', 'kullanici')
        .order_by('-basvuru_tarihi')
    )
    return render(request, 'ytablesSonuclananB.html', {
        'basvurular': basvurular
    })

def detail_application(request, basvuru_id):
    basvuru = get_object_or_404(
        Basvurular.objects.select_related('kullanici', 'ilan'),
        pk=basvuru_id
    )
    return render(request, 'ydetailapplication.html', {
        'basvuru': basvuru,
        'ilan':    basvuru.ilan,
        'kisi':    basvuru.kullanici,
    })

def kayitli_kullanicilar(request):
    if request.method == 'POST':
        # Checkbox’lar için
        juri_ids = request.POST.getlist('juri_ids')
        # İlana atanacak her satırın select’i için
        ilan_ids = request.POST.getlist('ilan_ids')

        # Debug: terminale bakalım
        print("POST juri_ids:", juri_ids, "ilan_ids:", ilan_ids)

        # Her seçili juri ⇄ ilan ikilisini kaydet
        for jid, iid in zip(juri_ids, ilan_ids):
            # JuriDegerlendirme tablosuna
            JuriDegerlendirme.objects.create(
                juriid_id=jid,
                basvuruid=None,
            )
            # JuriAdaylari tablosundaki ilanid alanını da güncelle
            JuriAdaylari.objects.filter(pk=jid).update(ilanid_id=iid)

        # POST işleminden sonra success=1 parametresiyle yönlendir
        success_url = reverse('kayitli_kullanicilar') + '?success=1'
        return redirect(success_url)

    # GET isteğinde listeyi gönder
    juri_adaylari = JuriAdaylari.objects.select_related('ilanid').all()
    ilanlar       = Ilan.objects.all()
    return render(request, 'kayıtlıKullanicilar.html', {
        'juri_adaylari': juri_adaylari,
        'ilanlar': ilanlar,
    })

from django.shortcuts import render, redirect
from .models import JuriAdaylari

def yeni_juri_olustur(request):
    if request.method == 'POST':
        # Form alanlarından verileri al
        isim      = request.POST.get('isim')
        soyisim   = request.POST.get('soyIsim')
        unvan     = request.POST.get('unvan')
        rol       = request.POST.get('rol')
        tc        = request.POST.get('kimlikNo')

        # Basit doğrulama (hepsi dolu mu?)
        if isim and soyisim and unvan and rol and tc:
            JuriAdaylari.objects.create(
                isim         = isim,
                soyisim      = soyisim,
                unvan        = unvan,
                kullanici_rolu = rol,
                tc           = tc
            )
            return redirect('kayitli_kullanicilar')
        else:
            error = "Lütfen tüm alanları doldurun."
            return render(request, 'yyeniKullanici.html', {'error': error})

    # GET geldiğinde formu göster
    return render(request, 'yyeniKullanici.html')
