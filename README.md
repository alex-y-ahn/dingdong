# Dingdong🔔: Brain Dump Repository 
일과 중 자기관찰을 위한 빠른 메모 트래킹 프로그램

## 📌 프로젝트 소개
업무나 학습 중 떠오르는 생각, 할 일, 자기관찰 내용을 빠르게 기록하기 위한 데스크톱 애플리케이션입니다.
전역 단축키로 언제든 메모를 남기고, 시간대별로 누적된 데이터를 분석할 수 있습니다.

## ✨ 주요 기능
- **🚀 빠른 입력**: `Ctrl+Space`로 즉시 메모창 호출
- **📊 분류 관리**: 잡생각 / 할일 / 자기관찰 3가지 카테고리
- **⏰ 자동 타임스탬프**: 모든 기록에 시간 자동 저장
- **🔍 필터링 조회**: 날짜별, 분류별 필터링 지원
- **💾 데이터 추출**: TXT 형식으로 내보내기
- **🌙 백그라운드 실행**: 시스템 트레이에서 상시 대기

## 🎯 개발 동기
- 일하면서 떠오르는 생각들을 빠르게 기록하고 싶었음
- 시간대별 사고 패턴과 컨디션을 분석하고 싶었음

## 🛠️ 기술 스택
- **Language**: Python 3.x
- **GUI**: Tkinter
- **단축키**: pynput
- **패키징**: PyInstaller

## 📦 설치 및 실행
### 필요 패키지 설치
```bash
pip install pynput
```

### 실행 방법
```bash
python dingdong.py
```

### EXE 파일 생성
```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed dingdong.py
```

### 시작프로그램 등록
1. `Win + R` → `shell:startup`
2. `dingdong.exe` 파일을 해당 폴더에 복사
3. 재부팅 시 자동 실행

## 🎮 사용법
### 단축키
- `Ctrl + Space`: 입력창 열기
- `Ctrl + Shift + Space`: 조회창 열기
- `ESC`: 입력창 닫기

### 메모 입력
1. `Ctrl + Space`로 입력창 호출
2. 내용 입력
3. 마지막에 분류 번호 입력:
   - `1` + Enter: 잡생각
   - `2` + Enter: 할일
   - `3` + Enter: 자기관찰
4. '띵' 소리와 함께 저장 완료

### 데이터 조회
- 날짜 필터: 오늘 / 어제 / 최근 7일 / 전체
- 분류 필터: 전체 / 잡생각 / 할일 / 자기관찰
- TXT 추출: 필터링된 데이터를 파일로 저장
- 데이터 리셋: 모든 기록 삭제

## 📁 데이터 저장 위치

```
C:\Users\사용자명\Documents\tracking_data.json
```

## 🤝 개발 과정
1. 요구사항 정의 및 기능 기획
2. Claude AI를 활용한 바이브코딩
- Python/Tkinter를 활용한 GUI 구현
- 전역 단축키 구현 (pynput)
- 데이터 저장 및 필터링 로직 구현
- PyInstaller를 통한 실행 파일 배포

## 📝 라이선스
Claude
개인 프로젝트 - 자유롭게 사용 및 수정 가능
