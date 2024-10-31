document.addEventListener("DOMContentLoaded", function() {
    const toggleButton = document.getElementById("toggle-theme");
    const themeIcon = document.getElementById("theme-icon");

    const currentTheme = localStorage.getItem("theme") || "dark";
    document.body.className = currentTheme;
    themeIcon.innerText = currentTheme === "dark" ? "🌙" : "☀️";

    if (toggleButton) {
        toggleButton.addEventListener("click", function() {
            const newTheme = document.body.className === "dark" ? "light" : "dark";
            document.body.className = newTheme;
            localStorage.setItem("theme", newTheme);
            themeIcon.innerText = newTheme === "dark" ? "🌙" : "☀️";
        });
    }
});