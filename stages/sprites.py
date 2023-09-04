import pygame
from pygame.math import Vector2 as vector
from settings import *

class Generic(pygame.sprite.Sprite):
	def __init__(self, pos, surf, group):
		super().__init__(group)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)

class Player(Generic):
	def __init__(self, pos, assets, group, collision_sprites):
		self.animation_frames = assets
		self.frame_index = 0
		self.status = 'idle'
		self.orientation = 'right'
		self.is_sitting = False
		self.is_dead = False
		surf = self.animation_frames[f'{self.status}_{self.orientation}'][self.frame_index]
		super().__init__(pos, surf, group)

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
		self.pos = vector(self.rect.center)
		self.speed = 300
		self.gravity = 4
		self.on_floor = False

		# collision
		self.collision_sprites = collision_sprites
		self.hitbox = self.rect.inflate(-10, 0)
	
	def get_status(self):
		if self.direction.y < 0:
			self.status = 'jump'
		elif self.direction.y > 0.2:
			self.status = 'fall'
		elif self.is_sitting:
			self.status = 'sit'
		elif self.is_dead:
			self.status = 'death'
		else:
			self.status = 'walk' if self.direction.x != 0 and not self.is_sitting else 'idle'
		

	def input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT] and not self.is_sitting and not self.is_dead:
			self.direction.x = 1
			self.orientation = 'right'
		elif keys[pygame.K_LEFT] and not self.is_sitting and not self.is_dead:
			self.direction.x = -1
			self.orientation = 'left'
		else:
			self.is_sitting = False
			self.direction.x = 0
		
		if keys[pygame.K_DOWN] and self.on_floor and not self.is_dead:
			self.is_sitting = True
		
		if keys[pygame.K_SPACE] and self.on_floor and not self.is_dead:
			self.direction.y = -2
		
		if self.inventory['hp'] <= 0 and self.status != 'jump':
			self.is_dead = True
	
	def animate(self, dt):
		current_animation = self.animation_frames[f'{self.status}_{self.orientation}']
		self.frame_index += ANIMATION_SPEED * dt
		if not self.is_dead:
			self.frame_index = 0 if self.frame_index >= len(current_animation) else self.frame_index
			self.image = current_animation[int(self.frame_index)]
		else:
			self.image = current_animation[0]

	def move(self, dt):
		# horizontal
		self.pos.x += self.direction.x * self.speed * dt
		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		self.collision('horizontal')

		# vertical
		self.pos.y += self.direction.y * self.speed * dt
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		self.collision('vertical')
	
	def apply_gravity(self, dt):
		self.direction.y += self.gravity * dt
		self.rect.y += self.direction.y
	
	def check_on_floor(self):
		floor_rect = pygame.Rect(self.hitbox.bottomleft,(self.hitbox.width, 2))
		floor_sptites = [sprite for sprite in self.collision_sprites if sprite.rect.colliderect(floor_rect)]
		self.on_floor = True if floor_sptites else False
	
	def collision(self, direction):
		for sprite in self.collision_sprites:
			if sprite.rect.colliderect(self.hitbox):
				if direction == 'horizontal':
					self.hitbox.right = sprite.rect.left if self.direction.x >  0 else self.hitbox.right
					self.hitbox.left = sprite.rect.right if self.direction.x <  0 else self.hitbox.left
					self.rect.centerx, self.pos.x = self.hitbox.centerx, self.hitbox.centerx
				else:
					self.hitbox.top = sprite.rect.bottom if self.direction.y < 0 else self.hitbox.top
					self.hitbox.bottom = sprite.rect.top if self.direction.y > 0 else self.hitbox.bottom
					self.rect.centery, self.pos.y = self.hitbox.centery, self.hitbox.centery
					self.direction.y = 0


	def update(self, dt):
		self.input()
		self.apply_gravity(dt)
		self.move(dt)
		self.check_on_floor()
		self.get_status()
		self.animate(dt)

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



