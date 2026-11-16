document.addEventListener("DOMContentLoaded", function () {
    const chatArea = document.getElementById("chat-area");
    const chatInput = document.getElementById("chat-input");
    const chatSend = document.getElementById("chat-send");

    function addUserMessage(text) {
        const div = document.createElement("div");
        div.className = "chat-message user";
        div.textContent = text;
        chatArea.appendChild(div);
        chatArea.scrollTop = chatArea.scrollHeight;
    }

    function addBotMessage(text) {
        const div = document.createElement("div");
        div.className = "chat-message bot";
        const p = document.createElement("p");
        p.className = "small mb-0 mt-1";
        p.textContent = text;
        div.appendChild(p);
        chatArea.appendChild(div);
        chatArea.scrollTop = chatArea.scrollHeight;
    }

    function showLoading() {
        const div = document.createElement("div");
        div.className = "chat-message bot loading";
        div.id = "loading-bubble";
        div.textContent = "⏳ Analyse de votre profil en cours...";
        chatArea.appendChild(div);
        chatArea.scrollTop = chatArea.scrollHeight;
    }

    function hideLoading() {
        const bubble = document.getElementById("loading-bubble");
        if (bubble) bubble.remove();
    }

    async function sendMessage() {
        const interests = chatInput.value.trim();
        if (!interests) return;

        addUserMessage(interests);
        chatInput.value = "";
        showLoading();

        try {
            const response = await fetch("/api/orientation", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ interests: interests })
            });
            const data = await response.json();
            hideLoading();
            addBotMessage(data.answer);
        } catch (err) {
            hideLoading();
            addBotMessage("Erreur de connexion au serveur.");
        }
    }

    chatSend.addEventListener("click", sendMessage);
    chatInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") sendMessage();
    });
});