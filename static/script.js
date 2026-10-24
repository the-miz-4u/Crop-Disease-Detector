// --- Service Worker (PWA) ---
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').catch(err => console.log('SW failed', err));
    });
}

// --- Language Translation System ---
let currentLang = 'en';
let lastApiResult = null; // API result ko save karne ke liye

const uiTranslations = {
    'en': {
        'uploadPrompt': 'Upload Plant Image',
        'uploadSub': 'Drag & drop or click to browse',
        'runBtn': 'Run AI Analysis',
        'shareBtn': ' Share Diagnosis',
        'speakBtn': ' Bol Kar Sunein',
        'resetBtn': ' Scan Another Plant',
        'historyBtn': 'History',
        'historyTitle': 'Scan History',
        'noHistory': 'No scan history found.'
    },
    'hi': {
        'uploadPrompt': 'पौधे की फोटो अपलोड करें',
        'uploadSub': 'फोटो खींचें या गैलरी से चुनें',
        'runBtn': 'AI स्कैन शुरू करें',
        'shareBtn': ' रिपोर्ट शेयर करें',
        'speakBtn': ' बोल कर सुनें',
        'resetBtn': ' दूसरा पौधा चेक करें',
        'historyBtn': 'इतिहास',
        'historyTitle': 'पुराने स्कैन',
        'noHistory': 'कोई पुराना स्कैन नहीं मिला।'
    }
};

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
const speakBtn = document.getElementById('speakBtn'); 
const resetBtn = document.getElementById('resetBtn'); 
const langToggle = document.getElementById('langToggle');
const langText = document.getElementById('langText');

// History DOM Elements
const historyBtn = document.getElementById('historyBtn');
const historyBtnText = document.getElementById('historyBtnText');
const historyModal = document.getElementById('historyModal');
const closeHistoryBtn = document.getElementById('closeHistoryBtn');
const historyTitle = document.getElementById('historyTitle');
const historyList = document.getElementById('historyList');

// --- Language Toggle Logic ---
langToggle.addEventListener('click', () => {
    currentLang = currentLang === 'en' ? 'hi' : 'en';
    langText.innerText = currentLang === 'en' ? 'English' : 'हिन्दी';
    
    updateUILanguage();
    renderResultData(); // Result dikh raha ho toh use translate karega
    
    if (historyModal && !historyModal.classList.contains('hidden')) {
        renderHistory(); // History modal open ho toh usko bhi translate karega
    }
});

function updateUILanguage() {
    const t = uiTranslations[currentLang];
    
    // Update Upload Area
    if(document.querySelector('#uploadPrompt h3')) document.querySelector('#uploadPrompt h3').innerText = t.uploadPrompt;
    if(document.querySelector('#uploadPrompt p')) document.querySelector('#uploadPrompt p').innerText = t.uploadSub;
    
    // Update Run Button
    if(btnText) btnText.innerText = t.runBtn;
    
    // Update Action Buttons
    if(shareBtn) shareBtn.innerHTML = `<i class="fa-solid fa-share-nodes"></i> ${t.shareBtn}`;
    if(speakBtn) speakBtn.innerHTML = `<i class="fa-solid fa-volume-high"></i> ${t.speakBtn}`;
    if(resetBtn) resetBtn.innerHTML = `<i class="fa-solid fa-rotate-right"></i> ${t.resetBtn}`;
    
    // Update History Area
    if (historyBtnText) historyBtnText.innerText = t.historyBtn;
    if (historyTitle) historyTitle.innerText = t.historyTitle;
}

// --- Result Render Logic ---
function renderResultData() {
    if (!lastApiResult) return;
    const t = lastApiResult.treatment[currentLang];
    
    // Set Disease Name & Confidence
    resultText.innerHTML = `
        <div class="flex flex-col">
            <span>${t.name}</span>
            <span class="text-sm font-normal text-slate-400 mt-1">AI Confidence: <span class="text-emerald-400">${lastApiResult.confidence}%</span></span>
        </div>`;

    // Set Treatment Data
    document.getElementById('treatmentBox').classList.remove('hidden');
    document.getElementById('organicText').innerText = t.organic;
    document.getElementById('chemicalText').innerText = t.chemical;
    document.getElementById('preventionText').innerText = t.prevention;
}

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
    btnText.innerText = currentLang === 'en' ? "Analyzing pixels..." : "AI विश्लेषण कर रहा है...";
    submitBtn.disabled = true;
    submitBtn.classList.add('opacity-70', 'cursor-not-allowed');
    
    // Hide extra buttons during analysis
    shareBtn.classList.add('hidden');
    speakBtn.classList.add('hidden');
    resetBtn.classList.add('hidden');
    
    // Hide old results immediately
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
            lastApiResult = data; 
            renderResultData(); // Updates text based on language
            
            shareBtn.classList.remove('hidden');
            speakBtn.classList.remove('hidden');
            resetBtn.classList.remove('hidden');
            
            if (navigator.vibrate) navigator.vibrate([200, 100, 200]);
            
            // Save to Offline History
            saveToHistory(data, imagePreview.src);
            
            // Dynamic Styling based on Health
            if (data.prediction.toLowerCase().includes('healthy')) {
                statusIcon.className = "w-14 h-14 rounded-2xl flex items-center justify-center shrink-0 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-2xl";
                statusIcon.innerHTML = '<i class="fa-solid fa-shield-check"></i>';
                resultAccent.className = "absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-400 to-green-500";
            } else {
                statusIcon.className = "w-14 h-14 rounded-2xl flex items-center justify-center shrink-0 bg-rose-500/10 border border-rose-500/20 text-rose-400 text-2xl";
                statusIcon.innerHTML = '<i class="fa-solid fa-virus"></i>';
                resultAccent.className = "absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-rose-500 to-orange-500";
            }
            
            document.getElementById('resultBox').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
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
        resultText.innerText = currentLang === 'en' ? "Connection Failed!" : "कनेक्शन विफल!";
    } finally {
        scannerLine.style.display = 'none';
        updateUILanguage(); // Reset button text properly
        submitBtn.disabled = false;
        submitBtn.classList.remove('opacity-70', 'cursor-not-allowed');
    }
});

