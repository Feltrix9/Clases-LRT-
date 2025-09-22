function validarFormulario() {
    let nombre = document.getElementById("nombre").value;
    if (nombre.trim() === "") {
        alert("Debes ingresar un nombre de receta.");
        return;
    }
    alert("¡Receta enviada con éxito!");
}

function agregarReceta() {
    let receta = document.getElementById("nuevaReceta").value;
    if (receta.trim() === "") {
        alert("Por favor escribe un nombre de receta.");
        return;
    }
    let li = document.createElement("li");
    li.textContent = receta;
    document.getElementById("lista-recetas").appendChild(li);
    document.getElementById("nuevaReceta").value = "";
}
