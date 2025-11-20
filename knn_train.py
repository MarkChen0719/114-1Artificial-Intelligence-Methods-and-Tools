import os
import pickle
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# 數據和模型路徑
DATA_PATH = "dataset/training_data.pkl"
MODEL_PATH = "model/knn_model.pkl"

# 標籤映射
label_to_id = {"UP": 0, "DOWN": 1, "LEFT": 2, "RIGHT": 3}
id_to_label = {v: k for k, v in label_to_id.items()}


def main():
    # 1. 加載數據集
    print("Loading dataset...")
    if not os.path.exists(DATA_PATH):
        print(f"Error: Dataset file '{DATA_PATH}' does not exist.")
        print("Please run the data collection script first.")
        return
    
    with open(DATA_PATH, "rb") as f:
        data = pickle.load(f)
    
    num_samples = len(data)
    print(f"Loaded {num_samples} samples from {DATA_PATH}")
    
    if num_samples == 0:
        print("Error: Dataset is empty.")
        return
    
    # 2. 準備特徵和標籤
    print("Preparing features and labels...")
    X = []
    y = []
    
    for row in data:
        # 特徵：前 4 個元素
        features = row[:4]
        # 標籤：第 5 個元素（action_str）
        action_str = row[4]
        
        X.append(features)
        y.append(action_str)
    
    # 轉換為 numpy 數組
    X = np.array(X, dtype=np.float64)
    y = np.array(y)
    
    print(f"Features shape: {X.shape}")
    print(f"Labels shape: {y.shape}")
    
    # 將字符串標籤轉換為整數 ID
    y_id = np.array([label_to_id[label] for label in y])
    
    # 3. 訓練 KNN 分類器
    print("Training KNN classifier...")
    knn = KNeighborsClassifier(n_neighbors=7, weights="distance")
    knn.fit(X, y_id)
    print("Training completed!")
    
    # 4. 保存模型
    print("Saving model...")
    os.makedirs("model", exist_ok=True)
    
    model_data = {
        "model": knn,
        "label_to_id": label_to_id,
        "id_to_label": id_to_label,
    }
    
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model_data, f)
    
    print(f"Model saved to {MODEL_PATH}")
    print("\nTraining finished successfully!")


if __name__ == "__main__":
    main()

