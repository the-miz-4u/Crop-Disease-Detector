document.querySelector('form').addEventListener('submit', async (e) => {
    e.preventDefault(); // Page reload hone se rokna
    
    const form = e.target;
    const formData = new FormData(form);
    const button = form.querySelector('button');
    
    // Result dikhane ke liye ek naya div banate hain agar nahi hai toh
    let resultDiv = document.getElementById('result');
    if (!resultDiv) {
        resultDiv = document.createElement('div');
        resultDiv.id = 'result';
        resultDiv.style.marginTop = '20px';
        resultDiv.style.fontSize = '1.2rem';
        resultDiv.style.fontWeight = 'bold';
        form.appendChild(resultDiv);
    }
    
    button.innerText = "Analyzing...";
    resultDiv.style.color = 'black';
    resultDiv.innerText = "Checking image with AI...";
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        
        if (data.prediction) {
            resultDiv.style.color = 'green';
            // Folder ke naam (e.g. Tomato___Bacterial_spot) ko thoda clean karke dikhana
            let cleanName = data.prediction.replace(/___/g, ' - ').replace(/_/g, ' ');
            resultDiv.innerText = "Detected: " + cleanName;
        } else {
            resultDiv.style.color = 'red';
            resultDiv.innerText = "Error: " + data.error;
        }
    } catch (error) {
        resultDiv.style.color = 'red';
        resultDiv.innerText = "Something went wrong!";
    }
    
    button.innerText = "Upload & Predict";
});