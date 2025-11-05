$(document).ready(function () {
    $('#lang').selectize({
        sortField: 'text'
    });
});

const currentUrl = globalThis.location.href;
const urlParts = currentUrl.split('/');
const currentChapter = parseInt(urlParts[urlParts.length - 1]);

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
    const option = document.createElement("option");
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
        globalThis.location.href = urlParts.join('/');
    }
});

const selectbottom = document.getElementById("listbottom");

for (let i = 1; i <= 2334; i++) {
    const option = document.createElement("option");
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
        globalThis.location.href = urlParts.join('/');
    }
});

document.getElementById("prevChapter").addEventListener("click", function() {
    const currentUrl = globalThis.location.href;
    const urlParts = currentUrl.split('/');

    const currentChapter = parseInt(urlParts[urlParts.length - 1]);

    const prevChapter = currentChapter - 1;
    urlParts[urlParts.length - 1] = prevChapter;
    const newUrl = urlParts.join('/');
    globalThis.location.href = newUrl;
});
document.getElementById("nextChapter").addEventListener("click", function() {
    const currentUrl = globalThis.location.href;
    const urlParts = currentUrl.split('/');

    const currentChapter = parseInt(urlParts[urlParts.length - 1]);

    const nextChapter = currentChapter + 1;
    urlParts[urlParts.length - 1] = nextChapter;
    const newUrl = urlParts.join('/');
    globalThis.location.href = newUrl;
});

document.getElementById("prevChapterBottom").addEventListener("click", function() {
    const currentUrl = globalThis.location.href;
    const urlParts = currentUrl.split('/');

    const currentChapter = parseInt(urlParts[urlParts.length - 1]);

    const prevChapter = currentChapter - 1;
    urlParts[urlParts.length - 1] = prevChapter;
    const newUrl = urlParts.join('/');
    globalThis.location.href = newUrl;
});
document.getElementById("nextChapterBottom").addEventListener("click", function() {
    const currentUrl = globalThis.location.href;
    const urlParts = currentUrl.split('/');

    const currentChapter = parseInt(urlParts[urlParts.length - 1]);

    const nextChapter = currentChapter + 1;
    urlParts[urlParts.length - 1] = nextChapter;
    const newUrl = urlParts.join('/');
    globalThis.location.href = newUrl;
});

function LightDark() {
    const element = document.body;
    element.classList.toggle("dark-mode");

    if (element.classList.contains("dark-mode")) {
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }
}

function changeFont(font) {
    document.body.style.fontFamily = font;
    localStorage.setItem("fontFamily", font);
}

function changeFontSize(size) {
    document.querySelectorAll('.content').forEach(el => {
        el.style.fontSize = size;
        localStorage.setItem("fontSize", size);
    });
}

async function streamContent() {
    const contentDiv = document.getElementById('content');

    const pathParts = globalThis.location.pathname.split('/').filter(Boolean);
    const [lang, chapter] = pathParts;

    if (!lang || !chapter) {
        console.error("Cannot determine lang or chapter from URL.");
        return;
    }

    const response = await fetch(`/api/${lang}/${chapter}`);
    
    if (!response.body) {
        console.error("Streaming not supported by this response.");
        return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        const lines = buffer.split('\n');
        buffer = lines.pop();

        lines.forEach(line => {
            if (line.trim()) {
                const p = document.createElement('p');
                p.textContent = line;
                contentDiv.appendChild(p);
            }
        });

        contentDiv.scrollTop = contentDiv.scrollHeight;
    }

    if (buffer.trim()) {
        const p = document.createElement('p');
        p.textContent = buffer;
        contentDiv.appendChild(p);
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
        document.body.classList.add("dark-mode");
    }
    const savedFont = localStorage.getItem("fontFamily");
    if (savedFont) {
        document.body.style.fontFamily = savedFont;
        const fontSelector = document.getElementById('fontSelector');
        if (fontSelector) fontSelector.value = savedFont;
    }
    const savedFontSize = localStorage.getItem("fontSize");
    if (savedFontSize) {
        document.querySelectorAll('.content').forEach(el => {
            el.style.fontSize = savedFontSize;
        });
        const fontSizeSelector = document.getElementById('fontSizeSelector');
        if (fontSizeSelector) fontSizeSelector.value = savedFontSize;
    }
    streamContent();
});

const defaultOptionTop = document.getElementById('defaultoptiontop');
defaultOptionTop.textContent = `Chapter ${currentChapter}`;
defaultOptionTop.value = currentChapter;

const defaultOptionBottom = document.getElementById('defaultoptionbottom');
defaultOptionBottom.textContent = `Chapter ${currentChapter}`;
defaultOptionBottom.value = currentChapter;

function redirectToPage() {
    const select = document.getElementById('lang');
    const value = select.value;
    if (value) {
        globalThis.location.href = `/${value}/1`;
    }
}
