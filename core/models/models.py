from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


# Kullanıcı Rolleri
ROL_SECENEKLERI = [
    ('YONETICI', 'Yönetici'),
    ('ADAY',     'Aday'),
    ('JURI',     'Jüri'),
    ('ADMIN',    'Admin'),
]

AKADEMIK_UNVAN_SECENEKLERI = [
    ('ASISTAN',   'Asistan'),
    ('OGRETIM_UYESI', 'Öğretim Üyesi'),
    ('DOCENT',    'Doçent'),
    ('PROFESOR',  'Profesör'),
]

# Bilimsel Toplantı Seçenekleri
BILIMSEL_TOPLANTI_SECENEKLERI = [
    ("B1",  "Uluslararası bilimsel toplantılarda sözlü olarak sunulan, tam metni matbu veya elektronik olarak bildiri kitapçığında yayımlanmış çalışmalar"),
    ("B2",  "Uluslararası bilimsel toplantılarda sözlü olarak sunulan, özet metni matbu veya elektronik olarak bildiri kitapçığında yayımlanmış çalışmalar"),
    ("B3",  "Uluslararası bilimsel toplantılarda poster olarak sunulan çalışmalar"),
    ("B4",  "Ulusal bilimsel toplantılarda sözlü olarak sunulan tam metni matbu veya elektronik olarak bildiri kitapçığında yayımlanmış çalışmalar"),
    ("B5",  "Ulusal bilimsel toplantılarda sözlü olarak sunulan, özet metni matbu veya elektronik olarak bildiri kitapçığında yayımlanmış çalışmalar"),
    ("B6",  "Ulusal bilimsel toplantılarda poster olarak sunulan çalışmalar"),
    ("B7",  "Uluslararası bir kongre, konferans veya sempozyumda organizasyon veya yürütme komitesinde düzenleme kurulu üyeliği veya bilim kurulu üyeliği yapmak"),
    ("B8",  "Ulusal bir kongre, konferans veya sempozyumda organizasyon veya yürütme komitesinde düzenleme kurulu üyeliği veya bilim kurulu üyeliği yapmak"),
    ("B9",  "Uluslararası konferanslarda, bilimsel toplantı, seminerlerde davetli konuşmacı olarak yer almak"),
    ("B10", "Ulusal konferanslarda, bilimsel toplantı, seminerlerde davetli konuşmacı olarak yer almak"),
    ("B11", "Uluslararası veya ulusal çeşitli kurumlarla işbirliği içinde atölye, çalıştay, yaz okulu organize ederek gerçekleştirmek"),
    ("B12", "Uluslararası veya ulusal çeşitli kurumlarla işbirliği içinde atölye, çalıştay, panel, seminer, yaz okulunda konuşmacı veya panelist olarak görev almak"),
]

ATIF_TURU_CHOICES = [
    ("D1", "1) SCI-E, SSCI ve AHCI tarafından taranan dergilerde; Uluslararası yayınevleri tarafından yayımlanmış … her eseri için"),
    ("D2", "2) E-SCI tarafından taranan dergilerde ve adayın yazar olarak yer almadığı yayınlardan her birinde…"),
    ("D3", "3) SCI-E, SSCI, AHCI, E-SCI dışındaki uluslararası indeksli dergilerde; Uluslararası yayınevlerinde bölümler için"),
    ("D4", "4) Ulusal hakemli dergilerde; Ulusal yayınevlerinde yayımlanmış kitaplarda…"),
    ("D5", "5) Güzel sanat eserlerinin uluslararası kaynaklarda yayımlanması veya gösterilmesi"),
    ("D6", "6) Güzel sanat eserlerinin ulusal kaynaklarda yayımlanması veya gösterilmesi"),


]

EGITIM_TURU_CHOICES = [
    ("E1", "1) Ön lisans / lisans dersleri"),
    ("E2", "2) Ön lisans / lisans dersleri (Yabancı dilde)"),
    ("E3", "3) Lisansüstü dersleri"),
    ("E4", "4) Lisansüstü dersleri (Yabancı dilde)"),
]

TEZ_TURU_CHOICES = [
    ("F1", "Doktora/Sanatta Yeterlik veya Tıp/Diş Hekimliğinde Uzmanlık tez yönetimi"),
    ("F2", "Yüksek Lisans Tez Yönetimi"),
    ("F3", "Doktora/Sanatta Yeterlik (Eş Danışman)"),
    ("F4", "Yüksek Lisans/Sanatta Yeterlik Tez Yönetimi (Eş Danışman)"),
]

PATENT_TURU_CHOICES = [
    ("G1", "Lisanslanan Uluslararası Patent"),
    ("G2", "Tescillenmiş Uluslararası Patent"),
    ("G3", "Uluslararası Patent Başvurusu"),
    ("G4", "Lisanslanan Ulusal Patent"),
    ("G5", "Tescillenmiş Ulusal Patent"),
    ("G6", "Ulusal Patent Başvurusu"),
    ("G7", "Lisanslanan Faydalı Model, Endüstriyel Tasarım, Marka"),
    ("G8", "Faydalı Model ve Endüstriyel Tasarım"),
]

