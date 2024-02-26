function Form() {
    var form = document.getElementById("email").value;
    var error = document.getElementById("error");

    if (form.trim() === "") {
        error.textContent = "Emtpy"
    }
}