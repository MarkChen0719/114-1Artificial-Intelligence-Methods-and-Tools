# **Swimming Squid** 魷來魷去

![swimming_squid](https://img.shields.io/github/v/tag/PAIA-Playful-AI-Arena/swimming_squid)

[![MLGame](https://img.shields.io/badge/MLGame->10.4.6a2-<COLOR>.svg)](https://github.com/PAIA-Playful-AI-Arena/MLGame)


這是一個魷魚吃東西小遊戲，茫茫的海洋中有美味的食物，也有人類拋棄的垃圾，請用你的AI幫助小小魷魚平安長大。

![demo](https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/swimming_squid/refs/heads/main/asset/swimming-squid.gif)

---
## 基礎介紹

### 啟動方式

- 直接啟動 [main.py](https://github.com/PAIA-Playful-AI-Arena/swimming_squid/blob/main/main.py) 即可執行

### 遊戲參數設定

```python
# main.py 
game = SwimmingSquid(
            level: int = 1,
            level_file: str = None,
            sound: str = "off")
```
- `level`: 選定內建關卡，預設為 1 選擇第一關。
- `level_file`: 使用外部檔案作為關卡，請注意，使用此設定將會覆蓋掉關卡編號，並且不會自動進入下一關。
- `sound`: 音效。

### 玩法

- 使用鍵盤 上、下、左、右 控制方塊

### 目標

1. 在遊戲時間截止前，盡可能吃到愈多的食物吧！

#### 通關條件

1. 時間結束前，吃到的食物超過`score`，即可過關。

#### 失敗條件

1. 時間結束前，吃到的食物少於`score`，即算失敗。

## 座標系統
1. 使用 pygame 座標系，`左上角`為原點，`X軸`往`右`為正，`Y軸`往`下`為正
2. 回傳的物件座標，皆為物體`中心點`座標


---


## 進階說明

### 使用ＡＩ玩遊戲

**直接使用現有策略：**

```bash
# 使用模板策略（ml_play_template.py）
python -m mlgame -i ./ml/ml_play_template.py ./ --level 1

# 使用 collect 策略（ml_play_collect_data.py，包含數據收集功能）
python -m mlgame -i ./ml/ml_play_collect_data.py ./ --level 1

# 使用 KNN 混合策略（需要先訓練模型，見下方說明）
python -m mlgame -i ./ml/ml_play_knn.py ./ --level 1

# 指定關卡
python -m mlgame -i ./ml/ml_play_template.py ./ --level 3

# 使用自定義關卡文件
python -m mlgame -i ./ml/ml_play_template.py ./ --level_file /path_to_file/level_file.json
```

**注意：**
- `ml_play_template.py` 和 `ml_play_collect_data.py` 可以直接使用，不需要額外數據
- `ml_play_knn.py` 需要先訓練模型（見下方「使用 KNN 模型」說明）
- 如果模型不存在，`ml_play_knn.py` 會自動降級為 collect 策略

### 程式碼結構

專案的主要程式碼結構如下：

- **`main.py`**：遊戲的主入口，負責初始化遊戲環境並啟動遊戲循環
- **`ml/ml_play_template.py`**：玩家的自定義 AI 策略文件，玩家需要在此文件中編寫控制魷魚行為的程式碼
- **`src/`**：包含遊戲的核心邏輯，包括遊戲物件、規則和事件處理等
- **`asset/`**：存放遊戲所需的資源文件，如圖片、音效等

### 作者的 collect 策略說明

在 `ml/ml_play_collect_data.py` 中實作了一個基於方位評分的策略，核心思路如下：

**基本概念：**
以魷魚為中心，在一個動態半徑 R 的範圍內搜索所有食物和垃圾。半徑 R 會根據場地大小自動調整，通常是場地短邊的 70% 左右，這樣可以專注在中距離的目標，不會被太遠的食物誤導。

**四個方位評分：**
先把遊戲區域劃分成四個方位：上、下、左、右。對於半徑 R 內的每個物體，看它相對於魷魚的位置，歸類到對應的方位。然後計算每個方位的總分：
- 食物的分數是正數（+1、+2、+4），距離越近權重越大
- 垃圾的分數是負數（-1、-4、-10），距離越近影響越大
- 用距離權重函數，讓近距離的物體影響更明顯

**食物選擇邏輯：**
不是單純看方位分數，而是對每個食物單獨計算「效用值」：
1. **食物吸引力**：食物的分數除以距離的某次方，距離越近吸引力越大
2. **垃圾威脅**：檢查這顆食物附近是否有垃圾，如果有就扣分。垃圾的威脅會根據距離和分數大小計算，-10 的垃圾特別危險
3. **+4 偏好**：對分數為 +4 的食物給予額外加成，因為它性價比最高
4. 選出效用值最高的食物作為目標

**方向決定：**
選定目標食物後，模擬往四個方向各走一步，看哪個方向能更接近目標。同時考慮：
- **靠牆懲罰**：如果某個方向會讓魷魚太靠近邊界，就扣分
- **前方垃圾懲罰**：如果某個方向的前方有垃圾（特別是 -10 的垃圾），會大幅扣分
- **防抖機制**：如果新方向只比當前方向好一點點（差距小於閾值），就維持當前方向，避免頻繁切換造成抖動

**特殊處理：**
- 如果場上沒有食物，就遠離垃圾並往場地中心移動
- 如果所有食物都太遠（超出半徑 R），也往中心移動等待新食物刷新
- 如果某個方位的總分為 0（沒有任何物體），會設為 -999，避免選擇空區域

這個策略的核心是平衡「追求高價值食物」和「避開危險垃圾」，同時考慮距離、方位和移動效率。實際測試時可以根據不同關卡調整參數，比如在高難度關卡可以加大垃圾威脅的權重。

### 如何編寫自己的策略

要編寫自己的 AI 策略，可以參考以下步驟：

**1. 複製模板文件**

```bash
# 複製 ml_play_template.py 作為起點
cp ml/ml_play_template.py ml/ml_play_my_strategy.py
```

**2. 了解基本結構**

每個策略文件都需要實作一個 `MLPlay` 類，包含三個主要方法：

```python
class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        """
        初始化方法，遊戲開始時會呼叫一次
        可以在這裡設定變數、載入模型等
        """
        print("Initial ml script")
        # 初始化你的變數
        self.some_variable = 0
    
    def update(self, scene_info: dict, *args, **kwargs):
        """
        每一幀都會呼叫這個方法
        scene_info 包含當前遊戲狀態的所有資訊
        回傳一個動作字串：["UP"], ["DOWN"], ["LEFT"], ["RIGHT"], 或 ["NONE"]
        """
        # 根據 scene_info 決定動作
        return ["UP"]
    
    def reset(self):
        """
        遊戲結束時會呼叫，可以用來重置狀態
        """
        print("reset ml script")
        pass
```

**3. 使用 scene_info**

`scene_info` 是一個字典，包含：
- `self_x`, `self_y`：魷魚當前位置
- `self_vel`：魷魚當前速度
- `self_lv`：魷魚當前等級
- `foods`：場上所有物體的列表，每個物體有 `x`, `y`, `score`, `type` 等資訊
- `score`：當前分數
- `score_to_pass`：通關所需分數
- `env`：環境參數，包含場地大小、邊界等

**4. 測試策略**

```bash
# 使用你的策略運行遊戲
python -m mlgame -i ./ml/ml_play_my_strategy.py ./ --level 1
```

**5. 迭代優化**

觀察策略的表現，調整參數和邏輯。可以：
- 調整搜索半徑
- 改變距離權重
- 修改垃圾威脅的計算方式
- 加入更多特殊情況的處理

### ＡＩ範例

以下是一個簡單的隨機策略範例：

```python
import random

class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        print("Initial ml script")

    def update(self, scene_info: dict, *args, **kwargs):
        # print("AI received data from game :", scene_info)
        actions = ["UP", "DOWN", "LEFT", "RIGHT", "NONE"]
        return random.sample(actions, 1)

    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
        pass
```

### 初始化操作說明

**1. 安裝環境**

確保已安裝 Python 3.6 或以上版本，然後安裝必要的依賴：

```bash
pip install -r requirements.txt
```

**2. 準備策略文件**

在 `ml/` 目錄下創建或修改你的策略文件。可以：
- 直接修改 `ml_play_template.py`
- 或複製它創建新的策略文件

**3. 運行遊戲**

使用 MLGame 框架運行遊戲：

```bash
# 使用模板策略
python -m mlgame -i ./ml/ml_play_template.py ./ --level 1

# 使用自定義策略（替換為你的文件名）
python -m mlgame -i ./ml/ml_play_my_strategy.py ./ --level 1

# 指定關卡
python -m mlgame -i ./ml/ml_play_template.py ./ --level 3

# 使用自定義關卡文件
python -m mlgame -i ./ml/ml_play_template.py ./ --level_file /path_to_file/level_file.json
```

**4. 觀察結果**

遊戲運行時會顯示：
- 魷魚的移動軌跡
- 分數變化
- 遊戲結束時的結果（通過/失敗）

在終端機中可以看到詳細的遊戲資訊和策略的輸出訊息。

### 遊戲資訊

- scene_info 的資料格式如下

```json
{
  "frame": 15,
  "score": 8,
  "score_to_pass": 10,
  "self_x": 350,
  "self_y": 300,
  "self_h": 60,
  "self_w": 40,
  "self_lv": 1,
  "self_vel": 10,
  "status": "GAME_ALIVE",
  "foods": [
    {
      "h": 30,
      "score": 1,
      "type": "FOOD_1",
      "w": 30,
      "x": 40,
      "y": 134
    },
    {
      "h": 40,
      "score": 2,
      "type": "FOOD_2",
      "w": 40,
      "x": 422,
      "y": 192
    },
    {
      "h": 50,
      "score": 4,
      "type": "FOOD_3",
      "w": 50,
      "x": 264,
      "y": 476
    },
    {
      "h": 30,
      "score": -1,
      "type": "GARBAGE_1",
      "w": 30,
      "x": 100,
      "y": 496
    },
    {
      "h": 40,
      "score": -4,
      "type": "GARBAGE_2",
      "w": 40,
      "x": 633,
      "y": 432
    },
    {
      "h": 50,
      "score": -10,
      "type": "GARBAGE_3",
      "w": 50,
      "x": 54,
      "y": 194
    }
  ],
  "env": {
      "time_to_play": 600,
      "playground_size_w":700, 
      "playground_size_h":550,
      "left": 100,
      "right": 500,
      "top": 100,
      "bottom": 600,
      "food_1": 6,
      "food_2": 4,
      "food_3": 2,
      "garbage_1": 3,
      "garbage_2": 2,
      "garbage_3": 2,
      "score_to_pass": 80
  }

}
```

- `frame`：遊戲畫面更新的編號
- `self_x`：玩家角色的Ｘ座標，表示方塊的`中心點`座標值，單位 pixel。
- `self_y`：玩家角色的Ｙ座標，表示方塊的`中心點`座標值，單位 pixel。
- `self_w`：玩家角色的寬度，單位 pixel。
- `self_h`：玩家角色的高度，單位 pixel。
- `self_vel`：玩家角色的速度，表示方塊每幀移動的像素，單位 pixel。
- `self_lv`：玩家角色的等級，最小 1 ，最大 6。
- `foods`：食物的清單，清單內每一個物件都是一個食物的`中心點`座標值，也會提供此食物是什麼類型和分數多少。
  -  `type` 食物類型： `FOOD_1`, `FOOD_2`, `FOOD_3`, `GARBAGE_1`, `GARBAGE_2`, `GARBAGE_3`
- `score`：目前得到的分數
- `score_to_pass`：通關分數
- `env`：環境資訊，裡面會包含遊戲設定檔的所有參數，也可以拿到邊界資訊。

- `status`： 目前遊戲的狀態
    - `GAME_ALIVE`：遊戲進行中
    - `GAME_PASS`：遊戲通關
    - `GAME_OVER`：遊戲結束

### 動作指令

- 在 update() 最後要回傳一個字串，主角物件即會依照對應的字串行動，一次只能執行一個行動。
    - `UP`：向上移動
    - `DOWN`：向下移動
    - `LEFT`：向左移動
    - `RIGHT`：向右移動
    - `NONE`：原地不動

### 遊戲結果

- 最後結果會顯示在console介面中，若是PAIA伺服器上執行，會回傳下列資訊到平台上。

```json
{
  "frame_used": 100,
  "status": "fail",
  "attachment": [
    {
      "squid": "1P",
      "score": 0,
      "rank": 1,
      "passed": false
    }
  ]
}
```

- `frame_used`：表示使用了多少個frame
- `status`：表示遊戲結束的狀態
  - `passed`:達到指定分數，回傳通過
  - `un_passed`:沒有達到指定分數，回傳不通過
- `attachment`：紀錄遊戲各個玩家的結果與分數等資訊
    - `squid`：玩家編號
    - `score`：吃到的食物總數
    - `rank`：排名
    - `passed`：是否通關

---

## 使用 KNN 模型（可選）

如果你想使用 KNN 混合策略（`ml_play_knn.py`），需要先收集數據並訓練模型：

**1. 收集訓練數據**

使用 `ml_play_collect_data.py` 收集數據，這個策略會在通關時自動保存訓練數據：

```bash
# 收集數據（建議在關卡 14、15 收集，數據質量較好）
python -m mlgame -i ./ml/ml_play_collect_data.py ./ --level 14
python -m mlgame -i ./ml/ml_play_collect_data.py ./ --level 15
```

數據會自動保存到 `dataset/training_data.pkl`。

**2. 檢查數據**

```bash
python check_data.py
```

**3. 訓練 KNN 模型**

```bash
python knn_train.py
```

模型會保存到 `model/knn_model.pkl`。

**4. 使用訓練好的模型**

```bash
python -m mlgame -i ./ml/ml_play_knn.py ./ --level 1
```

**提示：**
- 數據和模型文件（`.pkl`）不會上傳到 GitHub（已在 `.gitignore` 中）
- 每個使用者需要自己收集數據和訓練模型
- 或者直接使用 `ml_play_template.py` 或 `ml_play_collect_data.py`，它們不需要模型

---

## 參考資源
- 音效
    1. https://soundeffect-lab.info/sound/anime/
- 背景音樂
    1. https://www.motionelements.com/zh-hant/stock-music-28190007-bossa-nova-short-loop
- 圖片
    1. 魷魚 https://illustcenter.com/2022/07/03/rdesign_1659/
    2. 湯匙 https://illustcenter.com/2021/11/24/rdesign_6275/
    3. 薯條 https://illustcenter.com/2021/11/16/rdesign_5098/
    4. 空罐 https://illustcenter.com/2021/11/19/rdesign_5772/
    5. 魚1 https://illustcenter.com/2021/12/22/rdesign_8914/
    6. 魚2 https://illustcenter.com/2021/10/28/rdesign_3149/
    7. 蝦子 https://illustcenter.com/2021/10/28/rdesign_3157/