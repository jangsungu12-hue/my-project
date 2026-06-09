"""사칙연산 계산기."""

from __future__ import annotations

import operator
import sys
from typing import Callable


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("0으로 나눌 수 없습니다.")
    return a / b


OPERATIONS: dict[str, Callable[[float, float], float]] = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}


def calculate(a: float, op: str, b: float) -> float:
    if op not in OPERATIONS:
        raise ValueError(f"지원하지 않는 연산자입니다: {op!r} (사용 가능: +, -, *, /)")
    return OPERATIONS[op](a, b)


def _format(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return str(value)


def repl() -> None:
    print("사칙연산 계산기 (종료: 'q' 또는 Ctrl+D)")
    print("입력 형식: <숫자> <연산자> <숫자>   예) 3 + 4")
    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            print()
            return
        if not line:
            continue
        if line.lower() in {"q", "quit", "exit"}:
            return
        parts = line.split()
        if len(parts) != 3:
            print("형식이 올바르지 않습니다. 예: 3 + 4")
            continue
        a_str, op, b_str = parts
        try:
            a = float(a_str)
            b = float(b_str)
            result = calculate(a, op, b)
        except ValueError as e:
            print(f"오류: {e}")
            continue
        except ZeroDivisionError as e:
            print(f"오류: {e}")
            continue
        print(_format(result))


def main(argv: list[str]) -> int:
    if len(argv) == 1:
        repl()
        return 0
    if len(argv) == 4:
        try:
            a = float(argv[1])
            b = float(argv[3])
            result = calculate(a, argv[2], b)
        except (ValueError, ZeroDivisionError) as e:
            print(f"오류: {e}", file=sys.stderr)
            return 1
        print(_format(result))
        return 0
    print("사용법: python calculator.py [<숫자> <연산자> <숫자>]", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