// --- Share Logic ---
shareBtn.addEventListener('click', async () => {
    const t = lastApiResult.treatment[currentLang];
    const textToShare = currentLang === 'en' 
        ? `I just checked my crop using AgriVision AI. The diagnosis is: *${t.name}*.` 
        : `मैंने AgriVision AI से अपनी फसल की जांच की है। बीमारी का नाम है: *${t.name}*।`;

    if (navigator.share) {
        try {
            await navigator.share({
                title: 'AgriVision AI - Plant Diagnosis',
                text: textToShare,
                url: window.location.href
            });
        } catch (error) {
            console.log('Error sharing:', error);
        }
    } else {
        alert(currentLang === 'en' ? "Sharing is not supported on this browser." : "आपके ब्राउज़र में शेयर सपोर्ट नहीं है।");
    }
});

// --- Voice Assistant Logic (Bilingual) ---
speakBtn.addEventListener('click', () => {
    if (!lastApiResult) return;
    const t = lastApiResult.treatment[currentLang];
    const speech = new SpeechSynthesisUtterance();
    
    if (currentLang === 'hi') {
        speech.text = `आपके पौधे में ${t.name} पाया गया है।`;
        speech.lang = 'hi-IN';
    } else {
        speech.text = `The detected condition is ${t.name}.`;
        speech.lang = 'en-US';
    }
    
    speech.rate = 0.9;
    window.speechSynthesis.speak(speech);
});

// --- Reset App for New Scan ---
resetBtn.addEventListener('click', () => {
    window.location.reload(); 
});

// --- Network Awareness (Online/Offline Indicator) ---
const networkBadge = document.getElementById('networkBadge');
const networkText = document.getElementById('networkText');

function updateNetworkStatus() {
    if(!networkBadge) return;
    
    if (navigator.onLine) {
        networkBadge.className = "fixed top-4 left-4 z-50 px-3 py-1.5 rounded-full text-xs font-semibold tracking-wide bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 backdrop-blur-md transition-all duration-300 shadow-lg";
        networkText.innerHTML = currentLang === 'en' ? "Online" : "ऑनलाइन";
        networkBadge.querySelector('i').className = "fa-solid fa-wifi mr-1.5";
    } else {
        networkBadge.className = "fixed top-4 left-4 z-50 px-3 py-1.5 rounded-full text-xs font-semibold tracking-wide bg-rose-500/20 text-rose-400 border border-rose-500/30 backdrop-blur-md transition-all duration-300 shadow-lg";
        networkText.innerHTML = currentLang === 'en' ? "Offline Mode" : "ऑफलाइन मोड";
        networkBadge.querySelector('i').className = "fa-solid fa-wifi-slash mr-1.5";
    }
}

window.addEventListener('online', updateNetworkStatus);
window.addEventListener('offline', updateNetworkStatus);
updateNetworkStatus();


// --- Offline Scan History Logic ---
if (historyBtn && historyModal && closeHistoryBtn) {
    historyBtn.addEventListener('click', () => {
        historyModal.classList.remove('hidden');
        historyModal.classList.add('flex');
        renderHistory();
    });

    closeHistoryBtn.addEventListener('click', () => {
        historyModal.classList.add('hidden');
        historyModal.classList.remove('flex');
    });
}

function saveToHistory(apiData, imgSrc) {
    let history = JSON.parse(localStorage.getItem('agriVisionHistory')) || [];
    const newEntry = {
        id: Date.now(),
        date: new Date().toLocaleString(),
        image: imgSrc,
        data: apiData
    };
    history.unshift(newEntry); 
    if (history.length > 10) history.pop(); // Save only the last 10 scans
    localStorage.setItem('agriVisionHistory', JSON.stringify(history));
}

function renderHistory() {
    if(!historyList) return;
    let history = JSON.parse(localStorage.getItem('agriVisionHistory')) || [];
    const t = uiTranslations[currentLang];
    
    if (history.length === 0) {
        historyList.innerHTML = `<p class="text-slate-400 text-center mt-6">${t.noHistory}</p>`;
        return;
    }

    historyList.innerHTML = history.map(item => {
        const treat = item.data.treatment[currentLang];
        // Check for healthy condition to assign color
        const isHealthy = treat.name.toLowerCase().includes('healthy') || treat.name.includes('स्वस्थ');
        const statusColor = isHealthy ? 'text-emerald-400' : 'text-rose-400';
        
        return `
        <div class="bg-slate-800/50 p-4 rounded-2xl border border-slate-700 flex gap-4 items-center mb-3">
            <img src="${item.image}" class="w-20 h-20 object-cover rounded-xl border border-slate-600 shrink-0">
            <div class="flex-1 overflow-hidden">
                <h3 class="text-lg font-bold text-white truncate">${treat.name}</h3>
                <p class="text-xs text-slate-400 mb-1"><i class="fa-regular fa-clock"></i> ${item.date}</p>
                <p class="text-sm ${statusColor} font-medium">Confidence: ${item.data.confidence}%</p>
            </div>
        </div>`;
    }).join('');
}