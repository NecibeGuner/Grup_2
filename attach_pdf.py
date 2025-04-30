from django.core.files import File
from core.models import Basvuru

b = Basvuru.objects.get(id=1)
with open(r"C:\Users\Tugce\Desktop\Android-OS.pdf", "rb") as f:
    b.basvuru_pdf.save("Android-OS.pdf", File(f), save=True)
print("PDF başarıyla yüklendi.")
