import math
import os
import pickle


class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        print("Initial target-based AI with strong garbage avoidance and +4 preference:", ai_name)

        # 搜索半徑（根據場地大小初始化）
        self.R = None

        # 食物與垃圾的距離權重指數
        self.food_dist_power = 1.0
        # 強化垃圾影響：距離越近越可怕
        self.garbage_dist_power = 2.2   # 原本 1.8，可再微調

        # 垃圾懲罰倍率（越大越怕垃圾）
        self.garbage_lambda = 2.5       # 原本 2.0，可再微調

        # 計算垃圾威脅時的範圍（比 R 小）
        self.garbage_radius_ratio = 0.65

        # 靠牆安全距離
        self.wall_margin = 40

        # 場地資訊
        self.center_x = None
        self.center_y = None
        self.left = None
        self.right = None
        self.top = None
        self.bottom = None

        # 防抖用：上一幀的方向
        self.last_dir = "NONE"
        self.last_pos = None  # (x, y)

        # 數據收集相關變量
        self.data = []  # 本局收集的數據
        self.all_data = []  # 所有歷史數據
        self.last_status = "GAME_ALIVE"  # 記錄上一幀的狀態
        
        # 資料集路徑
        self.dataset_dir = "dataset"
        self.dataset_path = os.path.join(self.dataset_dir, "training_data.pkl")
        
        # 如果資料檔已經存在，就先把舊資料載進來
        if os.path.exists(self.dataset_path):
            try:
                with open(self.dataset_path, "rb") as f:
                    self.all_data = pickle.load(f)
                print(f"載入既有資料集，共 {len(self.all_data)} 筆資料")
            except Exception as e:
                print("載入既有資料失敗，將從空白資料集開始:", e)

    # ===== 環境初始化 =====

    def _init_env_info(self, scene_info: dict):
        if self.R is not None:
            return

        env = scene_info.get("env", {})
        playground_w = float(env.get("playground_size_w", 700))
        playground_h = float(env.get("playground_size_h", 550))

        # 搜尋半徑：取短邊 70%，看中距離即可
        short_side = min(playground_w, playground_h)
        self.R = short_side * 0.7

        # 邊界
        self.left = float(env.get("left", 0))
        self.right = float(env.get("right", playground_w))
        self.top = float(env.get("top", 0))
        self.bottom = float(env.get("bottom", playground_h))

        self.center_x = (self.left + self.right) / 2
        self.center_y = (self.top + self.bottom) / 2

    # ===== 小工具 =====

    def get_distance(self, x1, y1, x2, y2):
        """
        Calculate the distance between two points
        """
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def _distance(self, x1, y1, x2, y2):
        return math.hypot(x1 - x2, y1 - y2)

    def _distance_weight(self, dist, power):
        if dist <= 0:
            dist = 1e-6
        return 1.0 / (dist ** power)

    def _direction_toward_point(self, self_x, self_y, target_x, target_y):
        dx = target_x - self_x
        dy = target_y - self_y
        abs_dx = abs(dx)
        abs_dy = abs(dy)
        if abs_dx >= abs_dy:
            return "RIGHT" if dx > 0 else "LEFT"
        else:
            return "DOWN" if dy > 0 else "UP"

    def _direction_toward_center(self, self_x, self_y):
        if self.center_x is None or self.center_y is None:
            return "NONE"
        return self._direction_toward_point(self_x, self_y, self.center_x, self.center_y)

    def _avoid_wall_penalty(self, direction, x, y, vel):
        penalty = 0.0
        dist_top = y - self.top
        dist_bottom = self.bottom - y
        dist_left = x - self.left
        dist_right = self.right - x

        margin = self.wall_margin + vel

        if direction == "UP" and dist_top < margin:
            penalty += 60.0
        if direction == "DOWN" and dist_bottom < margin:
            penalty += 60.0
        if direction == "LEFT" and dist_left < margin:
            penalty += 60.0
        if direction == "RIGHT" and dist_right < margin:
            penalty += 60.0

        return penalty

    # ===== 前方高負垃圾避讓（含魷魚體積與等級） =====

    def _forward_garbage_penalty(
        self,
        direction,
        self_x,
        self_y,
        vel,
        garbages,
        self_w,
        self_h,
        high_level=False,
        self_lv=1,
    ):
        """
        專門懲罰「前方錐形區」內的高負垃圾（score <= -4）
        - level 14 / 15 時可忽略 -1
        - 把魷魚與垃圾的體積 (w, h) + 等級 (self_lv) 納入碰撞風險估計
        - 對於 -10：懲罰下限為 +4 bonus 的 e 倍
        """
        if not garbages:
            return 0.0

        # 魷魚的半寬/半高
        half_self_w = self_w / 2.0
        half_self_h = self_h / 2.0

        # 等級越高越胖：安全距離放大
        size_factor = 1.0 + 0.15 * max(0, self_lv - 1)  # lv1=1.0, lv6≈1.75

        # 往前看的距離：體積 + 速度 + 等級
        base_forward = max(self_w, self_h) * 1.5 + vel * 3
        ahead_dist = base_forward * size_factor

        # 左右檢查寬度
        base_lateral = self_w * 1.0
        lateral_margin = base_lateral * size_factor

        penalty = 0.0

        for g in garbages:
            gscore = float(g["score"])

            # 高關卡時忽略 -1 垃圾
            if high_level and gscore == -1:
                continue

            # 只加強 -4 / -10
            if gscore > -4:
                continue

            gx = float(g["x"])
            gy = float(g["y"])
            gw = float(g.get("w", 30.0))
            gh = float(g.get("h", 30.0))

            half_g_w = gw / 2.0
            half_g_h = gh / 2.0

            dx = gx - self_x
            dy = gy - self_y

            # 「邊到邊」的 gap，小於 0 代表幾乎貼到
            gap_x = abs(dx) - (half_self_w + half_g_w)
            gap_y = abs(dy) - (half_self_h + half_g_h)
            gap_x = max(gap_x, 0.0)
            gap_y = max(gap_y, 0.0)

            # 判斷是否在前方錐形區（用 gap 而不是純中心距離）
            in_cone = False
            if direction == "UP":
                if dy < 0 and gap_x <= lateral_margin and abs(dy) <= ahead_dist:
                    in_cone = True
            elif direction == "DOWN":
                if dy > 0 and gap_x <= lateral_margin and dy <= ahead_dist:
                    in_cone = True
            elif direction == "LEFT":
                if dx < 0 and gap_y <= lateral_margin and abs(dx) <= ahead_dist:
                    in_cone = True
            elif direction == "RIGHT":
                if dx > 0 and gap_y <= lateral_margin and dx <= ahead_dist:
                    in_cone = True

            if not in_cone:
                continue

            # 有效距離：中心距離扣掉一部分半徑和，避免太樂觀
            center_dist = math.hypot(dx, dy)
            eff_dist = max(
                1e-3,
                center_dist - (half_self_w + half_g_w + half_self_h + half_g_h) * 0.25,
            )

            # 距離越近懲罰越大（power 調高一點）
            w = self._distance_weight(eff_dist, power=2.7)
            base_pen = abs(gscore) * 130.0 * w * size_factor

            # ★★★ 對 -10：懲罰下限為 +4 bonus 的 e 倍 ★★★
            # +4 bonus 在下方 utility 中設為 1.0
            min_pen = 0.0
            if gscore == -10.0:
                plus4_bonus = 1.0
                min_pen = plus4_bonus * math.e  # 約 2.718

            penalty += max(base_pen, min_pen)

        return penalty

    def _calculate_four_direction_scores(self, self_x, self_y, objs):
        """
        計算四個方位（上、下、左、右）的分數
        基於策略說明：以魷魚為中心，半徑 R 內搜索，計算各方位分數
        """
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        scores = {d: 0.0 for d in directions}

        for obj in objs:
            obj_x = float(obj["x"])
            obj_y = float(obj["y"])
            obj_score = float(obj["score"])  # 食物 > 0，垃圾 < 0

            # 計算物體與魷魚的距離（歐幾里得距離）
            dx = obj_x - self_x
            dy = obj_y - self_y
            dist = self._distance(self_x, self_y, obj_x, obj_y)

            # 只考慮半徑 R 內的物體
            if dist > self.R:
                continue

            # 將物體分類到對應的方位
            direction = self._classify_direction_to_four(dx, dy)

            # 計算距離權重（距離越近權重越大）
            weight = self._distance_weight(dist, self.food_dist_power)

            # 計算貢獻分數：原始分數 × 距離權重
            contrib = obj_score * weight

            # 累加到對應方位的分數
            scores[direction] += contrib

        # 將分數轉換為向量：[上, 下, 左, 右]
        score_vector = [scores["UP"], scores["DOWN"], scores["LEFT"], scores["RIGHT"]]
        return score_vector

    def _classify_direction_to_four(self, dx, dy):
        """
        將物體分類到 4 個方位之一：上、下、左、右
        基於物體相對於魷魚的位置
        """
        abs_dx = abs(dx)
        abs_dy = abs(dy)

        if dy < 0:  # 在魷魚上方
            if abs_dx > abs_dy:
                return "RIGHT" if dx > 0 else "LEFT"
            else:
                return "UP"
        else:  # 在魷魚下方或同一水平 (dy >= 0)
            if abs_dx > abs_dy:
                return "RIGHT" if dx > 0 else "LEFT"
            else:
                return "DOWN"

    # ===== 主邏輯 =====

    def update(self, scene_info: dict, *args, **kwargs):
        """
        Generate the command according to the received scene information
        每一個 frame 會被呼叫一次，可以利用每次傳入的 scene_info，撰寫對應的移動策略
        """
        status = scene_info.get("status", "GAME_ALIVE")
        if status != "GAME_ALIVE":
            self.last_status = status
            return "RESET"

        self._init_env_info(scene_info)

        self_x = float(scene_info["self_x"])
        self_y = float(scene_info["self_y"])
        self_vel = float(scene_info.get("self_vel", 10.0))
        self_w = float(scene_info.get("self_w", 40.0))
        self_h = float(scene_info.get("self_h", 60.0))
        self_lv = int(scene_info.get("self_lv", 1))

        # 嘗試讀 level，方便在 14/15 忽略 -1
        env = scene_info.get("env", {})
        level = scene_info.get("level", env.get("level", None))
        high_level = level in (14, 15)

        objs = scene_info.get("foods", [])

        # 分開食物 / 垃圾
        foods = []
        garbages = []
        for obj in objs:
            if obj["score"] > 0:
                foods.append(obj)
            else:
                garbages.append(obj)

        # 場上沒有任何食物 → 遠離垃圾 + 回中間
        if not foods:
            fallback_dir = self._fallback_when_no_food(self_x, self_y, garbages, high_level)
            # 計算四個方位的分數（用於數據收集，不影響決策邏輯）
            score_vector = self._calculate_four_direction_scores(self_x, self_y, objs)
            # 收集訓練資料
            row = [score_vector[0], score_vector[1], score_vector[2], score_vector[3], fallback_dir]
            self.data.append(row)
            self.last_status = status
            return [fallback_dir]

        # ===== 1. 對每一顆食物算「效用」，加入 +4 偏好 =====
        best_food = None
        best_utility = -1e9
        garbage_radius = self.R * self.garbage_radius_ratio

        for food in foods:
            fx = float(food["x"])
            fy = float(food["y"])
            fscore = float(food["score"])

            dist_f = self._distance(self_x, self_y, fx, fy)
            if dist_f > self.R:
                # 太遠的食物不考慮，避免亂追超遠目標
                continue

            # 食物吸引力：score / dist^α
            food_weight = self._distance_weight(dist_f, self.food_dist_power)
            food_attract = fscore * food_weight

            # 垃圾威脅：以「這顆食物為中心」看附近垃圾
            garbage_threat = 0.0
            for g in garbages:
                gx = float(g["x"])
                gy = float(g["y"])
                gscore = float(g["score"])  # 負數

                dist_g = self._distance(fx, fy, gx, gy)
                if dist_g > garbage_radius:
                    continue

                # 在 level 14/15 時，忽略 -1 垃圾的威脅
                if high_level and gscore == -1:
                    continue

                w_g = self._distance_weight(dist_g, self.garbage_dist_power)
                garbage_threat += abs(gscore) * w_g

            # 基礎效用
            utility = food_attract - self.garbage_lambda * garbage_threat

            # ★★★ 對 +4 有偏好，但權重不會大於避 -10 ★★★
            # 這裡設定 +4 bonus = 1.0，對應上面 min_pen = 1.0 * e
            if fscore >= 4:
                utility += 1.0        # +4 額外 bonus
            elif fscore == 2:
                utility += 0.35       # +2 中等 bonus
            else:  # fscore == 1
                utility += 0.08       # +1 小小 bonus

            if utility > best_utility:
                best_utility = utility
                best_food = food

        # 如果所有 food 都被 R 過濾掉（太遠），就回中心等刷新
        if best_food is None:
            direction = self._direction_toward_center(self_x, self_y)
            self.last_dir = direction
            self.last_pos = (self_x, self_y)
            # 計算四個方位的分數（用於數據收集，不影響決策邏輯）
            score_vector = self._calculate_four_direction_scores(self_x, self_y, objs)
            # 收集訓練資料
            row = [score_vector[0], score_vector[1], score_vector[2], score_vector[3], direction]
            self.data.append(row)
            self.last_status = status
            return [direction]

        # ===== 2. 針對選中的最佳 food，決定方向 =====
        target_x = float(best_food["x"])
        target_y = float(best_food["y"])

        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        dir_score = {d: -1e9 for d in directions}

        for d in directions:
            # 模擬走一步後距離目標的變化
            next_x, next_y = self._simulate_step(self_x, self_y, d, self_vel)
            dist_after = self._distance(next_x, next_y, target_x, target_y)
            dist_now = self._distance(self_x, self_y, target_x, target_y)
            gain = dist_now - dist_after  # 越大越好（代表距離變近）

            # 靠牆懲罰
            wall_penalty = self._avoid_wall_penalty(d, self_x, self_y, self_vel)

            # 前方高危垃圾懲罰（含體積、等級）
            garbage_penalty = self._forward_garbage_penalty(
                d,
                self_x,
                self_y,
                self_vel,
                garbages,
                self_w,
                self_h,
                high_level=high_level,
                self_lv=self_lv,
            )

            dir_score[d] = gain - wall_penalty - garbage_penalty

        # 選出 dir_score 最好的方向
        best_dir = max(directions, key=lambda d: dir_score[d])

        # 防抖：如果新方向比上一幀方向只好一點點，就維持上一幀方向
        if self.last_dir in directions:
            diff = dir_score[best_dir] - dir_score[self.last_dir]
            jitter_threshold = 5.0
            if diff < jitter_threshold:
                best_dir = self.last_dir

        self.last_dir = best_dir
        self.last_pos = (self_x, self_y)

        # 計算四個方位的分數（用於數據收集，不影響決策邏輯）
        score_vector = self._calculate_four_direction_scores(self_x, self_y, objs)

        # 收集訓練資料：score_vector + 動作
        # score_vector 的索引 0 到 3 對應 [up, down, left, right] 區域的分數
        row = [score_vector[0], score_vector[1], score_vector[2], score_vector[3], best_dir]
        self.data.append(row)

        self.last_status = status

        return [best_dir]

    def _simulate_step(self, x, y, direction, vel):
        if direction == "UP":
            y -= vel
        elif direction == "DOWN":
            y += vel
        elif direction == "LEFT":
            x -= vel
        elif direction == "RIGHT":
            x += vel

        # 夾在邊界內（避免模擬出界）
        if self.left is not None:
            x = max(self.left, min(self.right, x))
        if self.top is not None:
            y = max(self.top, min(self.bottom, y))

        return x, y

    def _fallback_when_no_food(self, self_x, self_y, garbages, high_level: bool):
        """
        場上沒有食物時：優先遠離垃圾，其次回中心。
        在 level14/15 可忽略 -1 的威脅。
        """
        if not garbages:
            return self._direction_toward_center(self_x, self_y)

        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        danger = {d: 0.0 for d in directions}

        for g in garbages:
            gx = float(g["x"])
            gy = float(g["y"])
            gscore = float(g["score"])

            # 高關卡時忽略 -1 垃圾的威脅
            if high_level and gscore == -1:
                continue

            dx = gx - self_x
            dy = gy - self_y
            dist = math.hypot(dx, dy)
            if dist == 0:
                dist = 1e-6

            w = self._distance_weight(dist, self.garbage_dist_power)
            main_dir = self._direction_toward_point(self_x, self_y, gx, gy)
            danger[main_dir] += abs(gscore) * w

        safe_dir = min(directions, key=lambda d: danger[d])

        center_dir = self._direction_toward_center(self_x, self_y)
        if danger[center_dir] <= danger[safe_dir] * 1.2:
            return center_dir
        else:
            return safe_dir

    def reset(self):
        """
        Reset the status
        遊戲每結束一回合，reset 會被呼叫，如果此回合通過的話會將訓練資料儲存起來
        """
        print("reset ml script")
        print(f"本局狀態: {self.last_status}, 本局共收集 {len(self.data)} 筆資料")

        # 如果此回合通過的話會將訓練資料儲存起來
        if self.last_status == "GAME_PASS":
            self.all_data.extend(self.data)

            # 確保 dataset 資料夾存在
            os.makedirs(self.dataset_dir, exist_ok=True)

            # 將資料儲存到 training_data.pkl
            with open(self.dataset_path, "wb") as f:
                pickle.dump(self.all_data, f)
            print(f"Data appended, total {len(self.all_data)} entries saved.")
        else:
            print("❌ 沒過關，本局資料丟棄")

        # 清空本局資料
        self.data.clear()
        self.R = None
        self.last_dir = "NONE"
        self.last_pos = None
        self.last_status = "GAME_ALIVE"
