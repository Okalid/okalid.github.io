// Function to calculate a discount based on the selected contact method
function calculateDiscount() {
    // Get the elements from the form
    const contactMethod = document.getElementById("contactMethod");
    const checkbox = document.getElementById("checkbox");
    const resultElement = document.getElementById("calculationResult");

    // Define your specific calculation here
    // For example, a 10% discount if the user selects "email" and checks the checkbox
    let discount = 0;
    if (contactMethod.value === "email" && checkbox.checked) {
        discount = 0.10; // 10% discount
    }

    // Calculate the total and display it
    const total = 100 - (discount * 100); // Assuming the initial cost is $100
    resultElement.innerText = `Total cost: $${total}`;
    
    // set it's display to block to make it visible
    resultElement.style.display = "block";
}

// Add event listeners for change events
document.getElementById("contactMethod").addEventListener("change", calculateDiscount);
document.getElementById("checkbox").addEventListener("change", calculateDiscount);
