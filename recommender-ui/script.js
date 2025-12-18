const API_URL = "https://s9nja279qc.execute-api.us-east-2.amazonaws.com/prod";

async function recomendar() {
  const userId = document.getElementById("userId").value;
  const resultDiv = document.getElementById("results");
  resultDiv.innerHTML = "Carregando...";

  try {
    const response = await fetch(
      `${API_URL}/recommend?user_id=${userId}`
    );

    if (!response.ok) {
      throw new Error("Erro HTTP");
    }

    const data = await response.json();

    if (data.length === 0) {
      resultDiv.innerHTML = "<p>Nenhuma recomendação encontrada.</p>";
      return;
    }

    resultDiv.innerHTML = data
      .map(
        (item) => `
          <div class="card">
            <h3>${item.name}</h3>
            <p><strong>Categoria:</strong> ${item.category}</p>
            <p><strong>Marca:</strong> ${item.brand}</p>
            <p><strong>Preço:</strong> R$ ${item.price}</p>
          </div>
        `
      )
      .join("");
  } catch (error) {
    console.error(error);
    resultDiv.innerHTML =
      "<p style='color:red'>Erro ao consumir a API</p>";
  }
}
