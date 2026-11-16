/*
 chat.js - Assistant principal client-side script.
 Sends user questions to /api/chat and displays the answers in the chat area.
*/

document.addEventListener("DOMContentLoaded", function () {

    const chatArea  = document.getElementById("chat-area");
    const chatInput = document.getElementById("chat-input");
    const chatSend  = document.getElementById("chat-send");
    
    //clear-button 

    const clearBtn  = document.getElementById("clear-btn");
    clearBtn.addEventListener("click", function () {
        chatArea.innerHTML = "";
    });

    // ===== B2 : Category buttons =====
    const btnFrais       = document.getElementById("btn-frais");
    const btnEnseignants = document.getElementById("btn-enseignants");

    function addWelcomeMessage(text) {
        const div = document.createElement("div");
        div.className = "chat-message bot category-welcome";
        div.innerHTML = text;
        chatArea.appendChild(div);
        chatArea.scrollTop = chatArea.scrollHeight;
    }

    function setActiveCategory(category) {
        btnFrais.classList.remove("active-category");
        btnEnseignants.classList.remove("active-category");
        if (category === "frais")       btnFrais.classList.add("active-category");
        if (category === "enseignants") btnEnseignants.classList.add("active-category");
    }

    btnFrais.addEventListener("click", function () {
        setActiveCategory("frais");
        chatArea.innerHTML = "";
        addWelcomeMessage(
            "<strong>💰 Catégorie : Frais d'inscription</strong><br>" +
            "Bienvenue ! Dans cette catégorie, je réponds à toutes vos questions sur les frais, " +
            "tarifs, réductions et aides financières disponibles à la HEL. Posez votre question !"
        );
    });

    btnEnseignants.addEventListener("click", function () {
        setActiveCategory("enseignants");
        chatArea.innerHTML = "";
        addWelcomeMessage(
            "<strong>👨‍🏫 Catégorie : Enseignants</strong><br>" +
            "Bienvenue ! Dans cette catégorie, je réponds à vos questions sur les enseignants, " +
            "l'encadrement pédagogique et comment contacter les professeurs de la HEL. Posez votre question !"
        );
    });


    // ===== Helper: add a user bubble =====
    function addUserMessage(text) {
        const div = document.createElement("div");
        div.className = "chat-message user";
        div.textContent = text;
        chatArea.appendChild(div);
        chatArea.scrollTop = chatArea.scrollHeight;
    }


    // ===== Helper: add a bot bubble =====
    function addBotMessage(answer, source, confidence) {
        const div = document.createElement("div");
        const isUnreliable = (confidence === "faible");
        div.className = "chat-message bot" + (isUnreliable ? " unreliable" : "");

        if (isUnreliable) {
            const warn = document.createElement("strong");
            warn.textContent = "⚠️ Réponse non fiable";
            div.appendChild(warn);
        }

        const p = document.createElement("p");
        p.className = "small mb-1 mt-1";
        p.textContent = answer;
        div.appendChild(p);

        if (source) {
            const src = document.createElement("small");
            src.className = "text-muted d-block";
            src.innerHTML = "Source : <a href=\"" + source + "\" target=\"_blank\">" + source + "</a>";
            div.appendChild(src);
        }

        const conf = document.createElement("small");
        conf.className = "text-muted";
        conf.textContent = "Confiance : " + confidence;
        div.appendChild(conf);

        chatArea.appendChild(div);
        chatArea.scrollTop = chatArea.scrollHeight;
    }


    // ===== Helper: temporary "loading" bubble =====
    function showLoading() {
        const div = document.createElement("div");
        div.className = "chat-message bot loading";
        div.id = "loading-bubble";
        div.textContent = "⏳ Recherche en cours...";
        chatArea.appendChild(div);
        chatArea.scrollTop = chatArea.scrollHeight;
    }

    function hideLoading() {
        const bubble = document.getElementById("loading-bubble");
        if (bubble) bubble.remove();
    }


    // ===== Main: send the question to the server =====
    async function sendQuestion() {
        const question = chatInput.value.trim();
        if (!question) return;

        addUserMessage(question);
        chatInput.value = "";
        showLoading();

        try {
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: question })
            });
            const data = await response.json();
            hideLoading();
            addBotMessage(data.answer, data.source, data.confidence);
        } catch (err) {
            hideLoading();
            addBotMessage("Erreur de connexion au serveur.", null, "faible");
        }
    }


    // ===== Wire up the click + Enter key =====
    chatSend.addEventListener("click", sendQuestion);
    chatInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") sendQuestion();
    });

});