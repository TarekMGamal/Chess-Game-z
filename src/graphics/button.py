import pygame


class Button:
    def __init__(self, window, text, x, y, color, button_id):
        self.window = window
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = self.window.get_width() - 200
        self.height = 100
        self.button_id = button_id

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("arial", 60)
        text = font.render(self.text, 1, (255, 255, 255))
        window.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                           self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
