import pygame
class Spritesheet:
    def __init__ (self, filename):
        self.filename = filename
        self.spritesheet = pygame.image.load(filename).convert()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w,h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.spritesheet,(0,0),(x,y,w,h))
        return sprite
