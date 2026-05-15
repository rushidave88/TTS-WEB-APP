document.addEventListener("DOMContentLoaded", async () => {
    const languageSelect = document.getElementById("language");
    const textInput = document.getElementById("text");
    const generateBtn = document.getElementById("generate-btn");
    const btnText = document.getElementById("btn-text");
    const spinner = document.getElementById("spinner");
    const audioPlayer = document.getElementById("audio-player");
    const statusMessage = document.getElementById("status-message");

    // Fetch supported languages on load
    try {
        const res = await fetch("/languages");
        const languagesMap = await res.json(); // Now receiving { "en": "English", "hi": "Hindi", ... }
        
        languageSelect.innerHTML = "";

        // Iterate through the dictionary/object entries
        for (const [code, fullName] of Object.entries(languagesMap)) {
            const option = document.createElement("option");
            option.value = code;        // Sends short code (e.g., 'hi') to backend [cite: 48]
            option.textContent = fullName; // Displays full name (e.g., 'Hindi') to user 
            
            if (code === "hi") option.selected = true; // Set Hindi as default
            languageSelect.appendChild(option);
        }
        
        languageSelect.disabled = false;
    } catch (error) {
        console.error("Failed to load languages:", error);
        languageSelect.innerHTML = '<option value="">Error loading languages</option>';
    }

    // Handle Generation
    generateBtn.addEventListener("click", async () => {
        const text = textInput.value.trim();
        const language = languageSelect.value;

        if (!text) {
            alert("Please enter some text.");
            return;
        }

        // UI Loading State [cite: 18]
        generateBtn.disabled = true;
        btnText.textContent = "Generating...";
        spinner.classList.remove("hidden");
        audioPlayer.classList.add("hidden");
        statusMessage.textContent = "";

        try {
            const response = await fetch("/generate-tts", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text, language })
            });

            const data = await response.json();

            if (response.ok) {
                // Add timestamp to prevent browser from caching the audio file
                audioPlayer.src = data.audio_url + "?t=" + new Date().getTime();
                audioPlayer.classList.remove("hidden");
                audioPlayer.play();
                statusMessage.textContent = "Success! Playing audio...";
                statusMessage.style.color = "green";
            } else {
                throw new Error(data.detail || "Generation failed.");
            }
        } catch (error) {
            console.error(error);
            statusMessage.textContent = `Error: ${error.message}`;
            statusMessage.style.color = "red";
        } finally {
            // Restore UI state [cite: 18]
            generateBtn.disabled = false;
            btnText.textContent = "Generate Speech";
            spinner.classList.add("hidden");
        }
    });
});