import os
import pickle

# 資料集路徑
DATA_PATH = "dataset/training_data.pkl"

def check_training_data():
    """檢查訓練資料是否存在及統計資訊"""
    print("=" * 50)
    print("檢查通關資料儲存狀態")
    print("=" * 50)
    
    # 檢查目錄
    dataset_dir = "dataset"
    if not os.path.exists(dataset_dir):
        print(f"[X] {dataset_dir} 目錄不存在")
        print("   這表示還沒有任何通關資料被儲存")
        return
    
    print(f"[OK] {dataset_dir} 目錄存在")
    
    # 檢查檔案
    if not os.path.exists(DATA_PATH):
        print(f"[X] {DATA_PATH} 檔案不存在")
        print("   這表示還沒有任何通關資料被儲存")
        print("\n提示：")
        print("   1. 確保使用 ml/ml_play_collect_data.py 來遊玩")
        print("   2. 只有通關（GAME_PASS）的局才會儲存資料")
        print("   3. 失敗的局資料會被丟棄")
        return
    
    print(f"[OK] {DATA_PATH} 檔案存在")
    
    # 讀取並統計資料
    try:
        with open(DATA_PATH, "rb") as f:
            data = pickle.load(f)
        
        num_samples = len(data)
        file_size = os.path.getsize(DATA_PATH)
        
        print(f"\n[資料統計]")
        print(f"   總樣本數：{num_samples} 筆")
        print(f"   檔案大小：{file_size:,} bytes ({file_size/1024:.2f} KB)")
        
        if num_samples > 0:
            # 統計各方向的數量
            action_counts = {"UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0}
            for row in data:
                if len(row) >= 5:
                    action = row[4]
                    if action in action_counts:
                        action_counts[action] += 1
            
            print(f"\n[動作分布]")
            for action, count in action_counts.items():
                percentage = (count / num_samples * 100) if num_samples > 0 else 0
                print(f"   {action}: {count} 筆 ({percentage:.1f}%)")
            
            print(f"\n[OK] 資料儲存正常！")
        else:
            print(f"\n[警告] 檔案存在但資料為空")
            
    except Exception as e:
        print(f"❌ 讀取資料時發生錯誤：{e}")

if __name__ == "__main__":
    check_training_data()

