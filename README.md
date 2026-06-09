# 계산기

TypeScript로 작성된 웹 계산기입니다.

## TypeScript 웹 계산기

버튼 UI와 디스플레이를 갖춘 사칙연산 계산기입니다. 키보드 입력(`0-9`, `+-*/`, `Enter`, `.`, `Esc`)도 지원합니다.

### 실행

```bash
npm install
npm run build
python3 -m http.server 8000
# 또는
npm start
```

서버를 띄운 뒤 http://localhost:8000 으로 접속하세요.

### 구조

- `index.html` — 페이지와 버튼 마크업
- `styles.css` — 스타일
- `src/calculator.ts` — 계산기 상태/연산 로직
- `src/main.ts` — DOM 이벤트 처리
- `dist/` — `tsc` 컴파일 결과물
