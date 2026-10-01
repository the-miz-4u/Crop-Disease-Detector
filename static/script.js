// --- 1. Service Worker Registration (For PWA) ---
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(reg => console.log('Service Worker Registered'))
            .catch(err => console.log('SW Registration failed: ', err));
    });
}

// --- 2. PWA Install Logic ---
let deferredPrompt;
const installBtn = document.getElementById('installBtn');

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    installBtn.classList.remove('hidden'); // Show install button
});

installBtn.addEventListener('click', async () => {
    if (deferredPrompt) {
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        if (outcome === 'accepted') {
            installBtn.classList.add('hidden');
        }
        deferredPrompt = null;
    }
});

// --- 3. Image Preview Logic ---
const fileInput = document.getElementById('fileInput');
const previewContainer = document.getElementById('previewContainer');
const imagePreview = document.getElementById('imagePreview');
const uploadPrompt = document.getElementById('uploadPrompt');
const dropZone = document.getElementById('dropZone');

fileInput.addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            previewContainer.classList.remove('hidden');
            uploadPrompt.classList.add('hidden');
        }
        reader.readAsDataURL(file);
    }
});

// --- 4. Form Submission & API Fetch ---
const form = document.getElementById('uploadForm');
const submitBtn = document.getElementById('submitBtn');
const resultBox = document.getElementById('resultBox');
const resultText = document.getElementById('resultText');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // UI Update during loading
    const originalBtnHTML = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin text-xl"></i>';
    submitBtn.disabled = true;
    resultBox.classList.add('hidden');

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        
        resultBox.classList.remove('hidden');
        
        if (data.prediction) {
            let cleanName = data.prediction.replace(/___/g, ' - ').replace(/_/g, ' ');
            resultText.innerHTML = `<i class="fa-solid fa-circle-check text-green-300 mr-2"></i>${cleanName}`;
            resultText.className = "text-xl font-bold mt-1 text-white drop-shadow-md";
        } else {
            resultText.innerText = "Error: " + data.error;
            resultText.className = "text-xl font-bold mt-1 text-red-300";
        }
    } catch (error) {
        resultBox.classList.remove('hidden');
        resultText.innerText = "Something went wrong!";
        resultText.className = "text-xl font-bold mt-1 text-red-300";
    } finally {
        // Reset Button
        submitBtn.innerHTML = originalBtnHTML;
        submitBtn.disabled = false;
    }
});