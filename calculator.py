"""사칙연산 계산기."""


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


OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}


def calculate(a: float, op: str, b: float) -> float:
    if op not in OPERATIONS:
        raise ValueError(f"지원하지 않는 연산자입니다: {op}")
    return OPERATIONS[op](a, b)


def format_result(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return str(value)


def main() -> None:
    print("사칙연산 계산기 (종료: q)")
    print("형식: <숫자> <연산자(+,-,*,/)> <숫자>  예) 3 + 4")

    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line:
            continue
        if line.lower() in {"q", "quit", "exit"}:
            break

        parts = line.split()
        if len(parts) != 3:
            print("입력 형식이 올바르지 않습니다. 예) 3 + 4")
            continue

        a_str, op, b_str = parts
        try:
            a = float(a_str)
            b = float(b_str)
        except ValueError:
            print("숫자를 올바르게 입력해 주세요.")
            continue

        try:
            result = calculate(a, op, b)
        except (ZeroDivisionError, ValueError) as e:
            print(f"오류: {e}")
            continue

        print(format_result(result))


if __name__ == "__main__":
    main()
