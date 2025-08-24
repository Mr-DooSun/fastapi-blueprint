# -*- coding: utf-8 -*-
import argparse
import subprocess
import time
from dotenv import load_dotenv

def run_user_service():
    """User 마이크로서비스 실행"""
    print("🟢 Starting User Service on port 8001...")
    subprocess.Popen([
        "uvicorn", "src.user.app:app", 
        "--reload", "--host", "127.0.0.1", "--port", "8001"
    ])

def run_chat_service():
    """Chat 마이크로서비스 실행"""  
    print("🔵 Starting Chat Service on port 8002...")
    subprocess.Popen([
        "uvicorn", "src.chat.app:app",
        "--reload", "--host", "127.0.0.1", "--port", "8002" 
    ])

def run_gateway():
    """Gateway 실행"""
    print("🟣 Starting Gateway on port 8000...")
    subprocess.Popen([
        "uvicorn", "src.apps.gateway.app:app",
        "--reload", "--host", "127.0.0.1", "--port", "8000"
    ])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", required=True, help="Environment (local, dev, prod)")
    parser.add_argument("--with-gateway", action="store_true", help="Run with Gateway")
    args = parser.parse_args()
    
    # 환경변수 로드
    load_dotenv(dotenv_path=f"_env/{args.env}.env", override=True)
    
    print("🚀 Starting Microservices...")
    
    # 마이크로서비스들 실행
    run_user_service()
    time.sleep(2)
    
    run_chat_service()
    time.sleep(2)
    
    if args.with_gateway:
        run_gateway()
    
    print("✅ All services started!")
    print("📊 Services:")
    print("   - User Service: http://localhost:8001/docs")
    print("   - Chat Service: http://localhost:8002/docs")
    if args.with_gateway:
        print("   - Gateway: http://localhost:8000/docs-swagger")

if __name__ == "__main__":
    main()
