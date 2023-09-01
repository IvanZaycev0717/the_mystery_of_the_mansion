import pygame
from pygame.math import Vector2 as vector
from settings import *

class Generic(pygame.sprite.Sprite):
	def __init__(self, pos, surf, group):
		super().__init__(group)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)

class Player(Generic):
	def __init__(self, pos, group):
		super().__init__(pos, pygame.Surface((39,80)), group)
		self.image.fill('red')
		self.inventory = {
			'gears': 0,
			'yellow_key': False,
			'pink_key': False,
			'green_key': False,
			'hammer': False,
			'hp': 100,
			'lives': 1,
			}

		# movement
		self.direction = vector()
		self.pos = vector(self.rect.topright)
		self.speed = 300

	def input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
		else:
			self.direction.x = 0

	def move(self, dt):
		self.pos += self.direction * self.speed * dt
		self.rect.topleft = (round(self.pos.x),round(self.pos.y))


	def update(self, dt):
		self.input()
		self.move(dt)

class Animated(Generic):
	def __init__(self, assets, pos, group):
		self.animation_frames = assets
		self.frame_index = 0
		super().__init__(pos, self.animation_frames[self.frame_index], group)
    
	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		self.frame_index = 0 if self.frame_index >= len(self.animation_frames) else self.frame_index
		self.image = self.animation_frames[int(self.frame_index)]


	def update(self, dt):
		self.animate(dt)

class Key(Animated):
	def __init__(self, key_type, assets, pos, group):
		super().__init__(assets, pos, group)
		self.rect = self.image.get_rect(center=pos)
		self.key_type = key_type

class Gear(Animated):
	def __init__(self, assets, pos, group):
		super().__init__(assets, pos, group)
		self.rect = self.image.get_rect(center=pos)

class Taken(Animated):
	def __init__(self, assets, pos, group):
		super().__init__(assets, pos, group)
		self.rect = self.image.get_rect(center=pos)
	
	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		if self.frame_index < len(self.animation_frames):
			self.image = self.animation_frames[int(self.frame_index)]
		else:
			self.kill()

class Activator(Generic):
	def __init__(self, pos, surf, group, func):
		super().__init__(pos, surf, group)
		self.func = func

class Spikes(Generic):
	def __init__(self, surf, pos, group):
		super().__init__(pos, surf, group)

class Fire(Animated):
	def __init__(self, assets, pos, group):
		super().__init__(assets, pos, group)
		self.rect = self.image.get_rect(center=pos)

class Slime(Animated):
	def __init__(self, assets, pos, group):
		super().__init__(assets, pos, group)
		self.rect = self.image.get_rect(center=pos)

class Camel(Generic):
	def __init__(self, pos, surf, group):
		super().__init__(pos, surf, group)

class Wasp(Generic):
	def __init__(self, pos, surf, group):
		super().__init__(pos, surf, group)

class FlyingEnemy(Generic):
	def __init__(self, assets, pos, group):
		self.animation_frames = assets
		self.frame_index = 0
		surf = self.animation_frames[self.frame_index]
		super().__init__(pos, surf, group)

class WalkingEnemies(Generic):
	def __init__(self, assets, pos, group):
		self.animation_frames = assets
		self.frame_index = 0
		surf = self.animation_frames[self.frame_index]
		super().__init__(pos, surf, group)

class Angel(Generic):
	def __init__(self, assets, pos, group):
		self.animation_frames = assets
		self.frame_index = 0
		self.orientation = 'left'
		surf = self.animation_frames[f'run_{self.orientation}'][self.frame_index]
		super().__init__(pos, surf, group)

class Goat(Generic):
	def __init__(self, assets, pos, group):
		self.animation_frames = assets
		self.frame_index = 0
		self.orientation = 'right'
		surf = self.animation_frames[f'run_{self.orientation}'][self.frame_index]
		super().__init__(pos, surf, group)

class Harp(Animated):
	def __init__(self, assets, pos, group):
		super().__init__(assets, pos, group)
		self.rect = self.image.get_rect(center=pos)

class Bird(Generic):
	def __init__(self, assets, pos, group):
		self.animation_frames = assets
		self.frame_index = 0
		self.orientation = 'left'
		surf = self.animation_frames[f'fly_{self.orientation}'][self.frame_index]
		super().__init__(pos, surf, group)



