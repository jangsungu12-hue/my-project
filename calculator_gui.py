"""GUI 계산기 (tkinter).

식을 화면에 그대로 보여주면서 사칙연산과 괄호를 사용할 수 있다.
"""

import ast
import operator as op
import tkinter as tk
from tkinter import font


_BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
}

_UNARY_OPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}


def evaluate(expression: str) -> float:
    """파이썬 식을 안전하게 평가한다. +, -, *, /, 괄호, 단항 부호만 허용."""
    tree = ast.parse(expression, mode="eval")
    return _eval_node(tree.body)


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("숫자만 사용할 수 있습니다.")
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _BIN_OPS:
            raise ValueError("지원하지 않는 연산자입니다.")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if op_type is ast.Div and right == 0:
            raise ZeroDivisionError("0으로 나눌 수 없습니다.")
        return _BIN_OPS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _UNARY_OPS:
            raise ValueError("지원하지 않는 연산자입니다.")
        return _UNARY_OPS[op_type](_eval_node(node.operand))
    raise ValueError("지원하지 않는 식입니다.")


def format_result(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return str(value)


class CalculatorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("계산기")
        self.root.resizable(False, False)
        self.root.configure(bg="#1f1f1f")

        self.expression = ""
        self.result_shown = False

        self._build_display()
        self._build_buttons()

        self.root.bind("<Key>", self._on_key)

    def _build_display(self) -> None:
        display_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.display_var = tk.StringVar(value="0")
        display = tk.Label(
            self.root,
            textvariable=self.display_var,
            font=display_font,
            bg="#1f1f1f",
            fg="#ffffff",
            anchor="e",
            padx=16,
            pady=20,
            width=16,
        )
        display.grid(row=0, column=0, columnspan=5, sticky="nsew")

    def _build_buttons(self) -> None:
        btn_font = font.Font(family="Helvetica", size=14, weight="bold")

        layout = [
            [("C", "clear"), ("⌫", "back"), ("(", "paren"), (")", "paren"), ("/", "op")],
            [("7", "digit"), ("8", "digit"), ("9", "digit"), ("*", "op"), ("", "spacer")],
            [("4", "digit"), ("5", "digit"), ("6", "digit"), ("-", "op"), ("", "spacer")],
            [("1", "digit"), ("2", "digit"), ("3", "digit"), ("+", "op"), ("", "spacer")],
            [("0", "digit_wide"), (".", "dot"), ("=", "equals"), ("", "spacer")],
        ]

        colors = {
            "digit": ("#333333", "#ffffff"),
            "digit_wide": ("#333333", "#ffffff"),
            "dot": ("#333333", "#ffffff"),
            "op": ("#ff9500", "#ffffff"),
            "paren": ("#a5a5a5", "#000000"),
            "equals": ("#ff9500", "#ffffff"),
            "clear": ("#a5a5a5", "#000000"),
            "back": ("#a5a5a5", "#000000"),
        }

        for r, row in enumerate(layout, start=1):
            c = 0
            for label, kind in row:
                if kind == "spacer":
                    c += 1
                    continue
                bg, fg = colors[kind]
                colspan = 2 if kind == "digit_wide" else 1
                btn = tk.Button(
                    self.root,
                    text=label,
                    font=btn_font,
                    bg=bg,
                    fg=fg,
                    activebackground=bg,
                    activeforeground=fg,
                    bd=0,
                    width=4 if colspan == 1 else 9,
                    height=2,
                    command=lambda l=label, k=kind: self._on_button(l, k),
                )
                btn.grid(row=r, column=c, columnspan=colspan, sticky="nsew", padx=1, pady=1)
                c += colspan

        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)

    def _render(self) -> None:
        self.display_var.set(self.expression if self.expression else "0")

    def _append(self, text: str) -> None:
        if self.result_shown:
            # 결과가 보이는 상태에서 숫자나 여는 괄호를 누르면 새 식, 연산자/닫는 괄호는 이어쓰기.
            if text.isdigit() or text == "." or text == "(":
                self.expression = ""
            self.result_shown = False
        self.expression += text
        self._render()

    def _on_button(self, label: str, kind: str) -> None:
        if kind in ("digit", "digit_wide"):
            self._append(label)
        elif kind == "dot":
            self._append(".")
        elif kind == "op":
            if self.result_shown:
                self.result_shown = False
            self.expression += label
            self._render()
        elif kind == "paren":
            self._append(label)
        elif kind == "equals":
            self._compute()
        elif kind == "clear":
            self.expression = ""
            self.result_shown = False
            self._render()
        elif kind == "back":
            if self.result_shown:
                self.expression = ""
                self.result_shown = False
            elif self.expression:
                self.expression = self.expression[:-1]
            self._render()

    def _compute(self) -> None:
        if not self.expression:
            return
        try:
            value = evaluate(self.expression)
            self.expression = format_result(value)
        except ZeroDivisionError:
            self.expression = "오류: 0으로 나눌 수 없습니다"
        except (SyntaxError, ValueError):
            self.expression = "오류: 식을 확인해 주세요"
        self.result_shown = True
        self._render()

    def _on_key(self, event: tk.Event) -> None:
        ch = event.char
        keysym = event.keysym
        if ch.isdigit():
            self._append(ch)
        elif ch == ".":
            self._append(".")
        elif ch in "+-*/":
            self._on_button(ch, "op")
        elif ch in "()":
            self._append(ch)
        elif keysym in ("Return", "equal") or ch == "=":
            self._compute()
        elif keysym in ("Escape", "Delete"):
            self._on_button("C", "clear")
        elif keysym == "BackSpace":
            self._on_button("⌫", "back")


def main() -> None:
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
