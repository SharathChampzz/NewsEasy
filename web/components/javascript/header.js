document.getElementById("logout").addEventListener("click", function (e) {
  e.preventDefault();
  const endpoint = e.target.getAttribute("logout-url");
  console.log("Logout endpoint In Header File:", endpoint);

  fetch(endpoint, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      // Authorization: localStorage.getItem("access_token")
    },
    body: JSON.stringify({ refresh: localStorage.getItem("refresh_token")}),
  })
    .then((response) => response.json())
    .then((data) => {
    console.log("Logout Response:", data);
      console.log(data);
      if(data.error){
        alert(data.error)
      }
      else{
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          window.location.href = "/users/login";
      }
      // }
    })
    .catch((error) => {
      console.log("Redirecting to Login Page: ", "/users/login");
    //   window.location.href = "/users/login";
      console.error("Error:", error);
    });
});
