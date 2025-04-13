import gradio as gr
import os
import json
import sys
import io
from PIL import Image
import base64
import numpy as np
import matplotlib.pyplot as plt
import warnings

# matplotlib 경고 무시 설정
warnings.filterwarnings("ignore", category=UserWarning)

# 한글 인코딩 설정
import locale
locale_info = locale.getlocale()
print(f"현재 로케일: {locale_info}")

# 파이썬 버전 확인
print(f"파이썬 버전: {sys.version}")
print(f"기본 인코딩: {sys.getdefaultencoding()}")

# 모듈 임포트 수정 - JOB_TITLES 제거
from data import EMPLOYEES, EMPLOYEE_SKILLS, SAMPLE_EVALUATIONS
from ai_utils import analyze_evaluation
from job_descriptions import find_similar_job, format_job_description, JOB_DESCRIPTIONS

# 한글 폰트 해결을 위한 더 강력한 설정 시도
def try_set_korean_font():
    """한글 폰트 설정 시도"""
    try:
        # 기본 폰트 설정
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['axes.unicode_minus'] = False
        
        # 우선 설정할 한글 폰트 목록
        korean_fonts = [
            'NanumGothic',
            'Nanum Gothic',
            'NanumBarunGothic', 
            'NanumBarunGothicOTF',
            'NanumSquare',
            'Malgun Gothic',
            'AppleGothic',
            'Apple SD Gothic Neo',
            'Arial Unicode MS'
        ]
        
        # matplotlib 폰트 매니저에서 폰트 목록 가져오기
        import matplotlib.font_manager as fm
        font_names = [f.name for f in fm.fontManager.ttflist]
        
        # 폰트 목록 출력
        print(f"시스템에서 사용 가능한 폰트 목록 중 일부: {font_names[:10]}")
        
        # 우선순위에 따라 한글 폰트 검색
        for font in korean_fonts:
            if font in font_names:
                plt.rcParams['font.family'] = font
                print(f"한글 폰트 '{font}'를 사용합니다.")
                return True
        
        # 나눔 글꼴이 포함된 모든 폰트 검색
        for font in font_names:
            if 'Nanum' in font or '나눔' in font:
                plt.rcParams['font.family'] = font
                print(f"나눔 계열 폰트 '{font}'를 사용합니다.")
                return True
                
    except Exception as e:
        print(f"폰트 설정 오류: {e}")
    
    print("경고: 한글 폰트 설정 실패. 영어로 대체됩니다.")
    return False

# 폰트 설정 시도
korean_font_available = try_set_korean_font()

