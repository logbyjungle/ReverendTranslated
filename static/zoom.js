function detectZoom() {
    return window.devicePixelRatio || 1;
}

function scaleContainer() {
    const zoom = detectZoom(); // e.g. 1.25 for 125% zoom
    const container = document.getElementById('content');
    container.style.transform = `scale(${zoom})`;
}

window.addEventListener('resize', scaleContainer);
window.addEventListener('load', scaleContainer);
