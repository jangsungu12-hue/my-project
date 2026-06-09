import { CalculatorState, Operator } from "./calculator.js";

const state = new CalculatorState();
const display = document.getElementById("display") as HTMLDivElement;

function render(): void {
  display.textContent = state.getDisplay();
}

function handleAction(action: string, value: string): void {
  switch (action) {
    case "digit":
      state.inputDigit(value);
      break;
    case "decimal":
      state.inputDecimal();
      break;
    case "operator":
      state.inputOperator(value as Operator);
      break;
    case "equals":
      state.evaluate();
      break;
    case "clear":
      state.clear();
      break;
    case "sign":
      state.toggleSign();
      break;
  }
  render();
}

document.querySelectorAll<HTMLButtonElement>("button[data-action]").forEach((btn) => {
  btn.addEventListener("click", () => {
    const action = btn.dataset.action ?? "";
    const value = btn.dataset.value ?? btn.textContent ?? "";
    handleAction(action, value);
  });
});

document.addEventListener("keydown", (e) => {
  if (/^[0-9]$/.test(e.key)) {
    handleAction("digit", e.key);
  } else if (["+", "-", "*", "/"].includes(e.key)) {
    handleAction("operator", e.key);
  } else if (e.key === "Enter" || e.key === "=") {
    e.preventDefault();
    handleAction("equals", "");
  } else if (e.key === ".") {
    handleAction("decimal", "");
  } else if (e.key === "Escape") {
    handleAction("clear", "");
  }
});

render();
