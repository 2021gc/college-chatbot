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
                const input = document.getElementById("user_input");
                if (input) {
                    input.value = event.results[0][0].transcript;
                }
                recognition.stop();
            };

            recognition.onerror = function () {
                recognition.stop();
            };
        } else {
            alert("Speech recognition not supported");
        }
    };

    
