import pygame
import random
import sys

# --- 1. SETUP AND INITIALIZATION ---
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python MCQ Quiz Game")
clock = pygame.time.Clock()

# Colors (RGB format)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (65, 105, 225)
GREEN = (50, 205, 50)
RED = (220, 20, 60)
BG_COLOR = (240, 248, 255) # Alice Blue

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
    {"q":"Which function takes user input?","options":["input()","scan()","get()","read()"],"ans":"input()"},
    {"q":"Which keyword creates a class?","options":["class","object","define","struct"],"ans":"class"},
    {"q":"Which data type is immutable?","options":["tuple","list","set","dictionary"],"ans":"tuple"},
    {"q":"Which operator performs exponentiation?","options":["**","^","//","%%"],"ans":"**"},
    {"q":"Which keyword exits a loop?","options":["break","stop","exit","return"],"ans":"break"},
    {"q":"Which function converts string to integer?","options":["int()","str()","float()","num()"],"ans":"int()"},
    {"q":"Which data structure allows duplicate values?","options":["list","set","dictionary","none"],"ans":"list"},
    {"q":"Which keyword handles exceptions?","options":["try","catch","error","handle"],"ans":"try"},
    {"q":"Which operator performs floor division?","options":["//","/","%","**"],"ans":"//"},
    {"q":"Which function finds the maximum value?","options":["max()","maximum()","top()","big()"],"ans":"max()"},
    {"q":"Which keyword is used to import modules?","options":["import","include","using","require"],"ans":"import"}
]

# --- 3. GAME VARIABLES ---
state = "START"  # States: "START", "PLAY", "RESULT"
score = 0
time_limit = 120
start_time = 0
current_q_index = 0
current_options = []

# Button Rectangles (X, Y, Width, Height)
start_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 60)
# Option buttons (arranged in a 2x2 grid)
opt_btns = [
    pygame.Rect(100, 300, 280, 60), # Top Left
    pygame.Rect(420, 300, 280, 60), # Top Right
    pygame.Rect(100, 400, 280, 60), # Bottom Left
    pygame.Rect(420, 400, 280, 60)  # Bottom Right
]

def load_question():
    """Shuffles the options for the current question."""
    global current_options
    if current_q_index < len(quiz):
        current_options = quiz[current_q_index]["options"][:]
        random.shuffle(current_options)

def draw_text_centered(text, font, color, surface, x, y):
    """Helper function to draw text perfectly centered."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Shuffle the quiz initially
random.shuffle(quiz)

# --- 4. THE MAIN GAME LOOP ---
while True:
    screen.fill(BG_COLOR)

    # Calculate remaining time if playing
    if state == "PLAY":
        elapsed_seconds = (pygame.time.get_ticks() - start_time) // 1000
        time_left = time_limit - elapsed_seconds
        if time_left <= 0:
            state = "RESULT"

    # --- EVENT HANDLING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if state == "START":
                if start_btn.collidepoint(mouse_pos):
                    state = "PLAY"
                    start_time = pygame.time.get_ticks()
                    load_question()

            elif state == "PLAY":
                # Check if user clicked an option
                for i, btn in enumerate(opt_btns):
                    if btn.collidepoint(mouse_pos):
                        selected_ans = current_options[i]
                        correct_ans = quiz[current_q_index]["ans"]
                        
                        if selected_ans == correct_ans:
                            score += 1
                        
                        # Move to next question
                        current_q_index += 1
                        if current_q_index >= len(quiz):
                            state = "RESULT"
                        else:
                            load_question()

    # --- DRAWING THE SCREENS ---
    if state == "START":
        draw_text_centered("PYTHON MCQ QUIZ", font_title, BLACK, screen, WIDTH//2, HEIGHT//3)
        draw_text_centered(f"Time Limit: {time_limit} seconds", font_small, GRAY, screen, WIDTH//2, HEIGHT//3 + 50)
        
        pygame.draw.rect(screen, BLUE, start_btn, border_radius=10)
        draw_text_centered("START", font_opt, WHITE, screen, start_btn.centerx, start_btn.centery)

    elif state == "PLAY":
        # Draw Timer and Score
        timer_text = font_small.render(f"Time: {time_left}s", True, RED if time_left < 20 else BLACK)
        score_text = font_small.render(f"Score: {score}/{len(quiz)}", True, BLACK)
        screen.blit(timer_text, (20, 20))
        screen.blit(score_text, (WIDTH - 150, 20))

        # Draw Question Box
        q_text = quiz[current_q_index]["q"]
        pygame.draw.rect(screen, WHITE, (50, 100, 700, 120), border_radius=15)
        pygame.draw.rect(screen, BLUE, (50, 100, 700, 120), 3, border_radius=15)
        draw_text_centered(q_text, font_q, BLACK, screen, WIDTH//2, 160)

        # Draw Options
        for i, btn in enumerate(opt_btns):
            pygame.draw.rect(screen, WHITE, btn, border_radius=10)
            pygame.draw.rect(screen, GRAY, btn, 2, border_radius=10)
            
            # Highlight button lightly if mouse hovers over it
            if btn.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (220, 230, 255), btn, border_radius=10)

            draw_text_centered(current_options[i], font_opt, BLACK, screen, btn.centerx, btn.centery)

    elif state == "RESULT":
        draw_text_centered("===== RESULT =====", font_title, BLACK, screen, WIDTH//2, HEIGHT//4)
        
        draw_text_centered(f"Final Score: {score} / {len(quiz)}", font_q, BLUE, screen, WIDTH//2, HEIGHT//2 - 20)
        
        percentage = (score / len(quiz)) * 100
        draw_text_centered(f"Percentage: {percentage:.1f}%", font_q, BLACK, screen, WIDTH//2, HEIGHT//2 + 30)
        
        # Feedback logic
        if percentage >= 80:
            msg, color = "Excellent!", GREEN
        elif percentage >= 50:
            msg, color = "Good Job!", BLUE
        else:
            msg, color = "Keep Practicing!", RED
            
        draw_text_centered(msg, font_title, color, screen, WIDTH//2, HEIGHT//2 + 100)

    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate at 60 FPS
    clock.tick(60)