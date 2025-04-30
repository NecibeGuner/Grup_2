
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser



ROL_SECENEKLERI = [
    ('YONETICI',  'Yönetici'),
    ('ADAY',      'Aday'),
    ('JURI',      'Jüri'),
    ('ADMIN',     'Admin'),
]

from django.db import models

# ---------------------------------
# 1) Kullanıcı (kullanicilar tablosu)
# ---------------------------------
class Kullanici(models.Model):
    id               = models.AutoField(primary_key=True)
    tc_kimlik_no     = models.CharField(max_length=11, unique=True)
    ad_soyad         = models.TextField()
    sifre            = models.CharField(
        max_length=128,
        db_column='sifre_hash'    # veritabanında bu sütun böyle adlandırılmış
    )
    rol              = models.CharField(max_length=20)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    son_giris        = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'kullanicilar'

    def __str__(self):
        return f"{self.ad_soyad} ({self.tc_kimlik_no})"


# ---------------------------------
# 2) Kişisel Bilgiler (kisisel_bilgiler tablosu)
# ---------------------------------
KADRO_TURU_CHOICES = [
    ('PROFESOR',            'Profesör'),
    ('DOCENT',              'Doçent'),
    ('DOKTOR',              'Doktor'),
    ('OGRETIM_GOREVLISI',   'Öğretim Görevlisi'),
    ('ARASTIRMA_GOREVLISI', 'Araştırma Görevlisi'),
]

class KisiselBilgiler(models.Model):
    id             = models.AutoField(primary_key=True)
    kullanici      = models.ForeignKey(
                        Kullanici,
                        db_column='kullanici_id',
                        on_delete=models.CASCADE,
                        related_name='kisisel_bilgiler'
                     )
    ad_soyad       = models.TextField(db_column='ad_soyad')
    tc_kimlik_no   = models.CharField(
                        max_length=11,
                        db_column='tc_kimlik_no'
                     )
    dogum_tarihi   = models.DateField(
                        null=True,
                        blank=True,
                        db_column='dogum_tarihi'
                     )
    email          = models.TextField(
                        null=True,
                        blank=True,
                        db_column='email'
                     )
    adres          = models.TextField(
                        null=True,
                        blank=True,
                        db_column='adres'
                     )
    kadro_turu     = models.CharField(
                        max_length=20,
                        choices=KADRO_TURU_CHOICES,
                        null=True,
                        blank=True,
                        db_column='akademik_unvan'
                     )

    class Meta:
        managed  = False
        db_table = 'kisisel_bilgiler'

    def __str__(self):
        return f"{self.ad_soyad} — {self.get_kadro_turu_display() or '—'}"


# ---------------------------
# 3) Başvurular tablosu
# ---------------------------
class Basvurular(models.Model):
    id               = models.AutoField(primary_key=True)
    kullanici        = models.ForeignKey(
        'core.Kullanici',
        on_delete=models.CASCADE,
        db_column='kullanici_id'
    )
    kisisel_bilgi    = models.ForeignKey(
        'core.KisiselBilgiler',
        on_delete=models.CASCADE,
        db_column='kisisel_bilgi_id',
        null=True,
        blank=True
    )
    ilan             = models.ForeignKey(
        'core.Ilan',
        on_delete=models.CASCADE,
        db_column='ilan_id',
        null=True,      # <— Burayı ekledik
        blank=True      # <— ve bunu da
    )
    faaliyet_donemi  = models.TextField(null=True, blank=True)
    basvurulan_kadro = models.TextField()
    basvuru_aciklam  = models.TextField(null=True, blank=True)
    basvuru_tarihi   = models.DateField()

    class Meta:
        db_table = 'basvurular'


class Admin(models.Model):
    adminid = models.AutoField(db_column='adminID', primary_key=True)  # Field name made lowercase.
    tc = models.CharField(unique=True, max_length=11)
    sifre = models.TextField()

    class Meta:
        managed = False
        db_table = 'admin'


class ArastirmaProjeleri(models.Model):
    basvuru = models.ForeignKey('Basvurular', models.DO_NOTHING)
    proje_turu = models.TextField()  # This field type is a guess.
    proje_detaylari = models.TextField(blank=True, null=True)
    proje_belgesi = models.TextField(blank=True, null=True)
    gorev_belgesi = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'arastirma_projeleri'


class Atiflar(models.Model):
    basvuru = models.ForeignKey('Basvurular', models.DO_NOTHING)
    atif_turu = models.TextField()  # This field type is a guess.
    eserin_adi_ve_atis_sayisi = models.TextField(blank=True, null=True)
    pdf_yolu = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atiflar'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


from django.conf import settings
from django.db import models





