// TOGGLE CHATBOX
const chatboxToggle = document.querySelector('.chatbox-toggle');
const chatboxMessage = document.querySelector('.chatbox-message-wrapper');

chatboxToggle.addEventListener('click', function () {
    chatboxMessage.classList.toggle('show');
});

// DROPDOWN TOGGLE
const dropdownToggle = document.querySelector('.chatbox-message-dropdown-toggle');
const dropdownMenu = document.querySelector('.chatbox-message-dropdown-menu');

dropdownToggle.addEventListener('click', function () {
    dropdownMenu.classList.toggle('show');
});

document.addEventListener('click', function (e) {
    if (!e.target.matches('.chatbox-message-dropdown, .chatbox-message-dropdown *')) {
        dropdownMenu.classList.remove('show');
    }
});

// Keep chatbox open after response (assuming responseButton is a button triggering the response generation)
const responseButton = document.querySelector('#responseButton'); // Replace #responseButton with the actual ID or selector of your button

responseButton.addEventListener('click', function (e) {
    // Assuming you have elements for question and response
    const questionElement = document.querySelector('.chatbox-message-content .chatbox-message-no-message');
    const responseElement = document.querySelector('.chatbox-message-content .chatbox-message-item-text');

    // Replace this with your logic to generate a response
    const response = "This is a sample response.";

    // Update the elements with the generated response
    questionElement.textContent = "Your Question: " + "What's the meaning of life?";
    responseElement.textContent = "Response: " + response;

    // Keep the chatbox open after the response
    chatboxMessage.classList.add('show');

    // Prevent the default behavior of the button (you may not need this depending on your setup)
    e.preventDefault();
});
