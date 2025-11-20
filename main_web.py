"""
Web 版本的遊戲主程式
使用 pygbag 轉換成 WebAssembly，可在瀏覽器執行
支援手動模式和 AI 模式
"""
import asyncio
import sys
import os

import pygame

# 添加路徑以便導入模組
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mlgame.view.view import PygameView
from mlgame.game.generic import quit_or_esc
from mlgame.utils.enum import get_ai_name
from src.game import SwimmingSquid
from src.env import WIDTH, HEIGHT

# 導入 AI 模組（使用 template 版本，包含完整策略）
try:
    from ml.ml_play_template import MLPlay as AIPlayer
except ImportError:
    print("警告：無法載入 ml_play_template，將使用備用 AI")
    from ml.ml_play_manual import MLPlay as AIPlayer

FPS = 30


class GameMode:
    """遊戲模式"""
    MENU = "menu"
    MANUAL = "manual"
    AI = "ai"
    GAME_OVER = "game_over"


def draw_menu(screen, font):
    """繪製模式選擇選單"""
    screen.fill((43, 43, 73))  # BG_COLOR
    
    title_font = pygame.font.Font(None, 72)
    title_text = title_font.render("Swimming Squid", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH // 2, 150))
    screen.blit(title_text, title_rect)
    
    subtitle_font = pygame.font.Font(None, 36)
    subtitle_text = subtitle_font.render("選擇遊戲模式 / Choose Game Mode", True, (200, 200, 200))
    subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, 220))
    screen.blit(subtitle_text, subtitle_rect)
    
    # 手動模式按鈕
    manual_rect = pygame.Rect(WIDTH // 2 - 150, 300, 300, 60)
    pygame.draw.rect(screen, (100, 150, 200), manual_rect)
    pygame.draw.rect(screen, (255, 255, 255), manual_rect, 3)
    manual_text = font.render("手動模式 (Manual)", True, (255, 255, 255))
    manual_text_rect = manual_text.get_rect(center=manual_rect.center)
    screen.blit(manual_text, manual_text_rect)
    
    # AI 模式按鈕
    ai_rect = pygame.Rect(WIDTH // 2 - 150, 380, 300, 60)
    pygame.draw.rect(screen, (200, 100, 150), ai_rect)
    pygame.draw.rect(screen, (255, 255, 255), ai_rect, 3)
    ai_text = font.render("AI 模式 (AI Mode)", True, (255, 255, 255))
    ai_text_rect = ai_text.get_rect(center=ai_rect.center)
    screen.blit(ai_text, ai_text_rect)
    
    # 說明文字
    hint_font = pygame.font.Font(None, 24)
    hint_text = hint_font.render("點擊按鈕或按 M (手動) / A (AI) 選擇模式", True, (150, 150, 150))
    hint_rect = hint_text.get_rect(center=(WIDTH // 2, 480))
    screen.blit(hint_text, hint_rect)
    
    return manual_rect, ai_rect


def draw_game_over(screen, font, game, mode):
    """繪製遊戲結束畫面"""
    screen.fill((43, 43, 73))
    
    if game.is_passed:
        result_text = "過關！(PASSED!)"
        result_color = (118, 255, 3)  # SCORE_COLOR_PLUS
    else:
        result_text = "失敗 (FAILED)"
        result_color = (236, 64, 122)  # SCORE_COLOR_MINUS
    
    title_font = pygame.font.Font(None, 64)
    title = title_font.render(result_text, True, result_color)
    title_rect = title.get_rect(center=(WIDTH // 2, 200))
    screen.blit(title, title_rect)
    
    score_text = font.render(f"分數: {game.squid.score} / {game._score_to_pass}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WIDTH // 2, 280))
    screen.blit(score_text, score_rect)
    
    mode_text = font.render(f"模式: {'手動' if mode == GameMode.MANUAL else 'AI'}", True, (200, 200, 200))
    mode_rect = mode_text.get_rect(center=(WIDTH // 2, 320))
    screen.blit(mode_text, mode_rect)
    
    hint_text = font.render("按 R 重新開始，按 ESC 返回選單", True, (150, 150, 150))
    hint_rect = hint_text.get_rect(center=(WIDTH // 2, 400))
    screen.blit(hint_text, hint_rect)
    
    return hint_rect


async def main():
    """主遊戲循環（async 以支援 pygbag）"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Swimming Squid - Web Edition")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    # 遊戲狀態
    mode = GameMode.MENU
    game = None
    game_view = None
    ai_player = None
    current_level = 1
    
    running = True
    
    while running:
        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if mode == GameMode.MENU:
                        running = False
                    else:
                        # 返回選單
                        mode = GameMode.MENU
                        game = None
                        game_view = None
                        ai_player = None
                elif event.key == pygame.K_r and mode == GameMode.GAME_OVER:
                    # 重新開始遊戲
                    mode = GameMode.MANUAL if ai_player is None else GameMode.AI
                    game = SwimmingSquid(level=current_level)
                    scene_init_info_dict = game.get_scene_init_data()
                    game_view = PygameView(scene_init_info_dict)
                    if ai_player:
                        ai_player.reset()
                elif mode == GameMode.MENU:
                    if event.key == pygame.K_m:
                        mode = GameMode.MANUAL
                        game = SwimmingSquid(level=current_level)
                        scene_init_info_dict = game.get_scene_init_data()
                        game_view = PygameView(scene_init_info_dict)
                    elif event.key == pygame.K_a:
                        mode = GameMode.AI
                        game = SwimmingSquid(level=current_level)
                        scene_init_info_dict = game.get_scene_init_data()
                        game_view = PygameView(scene_init_info_dict)
                        # 初始化 AI
                        ai_player = AIPlayer("squid_ai")
            
            elif event.type == pygame.MOUSEBUTTONDOWN and mode == GameMode.MENU:
                mouse_pos = pygame.mouse.get_pos()
                manual_rect, ai_rect = draw_menu(screen, font)
                if manual_rect.collidepoint(mouse_pos):
                    mode = GameMode.MANUAL
                    game = SwimmingSquid(level=current_level)
                    scene_init_info_dict = game.get_scene_init_data()
                    game_view = PygameView(scene_init_info_dict)
                elif ai_rect.collidepoint(mouse_pos):
                    mode = GameMode.AI
                    game = SwimmingSquid(level=current_level)
                    scene_init_info_dict = game.get_scene_init_data()
                    game_view = PygameView(scene_init_info_dict)
                    # 初始化 AI
                    ai_player = AIPlayer("squid_ai")
        
        # 根據模式更新和繪製
        if mode == GameMode.MENU:
            manual_rect, ai_rect = draw_menu(screen, font)
            pygame.display.flip()
        
        elif mode == GameMode.MANUAL or mode == GameMode.AI:
            if game is None or game_view is None:
                continue
            
            # 獲取命令
            if mode == GameMode.MANUAL:
                # 手動模式：從鍵盤獲取命令
                commands = game.get_keyboard_command()
            else:
                # AI 模式：從 AI 獲取命令
                if ai_player is None:
                    ai_player = AIPlayer("squid_ai")
                
                scene_info = game.get_data_from_game_to_player()[get_ai_name(0)]
                ai_command = ai_player.update(scene_info)
                
                # 處理 AI 返回的命令格式
                if ai_command == "RESET":
                    # 遊戲結束，AI 要求重置
                    if game.is_passed:
                        current_level += 1
                    game.reset()
                    if ai_player:
                        ai_player.reset()
                    continue
                
                # 將 AI 命令轉換為遊戲格式（確保是列表）
                if isinstance(ai_command, str):
                    ai_command = [ai_command]
                elif not isinstance(ai_command, list):
                    ai_command = ["NONE"]
                
                commands = {get_ai_name(0): ai_command}
            
            # 更新遊戲
            result = game.update(commands)
            
            # 檢查遊戲狀態
            if not game.is_running:
                # 遊戲結束，顯示結果畫面
                mode = GameMode.GAME_OVER
                # 如果通關，準備下一關
                if game.is_passed:
                    current_level += 1
                    # 自動重置到下一關（可選）
                    # game.reset()
                    # if ai_player:
                    #     ai_player.reset()
            elif result == "RESET":
                # 遊戲內部要求重置（通常不會發生，因為我們已經檢查 is_running）
                if game.is_passed:
                    current_level += 1
                game.reset()
                if ai_player:
                    ai_player.reset()
            
            # 繪製遊戲畫面
            game_progress_data = game.get_scene_progress_data()
            game_view.draw(game_progress_data)
            pygame.display.flip()
        
        elif mode == GameMode.GAME_OVER:
            if game is not None:
                draw_game_over(screen, font, game, mode)
            else:
                # 如果 game 為 None，返回選單
                mode = GameMode.MENU
            pygame.display.flip()
        
        # 控制 FPS
        clock.tick(FPS)
        await asyncio.sleep(0)  # 讓出控制權，必要於 pygbag
    
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())

