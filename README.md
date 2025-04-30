# Akademik Personel Başvuru Sistemi

Bu proje, Kocaeli Üniversitesi'nde akademik personel başvuru süreçlerini dijital ortama taşıyarak daha verimli, şeffaf ve takip edilebilir bir hale getirmeyi amaçlamaktadır. Sistem; aday, jüri, yönetici ve admin rollerine göre kimlik doğrulama, rol tabanlı yetkilendirme, ilan oluşturma, başvuru izleme, jüri atama ve değerlendirme gibi modülleri içerir.

## Özellikler

- **Kullanıcı Kimlik Doğrulama:** T.C. Kimlik Numarası ve şifre ile güvenli giriş
- **Rol Tabanlı Yetkilendirme:** Aday, jüri, yönetici ve admin rollerine özel yetkiler
- **İlan Yönetimi:** Akademik personel ilanı oluşturma, düzenleme ve yayınlama
- **Başvuru Süreci:** Adayların ilanlara çevrim içi başvuru yapma ve belge yükleme
- **Jüri Değerlendirme:** Jüri üyelerine atanan başvuruları dijital ortamda inceleme ve rapor yükleme
- **Yönetici Modülü:** Başvuruları ve jüri değerlendirmelerini izleme, aşamaları yönetme
- **Admin Modülü:** Sistem genel yönetimi, kullanıcı hesapları ve ilan şablonları tanımlama
- **Otomatik Raporlama:** Başvuru verilerini kullanarak Tablo 5 ve PDF rapor oluşturma

## Teknolojiler

- Python 3.x, Django 4.2.x
- PostgreSQL 14.x
- AWS S3 (Belge depolama)
- Outlook SMTP (E-posta bildirimleri)
- HTML5, CSS3, JavaScript (ES6+)

## Kurulum

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/NecibeGuner/Grup_2.git
   cd Grup_2
   ```
2. Sanal ortam oluşturun ve aktif edin:
   ```bash
   python -m venv venv
   source venv/bin/activate  # UNIX
   venv\Scripts\activate    # Windows
   ```
3. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
4. Veritabanı ayarlarını `settings.py` dosyasında yapılandırın.
5. Veritabanı migrasyonlarını uygulayın:
   ```bash
   python manage.py migrate
   ```
6. Sunucuyu çalıştırın:
   ```bash
   python manage.py runserver
   ```

## Proje Raporu

[Grup2_rapor.docx](https://github.com/user-attachments/files/19978678/Grup2_rapor.docx)

## Lisans

MIT Lisansı