class BilimselToplantiFaaliyetleri(models.Model):
    basvuru = models.ForeignKey(Basvurular, models.DO_NOTHING)
    bilimsel_toplanti_turu = models.TextField()  # This field type is a guess.
    detaylar = models.TextField(blank=True, null=True)
    belge_yolu = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bilimsel_toplanti_faaliyetleri'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Editorluk(models.Model):
    basvuru = models.ForeignKey(Basvurular, models.DO_NOTHING)
    tur = models.TextField()  # This field type is a guess.
    aciklama = models.TextField(blank=True, null=True)
    gorev_belge = models.TextField(blank=True, null=True)
    indeks_belge = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'editorluk'


class EgitimFaaliyetleri(models.Model):
    basvuru = models.ForeignKey(Basvurular, models.DO_NOTHING)
    ders_turu = models.TextField()  # This field type is a guess.
    ders_detaylari = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'egitim_faaliyetleri'


class GuzelSanatlarFaaliyetleri(models.Model):
    basvuru = models.ForeignKey(Basvurular, models.DO_NOTHING)
    faaliyet_turu = models.TextField()  # This field type is a guess.
    detaylar = models.TextField(blank=True, null=True)
    dokuman = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guzel_sanatlar_faaliyetleri'


class IdariGorevler(models.Model):
    basvuru = models.ForeignKey(Basvurular, models.DO_NOTHING)
    gorev_turu = models.TextField()  # This field type is a guess.
    gorev_birimi_yili = models.TextField(blank=True, null=True)
    belge_yukle = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'idari_gorevler'


class Ilan(models.Model):
    ilanID = models.AutoField(primary_key=True)
    bolum = models.TextField()
    pozisyon = models.TextField()
    aciklama = models.TextField()
    bilgilendirme_dosya = models.BinaryField(blank=True, null=True)  # Bytea için BinaryField
    basl_tarih = models.DateField()
    bitis_tarih = models.DateField()
    kadro_sayi = models.IntegerField()
    basvuru_sayisi = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'ilan'

class JuriAdaylari(models.Model):
    juriid = models.AutoField(db_column='juriID', primary_key=True)  # Field name made lowercase.
    isim = models.TextField()
    soyisim = models.TextField()
    unvan = models.TextField()
    kullanici_rolu = models.TextField()
    ilanid = models.ForeignKey(Ilan, models.DO_NOTHING, db_column='ilanID', blank=True, null=True)  # Field name made lowercase.
    tc = models.CharField(unique=True, max_length=11)

    class Meta:
        managed = False
        db_table = 'juri_adaylari'


class JuriDegerlendirme(models.Model):
    juridegerlendirmeid = models.AutoField(db_column='juriDegerlendirmeID', primary_key=True)  # Field name made lowercase.
    juriid = models.ForeignKey(JuriAdaylari, models.DO_NOTHING, db_column='juriID', blank=True, null=True)  # Field name made lowercase.
    basvuruid = models.ForeignKey(Basvurular, models.DO_NOTHING, db_column='basvuruID', blank=True, null=True)  # Field name made lowercase.
    juri_raporu = models.TextField(blank=True, null=True)  # This field type is a guess.
    onay_durumu = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'juri_degerlendirme'



class Kitaplar(models.Model):
    basvuru = models.ForeignKey(Basvurular, models.DO_NOTHING)
    kitap_turu = models.TextField()  # This field type is a guess.
    kitap_detaylari = models.TextField(blank=True, null=True)
    kapak_ve_icindekiler_pdf = models.TextField(blank=True, null=True)
    yayin_taninirlik_pdf = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kitaplar'



class Makaleler(models.Model):
    basvuru = models.ForeignKey(Basvurular, models.DO_NOTHING)
    makale_turu = models.TextField()  # This field type is a guess.
    yazarlar_dergi_bilgi = models.TextField(blank=True, null=True)
    pdf_yolu = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'makaleler'


class Oduller(models.Model):
    basvuru = models.ForeignKey(Basvurular, models.DO_NOTHING)
    tur = models.TextField()  # This field type is a guess.
    aciklama = models.TextField(blank=True, null=True)
    belge_pdf = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'oduller'


class Patentler(models.Model):
    basvuru = models.ForeignKey(Basvurular, models.DO_NOTHING)
    patent_turu = models.TextField()  # This field type is a guess.
    patent_detaylari = models.TextField()
    patent_belgesi_pdf = models.TextField()

    class Meta:
        managed = False
        db_table = 'patentler'


class TezYoneticilikleri(models.Model):
    basvuru = models.ForeignKey(Basvurular, models.DO_NOTHING)
    tez_turu = models.TextField()  # This field type is a guess.
    tez_detaylari = models.TextField()
    tez_belgesi_pdf = models.TextField()

    class Meta:
        managed = False
        db_table = 'tez_yoneticilikleri'


class Yonetici(models.Model):
    yonetici_id = models.AutoField(primary_key=True)
    isim = models.TextField()
    soyisim = models.TextField()
    tc = models.CharField(unique=True, max_length=11)
    sifre = models.TextField()
    unvan = models.TextField()
    rol = models.TextField()

    class Meta:
        managed = False
        db_table = 'yonetici'