ARASTIRMA_PROJE_TURU_CHOICES = [
    ("H1",  "AB çerçeve programı/NSF/ERC bilimsel araştırma projesinde koordinatör/alt koordinatör olmak"),
    ("H2",  "AB çerçeve programı/NSF/ERC bilimsel araştırma projesinde yürütücü olmak"),
    ("H3",  "AB çerçeve programı/NSF/ERC bilimsel araştırma projesinde araştırmacı olmak"),
    ("H4",  "AB çerçeve dışı uluslararası projelerde koordinatör/alt koordinatör olmak"),
    ("H5",  "AB çerçeve dışı uluslararası projelerde yürütücü olmak"),
    ("H6",  "AB çerçeve dışı uluslararası projelerde araştırmacı olmak"),
    ("H7",  "AB çerçeve dışı uluslararası projelerde danışman olmak"),
    ("H8",  "TÜBİTAK ARGE/TÜSEB projelerinde yürütücü olmak"),
    ("H9",  "Diğer TÜBİTAK projelerinde yürütücü olmak"),
    ("H10", "TÜBİTAK dışındaki kamu kurumlarında yürütücü olmak"),
    ("H11", "Sanayi kuruluşları ile yapılan Ar-Ge projelerinde yürütücü olmak"),
    ("H12", "Diğer özel kuruluşlar ile yapılan Ar-Ge projelerinde yürütücü olmak"),
    ("H13", "TÜBİTAK ARGE (ARDEB, TEYDEB) ve TÜSEB projelerinde araştırmacı olmak"),
    ("H14", "Diğer TÜBİTAK projelerinde araştırmacı olmak"),
    ("H15", "TÜBİTAK dışı kamu kurumları projelerinde araştırmacı olmak"),
    ("H16", "Sanayi kuruluşları ile yapılan projelerde araştırmacı olmak"),
    ("H17", "Diğer özel kuruluşlarla yapılan projelerde araştırmacı olmak"),
    ("H18", "TÜBİTAK ARGE ve TÜSEB projelerinde danışman olmak"),
    ("H19", "Diğer TÜBİTAK projelerinde danışman olmak"),
    ("H20", "TÜBİTAK dışı kamu kurumları projelerinde danışman olmak"),
    ("H21", "Sanayi kuruluşlarıyla yapılan projelerde danışman olmak"),
    ("H22", "Özel kuruluşlarla yapılan projelerde danışman olmak"),
    ("H23", "BAP projelerinde yürütücü olmak"),
    ("H24", "BAP projelerinde araştırmacı olmak"),
    ("H25", "BAP projelerinde danışman olmak"),
    ("H26", "En az dört aylık yurtdışı araştırma çalışmasında bulunmak"),
    ("H27", "En az dört aylık yurtiçi araştırma çalışmasında bulunmak"),
    ("H28", "TÜBİTAK 2209-A, 2209-B, 2242 projelerinde danışman olmak"),
]

EDITORLUK_TURU_CHOICES = [
    ("E1",  "SCI-E, SSCI, AHCI veya E-SCI kapsamındaki dergilerde baş editörlük görevinde bulunmak"),
    ("E2",  "Yardımcı/ortak editörlük görevinde bulunmak"),
    ("E3",  "Asistan editörlük görevinde bulunmak"),
    ("E4",  "Yayın kurulu üyeliği"),
    ("E5",  "SCI-E dışı indeksli dergilerde baş editörlük görevinde bulunmak"),
    ("E6",  "SCI-E dışı indeksli dergilerde yardımcı/ortak editörlük görevinde bulunmak"),
    ("E7",  "SCI-E dışı indeksli dergilerde asistan editörlük görevinde bulunmak"),
    ("E8",  "SCI-E dışı indeksli dergilerde yayın kurulu üyeliği"),
    ("E9",  "ULAKBİM taramalı dergilerde baş editörlük görevi"),
    ("E10", "ULAKBİM taramalı dergilerde yayın kurulu üyeliği"),
    ("E11", "SCI-E, SSCI veya AHCI dergilerde hakemlik (her bir faaliyette)"),
    ("E12", "Uluslararası indeksli diğer dergilerde hakemlik (her bir faaliyette)"),
    ("E13", "ULAKBİM taramalı dergilerde hakemlik (her bir faaliyette)"),
]

ODUL_TURU_CHOICES = [
    ("D1", "Sürekli ve periyodik uluslararası bilim & sanat ödülleri"),
    ("D2", "TÜBİTAK Bilim, Özel ve Hizmet Ödülleri"),
    ("D3", "TÜBA Akademi Ödülleri"),
    ("D4", "TÜBİTAK Teşvik Ödülü"),
    ("D5", "TÜBA GEBİP & TESEP ödülleri"),
    ("D6", "Sürekli ve periyodik ulusal bilim & sanat ödülleri"),
    ("D7", "Jürisiz ulusal/uluslararası ödüller"),
    ("D8", "Uluslararası hakemli yarışmalarda birincilik"),
    ("D9", "… ikincilik"),
    ("D10","… üçüncülük"),
    ("D11","Ulusal hakemli yarışmalarda birincilik"),
    ("D12","… ikincilik"),
    ("D13","… üçüncülük"),
]

