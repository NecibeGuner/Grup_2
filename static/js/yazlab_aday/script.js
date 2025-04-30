function showLoginForm(role) {
    const formTitles = {
        "aday": "Aday Girişi",
        "admin": "Admin Girişi",
        "juri": "Jüri Girişi",
        "yonetici": "Yönetici Girişi"
    };

    // Başlık değiştir
    document.getElementById("form-title").textContent = formTitles[role] || "Giriş Yap";

    // Formu göster
    document.getElementById("login-form").style.display = "block";
}
document.addEventListener("DOMContentLoaded", function () {
    const accordionHeaders = document.querySelectorAll(".accordion-header");

    accordionHeaders.forEach(header => {
        header.addEventListener("click", function () {
            // İçeriği aç/kapat
            const content = this.nextElementSibling;
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
        });
    });
});
function showNewForm(show) {
    const form = document.getElementById("new-article-form");
    if (show) {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}
function filterJobs(category) {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        if (category === 'all') {
            card.style.display = 'block';
        } else {
            card.style.display = card.classList.contains(category) ? 'block' : 'none';
        }
    });
}

//

// İlanları filtreleme fonksiyonu
function filterJobs(category) {
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        if (category === 'all') {
            card.style.display = 'block';
        } else {
            card.style.display = card.classList.contains(category) ? 'block' : 'none';
        }
    });
}

// Başvur butonuna tıklanınca modal gösterme işlemi
document.addEventListener('DOMContentLoaded', () => {
    const applyButtons = document.querySelectorAll('.btn-apply');
    const modal = document.getElementById('apply-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');
    const modalClose = document.getElementById('modal-close');

    applyButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const card = e.target.closest('.card');
            const title = card.querySelector('.card-header').textContent;
            const description = card.querySelector('p').textContent;

            modalTitle.textContent = title;
            modalBody.textContent = description + '\n\nLütfen gerekli belgeleri PDF formatında sisteme yükleyiniz. Başvurunuz değerlendirilmeye alınacaktır.';

            modal.style.display = 'block';
        });
    });

    // Modal kapatma (X tuşu)
    modalClose.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Modal dışına tıklanınca da kapansın
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
});
document.addEventListener("DOMContentLoaded", function () {
    // Modal içindeki başvur butonunu bul
    const modalApplyButton = document.querySelector("#apply-modal .btn-apply");

    // Butona tıklanınca yeni sekmede formu aç
    modalApplyButton.addEventListener("click", function () {
        window.open("basvuruform.html", "_blank"); // düz HTML ortamında URL'yi "/basvuruform" yerine dosya olarak kullan
    });
});