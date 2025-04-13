"""
직무 설명 데이터베이스

이 모듈은 다양한 직무에 대한 상세 설명을 포함하고 있습니다.
각 직무별로 다음 정보를 제공합니다:
- 직무 개요
- 주요 책임
- 필요 역량
- 경력 발전 경로
"""

# 직무 설명 데이터베이스
JOB_DESCRIPTIONS = {
    "백엔드 개발자": {
        "description": """
백엔드 개발자는 사용자에게 보이지 않는 서버 측 로직을 설계하고 개발하는 전문가입니다. 
데이터베이스, 서버 아키텍처, API, 애플리케이션 로직 등을 담당하며, 프론트엔드와 효율적으로 
통신할 수 있는 시스템을 구축합니다.
        """,
        "responsibilities": [
            "RESTful API 설계 및 개발",
            "데이터베이스 설계, 구현 및 최적화",
            "서버 인프라 및 클라우드 서비스 관리",
            "보안 및 데이터 보호 기능 구현",
            "성능 병목 현상 식별 및 해결",
            "기술적 부채 관리 및 코드 리팩토링"
        ],
        "required_skills": [
            "Python, Java, Node.js 등 서버 측 프로그래밍 언어 전문성",
            "SQL 및 NoSQL 데이터베이스 지식",
            "RESTful API 및 GraphQL 설계 원칙",
            "Docker, Kubernetes 등 컨테이너화 기술",
            "CI/CD 파이프라인 구축 및 유지보수",
            "보안 모범 사례 및 인증 메커니즘"
        ],
        "career_path": [
            "주니어 백엔드 개발자",
            "백엔드 개발자",
            "시니어 백엔드 개발자",
            "백엔드 아키텍트",
            "기술 리드",
            "CTO"
        ],
        "related_jobs": ["풀스택 개발자", "DevOps 엔지니어", "데이터 엔지니어"]
    },
    
    "프론트엔드 개발자": {
        "description": """
프론트엔드 개발자는 사용자가 직접 상호작용하는 웹 애플리케이션의 사용자 인터페이스(UI)와
사용자 경험(UX)을 구현하는 전문가입니다. HTML, CSS, JavaScript를 기반으로 
반응형 웹사이트와 웹 애플리케이션을 개발합니다.
        """,
        "responsibilities": [
            "사용자 인터페이스 구현 및 반응형 디자인 적용",
            "웹 애플리케이션 성능 최적화",
            "백엔드 API와의 통합",
            "크로스 브라우저 호환성 확보",
            "사용자 경험 향상을 위한 UI 컴포넌트 개발",
            "웹 접근성 표준 준수"
        ],
        "required_skills": [
            "HTML5, CSS3, JavaScript/TypeScript 전문성",
            "React, Vue, Angular 등 프론트엔드 프레임워크 경험",
            "UI/UX 디자인 원칙 이해",
            "웹팩, Babel 등 빌드 도구 활용 능력",
            "REST API 및 GraphQL 통합 경험",
            "반응형 디자인 및 모바일 웹 개발"
        ],
        "career_path": [
            "주니어 프론트엔드 개발자",
            "프론트엔드 개발자",
            "시니어 프론트엔드 개발자",
            "프론트엔드 아키텍트",
            "UI/UX 개발 리드"
        ],
        "related_jobs": ["풀스택 개발자", "UI/UX 디자이너", "웹 디자이너"]
    },
    
    "데이터 사이언티스트": {
        "description": """
데이터 사이언티스트는 대규모 데이터를 분석하여 비즈니스 의사결정에 도움이 되는 통찰력을
도출하는 전문가입니다. 통계학, 머신러닝, 프로그래밍 기술을 활용해 데이터에서 패턴을 
찾고 예측 모델을 개발합니다.
        """,
        "responsibilities": [
            "비즈니스 문제를 위한 데이터 기반 솔루션 개발",
            "대용량 데이터셋에서 패턴 및 트렌드 식별",
            "머신러닝 및 딥러닝 모델 설계 및 구현",
            "데이터 시각화 및 결과 해석",
            "경영진에게 분석 결과 및 예측 제시",
            "데이터 파이프라인 구축 및 자동화"
        ],
        "required_skills": [
            "Python, R 등 데이터 분석 언어 능숙도",
            "SQL 및 NoSQL 데이터베이스 활용 능력",
            "통계학 및 확률론 지식",
            "머신러닝 알고리즘 및 프레임워크(TensorFlow, PyTorch, Scikit-learn)",
            "데이터 시각화 도구(Matplotlib, Tableau, PowerBI)",
            "빅데이터 기술(Hadoop, Spark)"
        ],
        "career_path": [
            "주니어 데이터 분석가",
            "데이터 사이언티스트",
            "시니어 데이터 사이언티스트",
            "머신러닝 엔지니어",
            "데이터 사이언스 리드",
            "AI 연구 책임자"
        ],
        "related_jobs": ["데이터 엔지니어", "머신러닝 엔지니어", "BI 분석가"]
    },
    
    "제품 관리자": {
        "description": """
제품 관리자는 제품의 비전부터 개발, 출시, 개선까지 전체 생명주기를 관리하는 역할을 합니다.
사용자 요구사항을 이해하고 비즈니스 목표와 기술적 제약을 조율하며 성공적인 제품을 
만들어내는 일을 담당합니다.
        """,
        "responsibilities": [
            "제품 비전 및 전략 수립",
            "사용자 요구사항 수집 및 우선순위 지정",
            "제품 로드맵 개발 및 관리",
            "개발 팀과 협력하여 기능 명세서 작성",
            "시장 및 경쟁사 분석",
            "제품 성과 지표 정의 및 모니터링"
        ],
        "required_skills": [
            "사용자 중심 설계 및 디자인 사고 능력",
            "데이터 기반 의사결정 능력",
            "우수한 커뮤니케이션 및 프레젠테이션 능력",
            "애자일 및 스크럼 방법론 이해",
            "기본적인 기술 지식 및 비즈니스 통찰력",
            "문제 해결 및 전략적 사고 능력"
        ],
        "career_path": [
            "주니어 제품 관리자",
            "제품 관리자",
            "시니어 제품 관리자",
            "제품 책임자(Head of Product)",
            "제품 부사장(VP of Product)",
            "최고 제품 책임자(CPO)"
        ],
        "related_jobs": ["제품 마케팅 관리자", "비즈니스 분석가", "UX 연구원"]
    },
    
    "UX/UI 디자이너": {
        "description": """
UX/UI 디자이너는 사용자가 제품이나 서비스와 상호작용할 때 최적의 경험을 할 수 있도록
인터페이스와 사용자 여정을 설계하는 전문가입니다. 사용자 중심 디자인 원칙을 적용하여
직관적이고 매력적인 디지털 경험을 창출합니다.
        """,
        "responsibilities": [
            "사용자 연구 및 페르소나 개발",
            "사용자 흐름 및 와이어프레임 설계",
            "프로토타입 제작 및 사용성 테스트 수행",
            "디자인 시스템 및 스타일 가이드 개발",
            "시각적 디자인 요소 및 인터랙션 디자인",
            "개발자 및 이해관계자와 협력"
        ],
        "required_skills": [
            "Figma, Adobe XD, Sketch 등 디자인 도구 전문성",
            "사용자 중심 디자인 방법론",
            "인터랙션 디자인 원칙",
            "시각적 디자인 기술(타이포그래피, 색상 이론, 레이아웃)",
            "기본적인 HTML, CSS 이해",
            "사용성 테스트 및 디자인 반복 능력"
        ],
        "career_path": [
            "주니어 UX/UI 디자이너",
            "UX/UI 디자이너",
            "시니어 UX/UI 디자이너",
            "UX 연구원 또는 UI 개발자",
            "디자인 책임자(Design Lead)",
            "UX 디렉터 또는 창의적 책임자(Creative Director)"
        ],
        "related_jobs": ["그래픽 디자이너", "제품 디자이너", "프론트엔드 개발자"]
    },
    
    "마케팅 매니저": {
        "description": """
마케팅 매니저는 회사의 제품 또는 서비스에 대한 인지도를 높이고 고객 확보 및 유지를 
위한 전략을 개발하고 실행합니다. 다양한 채널을 통해 브랜드 메시지를 전달하고
마케팅 캠페인의 효과를 측정 및 최적화합니다.
        """,
        "responsibilities": [
            "종합적인 마케팅 전략 개발",
            "디지털 및 전통적 마케팅 캠페인 계획 및 실행",
            "마케팅 예산 관리 및 ROI 분석",
            "브랜드 일관성 유지 및 브랜드 가이드라인 개발",
            "시장 조사 및 경쟁 분석 수행",
            "마케팅 성과 측정 및 보고"
        ],
        "required_skills": [
            "디지털 마케팅 전략(SEO, SEM, 소셜 미디어, 이메일 마케팅)",
            "데이터 분석 및 마케팅 측정 도구 활용 능력",
            "콘텐츠 마케팅 및 스토리텔링 능력",
            "프로젝트 관리 및 다중 작업 처리 능력",
            "브랜드 개발 및 포지셔닝 이해",
            "우수한 의사소통 능력 및 창의적 사고"
        ],
        "career_path": [
            "마케팅 코디네이터/스페셜리스트",
            "마케팅 매니저",
            "시니어 마케팅 매니저",
            "마케팅 디렉터",
            "마케팅 부사장(VP of Marketing)",
            "최고 마케팅 책임자(CMO)"
        ],
        "related_jobs": ["디지털 마케팅 전문가", "브랜드 매니저", "콘텐츠 마케팅 매니저"]
    },
    
    "인사 매니저": {
        "description": """
인사 매니저는 조직의 인적 자원을 관리하고 개발하는 역할을 담당합니다. 채용, 교육, 성과 관리,
복리후생, 조직 문화 등 직원 생애주기 전반에 걸친 전략과 프로그램을 설계하고 실행하여
조직의 인재 확보와 유지를 지원합니다.
        """,
        "responsibilities": [
            "채용 및 온보딩 프로세스 관리",
            "성과 평가 시스템 개발 및 관리",
            "직원 보상 및 복리후생 프로그램 설계",
            "직원 관계 및 갈등 해결 지원",
            "인재 개발 및 승계 계획 수립",
            "조직 문화 및 직원 참여 이니셔티브 추진"
        ],
        "required_skills": [
            "노동법 및 고용 규정 지식",
            "인적 자원 정보 시스템(HRIS) 활용 능력",
            "면접 및 인재 평가 기술",
            "중재 및 갈등 해결 능력",
            "데이터 분석 및 HR 메트릭스 활용 능력",
            "변화 관리 및 조직 개발 이해"
        ],
        "career_path": [
            "HR 코디네이터/어시스턴트",
            "HR 제너럴리스트/스페셜리스트",
            "HR 매니저",
            "HR 디렉터",
            "HR 부사장(VP of HR)",
            "최고인사책임자(CHRO)"
        ],
        "related_jobs": ["인재 확보 매니저", "교육 개발 매니저", "노사 관계 매니저"]
    },
    
    "영업 담당자": {
        "description": """
영업 담당자는 회사의 제품이나 서비스를 잠재 고객에게 소개하고 판매하는 역할을 합니다.
고객 관계 구축, 제품 데모, 계약 협상, 판매 마감 등을 통해 비즈니스 성장에 직접적인
영향을 미치는 중요한 역할을 담당합니다.
        """,
        "responsibilities": [
            "신규 영업 기회 창출 및 잠재 고객 발굴",
            "제품 및 서비스 데모 및 프레젠테이션",
            "고객 요구사항 이해 및 맞춤형 솔루션 제안",
            "계약 조건 협상 및 판매 마감",
            "CRM 시스템을 통한 영업 파이프라인 관리",
            "판매 보고서 작성 및 영업 목표 달성"
        ],
        "required_skills": [
            "탁월한 커뮤니케이션 및 대인 관계 능력",
            "영업 기법 및 협상 기술",
            "고객 중심 사고방식",
            "문제 해결 및 반대 의견 극복 능력",
            "CRM 소프트웨어 활용 능력",
            "시장 및 업계 동향 이해"
        ],
        "career_path": [
            "영업 개발 담당자(SDR)",
            "영업 담당자/영업 계정 관리자",
            "시니어 영업 담당자",
            "영업 관리자",
            "영업 디렉터",
            "영업 부사장(VP of Sales)"
        ],
        "related_jobs": ["계정 관리자", "고객 성공 관리자", "비즈니스 개발 관리자"]
    }
}

