def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("0으로 나눌 수 없습니다.")
    return a / b


OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}


def calculate(a, op, b):
    if op not in OPERATIONS:
        raise ValueError(f"지원하지 않는 연산자입니다: {op}")
    return OPERATIONS[op](a, b)


def main():
    print("계산기 프로그램 (종료: q)")
    print("사용법: 숫자 연산자(+,-,*,/) 숫자  예) 3 + 5")

    while True:
        line = input("> ").strip()
        if line.lower() in ("q", "quit", "exit"):
            print("종료합니다.")
            break

        parts = line.split()
        if len(parts) != 3:
            print("형식이 올바르지 않습니다. 예) 3 + 5")
            continue

        try:
            a = float(parts[0])
            op = parts[1]
            b = float(parts[2])
            result = calculate(a, op, b)
        except ValueError as e:
            print(f"오류: {e}")
            continue
        except ZeroDivisionError as e:
            print(f"오류: {e}")
            continue

        if result == int(result):
            result = int(result)
        print(f"= {result}")


if __name__ == "__main__":
    main()
