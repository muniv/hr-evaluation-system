import os

# 직접 환경 변수 확인
print("직접 환경 변수 확인:")
api_key = os.environ.get("OPENAI_API_KEY")
print(f"OPENAI_API_KEY: {api_key}")

# python-dotenv로 환경 변수 로드 시도
try:
    from dotenv import load_dotenv
    print("\ndotenv로 환경 변수 로드 시도...")
    load_dotenv(verbose=True)  # verbose=True로 자세한 로그 출력
    
    # 다시 환경 변수 확인
    api_key = os.environ.get("OPENAI_API_KEY")
    print(f"로드 후 OPENAI_API_KEY: {api_key}")
    
    # .env 파일 직접 읽기 시도
    print("\n.env 파일 직접 읽기 시도...")
    try:
        with open(".env", "r") as f:
            env_contents = f.read()
            print(f".env 파일 내용:\n{env_contents}")
    except Exception as e:
        print(f".env 파일 읽기 오류: {e}")
    
except ImportError:
    print("python-dotenv 패키지가 설치되지 않았습니다.")
except Exception as e:
    print(f"dotenv 로드 중 오류 발생: {e}")

# 현재 디렉토리 파일 목록 확인
print("\n현재 디렉토리 파일 목록:")
import os
for file in os.listdir("."):
    print(file) 