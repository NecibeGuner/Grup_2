# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has on_delete set to the desired behavior
#   * Remove managed = False lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Admin(models.Model):
    adminid = models.AutoField(db_column='adminID', primary_key=True)  # Field name made lowercase.
    tc = models.CharField(unique=True, max_length=11)
    sifre = models.TextField()

    class Meta:
        managed = False
        db_table = 'admin'


class ArastirmaProjelerii(models.Model):
    basvuru = models.ForeignKey('Basvurular', models.DO_NOTHING)
    proje_turu = models.TextField()  # This field type is a guess.
    proje_detaylari = models.TextField(blank=True, null=True)
    proje_belgesi = models.TextField(blank=True, null=True)
    gorev_belgesi = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'arastirma_projeleri'


class Atiflari(models.Model):
    basvuru = models.ForeignKey('Basvurular', models.DO_NOTHING)
    atif_turu = models.TextField()  # This field type is a guess.
    eserin_adi_ve_atis_sayisi = models.TextField(blank=True, null=True)
    pdf_yolu = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atiflar'




class Basvurular(models.Model):
    kullanici = models.ForeignKey('Kullanicilar', models.DO_NOTHING)
    faaliyet_donemi = models.TextField(blank=True, null=True)
    basvurulan_kadro = models.TextField()
    basvuru_tarihi = models.DateField()
    basvuru_pdf = models.BinaryField(blank=True, null=True)
    ilan = models.ForeignKey('Ilanı', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'basvurular'


class BilimselToplantiFaaliyetlerii(models.Model):
    basvuru = models.ForeignKey(Basvurular, models.DO_NOTHING)
    bilimsel_toplanti_turu = models.TextField()  # This field type is a guess.
    detaylar = models.TextField(blank=True, null=True)
    belge_yolu = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bilimsel_toplanti_faaliyetleri'



class Editorlukk(models.Model):
    basvuru = models.ForeignKey(Basvurular, models.DO_NOTHING)
    tur = models.TextField()  # This field type is a guess.
    aciklama = models.TextField(blank=True, null=True)
    gorev_belge = models.TextField(blank=True, null=True)
    indeks_belge = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'editorluk'


class EgitimFaaliyetlerii(models.Model):
    basvuru = models.ForeignKey(Basvurular, models.DO_NOTHING)
    ders_turu = models.TextField()  # This field type is a guess.
    ders_detaylari = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'egitim_faaliyetleri'


class GuzelSanatlarFaaliyetlerii(models.Model):
    basvuru = models.ForeignKey(Basvurular, models.DO_NOTHING)
    faaliyet_turu = models.TextField()  # This field type is a guess.
    detaylar = models.TextField(blank=True, null=True)
    dokuman = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guzel_sanatlar_faaliyetleri'


class IdariGorevleri(models.Model):
    basvuru = models.ForeignKey(Basvurular, models.DO_NOTHING)
    gorev_turu = models.TextField()  # This field type is a guess.
    gorev_birimi_yili = models.TextField(blank=True, null=True)
    belge_yukle = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'idari_gorevler'


class Ilanı(models.Model):
    ilanid = models.AutoField(db_column='ilanID', primary_key=True)  # Field name made lowercase.
    bolum = models.TextField()
    pozisyon = models.TextField()
    aciklama = models.TextField()
    bilgilendirme_dosya = models.TextField()  # This field type is a guess.
    basl_tarih = models.DateField()
    bitis_tarih = models.DateField()
    kadro_sayi = models.IntegerField()
    basvuru_sayisi = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ilan'


class JuriAdaylari(models.Model):
    juriid = models.AutoField(db_column='juriID', primary_key=True)  # Field name made lowercase.
    isim = models.TextField()
    soyisim = models.TextField()
    unvan = models.TextField()
    kullanici_rolu = models.TextField()
    ilanid = models.ForeignKey(Ilanı, models.DO_NOTHING, db_column='ilanID', blank=True, null=True)  # Field name made lowercase.
    tc = models.CharField(unique=True, max_length=11)
    sifre = models.TextField()

    class Meta:
        managed = True
        db_table = 'juri_adaylari'


class JuriDegerlendirmesi(models.Model):
    juridegerlendirmeid = models.AutoField(db_column='juriDegerlendirmeID', primary_key=True)  # Field name made lowercase.
    juriid = models.ForeignKey('core.JuriAdaylari', on_delete=models.CASCADE)
    basvuruid = models.ForeignKey(Basvurular, models.DO_NOTHING, db_column='basvuruID', blank=True, null=True)  # Field name made lowercase.
    juri_raporu = models.TextField(blank=True, null=True)  # This field type is a guess.
    onay_durumu = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'juri_degerlendirme'


class KisiselBilgileri(models.Model):
    kullanici = models.OneToOneField('Kullanicilar', models.DO_NOTHING)
    ad_soyad = models.TextField()
    tc_kimlik_no = models.CharField(max_length=11)
    dogum_tarihi = models.DateField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    adres = models.TextField(blank=True, null=True)
    akademik_unvan = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'kisisel_bilgiler'


class Kitaplari(models.Model):
    basvuru = models.ForeignKey(Basvurular, models.DO_NOTHING)
    kitap_turu = models.TextField()  # This field type is a guess.
    kitap_detaylari = models.TextField(blank=True, null=True)
    kapak_ve_icindekiler_pdf = models.TextField(blank=True, null=True)
    yayin_taninirlik_pdf = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kitaplar'


class Kullanicilar(models.Model):
    tc_kimlik_no = models.CharField(unique=True, max_length=11)
    ad_soyad = models.TextField()
    sifre_hash = models.TextField()
    rol = models.TextField() 
    olusturma_tarihi = models.DateTimeField()
    son_giris = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kullanicilar'


class Makaleleri(models.Model):
    basvuru = models.ForeignKey(Basvurular, models.DO_NOTHING)
    makale_turu = models.TextField()  # This field type is a guess.
    yazarlar_dergi_bilgi = models.TextField(blank=True, null=True)
    pdf_yolu = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'makaleler'


class Odulleri(models.Model):
    basvuru = models.ForeignKey(Basvurular, models.DO_NOTHING)
    tur = models.TextField()  # This field type is a guess.
    aciklama = models.TextField(blank=True, null=True)
    belge_pdf = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'oduller'


class Patentleri(models.Model):
    basvuru = models.ForeignKey(Basvurular, models.DO_NOTHING)
    patent_turu = models.TextField()  # This field type is a guess.
    patent_detaylari = models.TextField()
    patent_belgesi_pdf = models.TextField()

    class Meta:
        managed = False
        db_table = 'patentler'


class TezYoneticiliklerii(models.Model):
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
        managed = True
        db_table = 'yonetici'