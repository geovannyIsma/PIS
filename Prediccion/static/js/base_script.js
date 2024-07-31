const body = document.querySelector('body'),
    sidebar = body.querySelector('nav'),
    toggle = body.querySelector(".toggle"),
    modeSwitch = body.querySelector(".toggle-switch"),
    modeText = body.querySelector(".mode-text");

toggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
});

// Obtén el modo guardado en localStorage
const savedMode = localStorage.getItem('dark-mode');

if (savedMode === 'enabled') {
    body.classList.add('dark');
    modeText.innerText = "Modo Claro";
} else {
    modeText.innerText = "Modo Oscuro";
}

modeSwitch.addEventListener("click", () => {
    body.classList.toggle("dark");

    if (body.classList.contains("dark")) {
        localStorage.setItem('dark-mode', 'enabled');
        modeText.innerText = "Modo Claro";
    } else {
        localStorage.setItem('dark-mode', 'disabled');
        modeText.innerText = "Modo Oscuro";
    }
});