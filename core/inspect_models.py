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

class Makale(models.Model):
    basvuru               = models.ForeignKey(
                                'Basvuru',
                                on_delete=models.CASCADE,
                                related_name='makaleler',
                                db_column='makaleler_id'
                            )
    makale_turu_enum      = models.CharField(
                                max_length=30,
                                choices=MAKALE_TURU_CHOICES,
                                db_column='makale_turu'
                            )
    yazarlar_dergi_bilgi  = models.TextField(db_column='yazarlar_dergi_bilgi')
    pdf_yolu              = models.FileField(
                                upload_to='makaleler/',
                                db_column='pdf_yolu'
                            )

    class Meta:
        db_table = 'makaleler'

    def __str__(self):
        return f"{self.get_makale_turu_enum_display()} — {self.yazarlar_dergi_bilgi[:30]}…"
    
class Odul(models.Model):
    basvuru         = models.ForeignKey(
                          'Basvuru',
                          on_delete=models.CASCADE,
                          related_name='oduller'
                      )
    odul_turu_enum  = models.CharField(
                          max_length=3,
                          choices=ODUL_TURU_CHOICES,
                          db_column='odul_turu_enum'
                      )
    aciklama        = models.TextField(db_column='aciklama')
    belge_pdf       = models.FileField(
                          upload_to='oduller/',
                          db_column='belge_pdf'
                      )

    class Meta:
        db_table = 'oduller'

    def __str__(self):
        return f"{self.basvuru.id} – {self.get_odul_turu_enum_display()}"
class IdariGorev(models.Model):
    basvuru             = models.ForeignKey(
                              'Basvuru',
                              on_delete=models.CASCADE,
                              related_name='idari_gorevler'
                          )
    gorev_turu_enum     = models.CharField(
                              max_length=3,
                              choices=IDARI_GOREV_TURU_CHOICES,
                              db_column='gorev_turu_enum'
                          )
    gorev_birimi_yili   = models.TextField(db_column='gorev_birimi_yili')
    belge_yukle         = models.FileField(
                              upload_to='idari_gorevler/',
                              db_column='belge_yukle'
                          )

    class Meta:
        db_table = 'idari_gorevler'

    def __str__(self):
        return f"{self.basvuru.id} – {self.get_gorev_turu_enum_display()}"

class Editorluk(models.Model):
    basvuru             = models.ForeignKey(
                              'Basvuru',
                              on_delete=models.CASCADE,
                              related_name='editorluk_faaliyetleri'
                          )
    tur_editorluk_turu_enum = models.CharField(
                              max_length=3,
                              choices=EDITORLUK_TURU_CHOICES,
                              db_column='tur_editorluk_turu_enum'
                          )
    aciklama            = models.TextField(db_column='aciklama')
    gorev_belge         = models.FileField(
                              upload_to='editorluk_gorev_belgeleri/',
                              db_column='gorev_belge'
                          )
    indeks_belge        = models.FileField(
                              upload_to='editorluk_indeks_belgeleri/',
                              db_column='indeks_belge'
                          )

    class Meta:
        db_table = 'editorluk'

    def __str__(self):
        return f"{self.basvuru.id} – {self.tur_editorluk_turu_enum}"
    
class ArastirmaProjesi(models.Model):
    basvuru          = models.ForeignKey(
                           'Basvuru',
                           on_delete=models.CASCADE,
                           related_name='arastirma_projeleri'
                       )
    proje_turu_enum  = models.CharField(
                           max_length=3,
                           choices=ARASTIRMA_PROJE_TURU_CHOICES,
                           db_column='proje_turu_enum'
                       )
    proje_detaylari  = models.TextField(db_column='proje_detaylari')
    proje_belgesi    = models.FileField(upload_to='proje_belgeleri/', db_column='proje_belgesi')
    gorev_belgesi    = models.FileField(upload_to='gorev_belgeleri/', db_column='gorev_belgesi')

    class Meta:
        db_table = 'arastirma_projeleri'

    def __str__(self):
        return f"{self.basvuru.pk} – {self.proje_turu_enum}"
    
class TezYonetciligi(models.Model):
    basvuru           = models.ForeignKey(
                            'Basvuru',
                            on_delete=models.CASCADE,
                            related_name='tez_yonetcilikleri'
                        )
    tez_turu_enum     = models.CharField(
                            max_length=2,
                            choices=TEZ_TURU_CHOICES,
                            db_column='tez_turu_enum'
                        )
    tez_detaylari     = models.TextField(db_column='tez_detaylari')
    tez_belgesi_pdf   = models.FileField(
                            upload_to='tez_yonetcilikleri/',
                            db_column='tez_belgesi_pdf'
                        )

    class Meta:
        db_table = 'tez_yonetcilikleri'

    def __str__(self):
        return f"{self.basvuru.id} – {self.get_tez_turu_enum_display()}"

