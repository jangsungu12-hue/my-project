export type Operator = "+" | "-" | "*" | "/";

export function compute(a: number, op: Operator, b: number): number {
  switch (op) {
    case "+":
      return a + b;
    case "-":
      return a - b;
    case "*":
      return a * b;
    case "/":
      if (b === 0) {
        throw new Error("0으로 나눌 수 없습니다.");
      }
      return a / b;
  }
}

export function formatNumber(value: number): string {
  if (!Number.isFinite(value)) {
    return "오류";
  }
  if (Number.isInteger(value)) {
    return value.toString();
  }
  return parseFloat(value.toPrecision(12)).toString();
}

export class CalculatorState {
  private display: string = "0";
  private accumulator: number | null = null;
  private pendingOp: Operator | null = null;
  private resetOnNextDigit: boolean = false;
  private errored: boolean = false;

  getDisplay(): string {
    return this.display;
  }

  inputDigit(digit: string): void {
    if (this.errored) {
      this.clear();
    }
    if (this.resetOnNextDigit || this.display === "0") {
      this.display = digit;
      this.resetOnNextDigit = false;
    } else {
      this.display += digit;
    }
  }

  inputDecimal(): void {
    if (this.errored) {
      this.clear();
    }
    if (this.resetOnNextDigit) {
      this.display = "0.";
      this.resetOnNextDigit = false;
      return;
    }
    if (!this.display.includes(".")) {
      this.display += ".";
    }
  }

  inputOperator(op: Operator): void {
    if (this.errored) {
      return;
    }
    const current = parseFloat(this.display);
    if (this.accumulator === null) {
      this.accumulator = current;
    } else if (this.pendingOp !== null && !this.resetOnNextDigit) {
      try {
        this.accumulator = compute(this.accumulator, this.pendingOp, current);
        this.display = formatNumber(this.accumulator);
      } catch (e) {
        this.setError((e as Error).message);
        return;
      }
    }
    this.pendingOp = op;
    this.resetOnNextDigit = true;
  }

  evaluate(): void {
    if (this.errored || this.accumulator === null || this.pendingOp === null) {
      return;
    }
    const current = parseFloat(this.display);
    try {
      const result = compute(this.accumulator, this.pendingOp, current);
      this.display = formatNumber(result);
      this.accumulator = null;
      this.pendingOp = null;
      this.resetOnNextDigit = true;
    } catch (e) {
      this.setError((e as Error).message);
    }
  }

  toggleSign(): void {
    if (this.errored || this.display === "0") {
      return;
    }
    this.display = this.display.startsWith("-")
      ? this.display.slice(1)
      : "-" + this.display;
  }

  clear(): void {
    this.display = "0";
    this.accumulator = null;
    this.pendingOp = null;
    this.resetOnNextDigit = false;
    this.errored = false;
  }

  private setError(message: string): void {
    this.display = message;
    this.accumulator = null;
    this.pendingOp = null;
    this.resetOnNextDigit = false;
    this.errored = true;
  }
}
