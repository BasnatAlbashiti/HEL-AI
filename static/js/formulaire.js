document.getElementById("satisfaction-form").addEventListener("submit", async function(e) {
    e.preventDefault();

    const nom = document.getElementById("nom").value.trim();
    const email = document.getElementById("email").value.trim();
    const formation = document.getElementById("formation").value;
    const note = document.getElementById("note").value;
    const commentaire = document.getElementById("commentaire").value.trim();

    try {
        const response = await fetch("/api/formulaire", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nom, email, formation, note, commentaire })
        });
        const data = await response.json();

        if (data.success) {
            document.getElementById("success-message").classList.remove("d-none");
            document.getElementById("error-message").classList.add("d-none");
            document.getElementById("satisfaction-form").reset();
        } else {
            document.getElementById("error-message").classList.remove("d-none");
            document.getElementById("error-message").textContent = "❌ " + data.message;
        }
    } catch (err) {
        document.getElementById("error-message").classList.remove("d-none");
    }
});