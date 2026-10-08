// --- Service Worker (PWA) ---
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').catch(err => console.log('SW failed', err));
    });
}

// --- DOM Elements ---
const fileInput = document.getElementById('fileInput');
const previewContainer = document.getElementById('previewContainer');
const imagePreview = document.getElementById('imagePreview');
const uploadPrompt = document.getElementById('uploadPrompt');
const form = document.getElementById('uploadForm');
const submitBtn = document.getElementById('submitBtn');
const btnText = document.getElementById('btnText');
const resultBox = document.getElementById('resultBox');
const resultText = document.getElementById('resultText');
const scannerLine = document.getElementById('scannerLine');
const statusIcon = document.getElementById('statusIcon');
const resultAccent = document.getElementById('resultAccent');
const shareBtn = document.getElementById('shareBtn');

// --- Image Preview Logic ---
fileInput.addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            previewContainer.classList.remove('hidden');
            uploadPrompt.classList.add('hidden');
            
            // Reset result UI on new image
            resultBox.classList.add('opacity-0', 'translate-y-4');
            setTimeout(() => resultBox.classList.add('hidden'), 300);
        }
        reader.readAsDataURL(file);
    }
});

// --- API Request & Animations ---
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!fileInput.files[0]) return;

    // Start UI Animations
    scannerLine.style.display = 'block';
    btnText.innerText = "Analyzing pixels...";
    submitBtn.disabled = true;
    shareBtn.classList.add('hidden');
    submitBtn.classList.add('opacity-70', 'cursor-not-allowed');
    
    // FIX: Hide old results immediately bina kisi setTimeout ke
    resultBox.classList.add('hidden');
    resultBox.classList.remove('opacity-100', 'translate-y-0');
    resultBox.classList.add('opacity-0', 'translate-y-4');

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/predict', { method: 'POST', body: formData });
        const data = await response.json();
        
        resultBox.classList.remove('hidden');
        
        setTimeout(() => {
            resultBox.classList.remove('opacity-0', 'translate-y-4');
            resultBox.classList.add('opacity-100', 'translate-y-0');
        }, 50);
        
        if (data.prediction) {
            shareBtn.classList.remove('hidden');
            if (navigator.vibrate) navigator.vibrate([200, 100, 200]);
            let cleanName = data.prediction.replace(/___/g, ' - ').replace(/_/g, ' ');
            // Confidence aur naam dono dikhana
            resultText.innerHTML = `
                <div class="flex flex-col">
                    <span>${cleanName}</span>
                    <span class="text-sm font-normal text-slate-400 mt-1">AI Confidence: <span class="text-emerald-400">${data.confidence}%</span></span>
                </div>`;

                document.getElementById('treatmentBox').classList.remove('hidden');
                document.getElementById('organicText').innerText = data.treatment.organic;
                document.getElementById('chemicalText').innerText = data.treatment.chemical;
                document.getElementById('preventionText').innerText = data.treatment.prevention;
            
            if (cleanName.toLowerCase().includes('healthy')) {
                statusIcon.className = "w-14 h-14 rounded-2xl flex items-center justify-center shrink-0 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-2xl";
                statusIcon.innerHTML = '<i class="fa-solid fa-shield-check"></i>';
                resultAccent.className = "absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-400 to-green-500";
            } else {
                statusIcon.className = "w-14 h-14 rounded-2xl flex items-center justify-center shrink-0 bg-rose-500/10 border border-rose-500/20 text-rose-400 text-2xl";
                statusIcon.innerHTML = '<i class="fa-solid fa-virus"></i>';
                resultAccent.className = "absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-rose-500 to-orange-500";
            }
        }
        else {
            resultText.innerText = "Error: " + data.error;
        }
    } catch (error) {
        resultBox.classList.remove('hidden');
        setTimeout(() => {
            resultBox.classList.remove('opacity-0', 'translate-y-4');
            resultBox.classList.add('opacity-100', 'translate-y-0');
        }, 50);
        resultText.innerText = "Connection Failed!";
    } finally {
        // Stop Animations
        scannerLine.style.display = 'none';
        btnText.innerText = "Run AI Analysis";
        submitBtn.disabled = false;
        submitBtn.classList.remove('opacity-70', 'cursor-not-allowed');
    }
});

// --- Share Logic ---
shareBtn.addEventListener('click', async () => {
    // Result text se bimaari ka naam nikalna
    const diseaseName = document.querySelector('#resultText span').innerText;

    if (navigator.share) {
        try {
            await navigator.share({
                title: 'AgriVision AI - Plant Diagnosis',
                text: `I just checked my crop using AgriVision AI. The diagnosis is: *${diseaseName}*.`,
                url: window.location.href
            });
        } catch (error) {
            console.log('Error sharing:', error);
        }
    } else {
        alert("Sharing is not supported on this browser (Try on mobile).");
    }
    // --- Voice Assistant Logic ---
const speakBtn = document.getElementById('speakBtn');

// API result aane par button ko show karein 
// (Jahan aapne shareBtn.classList.remove('hidden'); likha hai, usi ke theek neeche ye likhein:)
// speakBtn.classList.remove('hidden');

speakBtn.addEventListener('click', () => {
    // Result text nikalna
    const diseaseName = document.querySelector('#resultText span').innerText;
    
    // Browser ka inbuilt text-to-speech engine use karna
    const speech = new SpeechSynthesisUtterance();
    speech.text = `The detected condition is ${diseaseName}.`;
    speech.lang = 'en-US'; // Aap isko hindi ke liye 'hi-IN' bhi try kar sakte hain agar text hindi me ho
    speech.rate = 0.9; // Bolne ki speed thodi slow
    
    window.speechSynthesis.speak(speech);
});
});