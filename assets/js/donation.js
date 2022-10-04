//https://stackoverflow.com/questions/41725725/access-css-variable-from-javascript
const primaryColor = '#00da5b';
const disableColor = '#e5e5e5';
const OtherInput = document.querySelector('#value-other');
const labelOtherInput = document.querySelector('label[for=value-other]');
const Buttons = document.querySelectorAll('.donation-value input[type=radio]');

OtherInput.addEventListener('click', () => {changeBackground(); uncheckRadioButtons();});

OtherInput.addEventListener('input', clearInput);

Buttons.forEach(button => button.addEventListener('click', () => {
    OtherInput.value = null;
    labelOtherInput.style.backgroundColor = disableColor;
    labelOtherInput.style.color = '#ababab';
}));

function changeBackground(){
    labelOtherInput.style.backgroundColor = primaryColor;
    labelOtherInput.style.color = '#fff';
}

function uncheckRadioButtons() {
    Buttons.forEach(button => button.checked = false);
}

function clearInput(){
    if (!OtherInput.value) {
        Buttons[0].checked = true; 
    }
}