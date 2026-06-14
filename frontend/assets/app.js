const output = document.getElementById("output");
const button = document.getElementById("load-sample");

button.addEventListener("click", async () => {
    output.textContent = "Consultando backend...";

    try {
        const response = await fetch("http://127.0.0.1:8000/api/schedules/sample");
        const data = await response.json();
        output.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        output.textContent =
            "No se pudo conectar con el backend.\n" +
            "Inicia FastAPI con: uvicorn backend.app.main:app --reload\n\n" +
            String(error);
    }
});
