import os
import json
from openai import OpenAI

# OpenAI 클라이언트를 전역 변수로 선언
client = None

def get_openai_client():
    """
    OpenAI 클라이언트를 반환하는 함수.
    클라이언트가 초기화되지 않았으면 초기화를 시도합니다.
    """
    global client
    
    # 이미 초기화된 클라이언트가 있으면 반환
    if client is not None:
        return client
    
    # 환경 변수에서 API 키 가져오기
    api_key = os.environ.get("OPENAI_API_KEY")
    
    # API 키 유효성 검사 및 클라이언트 초기화
    if api_key and api_key != "your-openai-api-key-here" and api_key != "sk-dummy-api-key-for-testing":
        try:
            # API 키 형식 기본 검사
            if not api_key.startswith("sk-"):
                print("경고: API 키가 'sk-'로 시작하지 않습니다. 올바른 OpenAI API 키 형식이 아닐 수 있습니다.")
            
            # 기본 설정으로 클라이언트 초기화
            client = OpenAI(api_key=api_key)
            print("OpenAI 클라이언트가 성공적으로 초기화되었습니다.")
            return client
        except Exception as e:
            print(f"OpenAI 클라이언트 초기화 오류: {e}")
            print("API 키가 올바른 형식인지 확인하세요. 일부 문자가 누락되었거나 잘못된 형식일 수 있습니다.")
            print("데모 모드로 전환합니다.")
            return None
    else:
        if not api_key:
            print("OpenAI API 키가 설정되지 않았습니다.")
        elif api_key == "your-openai-api-key-here":
            print("OpenAI API 키가 기본값으로 설정되어 있습니다. .env 파일을 수정하여 실제 API 키를 입력하세요.")
        elif api_key == "sk-dummy-api-key-for-testing":
            print("OpenAI API 키가 더미 값으로 설정되어 있습니다. 유효한 API 키를 설정하세요.")
        
        print("데모 모드로 실행됩니다. API 호출 없이 가짜 데이터를 사용합니다.")
        return None

def analyze_evaluation(name, job_title, skills, evaluation_text):
    """
    OpenAI GPT-4o를 사용하여 평가 내용을 분석합니다.
    API 키가 없는 경우 더미 데이터를 반환합니다.
    
    Args:
        name (str): 직원 이름
        job_title (str): 직무 타이틀
        skills (list): 평가해야 할 스킬 목록
        evaluation_text (str): 평가자가 작성한 평가 내용
        
    Returns:
        dict: 분석 결과 (장점, 단점, 키워드, 스킬 점수)
    """
    # OpenAI 클라이언트 초기화 시도
    client = get_openai_client()
    
    # API 키가 없거나 클라이언트가 초기화되지 않은 경우 더미 데이터 반환
    if client is None:
        print("유효한 OpenAI 클라이언트가 없어 더미 데이터를 생성합니다.")
        return generate_dummy_analysis(name, job_title, skills, evaluation_text)
        
    try:
        prompt = f"""
직원 이름: {name}
직무: {job_title}
평가해야 할 스킬: {', '.join(skills)}

평가 내용:
{evaluation_text}

위 평가 내용을 분석하여 다음 형식의 JSON으로 응답해주세요:
1. 장점 (strengths): 최소 3개, 최대 5개의 핵심 장점 목록
2. 단점 (areas_for_improvement): 최소 2개, 최대 3개의 개선이 필요한 영역 목록
3. 키워드 점수 (keyword_scores): 평가에서 언급된 주요 키워드와 해당 키워드의 점수 (1-10점) 
4. 스킬 점수 (skill_scores): 각 스킬별 1-10점 척도의 점수 (평가 내용에서 추론)

키워드 점수는 각 키워드가 얼마나 잘 수행되고 있는지를 나타내는 1-10점 척도의 점수입니다.
예를 들어, "코드 관리"라는 키워드가 있다면, 그 키워드에 대해 직원이 얼마나 역량을 발휘하고 있는지를 점수로 표현해주세요.

응답은 다음 JSON 형식을 따라야 합니다:
{{
  "strengths": ["장점1", "장점2", "장점3"],
  "areas_for_improvement": ["개선점1", "개선점2"],
  "keyword_scores": {{
    "키워드1": 8,
    "키워드2": 7,
    "키워드3": 9,
    "키워드4": 6,
    "키워드5": 8
  }},
  "skill_scores": {{
    "스킬1": 8,
    "스킬2": 7,
    ...
  }}
}}

직접적으로 언급되지 않은 스킬은 평가 내용에서 유추하여 점수를 매겨주세요.
"""

        print("OpenAI API에 분석 요청을 보냅니다.")
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "당신은 HR 분석 전문가로, 직원 평가 내용을 분석하여 객관적인 결과를 제공합니다."},
                    {"role": "user", "content": prompt}
                ],
            )
            
            print("API 응답을 받았습니다.")
            content = response.choices[0].message.content
            
            # JSON 파싱 오류 예외 처리 강화
            try:
                result = json.loads(content)
                print("JSON 파싱 성공")
                
                # 필수 키 확인
                required_keys = ["strengths", "areas_for_improvement", "keyword_scores", "skill_scores"]
                missing_keys = [key for key in required_keys if key not in result]
                
                if missing_keys:
                    print(f"응답에 다음 필수 키가 누락되었습니다: {missing_keys}")
                    print("더미 데이터를 사용합니다.")
                    return generate_dummy_analysis(name, job_title, skills, evaluation_text)
                    
                return result
            except json.JSONDecodeError as json_err:
                print(f"JSON 파싱 오류: {json_err}")
                print(f"받은 응답: {content[:200]}...")  # 응답의 일부만 로그로 기록
                print("더미 데이터를 사용합니다.")
                return generate_dummy_analysis(name, job_title, skills, evaluation_text)
        
        except Exception as api_error:
            print(f"API 호출 중 오류 발생: {api_error}")
            print("더미 데이터를 사용합니다.")
            return generate_dummy_analysis(name, job_title, skills, evaluation_text)
            
    except Exception as e:
        print(f"분석 처리 중 예상치 못한 오류 발생: {e}")
        print("더미 데이터를 사용합니다.")
        return generate_dummy_analysis(name, job_title, skills, evaluation_text)

