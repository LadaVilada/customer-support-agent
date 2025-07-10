#!/usr/bin/env python3
"""
Development script to run both FastAPI backend and Streamlit frontend concurrently.
"""

import subprocess
import time
from typing import List

def run_command(command: List[str], name: str) -> subprocess.Popen:
    """
    Run a command in a subprocess.
    
    Args:
        command: List of command arguments
        name: Name for logging purposes
        
    Returns:
        subprocess.Popen object
    """
    print(f"🚀 Starting {name}...")
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return process

def main():
    """Main function to run both servers."""
    print("🤖 Starting Thoughtful AI Customer Support Agent (Development Mode)")
    print("=" * 60)
    
    # Start FastAPI backend
    fastapi_process = run_command(
        ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
        "FastAPI Backend"
    )
    
    # Wait a moment for FastAPI to start
    time.sleep(3)
    
    # Start Streamlit frontend
    streamlit_process = run_command(
        ["streamlit", "run", "streamlit_app.py", "--server.port", "8501"],
        "Streamlit Frontend"
    )
    
    print("\n✅ Both servers are starting up!")
    print("📱 FastAPI Backend: http://localhost:8000")
    print("🌐 Streamlit Frontend: http://localhost:8501")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop both servers...")
    
    try:
        # Wait for both processes
        fastapi_process.wait()
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        
        # Terminate processes
        fastapi_process.terminate()
        streamlit_process.terminate()
        
        # Wait for graceful shutdown
        try:
            fastapi_process.wait(timeout=5)
            streamlit_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("⚠️ Force killing processes...")
            fastapi_process.kill()
            streamlit_process.kill()
        
        print("✅ Servers stopped.")

if __name__ == "__main__":
    main() 