IDARI_GOREV_TURU_CHOICES = [
    ("K1",  "Dekan/Enstitü/Yüksekokul/MYO/Merkez Müdürü"),
    ("K2",  "Enstitü Müdür Yrd. / Dekan Yrd. / ..."),
    ("K3",  "Bölüm Başkan Yrd. / Anabilim Dalı Başkanı"),
    ("K4",  "Rektörlükçe görevlendirilen Koordinatörlük"),
    ("K5",  "Rektörlükçe görevlendirilen Koordinatör Yardımcıları"),
    ("K6",  "Rektörlükçe görevlendirilen üniversite düzeyinde Komisyon/Kurul üyelikleri"),
    ("K7",  "Dekanlık/Y.O. Müdürlüğü/... görevlendirilen Komisyon/Kurul üyelikleri"),
    ("K8",  "Bölüm Başkanlıkları tarafından görevlendirilen Komisyon/Kurul üyelikleri"),
    ("K9",  "Rektörlük/Dekanlık/... eğitim, işbirliği vb. konularda katkı sağlamak"),
    ("K10", "Uluslararası nitelikteki bilimsel ve mesleki kurum/kuruluşlarda görev almak"),
    ("K11", "Ulusal nitelikteki bilimsel ve mesleki kurum/kuruluşlarda görev almak"),
    ("K12", "Yerel nitelikteki bilimsel ve mesleki kurum/kuruluşlarda görev almak"),
]

