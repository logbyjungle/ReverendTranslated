let currentUrl = window.location.href;
let urlParts = currentUrl.split('/');
let currentChapter = parseInt(urlParts[urlParts.length - 1]);

const prevButton = document.getElementById("prevChapter");
const nextButton = document.getElementById("nextChapter");

if (currentChapter === 1) {
    prevButton.style.display = "none";
}

if (currentChapter === 2334) {
    nextButton.style.display = "none";
}


const prevButtonBottom = document.getElementById("prevChapterBottom");
const nextButtonBottom = document.getElementById("nextChapterBottom");

if (currentChapter === 1) {
    prevButtonBottom.style.display = "none";
}

if (currentChapter === 2334) {
    nextButtonBottom.style.display = "none";
}

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

const selectbottom = document.getElementById("listbottom");

for (let i = 1; i <= 2334; i++) {
    let option = document.createElement("option");
    option.value = i;
    option.textContent = "Chapter " + i;
    if (i === currentChapter) {
        option.selected = true;
    }
    selectbottom.appendChild(option);
}

selectbottom.addEventListener("change", function() {
    const selectedChapter = selectbottom.value;
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

document.getElementById("prevChapterBottom").addEventListener("click", function() {
    let currentUrl = window.location.href;
    let urlParts = currentUrl.split('/');

    let currentChapter = parseInt(urlParts[urlParts.length - 1]);

    let prevChapter = currentChapter - 1;
    urlParts[urlParts.length - 1] = prevChapter;
    let newUrl = urlParts.join('/');
    window.location.href = newUrl;
});
document.getElementById("nextChapterBottom").addEventListener("click", function() {
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