def generate_dummy_analysis(name, job_title, skills, evaluation_text):
    """
    API 호출 없이 더미 분석 데이터를 생성합니다.
    실제로는 API를 사용하여 분석해야 하지만, 데모 목적으로만 사용됩니다.
    """
    print(f"더미 분석 데이터를 생성합니다: {name} ({job_title})")
    
    # 직무별 기본 강점 및 개선점 (간단한 예시)
    dummy_data = {
        "백엔드 개발자": {
            "strengths": [
                "기술적 전문성이 뛰어남",
                "문제 해결 능력이 탁월함",
                "시스템 아키텍처 설계에 강점이 있음"
            ],
            "areas_for_improvement": [
                "코드 문서화 개선 필요",
                "비개발자와의 의사소통 향상 필요"
            ],
            "keyword_scores": {
                "Python": 9,
                "Java": 8,
                "데이터베이스": 8,
                "확장성": 7,
                "아키텍처": 9,
                "문제해결": 9,
                "코드품질": 7
            },
            "skill_scores": {
                "기술적 전문성 (Python, Java, 데이터베이스 등)": 8,
                "시스템 아키텍처 설계 능력": 7,
                "문제 해결 능력": 9,
                "코드 품질 및 테스트": 6,
                "협업 및 커뮤니케이션": 7
            }
        },
        "프론트엔드 개발자": {
            "strengths": [
                "UI/UX 구현 능력이 뛰어남",
                "프레임워크 활용에 능숙함",
                "창의적인 디자인 솔루션 제공"
            ],
            "areas_for_improvement": [
                "일정 관리 개선 필요",
                "복잡한 상태 관리 패턴 학습 필요"
            ],
            "keyword_scores": {
                "React": 9,
                "Vue.js": 8,
                "UI/UX": 9,
                "반응형": 8,
                "성능 최적화": 7,
                "CSS": 8,
                "JavaScript": 9
            },
            "skill_scores": {
                "UI/UX 구현 능력 (HTML, CSS, JavaScript)": 9,
                "프레임워크 활용 능력 (React, Vue 등)": 8,
                "사용자 중심 개발": 8,
                "반응형 디자인 구현": 7,
                "성능 최적화": 6
            }
        },
        "데이터 사이언티스트": {
            "strengths": [
                "통계적 방법론에 대한 깊은 이해",
                "데이터 분석 및 모델링 능력 탁월",
                "데이터 시각화 전달력 우수"
            ],
            "areas_for_improvement": [
                "간단한 접근법 고려 필요",
                "리소스 최적화 필요"
            ],
            "keyword_scores": {
                "통계": 9,
                "머신러닝": 8,
                "Python": 9,
                "R": 7,
                "데이터 시각화": 9,
                "데이터 분석": 8,
                "모델링": 8
            },
            "skill_scores": {
                "통계 및 수학적 지식": 9,
                "데이터 분석 및 모델링 능력": 8,
                "프로그래밍 능력 (Python, R 등)": 8,
                "데이터 시각화 능력": 9,
                "비즈니스 문제 해결 능력": 7
            }
        }
    }
    
    # 기본 더미 데이터
    default_dummy = {
        "strengths": ["전문 지식이 뛰어남", "업무 수행 능력이 우수함", "팀 협업에 적극적임"],
        "areas_for_improvement": ["일부 영역에서 개선 필요", "시간 관리 향상 필요"],
        "keyword_scores": {
            "전문성": 8,
            "협업": 7,
            "의사소통": 6,
            "문제해결": 8,
            "리더십": 7,
            "시간관리": 5,
            "지식공유": 7
        },
        "skill_scores": {skill: 7 for skill in skills}  # 모든 스킬에 기본 7점 부여
    }
    
    # 직무에 맞는 더미 데이터 또는 기본 더미 데이터 반환
    return dummy_data.get(job_title, default_dummy)

def generate_skill_radar_data(skill_scores):
    """
    스킬 점수를 레이더 차트 데이터로 변환합니다.
    
    Args:
        skill_scores (dict): 스킬별 점수
        
    Returns:
        tuple: (labels, values) - 레이더 차트 데이터
    """
    labels = list(skill_scores.keys())
    values = list(skill_scores.values())
    return labels, values 