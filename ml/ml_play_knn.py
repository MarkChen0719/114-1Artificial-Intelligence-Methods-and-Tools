import math
import os
import pickle
import numpy as np


class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        print("Initial Hybrid AI (Collect Strategy + KNN fallback):", ai_name)

        # 搜索半徑（根據場地大小初始化）
        self.R = None

        # 食物與垃圾的距離權重指數
        self.food_dist_power = 1.0
        # 強化垃圾影響：距離越近越可怕
        self.garbage_dist_power = 2.2
        # 垃圾懲罰倍率（越大越怕垃圾）
        self.garbage_lambda = 2.5
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
        self.last_pos = None

        # 載入訓練好的 KNN 模型
        self.model = None
        self.id_to_label = None
        self.model_path = "model/knn_model.pkl"
        
        # KNN 使用閾值：當 collect 策略分數差異小於此值時，使用 KNN
        self.knn_uncertainty_threshold = 3.0
        
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, "rb") as f:
                    model_data = pickle.load(f)
                self.model = model_data["model"]
                self.id_to_label = model_data["id_to_label"]
                print(f"✅ 成功載入 KNN 模型：{self.model_path}")
            except Exception as e:
                print(f"❌ 載入模型失敗：{e}")
                print("將只使用 collect 策略（不使用 KNN）")
        else:
            print(f"⚠️  模型檔案不存在：{self.model_path}")
            print("將只使用 collect 策略（不使用 KNN）")

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
        """專門懲罰「前方錐形區」內的高負垃圾（score <= -4）"""
        if not garbages:
            return 0.0

        half_self_w = self_w / 2.0
        half_self_h = self_h / 2.0
        size_factor = 1.0 + 0.15 * max(0, self_lv - 1)

        base_forward = max(self_w, self_h) * 1.5 + vel * 3
        ahead_dist = base_forward * size_factor
        base_lateral = self_w * 1.0
        lateral_margin = base_lateral * size_factor

        penalty = 0.0

        for g in garbages:
            gscore = float(g["score"])

            if high_level and gscore == -1:
                continue
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

            gap_x = abs(dx) - (half_self_w + half_g_w)
            gap_y = abs(dy) - (half_self_h + half_g_h)
            gap_x = max(gap_x, 0.0)
            gap_y = max(gap_y, 0.0)

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

            center_dist = math.hypot(dx, dy)
            eff_dist = max(
                1e-3,
                center_dist - (half_self_w + half_g_w + half_self_h + half_g_h) * 0.25,
            )

            w = self._distance_weight(eff_dist, power=2.7)
            base_pen = abs(gscore) * 130.0 * w * size_factor

            min_pen = 0.0
            if gscore == -10.0:
                plus4_bonus = 1.0
                min_pen = plus4_bonus * math.e

            penalty += max(base_pen, min_pen)

        return penalty

    def _calculate_four_direction_scores(self, self_x, self_y, objs):
        """計算四個方位（上、下、左、右）的分數"""
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        scores = {d: 0.0 for d in directions}

        for obj in objs:
            obj_x = float(obj["x"])
            obj_y = float(obj["y"])
            obj_score = float(obj["score"])

            dx = obj_x - self_x
            dy = obj_y - self_y
            dist = self._distance(self_x, self_y, obj_x, obj_y)

            if dist > self.R:
                continue

            direction = self._classify_direction_to_four(dx, dy)
            weight = self._distance_weight(dist, self.food_dist_power)
            contrib = obj_score * weight
            scores[direction] += contrib

        score_vector = [scores["UP"], scores["DOWN"], scores["LEFT"], scores["RIGHT"]]
        return score_vector

    def _classify_direction_to_four(self, dx, dy):
        """將物體分類到 4 個方位之一：上、下、左、右"""
        abs_dx = abs(dx)
        abs_dy = abs(dy)

        if dy < 0:
            if abs_dx > abs_dy:
                return "RIGHT" if dx > 0 else "LEFT"
            else:
                return "UP"
        else:
            if abs_dx > abs_dy:
                return "RIGHT" if dx > 0 else "LEFT"
            else:
                return "DOWN"

    def _simulate_step(self, x, y, direction, vel):
        if direction == "UP":
            y -= vel
        elif direction == "DOWN":
            y += vel
        elif direction == "LEFT":
            x -= vel
        elif direction == "RIGHT":
            x += vel

        if self.left is not None:
            x = max(self.left, min(self.right, x))
        if self.top is not None:
            y = max(self.top, min(self.bottom, y))

        return x, y

    def _fallback_when_no_food(self, self_x, self_y, garbages, high_level: bool):
        """場上沒有食物時：優先遠離垃圾，其次回中心"""
        if not garbages:
            return self._direction_toward_center(self_x, self_y)

        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        danger = {d: 0.0 for d in directions}

        for g in garbages:
            gx = float(g["x"])
            gy = float(g["y"])
            gscore = float(g["score"])

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

    def _get_knn_prediction(self, score_vector):
        """使用 KNN 模型進行預測"""
        if self.model is None or self.id_to_label is None:
            return None

        features = np.array([score_vector], dtype=np.float64)
        predicted_id = self.model.predict(features)[0]
        predicted_action = self.id_to_label[predicted_id]
        return predicted_action

    # ===== 主邏輯 =====

    def update(self, scene_info: dict, *args, **kwargs):
        """
        Generate the command according to the received scene information
        使用 collect 策略，當策略不確定時使用 KNN 預測
        """
        status = scene_info.get("status", "GAME_ALIVE")
        if status != "GAME_ALIVE":
            return "RESET"

        self._init_env_info(scene_info)

        self_x = float(scene_info["self_x"])
        self_y = float(scene_info["self_y"])
        self_vel = float(scene_info.get("self_vel", 10.0))
        self_w = float(scene_info.get("self_w", 40.0))
        self_h = float(scene_info.get("self_h", 60.0))
        self_lv = int(scene_info.get("self_lv", 1))

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
            return [self._fallback_when_no_food(self_x, self_y, garbages, high_level)]

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
                continue

            food_weight = self._distance_weight(dist_f, self.food_dist_power)
            food_attract = fscore * food_weight

            garbage_threat = 0.0
            for g in garbages:
                gx = float(g["x"])
                gy = float(g["y"])
                gscore = float(g["score"])

                dist_g = self._distance(fx, fy, gx, gy)
                if dist_g > garbage_radius:
                    continue

                if high_level and gscore == -1:
                    continue

                w_g = self._distance_weight(dist_g, self.garbage_dist_power)
                garbage_threat += abs(gscore) * w_g

            utility = food_attract - self.garbage_lambda * garbage_threat

            if fscore >= 4:
                utility += 1.0
            elif fscore == 2:
                utility += 0.35
            else:
                utility += 0.08

            if utility > best_utility:
                best_utility = utility
                best_food = food

        # 如果所有 food 都被 R 過濾掉（太遠），就回中心等刷新
        if best_food is None:
            direction = self._direction_toward_center(self_x, self_y)
            self.last_dir = direction
            self.last_pos = (self_x, self_y)
            return [direction]

        # ===== 2. 針對選中的最佳 food，決定方向 =====
        target_x = float(best_food["x"])
        target_y = float(best_food["y"])

        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        dir_score = {d: -1e9 for d in directions}

        for d in directions:
            next_x, next_y = self._simulate_step(self_x, self_y, d, self_vel)
            dist_after = self._distance(next_x, next_y, target_x, target_y)
            dist_now = self._distance(self_x, self_y, target_x, target_y)
            gain = dist_now - dist_after

            wall_penalty = self._avoid_wall_penalty(d, self_x, self_y, self_vel)
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
        second_best_dir = max(
            [d for d in directions if d != best_dir],
            key=lambda d: dir_score[d],
            default=best_dir
        )

        # 計算分數差異（用於判斷是否不確定）
        score_diff = dir_score[best_dir] - dir_score[second_best_dir]

        # 方案2：當 collect 策略不確定時，使用 KNN 預測
        if score_diff < self.knn_uncertainty_threshold and self.model is not None:
            # 計算四個方位的分數
            score_vector = self._calculate_four_direction_scores(self_x, self_y, objs)
            # 使用 KNN 預測
            knn_prediction = self._get_knn_prediction(score_vector)
            if knn_prediction is not None:
                # 如果 KNN 預測的方向分數也不差，使用 KNN 預測
                if dir_score[knn_prediction] >= dir_score[best_dir] - 2.0:
                    best_dir = knn_prediction

        # 防抖：如果新方向比上一幀方向只好一點點，就維持上一幀方向
        if self.last_dir in directions:
            diff = dir_score[best_dir] - dir_score[self.last_dir]
            jitter_threshold = 5.0
            if diff < jitter_threshold:
                best_dir = self.last_dir

        self.last_dir = best_dir
        self.last_pos = (self_x, self_y)

        return [best_dir]

    def reset(self):
        """Reset the status"""
        print("reset ml script")
        self.R = None
        self.last_dir = "NONE"
        self.last_pos = None