GUZEL_SANATLAR_CHOICES = [
    ("L1",  "Özgün sanat eserlerinin, tasarım veya yorum çalışmalarının yurt dışında sanat, eğitim ve kültür kurumlarınca satın alınması veya bu eser(ler) için telif ödenmesi (Kurumlar bazında puanlama yapılır)"),
    ("L2",  "Özgün sanat eserlerinin, tasarım veya yorum çalışmalarının yurt içinde sanat, eğitim ve kültür kurumlarınca satın alınması veya bu eser(ler) için telif ödenmesi (Kurumlar bazında puanlama yapılır)"),
    ("L3",  "Yerel Yönetimler veya Özel Kuruluşların desteklediği kamusal alanda kalıcı olarak gerçekleştirilen sanat projeleri (Heykel, Duvar Resmi / Graffiti, Enstalasyon vb.) (Kurumlar bazında puanlama yapılır)"),
    ("L4",  "Galerilerde, müzelerde, sanat ve kültür merkezlerinde gerçekleştirilen Küratörlük etkinlikleri (En fazla iki kez puanlanır)"),
    ("L5",  "Özgün sanat eserleri, tasarımlar ya da yorum/icra çalışmalarıyla yurtdışında uluslararası jürili kişisel etkinlikte (sergi, bienal, sempozyum, trienal, gösteri, kareografi, performans, resital, dinleti, konser, kompozisyon, orkestra şefliği, festival, gösterim) bizzat katılım sağlayarak bulunmak."),
    ("L6",  "Özgün sanat eserleri, tasarımlar ya da yorum/icra çalışmalarıyla yurtiçinde jürili kişisel etkinlikte (sergi, bienal, sempozyum, trienal, gösteri, kareografi, performans, resital, dinleti, konser, kompozisyon, orkestra şefliği, festival, gösterim) bizzat katılım sağlayarak bulunmak."),
    ("L7",  "Özgün sanat eserleri, tasarımlar ya da yorum/icra çalışmalarıyla yurtdışında uluslararası jürili karma-ortak etkinlikte (sergi, bienal, sempozyum, trienal, gösteri, kareografi, performans, resital, dinleti, konser, kompozisyon, orkestra şefliği, festival, gösterim) bizzat katılım sağlayarak bulunmak."),
    ("L8",  "Özgün sanat eserleri, tasarımlar ya da yorum/icra çalışmalarıyla yurtiçinde ulusal jürili karma-ortak etkinlikte (sergi, bienal, sempozyum, trienal, gösteri, kareografi, performans, resital, dinleti, konser, kompozisyon, orkestra şefliği, festival, gösterim) bizzat katılım sağlayarak bulunmak."),
    ("L9",  "Uluslararası çalıştay/workshop (atölye çalışması)/uygulamalı sempozyum/yarışma/festival/şenlikte yöneticilik veya yürütücülük"),
    ("L10", "Ulusal çalıştay/workshop (atölye çalışması)/uygulamalı sempozyum/yarışma/festival/şenlikte yöneticilik veya yürütücülük"),
    ("L11", "Uluslararası çalıştay/workshop (atölye çalışması)/uygulamalı sempozyum/yarışma/festival/şenlikte araştırmacılık/kurul üyeliği"),
    ("L12", "Ulusal çalıştay/workshop (atölye çalışması)/uygulamalı sempozyum/yarışma/festival/şenlikte araştırmacılık/kurul üyeliği"),
    ("L13", "Uluslararası yarışmalarda/festivallerde/şenliklerde jüri üyeliği"),
    ("L14", "Ulusal yarışmalarda/festivallerde/şenliklerde jüri üyeliği"),
    ("L15", "Üretilen eserlerin uluslararası haber veya yayın organlarında yer alması veya gösterime ya da dinletime girmesi (her bir etkinlik için ayrı puanlanır ve her bir etkinlik için 5 haber ile sınırlıdır)"),
    ("L16", "Üretilen eserlerin ulusal haber veya yayın organlarında yer alması veya gösterime ya da dinletime girmesi (her bir etkinlik için ayrı puanlanır ve her bir etkinlik için 5 haber ile sınırlıdır)"),
    ("L17", "Uluslararası resital icra etmek"),
    ("L18", "Uluslararası Konserlerde, Orkestra, Koro, Geleneksel Topluluklar konserinde solist icracı olarak yer almak"),
    ("L19", "Uluslararası Konserlerde, Orkestra, Koro, Geleneksel Topluluklar konserinde karma icracı olarak yer almak"),
    ("L20", "Uluslararası Konserlerde, Orkestra Şefliği, Müzik Topluluğu Şefliği ve Koro Şefliği"),
    ("L21", "Ulusal Konserlerde, Oda Müziği Konserinde icracı olarak yer almak"),
    ("L22", "Ulusal Konserlerde, Orkestra Konserinde Grup Şefi olarak yer almak"),
    ("L23", "Ulusal Konserlerde, Orkestra Konserinde Grup Üyesi olarak yer almak"),
    ("L24", "Ulusal Konserlerde, Resital veya koro konserinde eşlikçi olarak yer almak"),
    ("L25", "Ulusal Konserlerde, Konser yönetmenliği / dinleti koordinatörlüğü"),
    ("L26", "Ulusal resital icra etmek"),
    ("L27", "Ulusal Konserlerde, Orkestra veya koro konserinde icracı olarak bireysel dinletide bulunmak"),
    ("L28", "Ulusal Konserlerde, Orkestra veya koro konserinde icracı olarak karma dinletide bulunmak"),
    ("L29", "Ulusal Konserlerde, Orkestra Şefliği, Müzik Topluluğu Şefliği ve Koro Şefliği"),
    ("L30", "Ulusal Konserlerde, Oda Müziği Konserinde icracı olarak yer almak"),
    ("L31", "Ulusal Konserlerde, Orkestra Konserinde Grup Şefi olarak yer almak"),
    ("L32", "Ulusal Konserlerde, Orkestra Konserinde Grup Üyesi olarak yer almak"),
    ("L33", "Ulusal Konserlerde, Resital veya koro konserinde eşlikçi olarak yer almak"),
    ("L34", "Ulusal Konserlerde, Konser yönetmenliği / dinleti koordinatörlüğü"),
    ("L35", "Uluslararası sesli ve görsel etkinlikler ve sesli yayınlar, icracı, besteci, orkestra şefi, müzik topluluğu şefi veya koro şefi olarak bireysel ses yayını"),
    ("L36", "Uluslararası sesli ve görsel etkinlikler ve sesli yayınlar, icracı, besteci, orkestra şefi, müzik topluluğu şefi veya koro şefi olarak karma ses yayını"),
    ("L37", "Uluslararası sesli ve görsel etkinlikler ve sesli yayınlar, Genel Sanat Yönetmeni/Müzik yönetmeni olarak ses yayını hazırlamak"),
    ("L38", "Uluslararası sesli ve görsel etkinlikler ve sesli yayınlar, Radyo ve TV Etkinliği - Program Hazırlamak"),
    ("L39", "Uluslararası sesli ve görsel etkinlikler ve sesli yayınlar, Radyo ve TV Etkinliği Katılımcılığı - Bireysel"),
    ("L40", "Uluslararası sesli ve görsel etkinlikler ve sesli yayınlar, Radyo ve TV Etkinliği Katılımcılığı - Karma"),
    ("L41", "Ulusal sesli ve görsel etkinlikler ve sesli yayınlar, İcracı, besteci, orkestra şefi, müzik topluluğu şefi veya koro şefi olarak bireysel ses yayını"),
    ("L42", "Ulusal sesli ve görsel etkinlikler ve sesli yayınlar, İcracı, besteci, orkestra şefi, müzik topluluğu şefi veya koro şefi olarak karma ses yayını"),
    ("L43", "Ulusal sesli ve görsel etkinlikler ve sesli yayınlar, Genel Sanat Yönetmeni/Müzik yönetmeni olarak ses yayını hazırlamak"),
    ("L44", "Ulusal sesli ve görsel etkinlikler ve sesli yayınlar, Radyo ve TV Etkinliği - Program Hazırlamak"),
    ("L45", "Ulusal sesli ve görsel etkinlikler ve sesli yayınlar, Radyo ve TV Etkinliği Katılımcılığı - Bireysel"),
    ("L46", "Ulusal sesli ve görsel etkinlikler ve sesli yayınlar, Radyo ve TV Etkinliği Katılımcılığı - Karma"),
    ("L47", "Ulusal Orkestra İçin Bestelenmiş Eser (4’lü, 3’lü, 2’li, Oda ve Yaylı Çalgılar Orkestrası) 0 – 5 dakikalık eser sahibi olmak"),
    ("L48", "Ulusal Orkestra İçin Bestelenmiş Eser (4’lü, 3’lü, 2’li, Oda ve Yaylı Çalgılar Orkestrası) 5 – 10 dakikalık eser sahibi olmak"),
    ("L49", "Ulusal Orkestra İçin Bestelenmiş Eser (4’lü, 3’lü, 2’li, Oda ve Yaylı Çalgılar Orkestrası) 10 – 15 dakikalık eser sahibi olmak"),
    ("L50", "Ulusal Orkestra İçin Bestelenmiş Eser (4’lü, 3’lü, 2’li, Oda ve Yaylı Çalgılar Orkestrası) 15 ve üzeri dakikalık eser sahibi olmak"),
    ("L51", "Ulusal Oda Müziği (Karma Oda Müziği, Vokal Müzik, Solo Çalgı Müzikleri) 0 – 5 dakikalık eser sahibi olmak"),
    ("L52", "Ulusal Oda Müziği (Karma Oda Müziği, Vokal Müzik, Solo Çalgı Müzikleri) 5 – 10 dakikalık eser sahibi olmak"),
    ("L53", "Ulusal Oda Müziği (Karma Oda Müziği, Vokal Müzik, Solo Çalgı Müzikleri) 10 – 15 dakikalık eser sahibi olmak"),
    ("L54", "Ulusal Oda Müziği (Karma Oda Müziği, Vokal Müzik, Solo Çalgı Müzikleri) 15 ve üzeri dakikalık eser sahibi olmak"),
    ("L55", "Ulusal Elektronik ve Elektro – Akustik Müzikler (Çalgı, elektronik ortam ve Bilgisayar ortamında Fix Medya Müziği) 0 – 5 dakikalık eser sahibi olmak"),
    ("L56", "Ulusal Elektronik ve Elektro – Akustik Müzikler (Çalgı, elektronik ortam ve Bilgisayar ortamında Fix Medya Müziği) 5 – 10 dakikalık eser sahibi olmak"),
    ("L57", "Ulusal Elektronik ve Elektro – Akustik Müzikler (Çalgı, elektronik ortam ve Bilgisayar ortamında Fix Medya Müziği) 10 – 15 dakikalık eser sahibi olmak"),
    ("L58", "Ulusal Elektronik ve Elektro – Akustik Müzikler (Çalgı, elektronik ortam ve Bilgisayar ortamında Fix Medya Müziği) 15 ve üzeri dakikalık eser sahibi olmak"),
    ("L59", "Uluslararası Orkestra İçin Bestelenmiş Eser (4’lü, 3’lü, 2’li, Oda ve Yaylı Çalgılar Orkestrası) 0 – 5 dakikalık eser sahibi olmak"),
    ("L60", "Uluslararası Orkestra İçin Bestelenmiş Eser (4’lü, 3’lü, 2’li, Oda ve Yaylı Çalgılar Orkestrası) 5 – 10 dakikalık eser sahibi olmak"),
    ("L61", "Uluslararası Orkestra İçin Bestelenmiş Eser (4’lü, 3’lü, 2’li, Oda ve Yaylı Çalgılar Orkestrası) 10 – 15 dakikalık eser sahibi olmak"),
    ("L62", "Uluslararası Orkestra İçin Bestelenmiş Eser (4’lü, 3’lü, 2’li, Oda ve Yaylı Çalgılar Orkestrası) 15 ve üzeri dakikalık eser sahibi olmak"),
    ("L63", "Uluslararası Oda Müziği (Karma Oda Müziği, Vokal Müzik, Solo Çalgı Müzikleri) 0 – 5 dakikalık eser sahibi olmak"),
    ("L64", "Uluslararası Oda Müziği (Karma Oda Müziği, Vokal Müzik, Solo Çalgı Müzikleri) 5 – 10 dakikalık eser sahibi olmak"),
    ("L65", "Uluslararası Oda Müziği (Karma Oda Müziği, Vokal Müzik, Solo Çalgı Müzikleri) 10 – 15 dakikalık eser sahibi olmak"),
    ("L66", "Uluslararası Oda Müziği (Karma Oda Müziği, Vokal Müzik, Solo Çalgı Müzikleri) 15 ve üzeri dakikalık eser sahibi olmak"),
    ("L67", "Uluslararası Elektronik ve Elektro – Akustik Müzikler (Çalgı, elektronik ortam ve Bilgisayar ortamında Fix Medya Müziği) 0 – 5 dakikalık eser sahibi olmak"),
    ("L68", "Uluslararası Elektronik ve Elektro – Akustik Müzikler (Çalgı, elektronik ortam ve Bilgisayar ortamında Fix Medya Müziği) 5 – 10 dakikalık eser sahibi olmak"),
    ("L69", "Uluslararası Elektronik ve Elektro – Akustik Müzikler (Çalgı, elektronik ortam ve Bilgisayar ortamında Fix Medya Müziği) 10 – 15 dakikalık eser sahibi olmak"),
    ("L70", "Uluslararası Elektronik ve Elektro – Akustik Müzikler (Çalgı, elektronik ortam ve Bilgisayar ortamında Fix Medya Müziği) 15 ve üzeri dakikalık eser sahibi olmak"),
    ("L71", "Türk Müziği makamlarını kullanarak geleneksel formlar (ayin, peşrev, kâr, kârçe, ağır semâi, yürük semâi, beste, şarkı vb …) çerçevesinde oluşturulmuş kompozisyonlar. Bestelenmiş Eser Sahibi Olmak (Nota ile belgelemek koşulu ile)"),
    ("L72", "Türk Müziği makamlarını kullanarak geleneksel formlar (ayin, peşrev, kâr, kârçe, ağır semâi, yürük semâi, beste, şarkı vb …) çerçevesinde oluşturulmuş kompozisyonlar. Bestelenmiş ve Seslendirilmiş Eser Sahibi Olmak (ulusal konser veya ses yayını)"),
    ("L73", "Türk Müziği makamlarını kullanarak geleneksel formlar (ayin, peşrev, kâr, kârçe, ağır semâi, yürük semâi, şarkı beste vb …) çerçevesinde oluşturulmuş kompozisyonlar. Bestelenmiş ve Seslendirilmiş Eser Sahibi Olmak (uluslararası konser veya yurt dışında basılmış ses yayını)"),
    ("L74", "Türk Halk Müziği alanında derleme yapmak. (TRT Müzik Dairesi Bşk. Repertuvar Kurulu tarafından onaylanmış)"),
    ("L75", "Türk Halk Müziği alanında derleme yapmak. (Nota ile belgelemek koşulu ile)"),
    ("L76", "Türk Halk Müziği alanında derlenmiş parçanın notaya alınması (TRT Müzik Dairesi Bşk. Repertuvar kurulu tarafından onaylanmış)"),
    ("L77", "Büyük oyun / film yönetmenliği"),
    ("L78", "Kısa oyun/film yönetmenliği"),
    ("L79", "Sahne oyunu / senaryo (uzun) ve dizi drama yazarlığı"),
    ("L80", "Kısa sahne oyunu ve senaryo yazarlığı"),
    ("L81", "Uyarlama oyun/senaryo yazmak, metin düzenlemek (uzun)"),
    ("L82", "Uyarlama oyun/senaryo yazmak, metin düzenlemek (kısa)"),
    ("L83", "Uzun oyun/senaryo/dizi drama dramaturjisi yapmak"),
    ("L84", "Kısa oyun/senaryo dramaturjisi yapmak"),
    ("L85", "Uzun oyun/senaryo/ dizi drama metni çevirmek"),
    ("L86", "Kısa oyun/senaryo metni çevirmek"),
    ("L87", "Uzun oyunda/sinema filminde/dizi dramada başrol"),
    ("L88", "Uzun oyunda/sinema filminde/dizi dramada diğer roller"),
    ("L89", "Kısa oyun/filmde başrol"),
    ("L90", "Kısa oyun/filmde diğer roller"),
    ("L91", "Sahne oyunu/ film (uzun) ve dizi drama dekor / kostüm / ışık / ses / efekt tasarımı"),
    ("L92", "Sahne oyunu/ film (uzun) ve dizi drama dekor / kostüm / ışık / ses / efekt tasarımı ekibinde görev almak"),
    ("L93", "Sahne oyunu/ film (kısa) dekor / kostüm / ışık / ses / efekt tasarımı"),
    ("L94", "Sahne oyunu/ film (kısa) dekor / kostüm / ışık / ses / efekt tasarımı ekibinde görev almak"),
    ("L95", "Sahne oyunu/ film (uzun) ve dizi dramada makyaj, mask, kukla, butafor vb tasarımı"),
    ("L96", "Sahne oyunu/ film (uzun) ve dizi dramada makyaj, mask, kukla, butafor vb tasarımı ekibinde görev almak"),
    ("L97", "Sahne oyunu/ film (kısa) makyaj, mask, kukla, butafor vb tasarımı"),
    ("L98", "Sahne oyunu/ film (kısa) makyaj, mask, kukla, butafor vb tasarımı ekibinde görev almak"),
    ("L99", "Sanat yönetmenliği (uzun prodüksiyonlar)"),
    ("L100","Sanat yönetmenliği (kısa prodüksiyonlar)"),
    ("L101","Koreografi, dramatizasyon, dinleti, performans, happening veya workshop (atölye) düzenleme/yönetme"),
    ("L102","Kongre, sempozyum, festival etkinliklerinde atölye çalışması düzenlemek"),
    ("L103","Yapıtın festival, şenlik vb. etkinliklere katılımı"),
    ("L104","Oyunun/senaryonun/filmin/sergilenmiş oyunun video kaydının vb. kamu/özel TV’ler/dijital platformlar/kurumsal kimlikli internet siteleri vb tarafından satın alınması/gösterilmesi; Devlet Tiyatroları/Şehir Tiyatroları vb tiyatroların repertuvarlarına girmesi"),
    ("L105","En az 10 kere gerçekleştirilmiş olan sanatsal bir yarışma/ödül organizasyonu tarafından yapıtın/sanatçının ödüllendirilmesi"),
]

