import pygame


class Menu:
    def __init__(self, window):
        self.window = window
        self.menu_screen()

    def menu_screen(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            self.window.fill((128, 128, 128))
            font = pygame.font.SysFont("comicsans", 60)
            text = font.render("Click to Play!", 1, (255, 0, 0))
            self.window.blit(text, (100, 200))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    run = False

        # main()
