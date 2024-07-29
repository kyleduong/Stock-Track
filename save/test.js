// Ensure the DOM is fully loaded before attaching event listeners
document.addEventListener('DOMContentLoaded', (event) => {
    // Select the button using its ID
    const alertButton = document.getElementById('alertButton');
    
    // Attach a click event listener to the button
    alertButton.addEventListener('click', () => {
        // Display an alert when the button is clicked
        alert('Hello! This is an alert.');
    });
});