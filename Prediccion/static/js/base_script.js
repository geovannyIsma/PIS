document.addEventListener("DOMContentLoaded", function() {
    var sidebarToggle = document.querySelector(".toggle-btn");
    var sidebar = document.querySelector("#sidebar");
    var main = document.querySelector(".main");

    sidebarToggle.addEventListener("click", function() {
        sidebar.classList.toggle("expand");

        if (sidebar.classList.contains("expand")) {
            main.style.marginLeft = '330px';  /* Cambiado a 300px */
            main.style.width = 'calc(100% - 330px)';  /* Cambiado a 300px */
        } else {
            main.style.marginLeft = '70px';
            main.style.width = 'calc(100% - 70px)';
        }
    });
});
