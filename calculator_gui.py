"""GUI 계산기 (tkinter)."""

import tkinter as tk
from tkinter import font

from calculator import OPERATIONS, calculate, format_result


class CalculatorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("계산기")
        self.root.resizable(False, False)
        self.root.configure(bg="#1f1f1f")

        self.current = "0"
        self.stored: float | None = None
        self.pending_op: str | None = None
        self.reset_on_next_digit = False

        self._build_display()
        self._build_buttons()

        self.root.bind("<Key>", self._on_key)

    def _build_display(self) -> None:
        display_font = font.Font(family="Helvetica", size=28, weight="bold")
        self.display_var = tk.StringVar(value=self.current)
        display = tk.Label(
            self.root,
            textvariable=self.display_var,
            font=display_font,
            bg="#1f1f1f",
            fg="#ffffff",
            anchor="e",
            padx=16,
            pady=20,
            width=12,
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew")

    def _build_buttons(self) -> None:
        btn_font = font.Font(family="Helvetica", size=16, weight="bold")

        layout = [
            [("C", "clear"), ("±", "neg"), ("%", "pct"), ("/", "op")],
            [("7", "digit"), ("8", "digit"), ("9", "digit"), ("*", "op")],
            [("4", "digit"), ("5", "digit"), ("6", "digit"), ("-", "op")],
            [("1", "digit"), ("2", "digit"), ("3", "digit"), ("+", "op")],
            [("0", "digit_wide"), (".", "dot"), ("=", "equals")],
        ]

        colors = {
            "digit": ("#333333", "#ffffff"),
            "digit_wide": ("#333333", "#ffffff"),
            "dot": ("#333333", "#ffffff"),
            "op": ("#ff9500", "#ffffff"),
            "equals": ("#ff9500", "#ffffff"),
            "clear": ("#a5a5a5", "#000000"),
            "neg": ("#a5a5a5", "#000000"),
            "pct": ("#a5a5a5", "#000000"),
        }

        for r, row in enumerate(layout, start=1):
            c = 0
            for label, kind in row:
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

        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

    def _set_display(self, text: str) -> None:
        self.current = text
        self.display_var.set(text)

    def _on_button(self, label: str, kind: str) -> None:
        if kind in ("digit", "digit_wide"):
            self._input_digit(label)
        elif kind == "dot":
            self._input_dot()
        elif kind == "op":
            self._input_operator(label)
        elif kind == "equals":
            self._compute()
        elif kind == "clear":
            self._clear()
        elif kind == "neg":
            self._negate()
        elif kind == "pct":
            self._percent()

    def _input_digit(self, d: str) -> None:
        if self.reset_on_next_digit or self.current == "0" or self.current == "Error":
            self._set_display(d)
            self.reset_on_next_digit = False
        else:
            self._set_display(self.current + d)

    def _input_dot(self) -> None:
        if self.reset_on_next_digit or self.current == "Error":
            self._set_display("0.")
            self.reset_on_next_digit = False
            return
        if "." not in self.current:
            self._set_display(self.current + ".")

    def _input_operator(self, op: str) -> None:
        if self.current == "Error":
            return
        try:
            value = float(self.current)
        except ValueError:
            return

        if self.pending_op is not None and not self.reset_on_next_digit:
            try:
                value = calculate(self.stored if self.stored is not None else 0.0, self.pending_op, value)
            except (ZeroDivisionError, ValueError):
                self._set_error()
                return
            self._set_display(format_result(value))

        self.stored = value
        self.pending_op = op
        self.reset_on_next_digit = True

    def _compute(self) -> None:
        if self.pending_op is None or self.stored is None or self.current == "Error":
            return
        try:
            value = float(self.current)
            result = calculate(self.stored, self.pending_op, value)
        except (ZeroDivisionError, ValueError):
            self._set_error()
            return
        self._set_display(format_result(result))
        self.stored = None
        self.pending_op = None
        self.reset_on_next_digit = True

    def _clear(self) -> None:
        self.stored = None
        self.pending_op = None
        self.reset_on_next_digit = False
        self._set_display("0")

    def _negate(self) -> None:
        if self.current == "Error" or self.current == "0":
            return
        if self.current.startswith("-"):
            self._set_display(self.current[1:])
        else:
            self._set_display("-" + self.current)

    def _percent(self) -> None:
        if self.current == "Error":
            return
        try:
            value = float(self.current) / 100
        except ValueError:
            return
        self._set_display(format_result(value))

    def _set_error(self) -> None:
        self.stored = None
        self.pending_op = None
        self.reset_on_next_digit = True
        self._set_display("Error")

    def _on_key(self, event: tk.Event) -> None:
        ch = event.char
        keysym = event.keysym
        if ch.isdigit():
            self._input_digit(ch)
        elif ch == ".":
            self._input_dot()
        elif ch in OPERATIONS:
            self._input_operator(ch)
        elif keysym in ("Return", "equal") or ch == "=":
            self._compute()
        elif keysym in ("Escape", "Delete") or ch.lower() == "c":
            self._clear()
        elif keysym == "BackSpace":
            if self.current == "Error":
                self._clear()
            elif len(self.current) > 1:
                self._set_display(self.current[:-1])
            else:
                self._set_display("0")


def main() -> None:
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