class Patent(models.Model):
    basvuru             = models.ForeignKey(
                              'Basvuru',
                              on_delete=models.CASCADE,
                              related_name='patentler'
                          )
    patent_turu_enum    = models.CharField(
                              max_length=2,
                              choices=PATENT_TURU_CHOICES,
                              db_column='patent_turu_enum'
                          )
    patent_detaylari    = models.TextField(db_column='patent_detaylari')
    patent_belgesi_pdf  = models.FileField(
                              upload_to='patentler/',
                              db_column='patent_belgesi_pdf'
                          )

    class Meta:
        db_table = 'patentler'

    def __str__(self):
        return f"{self.basvuru.id} – {self.get_patent_turu_enum_display()}"

class Atif(models.Model):
    basvuru                   = models.ForeignKey(
                                    'Basvuru',
                                    on_delete=models.CASCADE,
                                    related_name='atiflar'
                                )
    atif_turu                 = models.CharField(
                                    max_length=3,
                                    choices=ATIF_TURU_CHOICES,
                                    db_column='atif_turu'
                                )
    eserin_adi_ve_atis_sayisi = models.TextField(db_column='eserin_adi_ve_atis_sayisi')
    pdf_yolu                  = models.FileField(
                                    upload_to='atif_belgeleri/',
                                    db_column='pdf_yolu'
                                )

    class Meta:
        db_table = 'atiflar'

    def __str__(self):
        return f"{self.basvuru.id} – {self.atif_turu}"
    

class EgitimFaaliyeti(models.Model):
    basvuru         = models.ForeignKey(
                          'Basvuru',
                          on_delete=models.CASCADE,
                          related_name='egitim_faaliyetleri'
                      )
    ders_turu       = models.CharField(
                          max_length=2,
                          choices=EGITIM_TURU_CHOICES,
                          db_column='ders_turu'
                      )
    ders_detaylari  = models.TextField(db_column='ders_detaylari')

    class Meta:
        db_table = 'egitim_faaliyetleri'

    def __str__(self):
        return f"{self.basvuru.id} – {self.get_ders_turu_display()}"
# ---------------------------------
# 1) Kullanıcı (kullanicilar tablosu)
# ---------------------------------
class Kullanici(models.Model):
    id               = models.AutoField(primary_key=True)
    tc_kimlik_no     = models.CharField(max_length=11, unique=True)
    ad_soyad         = models.TextField()
    sifre_hash       = models.TextField(default='password123')
    rol              = models.CharField(max_length=20, choices=ROL_SECENEKLERI)
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
    tc_kimlik_no   = models.CharField(max_length=11, db_column='tc_kimlik_no')
    dogum_tarihi   = models.DateField(null=True, blank=True, db_column='dogum_tarihi')
    email          = models.TextField(null=True, blank=True, db_column='email')
    adres          = models.TextField(null=True, blank=True, db_column='adres')
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

