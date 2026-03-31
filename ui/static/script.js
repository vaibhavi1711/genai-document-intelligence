async function askQuestion() {

    const input = document.getElementById("question");
    const chatBox = document.getElementById("chat-box");

    const question = input.value.trim();

    if (!question) return;

    // Show user message
    const userDiv = document.createElement("div");
    userDiv.className = "user";
    const userMsg = document.createElement("div");
    userMsg.textContent = question;
    userDiv.appendChild(userMsg);
    chatBox.appendChild(userDiv);

    input.value = "";

    // Show loading message
    const loadingDiv = document.createElement("div");
    loadingDiv.className = "bot";
    const loadingContent = document.createElement("div");
    loadingContent.className = "bot-content";
    loadingContent.textContent = "AI is thinking...";
    loadingDiv.appendChild(loadingContent);
    chatBox.appendChild(loadingDiv);

    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question: question })
        });

        const data = await response.json();

        // Remove loading
        loadingDiv.remove();

        // Create bot response container
        const botDiv = document.createElement("div");
        botDiv.className = "bot";
        
        const botContent = document.createElement("div");
        botContent.className = "bot-content";
        
        // Format answer with paragraphs
        const formattedAnswer = data.answer
            .split('\n\n')  // Split by double newlines
            .filter(p => p.trim())  // Remove empty lines
            .map(p => `<p>${p.trim()}</p>`)  // Wrap each paragraph in <p>
            .join('');
        
        // Add answer text with formatted paragraphs
        const answerSpan = document.createElement("span");
        answerSpan.innerHTML = `<b>🤖 AI Response:</b><div style="margin-top: 10px; line-height: 1.6;">${formattedAnswer}</div>`;
        botContent.appendChild(answerSpan);
        
        // Add copy button
        const copyBtn = document.createElement("button");
        copyBtn.className = "copy-btn";
        copyBtn.innerHTML = "📋";
        copyBtn.title = "Copy to clipboard";
        copyBtn.onclick = () => copyToClipboard(data.answer, copyBtn);
        botContent.appendChild(copyBtn);
        
        // Add sources
        if (data.sources && data.sources.length > 0) {
            const sourcesBox = document.createElement("div");
            sourcesBox.className = "sources-box";
            
            const sourcesLabel = document.createElement("small");
            sourcesLabel.innerHTML = "<strong>📌 Sources:</strong> ";
            sourcesBox.appendChild(sourcesLabel);
            
            const sourcesBr = document.createElement("br");
            sourcesBox.appendChild(sourcesBr);
            
            data.sources.forEach((source, index) => {
                if (source.url) {
                    const link = document.createElement("a");
                    link.href = source.url;
                    link.target = "_blank";
                    link.textContent = source.name;
                    sourcesBox.appendChild(link);
                } else {
                    const span = document.createElement("span");
                    span.style.color = "#666";
                    span.textContent = source.name;
                    sourcesBox.appendChild(span);
                }
                
                // Add comma separator except for last item
                if (index < data.sources.length - 1) {
                    const comma = document.createElement("span");
                    comma.textContent = ", ";
                    comma.style.color = "#666";
                    sourcesBox.appendChild(comma);
                }
            });
            
            botContent.appendChild(sourcesBox);
        }
        
        botDiv.appendChild(botContent);
        chatBox.appendChild(botDiv);

    } catch (error) {
        console.error(error);
        loadingDiv.remove();

        const errorDiv = document.createElement("div");
        errorDiv.className = "bot";
        const errorContent = document.createElement("div");
        errorContent.className = "bot-content";
        errorContent.textContent = "⚠️ Error connecting to backend.";
        errorDiv.appendChild(errorContent);
        chatBox.appendChild(errorDiv);
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

function copyToClipboard(text, button) {
    navigator.clipboard.writeText(text).then(() => {
        // Change button state
        const originalText = button.innerHTML;
        button.innerHTML = "✓ Copied!";
        button.style.opacity = "1";
        
        // Revert after 2 seconds
        setTimeout(() => {
            button.innerHTML = originalText;
            button.style.opacity = "0";
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('Failed to copy text');
    });
}

async function uploadFiles() {
    const input = document.getElementById("fileInput");
    const files = input.files;
    const chatBox = document.getElementById("chat-box");

    if (files.length === 0) {
        alert("Please select at least one file.");
        return;
    }

    // Show uploading message in chat
    const fileNames = Array.from(files).map(f => f.name).join(", ");
    const uploadingDiv = document.createElement("div");
    uploadingDiv.className = "bot";
    const uploadingContent = document.createElement("div");
    uploadingContent.className = "bot-content";
    uploadingContent.innerHTML = `📤 <strong>Uploading files:</strong> ${fileNames}<br><small>Processing may take a moment...</small>`;
    uploadingDiv.appendChild(uploadingContent);
    uploadingDiv.id = "upload-message";
    chatBox.appendChild(uploadingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]); 
    }

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        
        // Update message with result
        const uploadMsg = document.getElementById("upload-message");
        if (uploadMsg) {
            if (response.ok) {
                uploadMsg.innerHTML = `<div class="bot-content" style="background: #e8f5e9; border-left: 4px solid #4caf50;">
                    ✅ <strong>Upload Successful!</strong><br>
                    <small>${data.message}</small><br>
                    <small style="color: #4caf50;">You can now ask questions about these documents.</small>
                </div>`;
            } else {
                uploadMsg.innerHTML = `<div class="bot-content" style="background: #ffebee; border-left: 4px solid #f44336;">
                    ❌ <strong>Upload Failed</strong><br>
                    <small>${data.message}</small>
                </div>`;
            }
        }
        
        // Clear file input
        input.value = "";

    } catch (error) {
        const uploadMsg = document.getElementById("upload-message");
        if (uploadMsg) {
            uploadMsg.innerHTML = `<div class="bot-content" style="background: #ffebee; border-left: 4px solid #f44336;">
                ❌ <strong>Upload Error</strong><br>
                <small>${error.message}</small>
            </div>`;
        }
    }
}