MAKALE_TURU_CHOICES= {
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





class ArastirmaProjesi(models.Model):
    proje_turu = models.CharField(
        max_length=3,
        choices=ARASTIRMA_PROJE_TURU_CHOICES,
        db_column='proje_turu'
    )
    proje_detaylari = models.TextField(
        blank=True, null=True,
        db_column='proje_detaylari'
    )
    proje_belgesi = models.TextField(
        blank=True, null=True,
        db_column='proje_belgesi'
    )
    gorev_belgesi = models.TextField(
        blank=True, null=True,
        db_column='gorev_belgesi'
    )

    class Meta:
        managed = False
        db_table = 'arastirma_projeleri'


class Atiflar(models.Model):
    atif_turu = models.CharField(
        max_length=2,
        choices=ATIF_TURU_CHOICES,
        db_column='atif_turu'
    )
    eserin_adi_ve_atis_sayisi = models.TextField(
        blank=True,
        null=True,
        db_column='eserin_adi_ve_atis_sayisi'
    )
    pdf_yolu = models.TextField(
        blank=True,
        null=True,
        db_column='pdf_yolu'
    )

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

DURUM_SECENEKLERI = [
        ('Beklemede', 'Beklemede'),
        ('Onaylandı', 'Onaylandı'),
        ('Reddedildi', 'Reddedildi'),
    ]


class Basvuru(models.Model):
    kullanici = models.ForeignKey('Kullanici', models.DO_NOTHING)
    faaliyet_donemi = models.TextField(blank=True, null=True)
    basvurulan_kadro = models.TextField()
    basvuru_tarihi = models.DateField()
    basvuru_aciklam = models.TextField(blank=True, null=True)
    ilan = models.ForeignKey('Ilan', models.DO_NOTHING, blank=True, null=True)
    kisisel_bilgi = models.ForeignKey('KisiselBilgiler', models.DO_NOTHING, blank=True, null=True)
    makaleler = models.ForeignKey('Makale', models.DO_NOTHING, blank=True, null=True)
    kitaplar = models.ForeignKey('Kitap', models.DO_NOTHING, blank=True, null=True)
    idari_gorevler = models.ForeignKey('IdariGorev', models.DO_NOTHING, blank=True, null=True)
    guzel_sanatlar_faaliyetleri = models.ForeignKey('GuzelSanatlarFaaliyeti', models.DO_NOTHING, blank=True, null=True)
    egitim_faaliyetleri = models.ForeignKey('EgitimFaaliyeti', models.DO_NOTHING, blank=True, null=True)
    editorluk = models.ForeignKey('Editorluk', models.DO_NOTHING, blank=True, null=True)
    bilimsel_toplanti_faaliyetleri = models.ForeignKey('BilimselToplantiFaaliyeti', models.DO_NOTHING, blank=True, null=True)
    atiflar = models.ForeignKey(Atiflar, models.DO_NOTHING, blank=True, null=True)
    arastirma_projeleri = models.ForeignKey(ArastirmaProjesi, models.DO_NOTHING, blank=True, null=True)
    tez_yoneticilikleri = models.ForeignKey('TezYonetciligi', models.DO_NOTHING, blank=True, null=True)
    patentler = models.ForeignKey('Patent', models.DO_NOTHING, blank=True, null=True)
    oduller = models.ForeignKey('Odul', models.DO_NOTHING, blank=True, null=True)
    basvuru_pdf = models.BinaryField(blank=True, null=True)

    durum = models.CharField(
    max_length=20,
    choices=[('Beklemede', 'Beklemede'), ('Onaylandı', 'Onaylandı'), ('Reddedildi', 'Reddedildi')],
    default='Beklemede',  # <-- eksik olan burası!
    blank=True,
    null=True
)
    class Meta:
        managed = False
        db_table = 'basvurular'


class BilimselToplantiFaaliyeti(models.Model):
    bilimsel_toplanti_turu = models.CharField(
        max_length=3,
        choices=BILIMSEL_TOPLANTI_SECENEKLERI,
        db_column='bilimsel_toplanti_turu'
    )
    detaylar = models.TextField(
        blank=True,
        null=True,
        db_column='detaylar'
    )
    belge_yolu = models.TextField(
        blank=True,
        null=True,
        db_column='belge_yolu'
    )

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


class EgitimFaaliyeti(models.Model):
    ders_turu = models.CharField(
        max_length=2,
        choices=EGITIM_TURU_CHOICES,
        db_column='ders_turu'
    )
    ders_detaylari = models.TextField(
        blank=True, null=True,
        db_column='ders_detaylari'
    )

    class Meta:
        managed = False
        db_table = 'egitim_faaliyetleri'


class Editorluk(models.Model):
    tur = models.CharField(
        max_length=3,
        choices=EDITORLUK_TURU_CHOICES,
        db_column='tur'
    )
    aciklama = models.TextField(
        blank=True, null=True,
        db_column='aciklama'
    )
    gorev_belge = models.TextField(
        blank=True, null=True,
        db_column='gorev_belge'
    )
    indeks_belge = models.TextField(
        blank=True, null=True,
        db_column='indeks_belge'
    )

    class Meta:
        managed = False
        db_table = 'editorluk'


class GuzelSanatlarFaaliyeti(models.Model):
    faaliyet_turu = models.CharField(
        max_length=4,   # örn. "L100"
        choices=GUZEL_SANATLAR_CHOICES,
        db_column='faaliyet_turu'
    )
    detaylar = models.TextField(
        blank=True, null=True,
        db_column='detaylar'
    )
    dokuman = models.TextField(
        blank=True, null=True,
        db_column='dokuman'
    )

    class Meta:
        managed = False
        db_table = 'guzel_sanatlar_faaliyetleri'


class IdariGorev(models.Model):
    gorev_turu = models.CharField(
        max_length=3,
        choices=IDARI_GOREV_TURU_CHOICES,
        db_column='gorev_turu'
    )
    gorev_birimi_yili = models.TextField(
        blank=True,
        null=True,
        db_column='gorev_birimi_yili'
    )
    belge_yukle = models.TextField(
        blank=True,
        null=True,
        db_column='belge_yukle'
    )
    # eğer idari görevlerin bir kullanıcıyla ilişkisi varsa:
    kullanici = models.ForeignKey(
        'core.Kullanici',          # app_label.ModelName formatında forward ref
        on_delete=models.DO_NOTHING,
        db_column='kullanici_id'
    )

    class Meta:
        managed = False
        db_table = 'idari_gorevler'


class Kullanici(models.Model):
    ROL_SECENEKLERI = [
        ('yönetici', 'Yönetici'),
        ('aday', 'Aday'),
        ('juri', 'Juri'),
        ('admin', 'Admin'),
    ]
    id = models.AutoField(primary_key=True, db_column='id')  # Birincil anahtar eklendi
    tc_kimlik_no    = models.CharField(max_length=11, unique=True, db_column='tc_kimlik_no')
    ad_soyad        = models.TextField(db_column='ad_soyad')
    sifre_hash      = models.TextField(db_column='sifre_hash')
    rol = models.CharField(max_length=20, choices=ROL_SECENEKLERI, db_column='rol')
    olusturma_tarihi= models.DateTimeField(db_column='olusturma_tarihi')
    son_giris       = models.DateTimeField(blank=True, null=True, db_column='son_giris')

    USERNAME_FIELD = 'tc_kimlik_no'  # Kullanıcıyı benzersiz şekilde tanımlayan alan
    REQUIRED_FIELDS = ['rol']  # Superuser oluşturulurken istenecek zorunlu alanlar (tc_kimlik_no zaten USERNAME_FIELD)

    def __str__(self):
        return self.tc_kimlik_no # Veya kullanıcıyı daha anlamlı bir şekilde temsil eden bir alan

    # İsteğe bağlı olarak gerekli olabilecek diğer metotlar:
    def is_active(self):
        return True

    def is_staff(self):
        return False

    def is_superuser(self):
        return False

    def get_full_name(self):
        return self.tc_kimlik_no # Veya kullanıcının tam adını döndürebilirsiniz

    def get_short_name(self):
        return self.tc_kimlik_no # Veya kullanıcının kısa adını döndürebilirsiniz

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    class Meta:
        managed = False
        db_table = 'kullanicilar'


class Ilan(models.Model):
    ilanid = models.AutoField(db_column='ilanID', primary_key=True)  # Field name made lowercase.
    bolum = models.TextField()
    pozisyon = models.TextField()
    aciklama = models.TextField()
    basl_tarih = models.DateField()
    bitis_tarih = models.DateField()
    kadro_sayi = models.IntegerField()
    basvuru_sayisi = models.IntegerField(blank=True, null=True)
    bilgilendirme_dosya = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ilan'



class JuriDegerlendirme(models.Model):
    juridegerlendirmeid = models.AutoField(primary_key=True, db_column='juriDegerlendirmeID')
    juriid = models.ForeignKey('core.JuriAdaylari', on_delete=models.CASCADE)
    kullanici = models.ForeignKey('Kullanici', on_delete=models.DO_NOTHING, db_column='kullanici_id', blank=True, null=True)
    basvuruid = models.ForeignKey('Basvuru', on_delete=models.DO_NOTHING, db_column='basvuruID')

    juri_raporu = models.FileField(upload_to='juri_raporlari/', blank=True, null=True)

    onay_durumu = models.CharField(
        max_length=20,
        choices=[
            ('beklemede', 'Beklemede'),
            ('onaylandi', 'Onaylandı'),
            ('reddedildi', 'Reddedildi')
        ],
        default='beklemede',
        blank=True,
        null=True
    )

    class Meta:
        managed = True
        db_table = 'juri_degerlendirme'

    def __str__(self):
        return f"Değerlendirme #{self.juridegerlendirmeid} - Başvuru {self.basvuruid_id}"

class KisiselBilgiler(models.Model):
    id = models.AutoField(
        primary_key=True,
        db_column='id'
    )
    kullanici = models.ForeignKey(
        'Kullanici',
        on_delete=models.DO_NOTHING,
        db_column='kullanici_id'
    )
    ad_soyad = models.TextField(
        db_column='ad_soyad'
    )
    tc_kimlik_no = models.CharField(
        max_length=11,
        unique=True,
        db_column='tc_kimlik_no'
    )
    dogum_tarihi = models.DateField(
        db_column='dogum_tarihi'
    )
    email = models.TextField(
        db_column='email'
    )
    adres = models.TextField(
        db_column='adres'
    )
    akademik_unvan = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        db_column='akademik_unvan'
    )

    class Meta:
        managed = False
        db_table = 'kisisel_bilgiler'
        verbose_name = 'Kişisel Bilgi'
        verbose_name_plural = 'Kişisel Bilgiler'

    def __str__(self):
        return self.ad_soyad
    

