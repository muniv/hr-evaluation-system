# AI 기반 인사 평가 시스템

이 프로젝트는 그라디오(Gradio)와 OpenAI의 GPT-4o를 활용하여 인사 평가를 객관화하고 효율화하는 데모입니다.

## 기능

1. 이름 입력 시 해당 직원의 직무 정보와 평가해야 할 스킬 표시
2. 평가자가 작성한 내용을 분석하여 해당 직원의 장점, 단점, 핵심 키워드 추출
3. 평가 결과를 기반으로 스킬 그래프 시각화

## 설치 및 실행

1. 저장소 클론 또는 다운로드 후 프로젝트 디렉토리로 이동
   ```bash
   git clone [repository-url]
   cd [project-directory]
   ```

2. 가상 환경 생성 및 활성화 (선택사항이지만 권장)
   ```bash
   # 가상 환경 생성
   python -m venv venv
   
   # 가상 환경 활성화 (Windows)
   venv\Scripts\activate
   
   # 가상 환경 활성화 (macOS/Linux)
   source venv/bin/activate
   ```

3. 필요한 패키지 설치
   ```bash
   pip install -r requirements.txt
   ```

4. OpenAI API 키 설정
   ```bash
   # .env.example 파일을 .env로 복사
   cp .env.example .env
   
   # .env 파일을 편집하여 API 키 설정
   # OPENAI_API_KEY=your-openai-api-key-here
   ```

5. 애플리케이션 실행
   ```bash
   python app.py
   ```

6. 웹 브라우저에서 표시된 URL로 접속하여 애플리케이션 사용
   (일반적으로 http://127.0.0.1:7860/)

## 사용 방법

1. 드롭다운 메뉴에서 직원 이름 선택
2. 해당 직원의 직무와 평가해야 할 스킬이 자동으로 표시됨
3. 평가 내용 입력란에 평가 내용을 직접 작성하거나 샘플 데이터 사용
4. "평가 분석하기" 버튼 클릭
5. AI가 분석한 결과 확인:
   - 주요 장점 및 강점
   - 개선이 필요한 영역
   - 스킬 레이더 차트
   - 핵심 키워드 분석

## 주요 파일 설명

- `app.py`: 그라디오 웹 인터페이스 및 메인 애플리케이션 로직
- `ai_utils.py`: OpenAI API 연동 및 평가 분석 함수
- `data.py`: 직원 정보, 직무별 스킬, 샘플 평가 데이터
- `visualization.py`: 레이더 차트 및 키워드 그래프 생성 함수

## 참고 사항

- 이 데모는 교육 및 시연 목적으로 제작되었습니다.
- 실제 환경에서 사용할 경우 보안과 개인정보 보호에 주의하세요.
- OpenAI API 사용에는 비용이 발생할 수 있습니다. 