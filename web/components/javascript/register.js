document.getElementById("register-form").addEventListener("submit", function (e) {
    e.preventDefault();

    const redirectEndpoiint = document.getElementById("users-login").getAttribute("data-url");
    const usersRegisterEndpoint = document.getElementById("users-register").getAttribute("data-url");
    console.log(`Sending request to ${usersRegisterEndpoint}`);

    const formData = new FormData(e.target);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });
    fetch(usersRegisterEndpoint, {
        method: "POST",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            // 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(data),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            window.location.href = redirectEndpoiint;
        });
});