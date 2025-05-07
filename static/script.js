// const uploadBtn = document.getElementById('upload-btn');
// const askBtn = document.getElementById('ask-btn');
// const fileInput = document.getElementById('file-upload');
// const userQueryInput = document.getElementById('user-query');
// const uploadStatus = document.getElementById('upload-status');
// const chatBox = document.getElementById('chat-box');

// let documentId = null; // This will store the document ID after upload

// // Upload PDF to server
// uploadBtn.addEventListener('click', () => {
//     const file = fileInput.files[0];
//     if (!file) {
//         alert('Please select a PDF file first');
//         return;
//     }

//     const formData = new FormData();
//     formData.append('file', file);

//     // Show uploading status
//     uploadStatus.textContent = 'Uploading PDF...';
    
//     fetch('http://127.0.0.1:5000/upload', {
//         method: 'POST',
//         body: formData
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.document_id) {
//             documentId = data.document_id;
//             uploadStatus.textContent = 'PDF uploaded successfully!';
//             appendMessage('bot', 'PDF uploaded successfully. You can now ask questions.');
//         } else {
//             uploadStatus.textContent = 'Error uploading document!';
//             appendMessage('bot', 'Failed to upload PDF. Please try again.');
//         }
//     })
//     .catch(error => {
//         uploadStatus.textContent = 'Error uploading document!';
//         appendMessage('bot', 'Error uploading PDF. Please try again.');
//     });
// });

// // Ask a question based on the uploaded PDF
// askBtn.addEventListener('click', () => {
//     const query = userQueryInput.value.trim();
//     if (!query) {
//         alert('Please enter a query');
//         return;
//     }

//     if (!documentId) {
//         alert('Please upload a document first');
//         return;
//     }

//     appendMessage('user', query);
//     userQueryInput.value = '';

//     const requestPayload = {
//         query: query
//     };

//     fetch('http://127.0.0.1:5000/query', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(requestPayload)
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.answer) {
//             appendMessage('bot', data.answer);
//         } else {
//             appendMessage('bot', 'Sorry, I could not find an answer to your question.');
//         }
//     })
//     .catch(error => {
//         appendMessage('bot', 'There was an error processing your query.');
//     });
// });

// // Function to append message to chat
// function appendMessage(sender, message) {
//     const messageDiv = document.createElement('div');
//     messageDiv.classList.add(sender === 'bot' ? 'bot-message' : 'user-message');
//     messageDiv.textContent = message;
//     chatBox.appendChild(messageDiv);
//     chatBox.scrollTop = chatBox.scrollHeight;  // Scroll to the latest message
// }
// script.js

// Get references to the DOM elements
const uploadBtn = document.getElementById('upload-btn');
const uploadInput = document.getElementById('file-upload');
const uploadStatus = document.getElementById('upload-status');
const askBtn = document.getElementById('ask-btn');
const userQueryInput = document.getElementById('user-query');
const chatBox = document.getElementById('chat-box');

// Upload PDF handler
uploadBtn.addEventListener('click', () => {
    const file = uploadInput.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        // Display upload status
        uploadStatus.textContent = 'Uploading PDF...';

        // Make an API request to upload the file
        fetch('/upload', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.document_id) {
                uploadStatus.textContent = 'PDF uploaded successfully!';
                // You can save the document ID here for future queries
            } else {
                uploadStatus.textContent = `Error: ${data.error}`;
            }
        })
        .catch(error => {
            uploadStatus.textContent = `Upload failed: ${error.message}`;
        });
    } else {
        uploadStatus.textContent = 'Please select a PDF file.';
    }
});

// Ask question handler
askBtn.addEventListener('click', () => {
    const query = userQueryInput.value.trim();
    if (query) {
        chatBox.innerHTML += `<div class="message user-message">${query}</div>`;
        userQueryInput.value = '';

        // Send query to backend
        fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        })
        .then(response => response.json())
        .then(data => {
            if (data.answer) {
                chatBox.innerHTML += `<div class="message bot-message">${data.answer}</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;  // Scroll to the latest message
            }
        })
        .catch(error => {
            chatBox.innerHTML += `<div class="message bot-message">Sorry, I couldn't answer that.</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        });
    }
});
