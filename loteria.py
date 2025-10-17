
import os
import sys
import random
import pygame

# -------- Settings --------
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Lotería Display"
IMAGE_DIR = os.path.join(os.path.dirname(__file__), "cards")
VALID_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

# Text & UI
BG_COLOR = (18, 18, 18)
TEXT_COLOR = (230, 230, 230)
COUNTER_POS = (20, 20)   # top-left
HELP_POS = (20, 50)
HELP_TEXT = "Space/→/Enter: Next | R: Reset | S: Shuffle | F: Fullscreen | Esc/Q: Quit"

def load_images(folder):
    if not os.path.isdir(folder):
        raise FileNotFoundError(f"Cards folder not found: {folder}")
    files = [f for f in os.listdir(folder) if os.path.splitext(f)[1].lower() in VALID_EXTS]
    if not files:
        raise FileNotFoundError("No image files found in 'cards' folder. Supported: " + ", ".join(sorted(VALID_EXTS)))
    # Deterministic ordering before shuffle, so runs are reproducible across machines
    files.sort()
    paths = [os.path.join(folder, f) for f in files]
    return paths

def scale_to_fit(image, max_w, max_h):
    iw, ih = image.get_size()
    scale = min(max_w / iw, max_h / ih)
    new_size = (max(1, int(iw * scale)), max(1, int(ih * scale)))
    return pygame.transform.smoothscale(image, new_size)

def draw_centered(surface, image):
    sw, sh = surface.get_size()
    iw, ih = image.get_size()
    x = (sw - iw) // 2
    y = (sh - ih) // 2
    surface.blit(image, (x, y))

def main():
    pygame.init()
    flags = pygame.RESIZABLE
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags)
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    # Fonts
    try:
        font = pygame.font.SysFont("Arial", 20)
    except:
        pygame.font.init()
        font = pygame.font.SysFont(None, 20)

    paths = load_images(IMAGE_DIR)
    deck = paths.copy()
    random.shuffle(deck)
    drawn = []

    fullscreen = False

    def reset_deck():
        nonlocal deck, drawn
        deck = paths.copy()
        random.shuffle(deck)
        drawn = []

    def shuffle_remaining():
        nonlocal deck
        random.shuffle(deck)

    def next_card():
        nonlocal deck, drawn
        if deck:
            drawn.append(deck.pop())
        # else: no-op when exhausted

    # Draw initial first card
    next_card()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key in (pygame.K_SPACE, pygame.K_RIGHT, pygame.K_RETURN):
                    next_card()
                elif event.key == pygame.K_r:
                    reset_deck()
                    next_card()
                elif event.key == pygame.K_s:
                    shuffle_remaining()
                elif event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)

        screen.fill(BG_COLOR)

        # Draw card
        if drawn:
            current_path = drawn[-1]
            try:
                img = pygame.image.load(current_path).convert_alpha()
            except Exception:
                # Fallback load without alpha conversion
                img = pygame.image.load(current_path)

            # Scale to fit with some padding
            sw, sh = screen.get_size()
            pad = 40
            scaled = scale_to_fit(img, max(1, sw - pad*2), max(1, sh - pad*2))
            draw_centered(screen, scaled)

        # Counter & help
        counter_surf = font.render(f"{len(drawn)} / {len(paths)}", True, TEXT_COLOR)
        screen.blit(counter_surf, COUNTER_POS)
        help_surf = font.render(HELP_TEXT, True, TEXT_COLOR)
        screen.blit(help_surf, HELP_POS)

        # If deck is exhausted, show a small message
        if not deck and len(drawn) == len(paths):
            msg_surf = font.render("Deck complete. Press R to reset.", True, TEXT_COLOR)
            mw, mh = msg_surf.get_size()
            sw, sh = screen.get_size()
            screen.blit(msg_surf, ((sw - mw)//2, sh - mh - 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e)
        print("Make sure you have a 'cards' folder with images next to this script.")
