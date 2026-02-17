document.addEventListener("DOMContentLoaded", function () {

    const chatBox = document.getElementById("chatBox");
    const typingIndicator = document.getElementById("typingIndicator");

    // Auto scroll
    if (chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Form submit with typing effect
    window.handleSubmit = function (event) {
        event.preventDefault();

        if (typingIndicator) {
            typingIndicator.style.display = "inline-flex";
        }

        if (chatBox) {
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        setTimeout(() => {
            event.target.submit();
        }, 1000);

        return false;
    };

    // Voice input
    window.startDictation = function () {
    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-IN';

        recognition.start();

        recognition.onresult = function (event) {
            const text = event.results[0][0].transcript;

            // Send to Flask backend
            fetch("/voice", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text: text })
            })
            .then(response => response.json())
            .then(data => {
                const chatBox = document.getElementById("chatBox");

                chatBox.innerHTML += `
                    <div><b>You:</b> ${text}</div>
                    <div><b>Bot:</b> ${data.reply}</div>
                `;

                chatBox.scrollTop = chatBox.scrollHeight;
            });

            recognition.stop();
        };

        recognition.onerror = function (event) {
            console.error("Voice error:", event.error);
            recognition.stop();
        };

    } else {
        alert("Speech recognition not supported");
    }
};

