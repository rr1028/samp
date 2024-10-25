document.getElementById("registrationForm").addEventListener("submit", function(event) {
    event.preventDefault();
  
    // Get the user input values
    const name = document.getElementById("name").value;
    const bloodType = document.getElementById("bloodType").value;
    const height = document.getElementById("height").value;
    const weight = document.getElementById("weight").value;
    const allergies = document.getElementById("allergies").value;
    const diagnosis = document.getElementById("diagnosis").value;
  
    // Store the input data in localStorage
    localStorage.setItem("name", name);
    localStorage.setItem("bloodType", bloodType);
    localStorage.setItem("height", height);
    localStorage.setItem("weight", weight);
    localStorage.setItem("allergies", allergies);
    localStorage.setItem("diagnosis", diagnosis);
  
    // Redirect to index.html
    window.location.href = "login.html";
  });
  