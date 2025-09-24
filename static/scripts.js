let currentUrl = window.location.href;
let urlParts = currentUrl.split('/');
let currentChapter = parseInt(urlParts[urlParts.length - 1]);

const select = document.getElementById("list");

for (let i = 1; i <= 2334; i++) {
    let option = document.createElement("option");
    option.value = i;
    option.textContent = "Chapter " + i;
    if (i === currentChapter) {
        option.selected = true;
    }
    select.appendChild(option);
}

select.addEventListener("change", function() {
    const selectedChapter = select.value;
    if (selectedChapter != currentChapter) {
        urlParts[urlParts.length - 1] = selectedChapter;
        window.location.href = urlParts.join('/');
    }
});

document.getElementById("prevChapter").addEventListener("click", function() {
    let currentUrl = window.location.href;
    let urlParts = currentUrl.split('/');

    let currentChapter = parseInt(urlParts[urlParts.length - 1]);

    let prevChapter = currentChapter - 1;
    urlParts[urlParts.length - 1] = prevChapter;
    let newUrl = urlParts.join('/');
    window.location.href = newUrl;
});
document.getElementById("nextChapter").addEventListener("click", function() {
    let currentUrl = window.location.href;
    let urlParts = currentUrl.split('/');

    let currentChapter = parseInt(urlParts[urlParts.length - 1]);

    let nextChapter = currentChapter + 1;
    urlParts[urlParts.length - 1] = nextChapter;
    let newUrl = urlParts.join('/');
    window.location.href = newUrl;
});
function LightDark() {
  var element = document.body;
  element.classList.toggle("dark-mode");
}
    let defaultOption = document.getElementById('defaultoption');
    defaultOption.textContent = `Chapter ${currentChapter}`;
    defaultOption.value = currentChapter;
