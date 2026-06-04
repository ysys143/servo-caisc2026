# CAISc 2026 — Servo 논문 작업 규칙

## 컴파일 및 산출물 관리

작업 단위(여러 편집이 하나의 목적으로 묶인 경우)가 완료되면 반드시 다음 순서를 직접 실행한다. 사소한 수정마다 돌리지 말 것.

### 1. 컴파일
```bash
cd /Users/jaesolshin/Documents/GitHub/CAISc_2026/submission
/usr/local/texlive/2026basic/bin/universal-darwin/bibtex main
/usr/local/texlive/2026basic/bin/universal-darwin/xelatex -interaction=nonstopmode main.tex
```
"Output written on main.pdf"와 오류 없음을 확인한다.

### 2. PDF 파일명 복사
```bash
cp submission/main.pdf submission/servo_caiscfp2026.pdf
```

### 3. 보충자료 ZIP 재생성
```bash
cd submission
zip -r caisc2026-servo-supplement.zip analysis/ references.bib --exclude "analysis/multicoder/.omc/*" "analysis/texput.log"
```

## 기타 규칙

- 이메일 주소를 어떤 외부 요청(curl, API 호출 등)에도 포함하지 않는다.
- 보충자료(`analysis/`) 파일이 변경되면 ZIP도 반드시 재생성한다.
