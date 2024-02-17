import pygame
import asyncio
from graphics.button import Button
from game import Game
from boards.board import Board
from network.network import Network


class Menu:
    def __init__(self):
        pygame.init()
        self.width = 1200
        self.height = 600
        self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.buttons = [Button(self.window, "PVP", 100, 100, (70, 70, 70), "pvp"),
                        Button(self.window, "Play Online", 100, 250, (70, 70, 70), "online"),
                        Button(self.window, "Play VS AI (coming soon)", 100, 400, (70, 70, 70), "ai")]
        self.menu_screen()

    def redraw_menu(self):
        self.window.fill((128, 128, 128))

        for button in self.buttons:
            button.draw(self.window)

        pygame.display.update()

    async def menu_screen(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(15)
            self.redraw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.click(pos):
                            if button.button_id == "online":
                                network = Network()

                                while True:
                                    font = pygame.font.Font(pygame.font.get_default_font(), 90)
                                    text = font.render("searching for a game...", 1, (255, 0, 0))
                                    self.window.blit(text,
                                                     (self.window.get_width() / 2 - text.get_width() / 2,
                                                      self.window.get_height() / 2 - text.get_height() / 2))
                                    pygame.display.update()

                                    board = network.send_and_receive("get")

                                    if board:
                                        print("found a board: ", board)
                                        game = Game(board, mode="online", network=network)
                                        game.run_game()
                                        self.window = pygame.display.set_mode((self.width, self.height),
                                                                              pygame.RESIZABLE)
                                        pygame.display.update()
                                        break
                            else:
                                dummy_network = Network(is_dummy=True)
                                board = Board(0)
                                game = Game(board, mode=button.button_id, network=dummy_network)
                                game.run_game()
                                self.window = pygame.display.set_mode((self.width, self.height),
                                                                      pygame.RESIZABLE)
                                pygame.display.update()
                elif event.type == pygame.VIDEORESIZE:
                    width, height = event.size
                    self.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            await asyncio.sleep(0)
