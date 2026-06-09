type Token =
    | { type: "number"; value: number }
    | { type: "op"; value: "+" | "-" | "*" | "/" }
    | { type: "lparen" }
    | { type: "rparen" };

const display = document.getElementById("display") as HTMLDivElement;
let expression = "";

function render(): void {
    display.textContent = expression === "" ? "0" : expression;
}

function appendValue(value: string): void {
    expression += value;
    render();
}

function clearAll(): void {
    expression = "";
    render();
}

function backspace(): void {
    expression = expression.slice(0, -1);
    render();
}

function tokenize(input: string): Token[] {
    const tokens: Token[] = [];
    let i = 0;
    while (i < input.length) {
        const ch = input[i];
        if (ch === " ") {
            i++;
            continue;
        }
        if (ch === "(") {
            tokens.push({ type: "lparen" });
            i++;
            continue;
        }
        if (ch === ")") {
            tokens.push({ type: "rparen" });
            i++;
            continue;
        }
        if (ch === "+" || ch === "-" || ch === "*" || ch === "/") {
            const isUnary =
                ch === "-" &&
                (tokens.length === 0 ||
                    tokens[tokens.length - 1].type === "op" ||
                    tokens[tokens.length - 1].type === "lparen");
            if (isUnary) {
                let j = i + 1;
                let numStr = "-";
                while (j < input.length && /[0-9.]/.test(input[j])) {
                    numStr += input[j];
                    j++;
                }
                if (numStr === "-") {
                    throw new Error("잘못된 표현식입니다.");
                }
                const num = parseFloat(numStr);
                if (Number.isNaN(num)) {
                    throw new Error("숫자를 해석할 수 없습니다.");
                }
                tokens.push({ type: "number", value: num });
                i = j;
                continue;
            }
            tokens.push({ type: "op", value: ch });
            i++;
            continue;
        }
        if (/[0-9.]/.test(ch)) {
            let numStr = "";
            while (i < input.length && /[0-9.]/.test(input[i])) {
                numStr += input[i];
                i++;
            }
            const num = parseFloat(numStr);
            if (Number.isNaN(num)) {
                throw new Error("숫자를 해석할 수 없습니다.");
            }
            tokens.push({ type: "number", value: num });
            continue;
        }
        throw new Error(`알 수 없는 문자: ${ch}`);
    }
    return tokens;
}

function toRPN(tokens: Token[]): Token[] {
    const output: Token[] = [];
    const stack: Token[] = [];
    const precedence: Record<string, number> = { "+": 1, "-": 1, "*": 2, "/": 2 };

    for (const token of tokens) {
        if (token.type === "number") {
            output.push(token);
        } else if (token.type === "op") {
            while (stack.length > 0) {
                const top = stack[stack.length - 1];
                if (top.type === "op" && precedence[top.value] >= precedence[token.value]) {
                    output.push(stack.pop()!);
                } else {
                    break;
                }
            }
            stack.push(token);
        } else if (token.type === "lparen") {
            stack.push(token);
        } else if (token.type === "rparen") {
            let matched = false;
            while (stack.length > 0) {
                const top = stack.pop()!;
                if (top.type === "lparen") {
                    matched = true;
                    break;
                }
                output.push(top);
            }
            if (!matched) {
                throw new Error("괄호가 맞지 않습니다.");
            }
        }
    }

    while (stack.length > 0) {
        const top = stack.pop()!;
        if (top.type === "lparen" || top.type === "rparen") {
            throw new Error("괄호가 맞지 않습니다.");
        }
        output.push(top);
    }

    return output;
}

function evalRPN(rpn: Token[]): number {
    const stack: number[] = [];
    for (const token of rpn) {
        if (token.type === "number") {
            stack.push(token.value);
            continue;
        }
        if (token.type !== "op") {
            throw new Error("잘못된 표현식입니다.");
        }
        const b = stack.pop();
        const a = stack.pop();
        if (a === undefined || b === undefined) {
            throw new Error("잘못된 표현식입니다.");
        }
        switch (token.value) {
            case "+":
                stack.push(a + b);
                break;
            case "-":
                stack.push(a - b);
                break;
            case "*":
                stack.push(a * b);
                break;
            case "/":
                if (b === 0) {
                    throw new Error("0으로 나눌 수 없습니다.");
                }
                stack.push(a / b);
                break;
        }
    }
    if (stack.length !== 1) {
        throw new Error("잘못된 표현식입니다.");
    }
    return stack[0];
}

function formatResult(value: number): string {
    if (Number.isInteger(value)) {
        return value.toString();
    }
    return parseFloat(value.toFixed(10)).toString();
}

function evaluate(): void {
    if (expression === "") {
        return;
    }
    try {
        const tokens = tokenize(expression);
        const rpn = toRPN(tokens);
        const result = evalRPN(rpn);
        expression = formatResult(result);
        render();
    } catch (err) {
        const message = err instanceof Error ? err.message : "오류";
        display.textContent = `오류: ${message}`;
        expression = "";
    }
}

document.querySelectorAll<HTMLButtonElement>("button").forEach((btn) => {
    btn.addEventListener("click", () => {
        const value = btn.dataset.value;
        const action = btn.dataset.action;

        if (value !== undefined) {
            appendValue(value);
            return;
        }
        if (action === "clear") {
            clearAll();
            return;
        }
        if (action === "backspace") {
            backspace();
            return;
        }
        if (action === "equals") {
            evaluate();
            return;
        }
    });
});

document.addEventListener("keydown", (e) => {
    if (e.ctrlKey || e.metaKey || e.altKey) {
        return;
    }

    const key = e.key;

    if (/^[0-9]$/.test(key) || key === "." || key === "+" || key === "-" || key === "*" || key === "/" || key === "(" || key === ")") {
        e.preventDefault();
        appendValue(key);
        return;
    }
    if (key === "Enter" || key === "=") {
        e.preventDefault();
        evaluate();
        return;
    }
    if (key === "Backspace") {
        e.preventDefault();
        backspace();
        return;
    }
    if (key === "Escape" || key === "c" || key === "C") {
        e.preventDefault();
        clearAll();
        return;
    }
});

render();
