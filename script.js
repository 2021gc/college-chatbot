<script>
    const chatBox = document.getElementById("chatBox");
    const typingIndicator = document.getElementById("typingIndicator");

    // Auto scroll
    chatBox.scrollTop = chatBox.scrollHeight;

    function handleSubmit(event) {
        // STOP immediate form submit
        event.preventDefault();

        // Show typing dots
        typingIndicator.style.display = "inline-flex";
        chatBox.scrollTop = chatBox.scrollHeight;

        // Submit after delay (typing effect)
        setTimeout(() => {
            event.target.submit();
        }, 1000); // 1 second delay

        return false;
    }

    // Voice input
    function startDictation() {
        if ('webkitSpeechRecognition' in window) {
            const recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-IN';

            recognition.start();

            recognition.onresult = function (event) {
                document.getElementById('user_input').value =
                    event.results[0][0].transcript;
                recognition.stop();
            };

            recognition.onerror = function () {
                recognition.stop();
            };
        }
    }
</script>
