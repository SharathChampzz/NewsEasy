document.getElementById("login-form").addEventListener("submit", function (e) {
    e.preventDefault();
    const usersLoginEndpoint = document.getElementById("users-login").getAttribute("data-url");
    const blogsPage = document.getElementById("web-blogs").getAttribute("data-url");
    console.log(`Sending request to ${this.action}`);

    const formData = new FormData(e.target);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });
    fetch(usersLoginEndpoint, {
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
            if (data.error) {
                alert(data.error);
            } else {
                console.log(data);
                access_token = data.access;
                refresh_token = data.refresh;
                is_superuser = data.is_superuser;
                localStorage.setItem("access_token", `Bearer  ${access_token}`);
                localStorage.setItem("refresh_token", refresh_token);
                localStorage.setItem("is_superuser", is_superuser);
                console.log(access_token);
                console.log(refresh_token);
                window.location.href = blogsPage;
            }
        });
});
