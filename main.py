import pygame
import menu
import classes

def main():
    """Lényegi program előkészítése és indítása."""
    pygame.init()
    pygame.display.set_caption("Aknakereső")
    pygame.display.set_icon(pygame.image.load("Files/bomba.png"))
    menu.menu(pygame.display.set_mode(classes.Screen.get_size()))
    pygame.quit()

main()