"""
本地測試 Web 版本的腳本
在構建 Web 版本前，可以先測試遊戲邏輯是否正常
"""
import sys
import os

# 添加路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 直接運行 main_web.py（不使用 pygbag）
if __name__ == "__main__":
    print("本地測試模式（不使用 pygbag）")
    print("注意：這會使用標準的 pygame，不是 Web 版本")
    print("要構建真正的 Web 版本，請使用: python build_web.py")
    print("-" * 50)
    
    # 直接導入並運行（會使用標準 asyncio，不是 pygbag）
    import asyncio
    from main_web import main
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n遊戲已停止")

