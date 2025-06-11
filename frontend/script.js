// API endpoints
const API_URL = 'http://127.0.0.1:8000';
const UPLOAD_ENDPOINT = `${API_URL}/api/upload`;
const QUERY_ENDPOINT = `${API_URL}/api/query`;

// DOM elements
const pdfFileInput = document.getElementById('pdfFile');
const uploadStatus = document.getElementById('uploadStatus');
const uploadPreview = document.getElementById('uploadPreview');
const previewText = document.getElementById('previewText');
const questionInput = document.getElementById('question');
const askButton = document.getElementById('askButton');
const answerSection = document.getElementById('answerSection');
const answerText = document.getElementById('answer');
const loadingAnswer = document.getElementById('loadingAnswer');

// Helper function to show error messages
function showError(message, element) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    element.appendChild(errorDiv);
    setTimeout(() => errorDiv.remove(), 5000);
}

// Helper function to show success messages
function showSuccess(message, element) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    element.appendChild(successDiv);
    setTimeout(() => successDiv.remove(), 5000);
}

// Drag and drop functionality
const dropZone = document.querySelector('.border-dashed');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
    dropZone.classList.add('drag-over');
}

function unhighlight(e) {
    dropZone.classList.remove('drag-over');
}

dropZone.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

// File input change handler
pdfFileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

function handleFiles(files) {
    if (files.length > 0) {
        const file = files[0];
        if (file.type === 'application/pdf') {
            uploadFile(file);
        } else {
            showError('Please upload a PDF file', dropZone);
        }
    }
}

// Upload file to server
async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        uploadStatus.classList.remove('hidden');
        uploadPreview.classList.add('hidden');
        dropZone.classList.add('uploading');

        const response = await fetch(UPLOAD_ENDPOINT, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            previewText.textContent = data.preview;
            uploadPreview.classList.remove('hidden');
            showSuccess(`Successfully processed ${data.num_chunks} chunks`, dropZone);
        } else {
            showError(data.detail || 'Error uploading file', dropZone);
        }
    } catch (error) {
        showError(`Error uploading file: ${error.message}`, dropZone);
    } finally {
        uploadStatus.classList.add('hidden');
        dropZone.classList.remove('uploading');
    }
}

// Ask question handler
askButton.addEventListener('click', async () => {
    const question = questionInput.value.trim();
    if (!question) {
        showError('Please enter a question', answerSection);
        return;
    }

    try {
        loadingAnswer.classList.remove('hidden');
        answerSection.classList.add('hidden');
        askButton.disabled = true;

        const response = await fetch(QUERY_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        if (response.ok) {
            answerText.textContent = data.answer;
            answerSection.classList.remove('hidden');
        } else {
            showError(data.detail || 'Error getting answer', answerSection);
        }
    } catch (error) {
        showError(`Error: ${error.message}`, answerSection);
    } finally {
        loadingAnswer.classList.add('hidden');
        askButton.disabled = false;
    }
}); 