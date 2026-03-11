import pygame
import random
import sys

# --- 1. SETUP AND INITIALIZATION ---
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python MCQ Quiz Game")
clock = pygame.time.Clock()

# Colors
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)
BLUE, GREEN, RED = (65, 105, 225), (50, 205, 50), (220, 20, 60)
BG_COLOR = (240, 248, 255)

# Fonts
font_title = pygame.font.Font(None, 60)
font_q = pygame.font.Font(None, 45)
font_opt = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 30)

# --- 2. GAME DATA ---
quiz = [
    {"q":"Which keyword defines a function in Python?","options":["def","function","fun","define"],"ans":"def"},
    {"q":"Which data type stores text?","options":["int","str","float","bool"],"ans":"str"},
    {"q":"Which symbol is used for comments?","options":["#","//","/*","--"],"ans":"#"},
    {"q":"Output of len('Python')?","options":["5","6","7","Error"],"ans":"6"},
    {"q":"Which loop iterates over a sequence?","options":["for","repeat","loop","iterate"],"ans":"for"},
    {"q":"Which keyword is used for conditions?","options":["if","check","switch","case"],"ans":"if"},
    {"q":"Which function prints output?","options":["print()","display()","echo()","output()"],"ans":"print()"},
    {"q":"Which operator means 'equal to'?","options":["==","=","!=","<>"],"ans":"=="},
    {"q":"Which data structure stores key-value pairs?","options":["dictionary","list","tuple","set"],"ans":"dictionary"},
    {"q":"Which function takes user input?","options":["input()","scan()","get()","read()"],"ans":"input()"}
]

# --- 3. GAME VARIABLES ---
state = "START"
score = 0
time_limit = 120
start_time = 0
current_q_index = 0
current_options = []

start_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 60)
restart_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 150, 200, 60)
opt_btns = [
    pygame.Rect(100, 300, 280, 60), pygame.Rect(420, 300, 280, 60),
    pygame.Rect(100, 400, 280, 60), pygame.Rect(420, 400, 280, 60)
]

def load_question():
    global current_options
    if current_q_index < len(quiz):
        current_options = quiz[current_q_index]["options"][:]
        random.shuffle(current_options)

def draw_text_centered(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

random.shuffle(quiz)

# --- 4. THE MAIN GAME LOOP ---
while True:
    screen.fill(BG_COLOR)
    time_left = 0 

    if state == "PLAY":
        elapsed_seconds = (pygame.time.get_ticks() - start_time) // 1000
        time_left = max(0, time_limit - elapsed_seconds)
        if time_left <= 0:
            state = "RESULT"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if state == "START" and start_btn.collidepoint(mouse_pos):
                state, score, current_q_index = "PLAY", 0, 0
                start_time = pygame.time.get_ticks()
                load_question()
            elif state == "PLAY":
                for i, btn in enumerate(opt_btns):
                    if btn.collidepoint(mouse_pos):
                        if current_options[i] == quiz[current_q_index]["ans"]:
                            score += 1
                        current_q_index += 1
                        if current_q_index >= len(quiz):
                            state = "RESULT"
                        else:
                            load_question()
            elif state == "RESULT" and restart_btn.collidepoint(mouse_pos):
                state = "START"
                random.shuffle(quiz)

    # --- DRAWING ---
    if state == "START":
        draw_text_centered("PYTHON MCQ QUIZ", font_title, BLACK, screen, WIDTH//2, HEIGHT//3)
        pygame.draw.rect(screen, BLUE, start_btn, border_radius=10)
        draw_text_centered("START", font_opt, WHITE, screen, start_btn.centerx, start_btn.centery)

    elif state == "PLAY":
        # UI Elements
        timer_text = font_small.render(f"Time: {time_left}s", True, RED if time_left < 20 else BLACK)
        score_text = font_small.render(f"Score: {score}/{len(quiz)}", True, BLACK)
        screen.blit(timer_text, (20, 20))
        screen.blit(score_text, (WIDTH - 150, 20))

        # Question Box
        q_box = pygame.Rect(50, 100, 700, 120)
        pygame.draw.rect(screen, WHITE, q_box, border_radius=15)
        pygame.draw.rect(screen, BLUE, q_box, 3, border_radius=15)
        draw_text_centered(quiz[current_q_index]["q"], font_q, BLACK, screen, q_box.centerx, q_box.centery)

        # Options
        for i, btn in enumerate(opt_btns):
            pygame.draw.rect(screen, WHITE, btn, border_radius=10)
            pygame.draw.rect(screen, GRAY, btn, 2, border_radius=10)
            if btn.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (220, 230, 255), btn, border_radius=10)
            draw_text_centered(current_options[i], font_opt, BLACK, screen, btn.centerx, btn.centery)

    elif state == "RESULT":
        draw_text_centered("===== RESULT =====", font_title, BLACK, screen, WIDTH//2, HEIGHT//4)
        draw_text_centered(f"Final Score: {score} / {len(quiz)}", font_q, BLUE, screen, WIDTH//2, HEIGHT//2 - 20)
        pygame.draw.rect(screen, GREEN, restart_btn, border_radius=10)
        draw_text_centered("RESTART", font_opt, WHITE, screen, restart_btn.centerx, restart_btn.centery)

    pygame.display.flip()
    clock.tick(60)