# 간단한 레이더 차트 생성 함수
def create_simple_radar_chart(skills, values, title="스킬 평가"):
    """
    간단한 레이더 차트를 생성합니다.
    """
    try:
        # 레이더 차트 데이터 준비
        categories = skills
        N = len(categories)
        
        # 입력 검증 - 스킬과 값의 갯수가 일치하는지 확인
        if len(values) != N:
            print(f"스킬과 값의 개수가 일치하지 않습니다: 스킬 {N}개, 값 {len(values)}개")
            # 필요하다면 값 조정
            if len(values) < N:
                values = values + [5.0] * (N - len(values))  # 부족한 값은 5.0으로 채우기
            else:
                values = values[:N]  # 초과하는 값은 자르기
        
        # 각도 계산
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        
        # 마지막 점을 처음으로 이어 닫힌 다각형 만들기
        values_plot = np.array(values).tolist() + [values[0]]
        angles_plot = angles + [angles[0]]
        
        # 그래프 생성
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, polar=True)
        
        # 레이더 차트 그리기
        ax.plot(angles_plot, values_plot, 'o-', linewidth=2)
        ax.fill(angles_plot, values_plot, alpha=0.25)
        
        # 스킬 라벨 설정
        if korean_font_available:
            # 한글 폰트를 사용할 수 있는 경우 원래 스킬 이름 사용
            ax.set_xticks(angles)
            ax.set_xticklabels(categories)
        else:
            # 한글 폰트를 사용할 수 없는 경우 영어 대체
            ax.set_xticks(angles)
            ax.set_xticklabels([f"Skill {i+1}" for i in range(N)])
            
            # 스킬 이름 범례 추가
            legend_text = "\n".join([f"Skill {i+1}: {skill}" for i, skill in enumerate(categories)])
            plt.figtext(0.95, 0.5, legend_text, fontsize=9, 
                       verticalalignment='center', bbox=dict(facecolor='white', alpha=0.8))
        
        # 점수 범위 설정
        ax.set_ylim(0, 10)
        
        # 제목 설정
        if korean_font_available:
            plt.title(f"{title}", size=15, color='blue', y=1.1)
        else:
            plt.title(f"Skill Assessment - {title}", size=15, color='blue', y=1.1)
        
        # 이미지를 PIL로 변환
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf)
        plt.close()
        
        return img
    except Exception as e:
        print(f"레이더 차트 생성 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        # 오류 발생 시 더미 이미지 반환
        dummy_img = Image.new('RGB', (400, 400), color=(255, 255, 255))
        return dummy_img

# 간단한 키워드 막대 그래프 생성 함수
def create_simple_keyword_graph(keyword_scores, title="키워드별 점수"):
    """
    간단한 키워드 막대 그래프를 생성합니다.
    """
    try:
        # 데이터 준비
        keywords = list(keyword_scores.keys())
        scores = list(keyword_scores.values())
        
        # 점수 기준으로 정렬 (내림차순)
        sorted_indices = np.argsort(scores)[::-1]
        sorted_keywords = [keywords[i] for i in sorted_indices]
        sorted_scores = [scores[i] for i in sorted_indices]
        
        # 가로 막대 그래프로 표현
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 키워드 라벨 설정
        if korean_font_available:
            # 한글 폰트를 사용할 수 있는 경우 원래 키워드 사용
            display_labels = sorted_keywords
        else:
            # 한글 폰트를 사용할 수 없는 경우 영어 대체
            display_labels = [f"Keyword {i+1}" for i in range(len(sorted_keywords))]
            
            # 키워드 이름 범례 추가
            legend_text = "\n".join([f"Keyword {i+1}: {kw}" for i, kw in enumerate(sorted_keywords)])
            plt.figtext(0.95, 0.5, legend_text, fontsize=9, 
                       verticalalignment='center', bbox=dict(facecolor='white', alpha=0.8))
        
        # 가로 막대 그래프 그리기
        bars = ax.barh(display_labels, sorted_scores, color='lightblue')
        
        # 그래프 스타일 설정
        if korean_font_available:
            ax.set_xlabel('점수 (1-10)')
            ax.set_title(f"{title}", fontsize=14)
        else:
            ax.set_xlabel('Score (1-10)')
            ax.set_title(f"Keyword Scores - {title}", fontsize=14)
            
        ax.set_xlim(0, 10)  # 점수 범위 0-10으로 설정
        
        # 각 막대 끝에 값 표시
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.1f}', 
                    ha='left', va='center')
        
        # 이미지를 PIL로 변환
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf)
        plt.close()
        
        return img
    except Exception as e:
        print(f"키워드 그래프 생성 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        # 오류 발생 시 더미 이미지 반환
        dummy_img = Image.new('RGB', (400, 400), color=(255, 255, 255))
        return dummy_img

# 스킬 점수 데이터 생성 함수
def generate_skill_radar_data(skill_scores):
    """
    스킬 점수 데이터를 레이더 차트용으로 변환합니다.
    """
    if isinstance(skill_scores, dict):
        labels = list(skill_scores.keys())
        values = list(skill_scores.values())
    else:
        # skill_scores가 리스트인 경우 (기존 코드와의 호환성)
        labels = [f"Skill {i+1}" for i in range(len(skill_scores))]
        values = skill_scores
        
    return labels, values

# Base64 이미지를 PIL 이미지로 변환하는 함수
def base64_to_pil(base64_str):
    try:
        if "base64," in base64_str:
            base64_str = base64_str.split("base64,")[1]
        image_bytes = base64.b64decode(base64_str)
        img = Image.open(io.BytesIO(image_bytes))
        return img
    except Exception as e:
        print(f"이미지 변환 오류: {e}")
        # 오류 발생 시 더미 이미지 반환
        dummy_img = Image.new('RGB', (300, 300), color=(255, 255, 255))
        return dummy_img

# 환경 변수 설정 - .env 파일에서 로드
try:
    from dotenv import load_dotenv
    print("dotenv 로드 시도 중...")
    load_dotenv(verbose=True)  # .env 파일의 환경 변수 로드
    print("환경 변수 파일(.env)을 로드했습니다.")
    api_key = os.environ.get("OPENAI_API_KEY")
    print(f"API 키 로드됨: {api_key != None}")
except ImportError:
    print("경고: python-dotenv 패키지가 설치되어 있지 않습니다.")
    print("'pip install python-dotenv'로 설치하세요.")
except Exception as e:
    print(f"경고: 환경 변수를 로드하는 중 오류 발생: {e}")

# 환경 변수 확인
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("\n" + "="*50)
    print("경고: OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
    print("데모 모드로 실행됩니다. OpenAI API 호출 없이 가짜 데이터를 사용합니다.")
    print("="*50 + "\n")
elif api_key == "your-openai-api-key-here":
    print("\n" + "="*50)
    print("경고: OPENAI_API_KEY가 기본값으로 설정되어 있습니다.")
    print(".env 파일을 수정하여 실제 OpenAI API 키를 입력하세요.")
    print("현재는 데모 모드로 실행됩니다. API 호출 없이 가짜 데이터를 사용합니다.")
    print("="*50 + "\n")

def get_job_and_skills(name):
    """
    이름으로 직무와 필요한 스킬 목록을 반환합니다.
    """
    if name in EMPLOYEES:
        # JOB_TITLES 대신 EMPLOYEES 사용
        job_title = EMPLOYEES[name]
        skills = EMPLOYEE_SKILLS.get(name, [])
        return job_title, skills
    else:
        return "직원 정보를 찾을 수 없습니다.", []

def get_sample_evaluation(name):
    """
    이름으로 샘플 평가 내용을 반환합니다.
    """
    return SAMPLE_EVALUATIONS.get(name, "")

def name_changed(name):
    """
    이름이 변경되었을 때 해당 직원의 직무, 스킬, 샘플 평가 내용을 반환합니다.
    """
    if not name or name not in EMPLOYEES:
        return "", "", ""
    job_title, skills = get_job_and_skills(name)
    skills_text = "- " + "\n- ".join(skills)
    sample_eval = get_sample_evaluation(name)
    
    return f"{job_title}", skills_text, sample_eval

def get_job_description(job_title):
    """
    직무명을 입력받아 해당 직무 또는 가장 유사한 직무에 대한 상세 설명을 반환합니다.
    
    Args:
        job_title: 직무명
        
    Returns:
        마크다운 형식의 직무 설명
    """
    print(f"직무 설명 조회 요청: {job_title}")
    
    # 직무명이 빈 문자열이거나 None인 경우 처리
    if not job_title or job_title.strip() == "":
        return "직무를 선택해주세요."
    
    # 직무명이 직무 설명 데이터베이스에 있는 경우 바로 조회
    if job_title in JOB_DESCRIPTIONS:
        print(f"직무 '{job_title}' 정보를 직접 찾았습니다.")
        description = format_job_description(job_title)
        # 정확한 일치인 경우 헤더에 정확한 매치임을 표시
        return f"## 🎯 정확한 매치: 100% 일치\n\n{description}"
    
    # 유사한 직무 찾기 (RAG 검색 단계)
    similar_job, similarity = find_similar_job(job_title)
    print(f"직무 '{job_title}'와 가장 유사한 직무는 '{similar_job}'입니다. (유사도: {similarity:.1f}%)")
    
    # 유사 직무에 대한 설명 반환 (유사도 정보 포함)
    description = format_job_description(similar_job)

    emoji = "🔍"
    similarity_text = f"**유사한 직무**: {similarity:.1f}% 일치"
    
    '''
    # 유사도에 따른 이모지 선택
    if similarity >= 80:
        emoji = "🔍"
        similarity_text = f"**매우 유사한 직무**: {similarity:.1f}% 일치"
    elif similarity >= 60:
        emoji = "🔎"
        similarity_text = f"**관련 직무**: {similarity:.1f}% 일치"
    elif similarity >= 40:
        emoji = "📋"
        similarity_text = f"**부분 관련 직무**: {similarity:.1f}% 일치"
    else:
        emoji = "❓"
        similarity_text = f"**유사도 낮음**: {similarity:.1f}% 일치"
    '''
    
    # RAG 정보 추가
    rag_header = f"""## {emoji} RAG 검색 결과: {similarity_text}

> **검색 쿼리**: '{job_title}'  
> **찾은 직무**: '{similar_job}'

"""
    
    return rag_header + description

def process_evaluation(name, evaluation_text=None):
    """
    평가 내용을 처리하고 결과를 반환합니다.
    """
    print(f"Process evaluation for {name}")
    
    if not name or name not in EMPLOYEES:
        print("Invalid employee name")
        return "유효한 직원 이름을 선택해주세요.", "", "", "", "", "", None, None, None
    
    # 직무와 스킬 목록 가져오기
    job_title, skills = get_job_and_skills(name)
    print(f"Job title: {job_title}")
    
    # 평가 내용이 비어있으면 샘플 데이터 사용
    if not evaluation_text or evaluation_text.strip() == "":
        evaluation_text = get_sample_evaluation(name)
    
    # 평가 분석
    try:
        # 실제 분석 로직 호출 (API 키가 있으면)
        if api_key and api_key != "your-openai-api-key-here":
            analysis_result = analyze_evaluation(name, job_title, skills, evaluation_text)
        else:
            # 데모 모드 - 미리 정의된 결과 사용
            print(f"데모 모드에서 {name}의 평가를 분석합니다.")
            analysis_result = {
                "strengths": [
                    "체계적인 프로젝트 관리 능력",
                    "명확한 의사소통 기술",
                    "문제 해결 능력이 뛰어남"
                ],
                "areas_for_improvement": [
                    "기술적 역량 강화 필요",
                    "시간 관리 개선 필요",
                    "팀 내 피드백 수용 능력 향상 필요"
                ],
                "keyword_scores": {
                    "프로젝트 관리": 8.5,
                    "의사소통": 8.0,
                    "문제 해결": 7.5,
                    "시간 관리": 6.0,
                    "기술 이해도": 5.5
                },
                "skill_scores": {skill: 7.0 + np.random.rand() * 3.0 for skill in skills}
            }
            
            # 직원별 맞춤형 분석 결과 (데모)
            if name == "김철수":
                analysis_result = {
                    "strengths": [
                        "뛰어난 소프트웨어 설계 능력",
                        "빠른 문제 해결 능력",
                        "팀원들과의 협업 우수"
                    ],
                    "areas_for_improvement": [
                        "문서화 작업 개선 필요",
                        "코드 리뷰 참여 증가 필요",
                        "신기술 학습 지속 필요"
                    ],
                    "keyword_scores": {
                        "코딩 스킬": 9.0,
                        "문제 해결": 8.5,
                        "협업": 7.5,
                        "문서화": 5.0,
                        "새로운 기술": 6.0
                    },
                    "skill_scores": {skill: 7.0 + np.random.rand() * 3.0 for skill in skills}
                }
        
        # 결과 추출
        strengths = analysis_result.get("strengths", [])
        areas_for_improvement = analysis_result.get("areas_for_improvement", [])
        keyword_scores = analysis_result.get("keyword_scores", {})
        skill_scores = analysis_result.get("skill_scores", {})
        
        # 결과를 텍스트로 변환
        strengths_text = "- " + "\n- ".join(strengths)
        improvements_text = "- " + "\n- ".join(areas_for_improvement)
        
        # 스킬 목록 텍스트로 변환
        skills_text = "- " + "\n- ".join(skills)
        
        # 결과 헤더
        result_header = f"## {name}님의 분석 결과\n직무: {job_title}"
        
        # 키워드 점수 텍스트
        keywords_text = ""
        for keyword, score in sorted(keyword_scores.items(), key=lambda x: x[1], reverse=True):
            keywords_text += f"- {keyword}: {score}/10\n"
        
        # 키워드만 있는 텍스트 (점수 없음)
        keywords_only_text = ", ".join([keyword for keyword in keyword_scores.keys()])
        
        # 스킬별 점수 텍스트
        skill_scores_text = "### 스킬별 점수\n\n"
        for skill, score in sorted(skill_scores.items(), key=lambda x: x[1], reverse=True):
            skill_scores_text += f"- **{skill}**: {score:.1f}/10\n"
        
        # 시각화 - 간단한 버전 사용
        print(f"이미지 생성 중... 스킬: {list(skill_scores.keys())[:2]}")
        
        # 데이터 준비
        labels, values = generate_skill_radar_data(skill_scores)
        
        # 시각화 함수 사용 (한글 제목 사용)
        radar_img = create_simple_radar_chart(labels, values, f"{name}의 스킬 평가")
        keyword_img = create_simple_keyword_graph(keyword_scores, f"{name}의 키워드별 역량 점수")
        
        return (
            result_header,
            skills_text,
            evaluation_text,
            strengths_text,
            improvements_text,
            keywords_only_text,
            radar_img,
            keyword_img,
            skill_scores_text
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error in process_evaluation: {e}")
        error_msg = f"평가 분석 중 오류가 발생했습니다: {str(e)}"
        return error_msg, skills_text, evaluation_text, "", "", "", None, None, None

# Gradio 3.x 인터페이스 구성
with gr.Blocks(title="AI 기반 인사 평가 시스템") as demo:
    gr.Markdown("# 🤖 AI 기반 인사 평가 시스템")
    gr.Markdown("이 시스템은 AI를 활용하여 인사 평가를 객관화하고 효율화합니다.")
    
    with gr.Row():
        with gr.Column(scale=1):
            name_input = gr.Dropdown(
                choices=list(EMPLOYEES.keys()),
                label="직원 이름",
                info="평가할 직원의 이름을 선택하세요."
            )
            
            job_output = gr.Textbox(label="직무", interactive=False)
            
            # 직무 설명 조회 버튼 추가
            job_info_button = gr.Button("🔍 직무 설명 검색하기", variant="secondary")
            
            skills_output = gr.Textbox(label="평가해야 할 스킬", lines=6, interactive=False)
        
        with gr.Column(scale=2):
            evaluation_input = gr.Textbox(
                label="자기 평가 내용",
                placeholder="평가 내용을 입력하세요. 비워두면 샘플 데이터가 사용됩니다.",
                lines=10
            )

            # job_description_output을 평가 내용 아래에 위치시킵니다
            job_description_output = gr.Markdown(visible=False, label="직무 설명")
    
    analyze_button = gr.Button("평가 분석하기", variant="primary")
    
    result_title = gr.Markdown(label="분석 결과")
    
    with gr.Tabs():
        with gr.TabItem("강점 및 개선점"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 강점")
                    strengths_output = gr.Textbox(label="", lines=6, interactive=False)
                
                with gr.Column():
                    gr.Markdown("### 개선 영역")
                    improvements_output = gr.Textbox(label="", lines=6, interactive=False)
            
            gr.Markdown("### 핵심 키워드")
            keywords_output = gr.Textbox(label="", interactive=False)
        
        with gr.TabItem("스킬 레이더 차트"):
            with gr.Row():
                with gr.Column(scale=2):
                    radar_output = gr.Image(label="스킬 평가", type="pil")
                with gr.Column(scale=1):
                    gr.Markdown("### 스킬별 점수")
                    skill_scores_output = gr.Markdown()
        
        with gr.TabItem("키워드별 역량 점수"):
            keywords_chart_output = gr.Image(label="키워드별 역량 점수", type="pil")
    
    # 이벤트 연결
    name_input.change(
        fn=name_changed,
        inputs=name_input,
        outputs=[job_output, skills_output, evaluation_input]
    )
    
    # toggle_job_description 함수를 수정합니다
    def toggle_job_description(job_title):
        """
        직무 설명을 표시하는 함수
        """
        description = get_job_description(job_title)
        return gr.update(visible=True, value=description)

    # job_info_button.click 이벤트 핸들러를 수정합니다
    job_info_button.click(
        fn=toggle_job_description,
        inputs=job_output,
        outputs=job_description_output
    )
    
    analyze_button.click(
        fn=process_evaluation,
        inputs=[name_input, evaluation_input],
        outputs=[
            result_title,
            skills_output,
            evaluation_input,
            strengths_output,
            improvements_output,
            keywords_output,
            radar_output,
            keywords_chart_output,
            skill_scores_output
        ]
    )
    
    gr.Markdown("""
    ### 참고 사항
    - 평가 내용은 최대한 구체적으로 작성할수록 더 정확한 분석이 가능합니다.
    - 스킬 평가는 1-10점 척도로 표시됩니다.
    - 모든 분석은 AI에 의해 자동으로 이루어지며, 결과는 참고용으로만 사용하세요.
    """)

# 애플리케이션 실행
if __name__ == "__main__":
    print("AI 기반 인사 평가 시스템을 시작합니다...")
    print("Gradio 웹 인터페이스가 시작됩니다.")
    demo.launch(share=True)  # share=True로 설정하면 공유 가능한 링크가 생성됩니다. 