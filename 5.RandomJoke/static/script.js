async function generateJoke() {
    try {
        const response = await fetch("/", {
            method: "POST",
        });
        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }
        const data = await response.json();
        document.getElementById("joke").textContent = data.joke;
    } catch (error) {
        console.error(error);
        document.getElementById("joke").textContent = "Failed to fetch a joke.";
    }
}