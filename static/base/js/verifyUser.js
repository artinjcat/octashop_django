const button = document.querySelector("button");
let arrayInputs = [];
arrayInputs = document.querySelectorAll(".inputVerify");
arrayInputs.forEach((input, index1) => {
  input.addEventListener("keyup", (e) => {
    const currentInput = input,
      nextInput = input.nextElementSibling,
      prevInput = input.previousElementSibling;
    if (currentInput.value.length > 1) {
      currentInput.value = "";
      return;
    }
    if (
      nextInput &&
      nextInput.hasAttribute("disabled") &&
      currentInput.value !== ""
    ) {
      nextInput.removeAttribute("disabled");
      nextInput.focus();
    }
    if (e.key === "Backspace") {
      arrayInputs.forEach((input, index2) => {
        if (index1 <= index2 && prevInput) {
          input.setAttribute("disabled", true);
          input.value = "";
          prevInput.focus();
        }
      });
    }
    if (!arrayInputs[4].disabled && arrayInputs[4].value !== "") {
      button.classList.add("active");
      return;
    }
    button.classList.remove("active");
  });

});

const digitsInput = document.querySelector("input[name='digits']");
function updateDigitsInput() {
  const digits = Array.from(arrayInputs)
    .map((input) => input.value)
    .join("");
  digitsInput.value = digits;
}
arrayInputs.forEach((input) => {
  input.addEventListener("input", updateDigitsInput);
  console.log("digits: ", digitsInput.value);
});


window.addEventListener("load", () => arrayInputs[0].focus());