class Basvuru(models.Model):
    id               = models.AutoField(primary_key=True)
    kullanici        = models.ForeignKey(
                          settings.AUTH_USER_MODEL,
                          on_delete=models.CASCADE,
                          db_column='kullanici_id'
                      )
    kisisel_bilgi    = models.ForeignKey(
                          'KisiselBilgiler',
                          on_delete=models.CASCADE,
                          db_column='kisisel_bilgi_id'
                      )
    ilan             = models.ForeignKey(
                          'Ilan',
                          on_delete=models.CASCADE,
                          db_column='ilan_id'
                      )
    faaliyet_donemi  = models.TextField(db_column='faaliyet_donemi')
    basvurulan_kadro = models.TextField(db_column='basvurulan_kadro')
    basvuru_tarihi   = models.DateField(db_column='basvuru_tarihi')
    basvuru_aciklam  = models.TextField(db_column='basvuru_aciklam')
    basvuru_pdf      = models.BinaryField(
                          null=True, blank=True,
                          db_column='basvuru_pdf'
                      )

    class Meta:
        db_table = 'basvurular'

    def __str__(self):
        return f"Başvuru #{self.id} — {self.kullanici}"
    
    # — Alt tabloların FK alanları —
    makale = models.ForeignKey(
        'Basvuru',
        on_delete=models.CASCADE,
        db_column='makaleler_id',
        null=True,
        blank=True,
        related_name='basvuru_makale'
    )
    kitap = models.ForeignKey(
        'Basvuru',
        on_delete=models.CASCADE,
        db_column='kitaplar_id',
        null=True,
        blank=True,
        related_name='basvuru_kitap'
    )
    idari_gorev = models.ForeignKey(
        'Basvuru',
        on_delete=models.CASCADE,
        db_column='idari_gorevler_id',
        null=True,
        blank=True,
        related_name='basvuru_idari'
    )
    guzel_sanat = models.ForeignKey(
        'Basvuru',
        on_delete=models.CASCADE,
        db_column='guzel_sanatlar_faaliyetleri_id',
        null=True,
        blank=True,
        related_name='basvuru_guzel_sanat'
    )
    egitim_faaliyet = models.ForeignKey(
        'Basvuru',
        on_delete=models.CASCADE,
        db_column='egitim_faaliyetleri_id',
        null=True,
        blank=True,
        related_name='basvuru_egitim'
    )
    editorluk = models.ForeignKey(
        'Basvuru',
        on_delete=models.CASCADE,
        db_column='editorluk_id',
        null=True,
        blank=True,
        related_name='basvuru_editorluk'
    )
    bilimsel_toplanti = models.ForeignKey(
        'Basvuru',
        on_delete=models.CASCADE,
        db_column='bilimsel_toplanti_faaliyetleri_id',
        null=True,
        blank=True,
        related_name='basvuru_toplanti'
    )
    atif = models.ForeignKey(
        'Basvuru',
        on_delete=models.CASCADE,
        db_column='atiflar_id',
        null=True,
        blank=True,
        related_name='basvuru_atif'
    )
    arastirma_projesi = models.ForeignKey(
        'Basvuru',
        on_delete=models.CASCADE,
        db_column='arastirma_projeleri_id',
        null=True,
        blank=True,
        related_name='basvuru_arastirma'
    )
    tez_yoneticilik = models.ForeignKey(
        'Basvuru',   # Burayı sınıf adıyla birebir eşle
        on_delete=models.CASCADE,
        db_column='tez_yoneticilikleri_id',  # sizin veritabanınızdaki kolon adı
        null=True,
        blank=True,
        related_name='basvuru_tez_yoneticilikleri'
    )
    patent = models.ForeignKey(
        'Basvuru',
        on_delete=models.CASCADE,
        db_column='patentler_id',
        null=True,
        blank=True,
        related_name='basvuru_patent'
    )
    odul = models.ForeignKey(
        'Basvuru',
        on_delete=models.CASCADE,
        db_column='oduller_id',
        null=True,
        blank=True,
        related_name='basvuru_odul'
    )

    # — Diğer alanlar —
    faaliyet_donemi  = models.TextField(null=True, blank=True)
    basvurulan_kadro = models.TextField()
    basvuru_aciklam  = models.TextField(null=True, blank=True)
    basvuru_tarihi   = models.DateField()

    class Meta:
        db_table = 'basvurular'

    basvuru_pdf = models.BinaryField(
        verbose_name="Başvuru Onay PDF’i",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Başvuru #{self.pk} – {self.kullanici}"
    
    # ---------------------------------
# 4) Bilimsel Toplantı Faaliyetleri
# ---------------------------------
class BilimselToplantiFaaliyeti(models.Model):
    basvuru = models.ForeignKey(
        'Basvuru',
        on_delete=models.CASCADE,
        related_name='toplanti_faaliyetleri'
    )
    bilimsel_toplanti_turu_enum = models.CharField(
        max_length=4,
        choices=BILIMSEL_TOPLANTI_SECENEKLERI,
        db_column='bilimsel_toplanti_turu_enum'
    )
    detaylar = models.TextField(db_column='detaylar')
    belge_yolu = models.FileField(
        upload_to='toplanti_belgeleri/',
        db_column='belge_yolu',
        null=True, blank=True
    )

    class Meta:
        db_table = 'bilimsel_toplanti_faaliyetleri'

    def __str__(self):
        return f"{self.basvuru.id} – {self.bilimsel_toplanti_turu_enum}"





class Admin(models.Model):
    adminid = models.AutoField(db_column='adminID', primary_key=True)  # Field name made lowercase.
    tc = models.CharField(unique=True, max_length=11)
    sifre = models.TextField()

    class Meta:
        managed = False
        db_table = 'admin'




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

class TezYoneticilikleri(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    tez_turu = models.TextField(db_column='tez_turu')
    tez_detaylari = models.TextField(db_column='tez_detaylari')
    tez_belgesi_pdf = models.TextField(db_column='tez_belgesi_pdf')

    class Meta:
        managed = False
        db_table = 'tez_yoneticilikleri'


# --- İlan ---
class Ilan(models.Model):
    ilanID = models.AutoField(primary_key=True, db_column='ilanID')
    bolum = models.TextField(db_column='bolum')
    pozisyon = models.TextField(db_column='pozisyon')
    aciklama = models.TextField(db_column='aciklama')
    basl_tarih = models.DateField(db_column='basl_tarih')
    bitis_tarih = models.DateField(db_column='bitis_tarih')
    kadro_sayi = models.IntegerField(db_column='kadro_sayi')
    basvuru_sayisi = models.IntegerField(db_column='basvuru_sayisi', null=True, blank=True)
    bilgilendirme_dosya = models.BinaryField(db_column='bilgilendirme_dosya', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'ilan'


# --- Jüri Adayları ---
class JuriAdaylari(models.Model):
    juriID = models.AutoField(primary_key=True, db_column='juriID')
    isim = models.TextField(db_column='isim')
    soyisim = models.TextField(db_column='soyisim')
    unvan = models.TextField(db_column='unvan')
    kullanici_rolu = models.TextField(db_column='kullanici_rolu')
    ilan = models.ForeignKey(
        Ilan,
        models.DO_NOTHING,
        db_column='ilanID',
        null=True,
        blank=True,
        related_name='juri_adaylari'
    )
    tc = models.CharField(db_column='tc', max_length=11, unique=True)

    class Meta:
        managed = False
        db_table = 'juri_adaylari'


# --- Jüri Değerlendirme ---
class JuriDegerlendirme(models.Model):
    juriDegerlendirmeID = models.AutoField(
        primary_key=True,
        db_column='juriDegerlendirmeID'
    )
    # Burada juriID, JuriAdaylari tablosuna bakmalıydı
    juri = models.ForeignKey(
        JuriAdaylari,
        models.DO_NOTHING,
        db_column='juriID',
        null=True,
        blank=True,
        related_name='degerlendirmeleri'
    )
    # basvuruID zaten sizin Basvuru tablonuz varsa o modele bakacak şekilde ayarlayın
    basvuru = models.ForeignKey(
        'Basvuru',               # kendi Basvuru modelinizin adı
        models.CASCADE,
        db_column='basvuruID',
        null=True,
        blank=True,
        related_name='juri_degerlendirmeleri'
    )
    # text[] tipli alanlar için ArrayField
    juri_raporu = ArrayField(
        models.TextField(),
        db_column='juri_raporu',
        null=True,
        blank=True
    )
    onay_durumu = models.TextField(
        db_column='onay_durumu',
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'juri_degerlendirme'


# --- İdari Görevler ---
class IdariGorevler(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    gorev_turu = models.TextField(db_column='gorev_turu')
    gorev_birimi_yili = models.TextField(db_column='gorev_birimi_yili')
    belge_yukle = models.TextField(db_column='belge_yukle')

    class Meta:
        managed = False
        db_table = 'idari_gorevler'


# --- Kitaplar ---
class Kitaplar(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    kitap_turu = models.TextField(db_column='kitap_turu')
    kitap_detaylari = models.TextField(db_column='kitap_detaylari', null=True, blank=True)
    kapak_ve_icindekiler_pdf = models.TextField(db_column='kapak_ve_icindekiler_pdf', null=True, blank=True)
    yayin_taninirlik_pdf = models.TextField(db_column='yayin_taninirlik_pdf', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'kitaplar'


# --- Makaleler ---
class Makaleler(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    makale_turu = models.TextField(db_column='makale_turu')
    yazarlar_dergi_bilgi = models.TextField(db_column='yazarlar_dergi_bilgi', null=True, blank=True)
    pdf_yolu = models.TextField(db_column='pdf_yolu', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'makaleler'


# --- Ödüller ---
class Oduller(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    tur = models.TextField(db_column='tur')
    aciklama = models.TextField(db_column='aciklama', null=True, blank=True)
    belge_pdf = ArrayField(
        models.TextField(),
        db_column='belge_pdf',
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'oduller'


# --- Patentler ---
class Patentler(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    patent_turu = models.TextField(db_column='patent_turu')
    patent_detaylari = models.TextField(db_column='patent_detaylari')
    patent_belgesi_pdf = models.TextField(db_column='patent_belgesi_pdf')

    class Meta:
        managed = False
        db_table = 'patentler'

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

