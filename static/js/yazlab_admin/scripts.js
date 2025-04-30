/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

    document.getElementById("ilanFormu").addEventListener("submit", function(event) {
        let files = document.getElementById("bilgiBelgeleri").files;
        for (let i = 0; i < files.length; i++) {
            if (files[i].type !== "application/pdf") {
                alert("Yalnızca PDF dosyaları yükleyebilirsiniz.");
                event.preventDefault();
                return;
            }
        }
    });
    document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll(".edit-btn, .save-btn, .delete-btn").forEach(button => {
            button.addEventListener("click", function () {
                if (!confirm("Emin misiniz?")) {
                    event.preventDefault();
                }
            });
        });
    });
    

});
