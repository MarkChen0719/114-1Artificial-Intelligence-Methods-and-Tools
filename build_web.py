"""
構建 Web 版本的腳本
使用 pygbag 將 Python 遊戲轉換為 WebAssembly
"""
import subprocess
import sys
import os
import shutil

def build_web():
    """構建 Web 版本"""
    print("開始構建 Web 版本...")
    
    # 檢查 pygbag 是否安裝
    try:
        import pygbag
        print("✅ pygbag 已安裝")
    except ImportError:
        print("❌ pygbag 未安裝，正在安裝...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygbag"])
    
    # 清理舊的構建產物
    build_dir = "build"
    if os.path.exists(build_dir):
        print(f"清理舊的構建目錄: {build_dir}")
        shutil.rmtree(build_dir)
    
    # 構建命令
    build_cmd = [
        sys.executable, "-m", "pygbag",
        "--app_name", "swimming_squid",
        "--title", "Swimming Squid",
        "--ume_block", "0",
        "main_web.py"
    ]
    
    print(f"執行命令: {' '.join(build_cmd)}")
    result = subprocess.run(build_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ 構建失敗:")
        print(result.stderr)
        return False
    
    # 檢查構建產物
    web_build_path = os.path.join(build_dir, "web")
    if not os.path.exists(web_build_path):
        # pygbag 可能將產物放在不同的位置，嘗試查找
        print("尋找構建產物...")
        for root, dirs, files in os.walk(build_dir):
            if "index.html" in files:
                web_build_path = root
                break
    
    if os.path.exists(web_build_path):
        print(f"\n✅ 構建完成！")
        print(f"構建產物在: {os.path.abspath(web_build_path)}")
        
        # 列出構建產物
        print("\n構建產物內容:")
        for item in os.listdir(web_build_path):
            item_path = os.path.join(web_build_path, item)
            if os.path.isdir(item_path):
                print(f"  📁 {item}/")
            else:
                size = os.path.getsize(item_path)
                print(f"  📄 {item} ({size} bytes)")
        
        return True
    else:
        print(f"❌ 找不到構建產物在 {web_build_path}")
        return False

if __name__ == "__main__":
    success = build_web()
    sys.exit(0 if success else 1)

