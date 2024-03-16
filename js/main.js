console.log("main.js loaded!");
const themeButton = document.getElementById("themeButton");
const lightModeLink = document.getElementById("lightTheme");
const darkModeLink = document.getElementById("darkTheme");

// Check localStorage for the theme and set the initial text accordingly.
if (localStorage.getItem("theme") === "dark") {
    lightModeLink.disabled = true;
    darkModeLink.removeAttribute("disabled");
    themeButton.innerHTML = "Light Mode";
} else {
    lightModeLink.removeAttribute("disabled");
    darkModeLink.disabled = true;
    themeButton.innerHTML = "Dark Mode";
    localStorage.setItem("theme", "light");
}

themeButton.addEventListener("click", function () {
    if (lightModeLink.disabled) {
        lightModeLink.removeAttribute("disabled");
        darkModeLink.disabled = true;
        localStorage.setItem("theme", "light");
        themeButton.innerHTML = "Dark Mode";
    } else {
        lightModeLink.disabled = true;
        darkModeLink.removeAttribute("disabled");
        localStorage.setItem("theme", "dark");
        themeButton.innerHTML = "Light Mode";
    }
});
