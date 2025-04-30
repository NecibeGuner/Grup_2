# core/views.py

from django.shortcuts               import render, redirect, get_object_or_404
from django.contrib                 import messages
from django.template.loader         import render_to_string
from django.http                    import HttpResponse, Http404
from django.utils                   import timezone
from django.urls                    import reverse
from django.contrib.auth.decorators import login_required
from django.core.files.base         import ContentFile
import traceback
import pdfkit
from .models import Ilan
from .models import Ilan, KisiselBilgiler, Basvuru, Makale, Kullanici
import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import datetime


from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit
import traceback

def verify_tc_kimlik(tc_kimlik_no, ad, soyad, dogum_yili):
    soap_request = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <TCKimlikNoDogrula xmlns="http://tckimlik.nvi.gov.tr/WS">
          <TCKimlikNo>{tc_kimlik_no}</TCKimlikNo>
          <Ad>{ad.upper()}</Ad>
          <Soyad>{soyad.upper()}</Soyad>
          <DogumYili>{dogum_yili}</DogumYili>
        </TCKimlikNoDogrula>
      </soap:Body>
    </soap:Envelope>"""

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "http://tckimlik.nvi.gov.tr/WS/TCKimlikNoDogrula"
    }

    try:
        response = requests.post(
            "https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx",
            data=soap_request.encode('utf-8'),
            headers=headers,
            timeout=10
        )

        root = ET.fromstring(response.content)
        namespace = {'ns': 'http://tckimlik.nvi.gov.tr/WS'}
        result = root.find('.//ns:TCKimlikNoDogrulaResult', namespace)

        return result is not None and result.text.lower() == 'true'

    except Exception as e:
        print(f"[TC Doğrulama Hatası] {e}")
        return False

def kayit(request):
    if request.method == 'POST':
        tc_no     = request.POST.get('tcNo', '').strip()
        adsoyad   = request.POST.get('adSoyad', '').strip()
        dogum_tarihi_str = request.POST.get('dogumTarihi', '').strip()
        unvan     = request.POST.get('unvan', '').strip()
        sifre     = request.POST.get('password', '').strip()

        # Ad soyadı ayırma
        try:
            ad, soyad = adsoyad.split(' ', 1)
        except ValueError:
            messages.error(request, "Lütfen ad ve soyadı boşlukla ayırın.")
            return redirect('kayit')

        # e-Devlet doğrulama
        try:
            dogum_yili = datetime.strptime(dogum_tarihi_str, "%Y-%m-%d").year
        except ValueError:
            messages.error(request, "Geçerli bir doğum tarihi giriniz (YYYY-AA-GG).")
            return redirect('kayit')

        if not verify_tc_kimlik(tc_no, ad, soyad, dogum_yili):
            messages.error(request, "TC Kimlik bilgileri e-Devlet doğrulamasından geçemedi.")
            return redirect('kayit')

        # TC varsa tekrar kayıt olmasın
        if Kullanici.objects.filter(tc_kimlik_no=tc_no).exists():
            messages.error(request, "Bu TC ile zaten kayıt olunmuş.")
            return redirect('kayit')

        # Kullanıcı kaydı (rol sabit: aday)
        kullanici = Kullanici.objects.create(
            tc_kimlik_no = tc_no,
            ad_soyad     = adsoyad,
            sifre_hash   = sifre,
            rol          = 'aday',
            olusturma_tarihi = timezone.now()
        )

        # Kişisel bilgiler tablosuna kayıt
        try:
            dogum_tarihi = datetime.strptime(dogum_tarihi_str, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Doğum tarihi dönüşümünde hata oluştu.")
            return redirect('kayit')

        KisiselBilgiler.objects.create(
            kullanici_id = kullanici.id,
            ad_soyad = adsoyad,
            tc_kimlik_no = tc_no,
            dogum_tarihi = dogum_tarihi,
            akademik_unvan = unvan
        )

        messages.success(request, "Kayıt başarıyla tamamlandı.")
        return redirect('giris')


    return render(request, 'kayıt.html')

def basvuru_degerlendirme(request):
    basvurular = Basvuru.objects.filter(durum='Beklemede').select_related('kullanici')
    
    enriched = []
    for basvuru in basvurular:
        unvan = None
        try:
            kisi_bilgi = KisiselBilgiler.objects.get(kullanici=basvuru.kullanici)
            unvan = kisi_bilgi.akademik_unvan
        except KisiselBilgiler.DoesNotExist:
            pass
        enriched.append({
            "basvuru": basvuru,
            "unvan": unvan
        })
    
    return render(request, 'basvurudegerlendirme.html', {"basvurular": enriched})
def basvuru_create(request, ilanID):
    """
    GET  → boş formu göster (show_modal=False)
    POST → Session’dan Kullanici’yı al, Basvuru kaydı oluştur,
           PDF şablonuna form verilerini bas, PDF’i kaydet,
           ardından basvuru_form view’ına yönlendir.
    """

    # 🔥 İlanı her iki durumda da çekiyoruz (hem GET, hem POST için lazım!)
    ilan = get_object_or_404(Ilan, pk=ilanID)

    if request.method == 'POST':
        # 1️⃣ Session’dan Kullanıcıyı çek
        kullanici_id = request.session.get('kullanici_id')
        if not kullanici_id:
            return redirect('giris')
        kullanici = get_object_or_404(Kullanici, pk=kullanici_id)

        # 2️⃣ Basvuru kaydını oluştur (İlanı artık burada verebiliyoruz)
        basvuru = Basvuru.objects.create(
            kullanici        = kullanici,
            basvurulan_kadro = '',  # (Eğer boşsa, gerekirse burada düzenlersin)
            basvuru_tarihi   = timezone.now().date(),
            ilan             = ilan,
        )

        # 3️⃣ Formdan gelen liste verilerini hazırla
        makaleler       = build_list(request, 'makale_turu[]',        'yazarlar_dergi_bilgi[]',      MAKALE_META)
        toplantilar     = build_list(request, 'toplanti_turu[]',      'toplanti_detay[]',            TOPLANTI_META)
        kitaplar        = build_list(request, 'kitap_turu[]',         'kitap_detaylari[]',           KITAP_META)
        atiflar         = build_list(request, 'atif_turu[]',          'atif_detay[]',                ATIF_META)
        egitimler       = build_list(request, 'egitim_turu[]',        'egitim_detay[]',              EGITIM_META)
        tezler          = build_list(request, 'tez_turu[]',           'tez_detay[]',                 TEZ_META)
        patentler       = build_list(request, 'patent_turu[]',        'patent_detay[]',              PATENT_META)
        projeler        = build_list(request, 'proje_turu[]',         'proje_detay[]',               PROJE_META)
        editorluklar    = build_list(request, 'editorluk[][tur]',     'editorluk[][gorev_suresi]',   EDITORLUK_META)
        oduller         = build_list(request, 'odul_turu[]',          'odul_kurul[]',                ODUL_META)
        idari_gorevler  = build_list(request, 'idari_gorev_turu[]',   'idari_gorev_detay[]',         IDARI_META)
        guzel_sanatlar  = build_list(request, 'guzelSanatlar[][tur]', 'guzelSanatlar[][detay]',      GUZEL_SANAT_META)

        # 4️⃣ PDF için context’i oluştur
        post = request.POST
        context = {
            'isim':            post.get('adSoyad', ''),
            'tarih':           post.get('tarih', ''),
            'kurum':           post.get('kurum', ''),
            'kadro':           post.get('kadro', ''),
            'imza':            post.get('imza', ''),
            'profesor':        post.get('profesor')   == 'on',
            'docent':          post.get('docent')     == 'on',
            'drOgrUyesi':      post.get('drOgrUyesi') == 'on',
            'makaleler':       makaleler,
            'toplantilar':     toplantilar,
            'kitaplar':        kitaplar,
            'atiflar':         atiflar,
            'egitimler':       egitimler,
            'tezler':          tezler,
            'patentler':       patentler,
            'projeler':        projeler,
            'editorluklar':    editorluklar,
            'oduller':         oduller,
            'idari_gorevler':  idari_gorevler,
            'guzel_sanatlar':  guzel_sanatlar,
        }

        # 5️⃣ PDF oluştur
        html_string = render_to_string('pdf_template.html', context)
        config = pdfkit.configuration(
            wkhtmltopdf=r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
        )
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': 'UTF-8',
            'enable-local-file-access': None,
        }

        try:
            pdf_bytes = pdfkit.from_string(
                html_string,
                False,
                configuration=config,
                options=options
            )
        except Exception:
            tb = traceback.format_exc()
            return HttpResponse(
                '<h1>PDF Oluşturma Hatası</h1><pre>%s</pre>' % tb,
                content_type='text/html'
            )

        # 6️⃣ PDF’i Basvuru kaydına kaydet
        basvuru.basvuru_pdf = pdf_bytes
        basvuru.save(update_fields=['basvuru_pdf'])

        # 7️⃣ Başarılı kayıt sonrası modal açmak için yönlendir
        return redirect('basvuru_form', pk=basvuru.pk)

    # — GET İsteği geldiğinde boş formu göster
    return render(request, 'basvuruform.html', {
        'show_modal': False,
        'ilan': ilan,  # formda ilan bilgisine de ihtiyacın olursa diye gönderdim
    })

def basvuru_onayla(request, pk):
    basvuru = get_object_or_404(Basvuru, pk=pk)
    basvuru.durum = "Onaylandı"
    basvuru.save(update_fields=["durum"])
    return redirect('basvuru_degerlendirme')


def basvuru_reddet(request, pk):
    basvuru = get_object_or_404(Basvuru, pk=pk)
    basvuru.durum = "Reddedildi"
    basvuru.save(update_fields=["durum"])
    return redirect('basvuru_degerlendirme')

    # 🔥 İlanı her iki durumda da çekiyoruz (hem GET, hem POST için lazım!)
    ilan = get_object_or_404(Ilan, pk=ilanID)

    if request.method == 'POST':
        # 1️⃣ Session’dan Kullanıcıyı çek
        kullanici_id = request.session.get('kullanici_id')
        if not kullanici_id:
            return redirect('giris')
        kullanici = get_object_or_404(Kullanici, pk=kullanici_id)

        # 2️⃣ Basvuru kaydını oluştur (İlanı artık burada verebiliyoruz)
        basvuru = Basvuru.objects.create(
            kullanici        = kullanici,
            basvurulan_kadro = '',  # (Eğer boşsa, gerekirse burada düzenlersin)
            basvuru_tarihi   = timezone.now().date(),
            ilan             = ilan,
        )

        # 3️⃣ Formdan gelen liste verilerini hazırla
        makaleler       = build_list(request, 'makale_turu[]',        'yazarlar_dergi_bilgi[]',      MAKALE_META)
        toplantilar     = build_list(request, 'toplanti_turu[]',      'toplanti_detay[]',            TOPLANTI_META)
        kitaplar        = build_list(request, 'kitap_turu[]',         'kitap_detaylari[]',           KITAP_META)
        atiflar         = build_list(request, 'atif_turu[]',          'atif_detay[]',                ATIF_META)
        egitimler       = build_list(request, 'egitim_turu[]',        'egitim_detay[]',              EGITIM_META)
        tezler          = build_list(request, 'tez_turu[]',           'tez_detay[]',                 TEZ_META)
        patentler       = build_list(request, 'patent_turu[]',        'patent_detay[]',              PATENT_META)
        projeler        = build_list(request, 'proje_turu[]',         'proje_detay[]',               PROJE_META)
        editorluklar    = build_list(request, 'editorluk[][tur]',     'editorluk[][gorev_suresi]',   EDITORLUK_META)
        oduller         = build_list(request, 'odul_turu[]',          'odul_kurul[]',                ODUL_META)
        idari_gorevler  = build_list(request, 'idari_gorev_turu[]',   'idari_gorev_detay[]',         IDARI_META)
        guzel_sanatlar  = build_list(request, 'guzelSanatlar[][tur]', 'guzelSanatlar[][detay]',      GUZEL_SANAT_META)

        # 4️⃣ PDF için context’i oluştur
        post = request.POST
        context = {
            'isim':            post.get('adSoyad', ''),
            'tarih':           post.get('tarih', ''),
            'kurum':           post.get('kurum', ''),
            'kadro':           post.get('kadro', ''),
            'imza':            post.get('imza', ''),
            'profesor':        post.get('profesor')   == 'on',
            'docent':          post.get('docent')     == 'on',
            'drOgrUyesi':      post.get('drOgrUyesi') == 'on',
            'makaleler':       makaleler,
            'toplantilar':     toplantilar,
            'kitaplar':        kitaplar,
            'atiflar':         atiflar,
            'egitimler':       egitimler,
            'tezler':          tezler,
            'patentler':       patentler,
            'projeler':        projeler,
            'editorluklar':    editorluklar,
            'oduller':         oduller,
            'idari_gorevler':  idari_gorevler,
            'guzel_sanatlar':  guzel_sanatlar,
        }

        # 5️⃣ PDF oluştur
        html_string = render_to_string('pdf_template.html', context)
        config = pdfkit.configuration(
            wkhtmltopdf=r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
        )
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': 'UTF-8',
            'enable-local-file-access': None,
        }

        try:
            pdf_bytes = pdfkit.from_string(
                html_string,
                False,
                configuration=config,
                options=options
            )
        except Exception:
            tb = traceback.format_exc()
            return HttpResponse(
                '<h1>PDF Oluşturma Hatası</h1><pre>%s</pre>' % tb,
                content_type='text/html'
            )

        # 6️⃣ PDF’i Basvuru kaydına kaydet
        basvuru.basvuru_pdf = pdf_bytes
        basvuru.save(update_fields=['basvuru_pdf'])

        # 7️⃣ Başarılı kayıt sonrası modal açmak için yönlendir
        return redirect('basvuru_form', pk=basvuru.pk)

    # — GET İsteği geldiğinde boş formu göster
    return render(request, 'basvuruform.html', {
        'show_modal': False,
        'ilan': ilan,  # formda ilan bilgisine de ihtiyacın olursa diye gönderdim
    })

def basvuru_form(request, pk):
    basvuru = get_object_or_404(Basvuru, pk=pk)
    ilan = basvuru.ilan  # başvurulan ilanı getir
    return render(request, 'basvuruform.html', {
        'show_modal': True,   # kayıt sonrası modal’ı aç
        'success':    True,
        'basvuru':    basvuru,
         'ilan': ilan,
    })



@login_required
def basvurudegerlendirme(request):
    basvurular = Basvuru.objects.select_related(
        'kullanici',
        'kisisel_bilgi'
    ).all()
    return render(request, 'basvurudegerlendirme.html', {
        'basvurular': basvurular
    })



def basvuru_pdf_indir(request, pk):
    basvuru = get_object_or_404(Basvuru, pk=pk)
    if not basvuru.basvuru_pdf:
        raise Http404
    response = HttpResponse(basvuru.basvuru_pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="basvuru_{pk}.pdf"'
    return response


def detail_application(request):
    # Eğer dinamik içerik gösterecekseniz:
    # basvuru = get_object_or_404(Basvuru, pk=basvuru_id)
    # return render(request, 'detailApplication.html', {'basvuru': basvuru})
    return render(request, 'detailApplication.html')

from .models import Ilan  # Ilan modelini import edin

@login_required
def download_bilgilendirme(request, ilanID):
    ilan = get_object_or_404(Ilan, pk=ilanID)

    if not ilan.bilgilendirme_dosya:
        raise Http404("Bu ilana ait PDF bulunamadı.")

    response = HttpResponse(ilan.bilgilendirme_dosya, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=ilan_{ilan.pk}_bilgilendirme.pdf'
    response['Content-Length'] = len(ilan.bilgilendirme_dosya)

    return response

def giris(request):
    if request.method == 'POST':
        tc_kimlik = request.POST.get('tcNo', '').strip()
        raw_pw = request.POST.get('password', '').strip()

        try:
            user = Kullanici.objects.get(tc_kimlik_no=tc_kimlik)
        except Kullanici.DoesNotExist:
            messages.error(request, "TC Kimlik No veya şifre hatalı.")
            return render(request, 'giris.html')

        if raw_pw == user.sifre_hash:
            request.session['kullanici_id'] = user.id  # Kullanıcıyı oturuma kaydet
            user.son_giris = timezone.now()
            user.save(update_fields=['son_giris'])

            # Rol bazlı yönlendirme
            if user.rol == 'aday':
                return redirect('ilanlar')
            elif user.rol == 'juri':
                return redirect('basvurudegerlendirme')  # <--- Burada istenen sayfa
            else:
                return redirect('anasayfa')  # admin, komisyon vs.

        messages.error(request, "TC Kimlik No veya şifre hatalı.")

    return render(request, 'giris.html')

def juri_degerlendirme_kaydet(request,JuriDegerlendirme):
    if request.method == 'POST':
        # 1️⃣ Oturumdaki kullanıcıyı al
        kullanici_id = request.session.get('kullanici_id')
        kullanici = get_object_or_404(Kullanici, id=kullanici_id)

        # 2️⃣ Başvuru ID’sini al
        basvuru_id = request.POST.get('basvuru_id')
        basvuru = get_object_or_404(Basvuru, id=basvuru_id)

        # 3️⃣ Onay durumu
        onay_durumu = request.POST.get('onay_durumu', 'beklemede')

        # 4️⃣ PDF dosyasını al
        juri_pdf = request.FILES.get('juryReport')

        # 5️⃣ Veritabanına kaydet
        JuriDegerlendirme.objects.create(
            kullanici=kullanici,
            basvuruid=basvuru,
            juri_raporu=juri_pdf,
            onay_durumu=onay_durumu
        )

        # 6️⃣ Başvuru tablosunu da güncelle
        basvuru.durum = 'Onaylandı' if onay_durumu == 'onaylandi' else 'Reddedildi'
        basvuru.save(update_fields=['durum'])

        return redirect('basvurudegerlendirme')

def kisisel_bilgiler(request):
    kullanici_id = request.session.get('kullanici_id')

    if not kullanici_id:
        return redirect('giris')

    try:
        kullanici_id = int(kullanici_id)
    except (ValueError, TypeError):
        return redirect('giris')

    kullanici = get_object_or_404(Kullanici, pk=kullanici_id)
    profil = get_object_or_404(KisiselBilgiler, kullanici_id=kullanici_id)

    return render(request, 'kisisel_bilgiler.html', {'profil': profil})



# 1) Her bölümün "kod → tam metin" eşlemesi
MAKALELER    = {
    "Q1": "1) SCI-E, SSCI veya AHCI kapsamındaki dergilerde yayımlanmış makale (Q1)",
    "Q2": "2) … yayımlanmış makale (Q2)",
    "Q3": "3) … yayımlanmış makale (Q3)",
    "Q4": "4) … yayımlanmış makale (Q4)",
    "ESCI": "5) ESCI taranan dergilerde yayımlanmış makale",
    "ULAKBIM_TR": "6) ULAKBİM TR Dizin taranmış dergilerde yayımlanmış makale",
    "ULUSAL": "7) Ulusal hakemli dergilerde yayımlanmış makale",
    "ULAKBIM_TR_ULUSAL": "8) ULAKBİM TR Dizin tarafından taranan ulusal hakemli dergilerde yayımlanmış makale",
    "ULUSAL_8_DISI": "9) 8. madde dışındaki ulusal hakemli dergilerde yayımlanmış makale",
}

TOPLANTILAR = {
    "B1":"1) Uluslararası bilimsel toplantılarda sözlü olarak sunulan, tam metni matbu veya elektronik olarak bildiri kitapçığında yayımlanmış çalışmalar",
    "B2":"2) Uluslararası bilimsel toplantılarda sözlü olarak sunulan, özet metni matbu veya elektronik olarak bildiri kitapçığında yayımlanmış çalışmalar",
    "B3":"3) Uluslararası bilimsel toplantılarda poster olarak sunulan çalışmalar",
    "B4":"4) Ulusal bilimsel toplantılarda sözlü olarak sunulan tam metni matbu veya elektronik olarak bildiri kitapçığında yayımlanmış çalışmalar",
    "B5":"5) Ulusal bilimsel toplantılarda sözlü olarak sunulan, özet metni matbu veya elektronik olarak bildiri kitapçığında yayımlanmış çalışmalar",
    "B6":"6) Ulusal bilimsel toplantılarda poster olarak sunulan çalışmalar",
    "B7":"7) Uluslararası bir kongre, konferans veya sempozyumda organizasyon veya yürütme komitesinde düzenleme kurulu üyeliği veya bilim kurulu üyeliği yapmak",
    "B8":"8) Ulusal bir kongre, konferans veya sempozyumda organizasyon veya yürütme komitesinde düzenleme kurulu üyeliği veya bilim kurulu üyeliği yapmak",
    "B9":"9) Uluslararası konferanslarda, bilimsel toplantı, seminerlerde davetli konuşmacı olarak yer almak",
    "B10":"10) Ulusal konferanslarda, bilimsel toplantı, seminerlerde davetli konuşmacı olarak yer almak",
    "B11":"11) Uluslararası veya ulusal çeşitli kurumlarla işbirliği içinde atölye, çalıştay, yaz okulu organize ederek gerçekleştirmek",
    "B12":"12) Uluslararası veya ulusal çeşitli kurumlarla işbirliği içinde atölye, çalıştay, panel, seminer, yaz okulunda konuşmacı veya panelist olarak görev almak"
    # B4…B12 aynı mantıkla
}

KITAPLAR    = {
    "C1": "1) Uluslararası yayınevleri tarafından yayımlanmış özgün kitap" ,
    "C2": "2) Uluslararası yayınevleri tarafından yayımlanmış özgün kitap editörlüğü, bölüm yazarlığı (Her bir kitap için maksimum 2 bölüm yazarlığı)",
    "C3": "3) Uluslararası yayımlanan ansiklopedi konusu/maddesi (en fazla 3 madde)" ,
    "C4": "4) Ulusal yayınevleri tarafından yayımlanmış özgün kitap" ,
    "C5": "5) Ulusal yayınevleri tarafından yayımlanmış özgün kitap editörlüğü, bölüm yazarlığı (Her bir kitap için maksimum 2 bölüm yazarlığı)",
    "C6": "6) Tam kitap çevirisi (Yayınevleri için ilgili ÜAK kriterleri geçerlidir)" ,
    "C7": "7) Çeviri kitap editörlüğü, kitap bölümü çevirisi (Her bir kitap için maksimum 2 bölüm çevirisi)" ,
    "C8": "8) Alanında ulusal yayımlanan ansiklopedi konusu/maddesi (en fazla 3 madde)" 
  
}

ATIFLAR     = {
    "D1": "1) SCI-E, SSCI ve AHCI tarafından taranan dergilerde; Uluslararası yayınevleri tarafından yayımlanmış ... her eseri için" ,
    "D2": "2) E-SCI tarafından taranan dergilerde ve adayın yazar olarak yer almadığı yayınlardan her birinde..." ,
    "D3": "3) SCI-E, SSCI, AHCI, E-SCI dışındaki uluslararası indeksli dergilerde; Uluslararası yayınevlerinde bölümler için" ,
    "D4": "4) Ulusal hakemli dergilerde; Ulusal yayınevlerinde yayımlanmış kitaplarda..." ,
    "D5": "5) Güzel sanat eserlerinin uluslararası kaynaklarda yayımlanması veya gösterilmesi" ,
    "D6": "6) Güzel sanat eserlerinin ulusal kaynaklarda yayımlanması veya gösterilmesi" 
}

EGITIMLER   = {
    "E1": "1) Ön lisans / lisans dersleri",
    "E2": "2) Önlisans/lisans dersleri (Yabancı dilde)",
    "E3": "3) Lisansüstü dersleri",
    "E4": "4) Lisansüstü dersleri (Yabancı dilde)",
}

TEZLER      = {
"F1": "1) Doktora/Sanatta Yeterlik veya Tıp/Diş Hekimliğinde Uzmanlık tez yönetimi" ,
"F2": "2) Yüksek Lisans Tez Yönetimi" ,
"F3": "3) Doktora/Sanatta Yeterlik (Eş Danışman)" ,
"F4": "4) Yüksek Lisans/Sanatta Yeterlik Tez Yönetimi (Eş Danışman)" ,
}

PATENTLER   = {
     "G1": "1) Lisanslanan Uluslararası Patent" ,
     "G2": "2) Tescillenmiş Uluslararası Patent" ,
     "G3": "3) Uluslararası Patent Başvurusu" ,
     "G4": "4) Lisanslanan Ulusal Patent" ,
     "G5": "5) Tescillenmiş Ulusal Patent" ,
     "G6": "6) Ulusal Patent Başvurusu" ,
     "G7": "7) Lisanslanan Faydalı Model, Endüstriyel Tasarım, Marka" ,
     "G8": "8) Faydalı Model ve Endüstriyel Tasarım" ,
}

PROJELER    = {
    "H1":  "AB çerçeve programı/NSF/ERC bilimsel araştırma projesinde koordinatör/alt koordinatör olmak",
    "H2":  "AB çerçeve programı/NSF/ERC bilimsel araştırma projesinde yürütücü olmak",
    "H3":  "AB çerçeve programı/NSF/ERC bilimsel araştırma projesinde araştırmacı olmak",
    "H4":  "AB çerçeve dışı uluslararası projelerde koordinatör/alt koordinatör olmak",
    "H5":  "AB çerçeve dışı uluslararası projelerde yürütücü olmak",
    "H6":  "AB çerçeve dışı uluslararası projelerde araştırmacı olmak",
    "H7":  "AB çerçeve dışı uluslararası projelerde danışman olmak",
    "H8":  "TÜBİTAK ARGE/TÜSEB projelerinde yürütücü olmak",
    "H9":  "Diğer TÜBİTAK projelerinde yürütücü olmak",
    "H10": "TÜBİTAK dışındaki kamu kurumlarında yürütücü olmak",
    "H11": "Sanayi kuruluşları ile yapılan Ar-Ge projelerinde yürütücü olmak",
    "H12": "Diğer özel kuruluşlar ile yapılan Ar-Ge projelerinde yürütücü olmak",
    "H13": "TÜBİTAK ARGE (ARDEB, TEYDEB) ve TÜSEB projelerinde araştırmacı olmak",
    "H14": "Diğer TÜBİTAK projelerinde araştırmacı olmak",
    "H15": "TÜBİTAK dışındaki kamu kurumlarıyla yapılan projelerde araştırmacı olmak",
    "H16": "Sanayi kuruluşları ile yapılan projelerde araştırmacı olmak",
    "H17": "Diğer özel kuruluşlarla yapılan projelerde araştırmacı olmak",
    "H18": "TÜBİTAK ARGE ve TÜSEB projelerinde danışman olmak",
    "H19": "Diğer TÜBİTAK projelerinde danışman olmak",
    "H20": "TÜBİTAK dışı kamu kurumları projelerinde danışman olmak",
    "H21": "Sanayi kuruluşlarıyla yapılan projelerde danışman olmak",
    "H22": "Özel kuruluşlarla yapılan projelerde danışman olmak",
    "H23": "BAP projelerinde yürütücü olmak",
    "H24": "BAP projelerinde araştırmacı olmak",
    "H25": "BAP projelerinde danışman olmak",
    "H26": "En az dört aylık yurtdışı araştırma çalışmasında bulunmak",
    "H27": "En az dört aylık yurtiçi araştırma çalışmasında bulunmak",
    "H28": "TÜBİTAK 2209-A, 2209-B, 2242 projelerinde danışman olmak",
}

EDITORLUK   = {
    "E1":  "SCI-E, SSCI, AHCI veya E-SCI kapsamındaki dergilerde baş editörlük görevinde bulunmak",
    "E2":  "… yardımcı/ortak editörlük görevinde bulunmak",
    "E3":  "… asistan editörlük görevinde bulunmak",
    "E4":  "… yayın kurulu üyeliği",
    "E5":  "SCI-E dışı indeksli dergilerde baş editörlük görevinde bulunmak",
    "E6":  "… yardımcı/ortak editörlük görevinde bulunmak",
    "E7":  "… asistan editörlük görevinde bulunmak",
    "E8":  "… yayın kurulu üyeliği",
    "E9":  "ULAKBİM taramalı dergilerde baş editörlük görevi",
    "E10": "ULAKBİM taramalı dergilerde yayın kurulu üyeliği",
    "E11": "SCI-E, SSCI veya AHCI dergilerde hakemlik (her bir faaliyette)",
    "E12": "Uluslararası indeksli diğer dergilerde hakemlik (her bir faaliyette)",
    "E13": "ULAKBİM taramalı dergilerde hakemlik (her bir faaliyette)",
}

ODULLER     = {
    "D1":  "Sürekli ve periyodik uluslararası bilim & sanat ödülleri",
    "D2": "TÜBİTAK Bilim, Özel ve Hizmet Ödülleri",
    "D3":  "TÜBA Akademi Ödülleri",
    "D4":  "TÜBİTAK Teşvik Ödülü",
    "D5":  "TÜBA GEBİP & TESEP ödülleri",
    "D6":  "Sürekli ve periyodik ulusal bilim & sanat ödülleri",
    "D7":  "Jürisiz ulusal/uluslararası ödüller",
    "D8":  "Uluslararası hakemli yarışmalarda birincilik",
    "D9":  "… ikincilik",
    "D10": "… üçüncülük",
    "D11": "Ulusal hakemli yarışmalarda birincilik",
    "D12": "… ikincilik",
    "D13": "… üçüncülük",
}

IDARI_GOREV = {
    "K1":  "Dekan/Enstitü/Yüksekokul/MYO/Merkez Müdürü",
    "K2":  "Enstitü Müdür Yrd. / Dekan Yrd. / ...",
    "K3":  "Bölüm Başkan Yrd. / Anabilim Dalı Başkanı",
    "K4":  "Rektörlükçe görevlendirilen Koordinatörlük",
    "K5":  "Rektörlükçe görevlendirilen Koordinatör Yardımcıları",
    "K6":  "Rektörlükçe görevlendirilen üniversite düzeyinde Komisyon/Kurul üyelikleri",
    "K7":  "Dekanlık/Y.O. Müdürlüğü/... görevlendirilen Komisyon/Kurul üyelikleri",
    "K8":  "Bölüm Başkanlıkları tarafından görevlendirilen Komisyon/Kurul üyelikleri",
    "K9":  "Rektörlük/Dekanlık/... eğitim, işbirliği vb. konularda katkı sağlamak",
    "K10": "Uluslararası nitelikteki bilimsel ve mesleki kurum/kuruluşlarda görev almak",
    "K11": "Ulusal nitelikteki bilimsel ve mesleki kurum/kuruluşlarda görev almak",
    "K12": "Yerel nitelikteki bilimsel ve mesleki kurum/kuruluşlarda görev almak",
}

GUZEL_SANAT = {
    "L1":  "Özgün sanat eserlerinin, tasarım veya yorum çalışmalarının yurt dışında sanat, eğitim ve kültür kurumlarınca satın alınması veya bu eser(ler) için telif ödenmesi (Kurumlar bazında puanlama yapılır)",
    "L2":  "Özgün sanat eserlerinin, tasarım veya yorum çalışmalarının yurt içinde sanat, eğitim ve kültür kurumlarınca satın alınması veya bu eser(ler) için telif ödenmesi (Kurumlar bazında puanlama yapılır)",
    "L3":  "Yerel Yönetimler veya Özel Kuruluşların desteklediği kamusal alanda kalıcı olarak gerçekleştirilen sanat projeleri (Heykel, Duvar Resmi / Graffiti, Enstalasyon vb.) (Kurumlar bazında puanlama yapılır)",
    "L4":  "Galerilerde, müzelerde, sanat ve kültür merkezlerinde gerçekleştirilen Küratörlük etkinlikleri (En fazla iki kez puanlanır)",
    "L5":  "Özgün sanat eserleri, tasarımlar ya da yorum/icra çalışmalarıyla yurtdışında uluslararası jürili kişisel etkinlikte (sergi, bienal, sempozyum, trienal, gösteri, kareografi, performans, resital, dinleti, konser, kompozisyon, orkestra şefliği, festival, gösterim) bizzat katılım sağlayarak bulunmak.",
    "L6":  "Özgün sanat eserleri, tasarımlar ya da yorum/icra çalışmalarıyla yurtiçinde jürili kişisel etkinlikte (sergi, bienal, sempozyum, trienal, gösteri, kareografi, performans, resital, dinleti, konser, kompozisyon, orkestra şefliği, festival, gösterim) bizzat katılım sağlayarak bulunmak.",
    "L7":  "Özgün sanat eserleri, tasarımlar ya da yorum/icra çalışmalarıyla yurtdışında uluslararası jürili karma-ortak etkinlikte (sergi, bienal, sempozyum, trienal, gösteri, kareografi, performans, resital, dinleti, konser, kompozisyon, orkestra şefliği, festival, gösterim) bizzat katılım sağlayarak bulunmak.",
    "L8":  "Özgün sanat eserleri, tasarımlar ya da yorum/icra çalışmalarıyla yurtiçinde ulusal jürili karma-ortak etkinlikte (sergi, bienal, sempozyum, trienal, gösteri, kareografi, performans, resital, dinleti, konser, kompozisyon, orkestra şefliği, festival, gösterim) bizzat katılım sağlayarak bulunmak.",
    "L9":  "Uluslararası çalıştay/workshop (atölye çalışması)/uygulamalı sempozyum/yarışma/festival/şenlikte yöneticilik veya yürütücülük",
    "L10": "Ulusal çalıştay/workshop (atölye çalışması)/uygulamalı sempozyum/yarışma/festival/şenlikte yöneticilik veya yürütücülük",
    "L11": "Uluslararası çalıştay/workshop (atölye çalışması)/uygulamalı sempozyum/yarışma/festival/şenlikte araştırmacılık/kurul üyeliği",
    "L12": "Ulusal çalıştay/workshop (atölye çalışması)/uygulamalı sempozyum/yarışma/festival/şenlikte araştırmacılık/kurul üyeliği",
    "L13": "Uluslararası yarışmalarda/festivallerde/şenliklerde jüri üyeliği",
    "L14": "Ulusal yarışmalarda/festivallerde/şenliklerde jüri üyeliği",
    "L15": "Üretilen eserlerin uluslararası haber veya yayın organlarında yer alması veya gösterime ya da dinletime girmesi (her bir etkinlik için ayrı puanlanır ve her bir etkinlik için 5 haber ile sınırlıdır)",
    "L16": "Üretilen eserlerin ulusal haber veya yayın organlarında yer alması veya gösterime ya da dinletime girmesi (her bir etkinlik için ayrı puanlanır ve her bir etkinlik için 5 haber ile sınırlıdır)",
    "L17": "Uluslararası resital icra etmek",
    "L18": "Uluslararası Konserlerde, Orkestra, Koro, Geleneksel Topluluklar konserinde solist icracı olarak yer almak",
    "L19": "Uluslararası Konserlerde, Orkestra, Koro, Geleneksel Topluluklar konserinde karma icracı olarak yer almak",
    "L20": "Uluslararası Konserlerde, Orkestra Şefliği, Müzik Topluluğu Şefliği ve Koro Şefliği",
    "L21": "Ulusal Konserlerde, Oda Müziği Konserinde icracı olarak yer almak",
    "L22": "Ulusal Konserlerde, Orkestra Konserinde Grup Şefi olarak yer almak",
    "L23": "Ulusal Konserlerde, Orkestra Konserinde Grup Üyesi olarak yer almak",
    "L24": "Ulusal Konserlerde, Resital veya koro konserinde eşlikçi olarak yer almak",
    "L25": "Ulusal Konserlerde, Konser yönetmenliği / dinleti koordinatörlüğü",
    "L26": "Ulusal resital icra etmek",
    "L27": "Ulusal Konserlerde, Orkestra veya koro konserinde icracı olarak bireysel dinletide bulunmak",
    "L28": "Ulusal Konserlerde, Orkestra veya koro konserinde icracı olarak karma dinletide bulunmak",
    "L29": "Ulusal Konserlerde, Orkestra Şefliği, Müzik Topluluğu Şefliği ve Koro Şefliği",
    "L30": "Ulusal Konserlerde, Oda Müziği Konserinde icracı olarak yer almak",
    "L31": "Ulusal Konserlerde, Orkestra Konserinde Grup Şefi olarak yer almak",
    "L32": "Ulusal Konserlerde, Orkestra Konserinde Grup Üyesi olarak yer almak",
    "L33": "Ulusal Konserlerde, Resital veya koro konserinde eşlikçi olarak yer almak",
    "L34": "Ulusal Konserlerde, Konser yönetmenliği / dinleti koordinatörlüğü",
    "L35": "Uluslararası sesli ve görsel etkinlikler ve sesli yayınlar, icracı, besteci, orkestra şefi, müzik topluluğu şefi veya koro şefi olarak bireysel ses yayını",
    "L36": "Uluslararası sesli ve görsel etkinlikler ve sesli yayınlar, icracı, besteci, orkestra şefi, müzik topluluğu şefi veya koro şefi olarak karma ses yayını",
    "L37": "Uluslararası sesli ve görsel etkinlikler ve sesli yayınlar, Genel Sanat Yönetmeni/Müzik yönetmeni olarak ses yayını hazırlamak",
    "L38": "Uluslararası sesli ve görsel etkinlikler ve sesli yayınlar, Radyo ve TV Etkinliği - Program Hazırlamak",
    "L39": "Uluslararası sesli ve görsel etkinlikler ve sesli yayınlar, Radyo ve TV Etkinliği Katılımcılığı - Bireysel",
    "L40": "Uluslararası sesli ve görsel etkinlikler ve sesli yayınlar, Radyo ve TV Etkinliği Katılımcılığı - Karma",
    "L41": "Ulusal sesli ve görsel etkinlikler ve sesli yayınlar, İcracı, besteci, orkestra şefi, müzik topluluğu şefi veya koro şefi olarak bireysel ses yayını",
    "L42": "Ulusal sesli ve görsel etkinlikler ve sesli yayınlar, İcracı, besteci, orkestra şefi, müzik topluluğu şefi veya koro şefi olarak karma ses yayını",
    "L43": "Ulusal sesli ve görsel etkinlikler ve sesli yayınlar, Genel Sanat Yönetmeni/Müzik yönetmeni olarak ses yayını hazırlamak",
    "L44": "Ulusal sesli ve görsel etkinlikler ve sesli yayınlar, Radyo ve TV Etkinliği - Program Hazırlamak",
    "L45": "Ulusal sesli ve görsel etkinlikler ve sesli yayınlar, Radyo ve TV Etkinliği Katılımcılığı - Bireysel",
    "L46": "Ulusal sesli ve görsel etkinlikler ve sesli yayınlar, Radyo ve TV Etkinliği Katılımcılığı - Karma",
    "L47": "Ulusal Orkestra İçin Bestelenmiş Eser (4’lü, 3’lü, 2’li, Oda ve Yaylı Çalgılar Orkestrası) 0 – 5 dakikalık eser sahibi olmak",
    "L48": "Ulusal Orkestra İçin Bestelenmiş Eser (4’lü, 3’lü, 2’li, Oda ve Yaylı Çalgılar Orkestrası) 5 – 10 dakikalık eser sahibi olmak",
    "L49": "Ulusal Orkestra İçin Bestelenmiş Eser (4’lü, 3’lü, 2’li, Oda ve Yaylı Çalgılar Orkestrası) 10 – 15 dakikalık eser sahibi olmak",
    "L50": "Ulusal Orkestra İçin Bestelenmiş Eser (4’lü, 3’lü, 2’li, Oda ve Yaylı Çalgılar Orkestrası) 15 ve üzeri dakikalık eser sahibi olmak",
    "L51": "Ulusal Oda Müziği (Karma Oda Müziği, Vokal Müzik, Solo Çalgı Müzikleri) 0 – 5 dakikalık eser sahibi olmak",
    "L52": "Ulusal Oda Müziği (Karma Oda Müziği, Vokal Müzik, Solo Çalgı Müzikleri) 5 – 10 dakikalık eser sahibi olmak",
    "L53": "Ulusal Oda Müziği (Karma Oda Müziği, Vokal Müzik, Solo Çalgı Müzikleri) 10 – 15 dakikalık eser sahibi olmak",
    "L54": "Ulusal Oda Müziği (Karma Oda Müziği, Vokal Müzik, Solo Çalgı Müzikleri) 15 ve üzeri dakikalık eser sahibi olmak",
    "L55": "Ulusal Elektronik ve Elektro – Akustik Müzikler (Çalgı, elektronik ortam ve Bilgisayar ortamında Fix Medya Müziği) 0 – 5 dakikalık eser sahibi olmak",
    "L56": "Ulusal Elektronik ve Elektro – Akustik Müzikler (Çalgı, elektronik ortam ve Bilgisayar ortamında Fix Medya Müziği) 5 – 10 dakikalık eser sahibi olmak",
    "L57": "Ulusal Elektronik ve Elektro – Akustik Müzikler (Çalgı, elektronik ortam ve Bilgisayar ortamında Fix Medya Müziği) 10 – 15 dakikalık eser sahibi olmak",
    "L58": "Ulusal Elektronik ve Elektro – Akustik Müzikler (Çalgı, elektronik ortam ve Bilgisayar ortamında Fix Medya Müziği) 15 ve üzeri dakikalık eser sahibi olmak",
    "L59": "Uluslararası Orkestra İçin Bestelenmiş Eser (4’lü, 3’lü, 2’li, Oda ve Yaylı Çalgılar Orkestrası) 0 – 5 dakikalık eser sahibi olmak",
    "L60": "Uluslararası Orkestra İçin Bestelenmiş Eser (4’lü, 3’lü, 2’li, Oda ve Yaylı Çalgılar Orkestrası) 5 – 10 dakikalık eser sahibi olmak",
    "L61": "Uluslararası Orkestra İçin Bestelenmiş Eser (4’lü, 3’lü, 2’li, Oda ve Yaylı Çalgılar Orkestrası) 10 – 15 dakikalık eser sahibi olmak",
    "L62": "Uluslararası Orkestra İçin Bestelenmiş Eser (4’lü, 3’lü, 2’li, Oda ve Yaylı Çalgılar Orkestrası) 15 ve üzeri dakikalık eser sahibi olmak",
    "L63": "Uluslararası Oda Müziği (Karma Oda Müziği, Vokal Müzik, Solo Çalgı Müzikleri) 0 – 5 dakikalık eser sahibi olmak",
    "L64": "Uluslararası Oda Müziği (Karma Oda Müziği, Vokal Müzik, Solo Çalgı Müzikleri) 5 – 10 dakikalık eser sahibi olmak",
    "L65": "Uluslararası Oda Müziği (Karma Oda Müziği, Vokal Müzik, Solo Çalgı Müzikleri) 10 – 15 dakikalık eser sahibi olmak",
    "L66": "Uluslararası Oda Müziği (Karma Oda Müziği, Vokal Müzik, Solo Çalgı Müzikleri) 15 ve üzeri dakikalık eser sahibi olmak",
    "L67": "Uluslararası Elektronik ve Elektro – Akustik Müzikler (Çalgı, elektronik ortam ve Bilgisayar ortamında Fix Medya Müziği) 0 – 5 dakikalık eser sahibi olmak",
    "L68": "Uluslararası Elektronik ve Elektro – Akustik Müzikler (Çalgı, elektronik ortam ve Bilgisayar ortamında Fix Medya Müziği) 5 – 10 dakikalık eser sahibi olmak",
    "L69": "Uluslararası Elektronik ve Elektro – Akustik Müzikler (Çalgı, elektronik ortam ve Bilgisayar ortamında Fix Medya Müziği) 10 – 15 dakikalık eser sahibi olmak",
    "L70": "Uluslararası Elektronik ve Elektro – Akustik Müzikler (Çalgı, elektronik ortam ve Bilgisayar ortamında Fix Medya Müziği) 15 ve üzeri dakikalık eser sahibi olmak",
    "L71": "Türk Müziği makamlarını kullanarak geleneksel formlar (ayin, peşrev, kâr, kârçe, ağır semâi, yürük semâi, beste, şarkı vb …) çerçevesinde oluşturulmuş kompozisyonlar. Bestelenmiş Eser Sahibi Olmak (Nota ile belgelemek koşulu ile)",
    "L72": "Türk Müziği makamlarını kullanarak geleneksel formlar … Bestelenmiş ve Seslendirilmiş Eser Sahibi Olmak (ulusal konser veya ses yayını)",
    "L73": "Türk Müziği makamlarını kullanarak geleneksel formlar … Bestelenmiş ve Seslendirilmiş Eser Sahibi Olmak (uluslararası konser veya yurt dışında basılmış ses yayını)",
    "L74": "Türk Halk Müziği alanında derleme yapmak. (TRT Müzik Dairesi Bşk. Repertuvar Kurulu tarafından onaylanmış)",
    "L75": "Türk Halk Müziği alanında derleme yapmak. (Nota ile belgelemek koşulu ile)",
    "L76": "Türk Halk Müziği alanında derlenmiş parçanın notaya alınması (TRT Müzik Dairesi Bşk. Repertuvar kurulu tarafından onaylanmış)",
    "L77": "Büyük oyun /film yönetmenliği",
    "L78": "Kısa oyun/film yönetmenliği",
    "L79": "Sahne oyunu / senaryo (uzun) ve dizi drama yazarlığı",
    "L80": "Kısa sahne oyunu ve senaryo yazarlığı",
    "L81": "Uyarlama oyun/senaryo yazmak, metin düzenlemek (uzun)",
    "L82": "Uyarlama oyun/senaryo yazmak, metin düzenlemek (kısa)",
    "L83": "Uzun oyun/senaryo/dizi drama dramaturjisi yapmak",
    "L84": "Kısa oyun/senaryo dramaturjisi yapmak",
    "L85": "Uzun oyun/senaryo/ dizi drama metni çevirmek",
    "L86": "Kısa oyun/senaryo metni çevirmek",
    "L87": "Uzun oyunda/sinema filminde/dizi dramada başrol",
    "L88": "Uzun oyunda/sinema filminde/dizi dramada diğer roller",
    "L89": "Kısa oyun/filmde başrol",
    "L90": "Kısa oyun/filmde diğer roller",
    "L91": "Sahne oyunu/ film (uzun) ve dizi drama dekor / kostüm / ışık / ses / efekt tasarımı",
    "L92": "Sahne oyunu/ film (uzun) ve dizi drama dekor / kostüm / ışık / ses / efekt tasarımı ekibinde görev almak",
    "L93": "Sahne oyunu/ film (kısa) dekor / kostüm / ışık / ses / efekt tasarımı",
    "L94": "Sahne oyunu/ film (kısa) dekor / kostüm / ışık / ses / efekt tasarımı ekibinde görev almak",
    "L95": "Sahne oyunu/ film (uzun) ve dizi dramada makyaj, mask, kukla, butafor vb tasarımı",
    "L96": "Sahne oyunu/ film (uzun) ve dizi dramada makyaj, mask, kukla, butafor vb tasarımı ekibinde görev almak",
    "L97": "Sahne oyunu/ film (kısa) makyaj, mask, kukla, butafor vb tasarımı",
    "L98": "Sahne oyunu/ film (kısa) makyaj, mask, kukla, butafor vb tasarımı ekibinde görev almak",
    "L99": "Sanat yönetmenliği (uzun prodüksiyonlar)",
    "L100":"Sanat yönetmenliği (kısa prodüksiyonlar)",
    "L101":"Koreografi, dramatizasyon, dinleti, performans, happening veya workshop (atölye) düzenleme/yönetme",
    "L102":"Kongre, sempozyum, festival etkinliklerinde atölye çalışması düzenlemek",
    "L103":"Yapıtın festival, şenlik vb. etkinliklere katılımı",
    "L104":"Oyunun/senaryonun/filmin/sergilenmiş oyunun video kaydının vb. kamu/özel TV’ler/dijital platformlar/kurumsal kimlikli internet siteleri vb tarafından satın alınması/gösterilmesi; Devlet Tiyatroları/Şehir Tiyatroları vb tiyatroların repertuvarlarına girmesi",
    "L105":"En az 10 kere gerçekleştirilmiş olan sanatsal bir yarışma/ödül organizasyonu tarafından yapıtın/sanatçının ödüllendirilmesi",
},


# 2) Alias tanımlamaları
MAKALE_META       = MAKALELER
TOPLANTI_META     = TOPLANTILAR
KITAP_META        = KITAPLAR
ATIF_META         = ATIFLAR
EGITIM_META       = EGITIMLER
TEZ_META          = TEZLER
PATENT_META       = PATENTLER
PROJE_META        = PROJELER
EDITORLUK_META    = EDITORLUK
ODUL_META         = ODULLER
IDARI_META        = IDARI_GOREV
GUZEL_SANAT_META  = GUZEL_SANAT

# 3) Sayfa görüntüleme view'ları

def ilanlar(request):
    ilanlar = Ilan.objects.all()
    return render(request, 'ilanlar.html', {'ilanlar': ilanlar})




def build_list(request, post_kod, post_detay, mapping):
    kodlar = request.POST.getlist(post_kod)
    detaylar = request.POST.getlist(post_detay)
    result = []
    for kod, det in zip(kodlar, detaylar):
        if det.strip():
            uzun = mapping.get(kod, kod)
            result.append((uzun, det))
    return result

def basvuru_pdf(request):
    path_wkhtmltopdf = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    if request.method == 'GET':
        html_string = render_to_string('pdf_template.html', {'data': 'Örnek Başvuru Verisi'})
        pdf_file = pdfkit.from_string(html_string, False, configuration=config)

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="basvuru.pdf"'
        return response

    # POST ise formdan gelen verileri al
    makaleler       = build_list(request, 'makale_turu[]', 'yazarlar_dergi_bilgi[]', MAKALE_META)
    toplantilar     = build_list(request, 'toplanti_turu[]', 'toplanti_detay[]', TOPLANTI_META)
    kitaplar        = build_list(request, 'kitap_turu[]', 'kitap_detaylari[]', KITAP_META)
    atiflar         = build_list(request, 'atif_turu[]', 'atif_detay[]', ATIF_META)
    egitimler       = build_list(request, 'egitim_turu[]', 'egitim_detay[]', EGITIM_META)
    tezler          = build_list(request, 'tez_turu[]', 'tez_detay[]', TEZ_META)
    patentler       = build_list(request, 'patent_turu[]', 'patent_detay[]', PATENT_META)
    projeler        = build_list(request, 'proje_turu[]', 'proje_detay[]', PROJE_META)
    editorluklar    = build_list(request, 'editorluk[][tur]', 'editorluk[][gorev_suresi]', EDITORLUK_META)
    oduller         = build_list(request, 'odul_turu[]', 'odul_kurul[]', ODUL_META)
    idari_gorevler  = build_list(request, 'idari_gorev_turu[]', 'idari_gorev_detay[]', IDARI_META)
    guzel_sanatlar  = build_list(request, 'guzelSanatlar[][tur]', 'guzelSanatlar[][detay]', GUZEL_SANAT_META)

    context = {
        'isim': request.POST.get('isim', ''),
        'tarih': request.POST.get('tarih', ''),
        'kurum': request.POST.get('kurum', ''),
        'kadro': request.POST.get('kadro', ''),
        'imza': request.POST.get('imza', ''),
        'profesor': request.POST.get('profesor') == 'on',
        'docent': request.POST.get('docent') == 'on',
        'drOgrUyesi': request.POST.get('drOgrUyesi') == 'on',

        'makaleler':      makaleler,
        'toplantilar':    toplantilar,
        'kitaplar':       kitaplar,
        'atiflar':        atiflar,
        'egitimler':      egitimler,
        'tezler':         tezler,
        'patentler':      patentler,
        'projeler':       projeler,
        'editorluklar':   editorluklar,
        'oduller':        oduller,
        'idari_gorevler': idari_gorevler,
        'guzel_sanatlar': guzel_sanatlar,
    }

    html_string = render_to_string('pdf_template.html', context)

    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': 'UTF-8',
        'enable-local-file-access': None,
    }

    try:
        pdf_bytes = pdfkit.from_string(
            html_string, False,
            configuration=config, options=options, verbose=True
        )
    except Exception:
        tb = traceback.format_exc()
        return HttpResponse(
            '<h1>PDF Oluşturma Hatası</h1><pre>' + tb + '</pre>',
            content_type='text/html'
        )

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="basvuru.pdf"'
    return response