# 직무 유사성 검색을 위한 임베딩 함수
def find_similar_job(query, job_titles=None):
    """
    쿼리와 가장 유사한 직무를 찾습니다.
    매우 단순한 방식으로 구현됨 (실제로는 벡터 임베딩 등을 사용할 수 있음)
    
    Args:
        query: 검색할 직무명 또는 설명
        job_titles: 검색할 직무 리스트 (기본값은 JOB_DESCRIPTIONS의 모든 키)
        
    Returns:
        (가장 유사한 직무명, 유사도 점수) 튜플
    """
    if job_titles is None:
        job_titles = list(JOB_DESCRIPTIONS.keys())
    
    # 실제 구현에서는 임베딩 기반 유사도를 사용할 수 있음
    # 여기서는 간단한 문자열 포함 여부로 유사도 계산
    best_match = None
    highest_score = -1
    max_possible_score = 10  # 최대 가능 점수 (임의 설정)
    
    for job in job_titles:
        # 직무명이 정확히 일치하면 100% 유사도
        if query.lower() == job.lower():
            return job, 100.0
        
        # 직무명 자체가 쿼리에 포함되어 있으면 높은 점수
        if query.lower() in job.lower() or job.lower() in query.lower():
            similarity = 90.0
            return job, similarity
        
        # 간단한 유사도 계산 (공통 단어 수)
        query_words = set(query.lower().split())
        job_words = set(job.lower().split())
        
        # 직무 설명에서도 단어 추출
        desc_words = set(JOB_DESCRIPTIONS[job]["description"].lower().split())
        
        # 책임 및 역량에서도 단어 추출
        resp_words = set()
        for resp in JOB_DESCRIPTIONS[job]["responsibilities"]:
            resp_words.update(resp.lower().split())
        
        skill_words = set()
        for skill in JOB_DESCRIPTIONS[job]["required_skills"]:
            skill_words.update(skill.lower().split())
        
        # 유사도 점수 계산
        common_with_title = len(query_words.intersection(job_words)) * 2.0  # 직무명 일치는 가중치 2배
        common_with_desc = len(query_words.intersection(desc_words)) * 1.0
        common_with_resp = len(query_words.intersection(resp_words)) * 0.7
        common_with_skills = len(query_words.intersection(skill_words)) * 0.5
        
        # 전체 점수 계산
        score = common_with_title + common_with_desc + common_with_resp + common_with_skills
        
        if score > highest_score:
            highest_score = score
            best_match = job
    
    # 매칭되는 것이 없으면 첫 번째 직무 반환
    if highest_score <= 0:
        return job_titles[0], 30.0  # 기본 유사도 30%
    
    # 점수를 0-100 범위의 퍼센트로 변환 (최대 점수를 기준으로)
    # 여기서는 간단하게 매핑하지만, 실제로는 좀 더 복잡한 정규화가 필요할 수 있음
    similarity_percent = min(100.0, (highest_score / max_possible_score) * 100)
    
    # 최소 유사도는 30%로 설정
    similarity_percent = max(30.0, similarity_percent)
    
    return best_match, similarity_percent

# 직무 설명 포맷팅 함수
def format_job_description(job_title):
    """
    직무 설명을 마크다운 형식으로 포맷팅합니다.
    
    Args:
        job_title: 직무명
        
    Returns:
        마크다운 형식의 직무 설명 문자열
    """
    if job_title not in JOB_DESCRIPTIONS:
        return f"# {job_title}\n\n해당 직무에 대한 정보가 없습니다."
    
    job_data = JOB_DESCRIPTIONS[job_title]
    
    # 마크다운 포맷으로 직무 설명 구성
    md = f"# {job_title}\n\n"
    md += f"## 직무 개요\n{job_data['description'].strip()}\n\n"
    
    md += "## 주요 책임\n"
    for resp in job_data["responsibilities"]:
        md += f"- {resp}\n"
    md += "\n"
    
    md += "## 필요 역량\n"
    for skill in job_data["required_skills"]:
        md += f"- {skill}\n"
    md += "\n"
    
    md += "## 경력 발전 경로\n"
    for i, step in enumerate(job_data["career_path"], 1):
        md += f"{i}. {step}\n"
    md += "\n"
    
    md += "## 관련 직무\n"
    md += ", ".join(job_data["related_jobs"])
    
    return md 