class Kitap(models.Model):
    kitap_turu = models.TextField()  # This field type is a guess.
    kitap_detaylari = models.TextField(blank=True, null=True)
    kapak_ve_icindekiler_pdf = models.TextField(blank=True, null=True)
    yayin_taninirlik_pdf = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kitaplar'




class Makale (models.Model):
    makale_turu = models.CharField(
        max_length=17,  # en uzun anahtar "ULAKBIM_TR_ULUSAL" uzunluğu kadar
        choices=MAKALE_TURU_CHOICES,
        db_column='makale_turu'
    )
    yazarlar_dergi_bilgi = models.TextField(
        blank=True, null=True,
        db_column='yazarlar_dergi_bilgi'
    )
    pdf_yolu = models.TextField(
        blank=True, null=True,
        db_column='pdf_yolu'
    )

    class Meta:
        managed = False
        db_table = 'makaleler'

class Odul(models.Model):
    tur = models.CharField(
        max_length=3,
        choices=ODUL_TURU_CHOICES,
        db_column='tur'
    )
    aciklama = models.TextField(
        blank=True, null=True,
        db_column='aciklama'
    )
    belge_pdf = models.TextField(
        blank=True, null=True,
        db_column='belge_pdf'
    )

    class Meta:
        managed = False
        db_table = 'oduller'


class TezYonetciligi(models.Model):
    tez_turu = models.CharField(
        max_length=2,
        choices=TEZ_TURU_CHOICES,
        db_column='tez_turu'
    )
    tez_detaylari = models.TextField(
        db_column='tez_detaylari'
    )
    tez_belgesi_pdf = models.TextField(
        db_column='tez_belgesi_pdf'
    )

    class Meta:
        managed = False
        db_table = 'tez_yoneticilikleri'


class Patent(models.Model):
    patent_turu = models.CharField(
        max_length=2,
        choices=PATENT_TURU_CHOICES,
        db_column='patent_turu'
    )
    patent_detaylari = models.TextField(
        db_column='patent_detaylari'
    )
    patent_belgesi_pdf = models.TextField(
        db_column='patent_belgesi_pdf'
    )

    class Meta:
        managed = False
        db_table = 'patentler'


class Yoneticii(models.Model):
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



