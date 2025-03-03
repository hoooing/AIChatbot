// Function to format Markdown (Handles bold and italic text)
function formatMarkdown(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>")  // Bold (**text**)
        .replace(/\*(.*?)\*/g, "<i>$1</i>")      // Italic (*text*)
        .replace(/\n/g, "<br>");                 // New lines
}

// Function to send user message to backend and display AI response
function sendMessage() {
    let userMessage = document.getElementById("userInput").value;
    if (!userMessage) return;

    let chatbox = document.getElementById("chat-container");

    // Display user message
    chatbox.innerHTML += `<div class="chat-message user-message"><b>You:</b> ${userMessage}</div>`;
    document.getElementById("userInput").value = "";  // Clear input field

    // Send message to Flask backend
    fetch("https://aichatbot-tbc1.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        let formattedResponse = formatMarkdown(data.response); // Convert Markdown to HTML
        chatbox.innerHTML += `<div class="chat-message bot-message"><b>AI BOT:</b> ${formattedResponse}</div>`;
        chatbox.scrollTop = chatbox.scrollHeight; // Auto-scroll
    })
    .catch(error => console.error("Error:", error));
}
