
function admin_login(event) {
    event.preventDefault();
    const admin_email = document.getElementById("admin-email").value;
    const admin_password = document.getElementById("admin-password").value;

    fetch(`http://127.0.0.1:5000/admin/login`, {
        method: 'POST',
        body: JSON.stringify({ email: admin_email, password: admin_password }),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Invalid email or password");
        }
        return response.json();
    })
    .then(data => {
        localStorage.setItem("token", JSON.stringify(data.access_token));
        window.location.href = "admin_main.html";
    })
    .catch(error => {
        // Handle error (e.g., display an error message to the user)
        console.error(error.message);
        alert("Invalid email or password. Please try again.");
        window.location.href = "admin_signin.html"; // or whatever your sign-in page URL is
    
    });
}
function customer_login(event) {
    event.preventDefault();
    const customer_email = document.getElementById("customer_email").value;
    const customer_password = document.getElementById("customer_password").value;

    fetch(`http://127.0.0.1:5000/customer/login`, {
        method: 'POST',
        body: JSON.stringify({ email: customer_email, password: customer_password }),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Invalid email or password");
        }
        return response.json();
    })
    .then(data => {
        localStorage.setItem("customer_token", JSON.stringify(data.access_token));
        localStorage.setItem("customer_id", JSON.stringify(data));
        window.location.href = "customer_main.html";
    })
    .catch(error => {
        console.error(error.message);
        alert("Invalid email or password. Please try again.");
        window.location.href = "customer_signin.html"; 
    });

}
