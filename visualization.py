import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import matplotlib as mpl
import os
from matplotlib import font_manager

# 한글 폰트 설정
def set_korean_font():
    # OS 확인 (맥OS와 윈도우는 다른 폰트 사용)
    system_os = os.name
    
    # 기본 폰트 목록
    font_found = False
    
    # macOS 폰트 우선 목록
    mac_fonts = [
        'AppleGothic',
        'Apple SD Gothic Neo',
        'NanumGothic',
        'Malgun Gothic',
        'Nanum Gothic',
        'NanumBarunGothic',
        'NanumBarunGothicOTF',
        'NanumSquare'
    ]
    
    # Windows 폰트 우선 목록
    win_fonts = [
        'Malgun Gothic',
        'NanumGothic',
        'Nanum Gothic',
        'NanumBarunGothic',
        'NanumBarunGothicOTF',
        'NanumSquare',
        'Gulim'
    ]
    
    # Linux 폰트 우선 목록
    linux_fonts = [
        'NanumGothic',
        'Nanum Gothic',
        'NanumBarunGothic',
        'NanumBarunGothicOTF',
        'NanumSquare',
        'UnDotum'
    ]
    
    # 시스템에 따른 폰트 목록 선택
    if system_os == 'posix':  # macOS, Linux
        if 'darwin' in os.sys.platform:  # macOS
            font_list = mac_fonts
        else:  # Linux
            font_list = linux_fonts
    else:  # Windows
        font_list = win_fonts
    
    # 시스템 폰트 목록 가져오기
    system_fonts = [f.name for f in font_manager.fontManager.ttflist]
    
    # 선호 폰트 중 시스템에 있는 폰트 찾기
    for font in font_list:
        if font in system_fonts:
            try:
                plt.rcParams['font.family'] = font
                print(f"한글 폰트 설정: {font}")
                font_found = True
                break
            except:
                continue
    
    # 폰트를 찾지 못한 경우 기본 폰트 사용
    if not font_found:
        print("한글 폰트를 찾을 수 없습니다. 영문 폰트로 대체합니다.")
        plt.rcParams['font.family'] = 'DejaVu Sans'
        # 유니코드 문제 방지
        plt.rcParams['axes.unicode_minus'] = False

# 시작시 한글 폰트 설정
set_korean_font()

def create_radar_chart(labels, values, title="스킬 평가"):
    """
    레이더 차트(스킬 그래프)를 생성합니다.
    
    Args:
        labels (list): 스킬 이름 목록
        values (list): 각 스킬에 해당하는 점수 목록
        title (str): 차트 제목
        
    Returns:
        str: Base64로 인코딩된 이미지
    """
    # 데이터 준비
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    # 첫 번째 변수를 마지막에 복사하여 폐곡선 형태로 만듦
    values += values[:1]
    angles += angles[:1]
    labels += labels[:1]
    
    # 그래프 생성
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # 축 레이블 설정
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels[:-1])
    
    # 레이더 차트 그리기
    ax.plot(angles, values, linewidth=2, linestyle='solid', label=title)
    ax.fill(angles, values, alpha=0.25)
    
    # 눈금 설정
    ax.set_rlabel_position(0)
    ax.set_rticks([2, 4, 6, 8, 10])
    ax.set_rlim(0, 10)
    
    # 제목 설정
    plt.title(title, size=15, color='blue', y=1.1)
    
    # 이미지를 Base64로 인코딩
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return img_str

def create_keyword_graph(keywords, title="핵심 키워드"):
    """
    키워드 시각화 그래프를 생성합니다.
    
    Args:
        keywords (list): 키워드 목록
        title (str): 차트 제목
        
    Returns:
        str: Base64로 인코딩된 이미지
    """
    # 간단한 가로 막대 그래프로 키워드 표현
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 임의의 중요도 점수 부여 (실제로는 AI 분석에서 키워드 중요도를 계산할 수 있음)
    keyword_values = np.linspace(10, 5, len(keywords))
    
    # 가로 막대 그래프 그리기
    bars = ax.barh(keywords, keyword_values, color='skyblue')
    
    # 그래프 스타일 설정
    ax.set_xlabel('중요도')
    ax.set_title(title)
    ax.invert_yaxis()  # 위에서 아래로 중요도 순서대로 표시
    
    # 각 막대 끝에 값 표시
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.1f}', 
                ha='left', va='center')
    
    # 이미지를 Base64로 인코딩
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return img_str

def create_keyword_score_graph(keyword_scores, title="키워드별 점수"):
    """
    키워드별 점수 시각화 그래프를 생성합니다.
    
    Args:
        keyword_scores (dict): 키워드별 점수 딕셔너리 {키워드: 점수}
        title (str): 차트 제목
        
    Returns:
        str: Base64로 인코딩된 이미지
    """
    # 데이터 준비
    keywords = list(keyword_scores.keys())
    scores = list(keyword_scores.values())
    
    # 점수 기준으로 정렬 (내림차순)
    sorted_indices = np.argsort(scores)[::-1]
    keywords = [keywords[i] for i in sorted_indices]
    scores = [scores[i] for i in sorted_indices]
    
    # 가로 막대 그래프로 표현
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 가로 막대 그래프 그리기
    bars = ax.barh(keywords, scores, color='lightblue')
    
    # 그래프 스타일 설정
    ax.set_xlabel('점수 (1-10)')
    ax.set_title(title)
    ax.set_xlim(0, 10)  # 점수 범위 0-10으로 설정
    
    # 각 막대 끝에 값 표시
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.1f}', 
                ha='left', va='center')
    
    # 이미지를 Base64로 인코딩
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return img_str 