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

    function addBotMessage(answer, source, niveau, redirect) {
        const div = document.createElement("div");
        div.className = "chat-message bot";

        if (niveau) {
            const badge = document.createElement("small");
            badge.className = "text-muted d-block mb-1";
            badge.textContent = "🔀 " + niveau;
            div.appendChild(badge);
        }

        const p = document.createElement("p");
        p.className = "small mb-1 mt-1";
        p.textContent = answer;
        div.appendChild(p);

        if (source) {
            const src = document.createElement("small");
            src.className = "text-muted d-block";
            src.innerHTML = "Source : <a href='" + source + "' target='_blank'>" + source + "</a>";
            div.appendChild(src);
        }

        if (redirect) {
            const btn = document.createElement("a");
            btn.href = redirect;
            btn.className = "btn btn-dark btn-sm mt-2";
            btn.textContent = "👉 Aller à l'Assistant principal";
            div.appendChild(btn);
        }

        chatArea.appendChild(div);
        chatArea.scrollTop = chatArea.scrollHeight;
    }

    function showLoading() {
        const div = document.createElement("div");
        div.className = "chat-message bot loading";
        div.id = "loading-bubble";
        div.textContent = "⏳ Analyse en cours...";
        chatArea.appendChild(div);
        chatArea.scrollTop = chatArea.scrollHeight;
    }

    function hideLoading() {
        const bubble = document.getElementById("loading-bubble");
        if (bubble) bubble.remove();
    }

    async function sendQuestion() {
        const question = chatInput.value.trim();
        if (!question) return;

        addUserMessage(question);
        chatInput.value = "";
        showLoading();

        try {
            const response = await fetch("/api/chat-orchestrator", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: question })
            });
            const data = await response.json();
            hideLoading();
            addBotMessage(data.answer, data.source, data.niveau, data.redirect);
        } catch (err) {
            hideLoading();
            addBotMessage("Erreur de connexion au serveur.");
        }
    }

    chatSend.addEventListener("click", sendQuestion);
    chatInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") sendQuestion();
    });
});