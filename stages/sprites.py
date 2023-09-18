from math import degrees, sin
from random import choice, randint
import pygame
from pygame.math import Vector2 as vector
from settings import *
import timer

class Generic(pygame.sprite.Sprite):
	def __init__(self, pos, surf, group, z=LEVEL_LAYERS['main']):
		super().__init__(group)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.z = z

class Block(Generic):
    def __init__(self, pos, size, group):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, group)

class Cloud(Generic):
	def __init__(self, pos, surf, group, left_limit):
		super().__init__(pos, surf, group, LEVEL_LAYERS['clouds'])
		self.left_limit = left_limit
	
		self.pos = vector(self.rect.topleft)
		self.speed = randint(20, 30)


	def update(self, dt, player_pos):
		self.pos.x -= self.speed * dt
		self.rect.x = round(self.pos.x)
		if self.rect.x <= self.left_limit:
			self.kill()

class Player(Generic):
	def __init__(self, pos, assets, group, collision_sprites, jump_sound, walk_sound):
		self.animation_frames = assets
		self.frame_index = 0
		self.status = 'idle'
		self.orientation = 'right'
		self.is_sitting = False
		self.current_hp = 100
		surf = self.animation_frames[f'{self.status}_{self.orientation}'][self.frame_index]
		super().__init__(pos, surf, group)
		self.mask = pygame.mask.from_surface(self.image)

		# movement
		self.direction = vector()
		self.pos = vector(self.rect.center)
		self.speed = 300
		self.gravity = 4
		self.on_floor = False

		# collision
		self.collision_sprites = collision_sprites
		self.hitbox = self.rect.inflate(-10, 0)

		# timer
		self.invul_timer = timer.Timer(200)

		# sound
		self.jump_sound = jump_sound
		self.jump_sound.set_volume(0.1)
		self.walk_sound = walk_sound
		self.walk_sound.set_volume(0.04)
	
	def damage(self):
		if not self.invul_timer.active and self.status != 'death':
			self.invul_timer.activate()
			self.direction.y -= 2
	
	def get_status(self):
		if self.direction.y < 0:
			self.status = 'jump'
		elif self.direction.y > 0.2:
			self.status = 'fall'
		elif self.is_sitting:
			self.status = 'sit'
		elif self.current_hp <= 0 and self.status != 'jump':
			self.status = 'death'
		else:
			self.status = 'walk' if self.direction.x != 0 and not self.is_sitting else 'idle'
		

	def input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT] and not self.is_sitting and self.status != 'death':
			self.direction.x = 1
			self.orientation = 'right'
			if self.status != 'jump' and self.status != 'fall':
				self.walk_sound.play()
		elif keys[pygame.K_LEFT] and not self.is_sitting and self.status != 'death':
			self.direction.x = -1
			self.orientation = 'left'
			if self.status != 'jump' and self.status != 'fall':
				self.walk_sound.play()
		else:
			self.is_sitting = False
			self.direction.x = 0
		
		if keys[pygame.K_DOWN] and self.on_floor and self.status != 'death':
			self.is_sitting = True
		
		if keys[pygame.K_SPACE] and self.on_floor and self.status != 'death':
			self.walk_sound.stop()
			self.direction.y = -2
			self.jump_sound.play()
			
	
	def animate(self, dt):
		current_animation = self.animation_frames[f'{self.status}_{self.orientation}']
		self.frame_index += ANIMATION_SPEED * dt
		if self.status != 'death':
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


	def update(self, dt, player_pos):
		self.input()
		self.apply_gravity(dt)
		self.move(dt)
		self.check_on_floor()
		self.invul_timer.update()
		self.get_status()
		self.animate(dt)

class Animated(Generic):
	def __init__(self, assets, pos, group, z=LEVEL_LAYERS['main']):
		self.animation_frames = assets
		self.frame_index = 0
		super().__init__(pos, self.animation_frames[self.frame_index], group, z)
    
	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		self.frame_index = 0 if self.frame_index >= len(self.animation_frames) else self.frame_index
		self.image = self.animation_frames[int(self.frame_index)]


	def update(self, dt, player_pos):
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
	def __init__(self, pos, surf, group, id):
		super().__init__(pos, surf, group)
		self.id = id

class Spikes(Generic):
	def __init__(self, surf, pos, group):
		super().__init__(pos, surf, group)
		self.mask = pygame.mask.from_surface(self.image)

class Fire(Animated):
	def __init__(self, assets, pos, group):
		super().__init__(assets, pos, group)

class Slime(Animated):
	def __init__(self, assets, pos, group):
		super().__init__(assets, pos, group)

class Camel(Generic):
	def __init__(self, pos, surf, group, splutter_surf, enemy_sprites):
		pos = list(pos)
		pos[1] -= 10
		pos = tuple(pos)
		super().__init__(pos, surf, group)

		# f*cking camel spit on me
		self.splutter_surf = splutter_surf
		self.has_shot = False
		self.attack_cooldown = timer.Timer(6000)
		self.enemy_sprites = enemy_sprites
	
	def animate(self, dt):
		if not self.has_shot:
			self.attack_cooldown.activate()
			splutter_direction = vector(-1, 0)
			Splutter(self.rect.center + vector(-60, -30), splutter_direction, self.splutter_surf, [self.groups(), self.enemy_sprites])
			self.has_shot = True
		if self.attack_cooldown.start_time == 0:
			self.has_shot = False
	
	def update(self, dt, player_pos):
		self.animate(dt)
		self.attack_cooldown.update()


class Splutter(Generic):
	def __init__(self, pos, direction, surf, group):
		super().__init__(pos, surf, group)
		self.mask = pygame.mask.from_surface(self.image)
	
		#movement
		self.pos = vector(self.rect.topleft)
		self.direction = direction
		self.speed = 150

		# self destruct
		self.timer = timer.Timer(6000)
		self.timer.activate()
	
	def update(self, dt, player_pos):
		# movement
		self.pos.x += self.direction.x * self.speed * dt
		self.rect.x = round(self.pos.x)

        # timer
		self.timer.update()
		if not self.timer.active:
			self.kill()


class Wasp(Generic):
	def __init__(self, pos, surf, group, collision_sprites):
		super().__init__(pos, surf, group)
		self.pos = vector(self.rect.topleft)
		self.speed = 120
		self.collision_sprites = collision_sprites
	
	def move(self, dt):

		self.pos.x -= self.speed * dt
		self.pos.y += self.speed // 2 * dt
		self.rect.x = round(self.pos.x)
		self.rect.y = round(self.pos.y)

		if [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(self.rect.midbottom + vector(0, 10))]:
			self.kill()
	
	def update(self, dt, player_pos):
		if abs(player_pos[0] - self.pos[0]) <= 450:
			self.move(dt)

class FlyingEnemy(Generic):
	def __init__(self, assets, pos, group, collision_sprites):
		self.animation_frames = assets
		self.frame_index = 0
		surf = self.animation_frames[self.frame_index]
		super().__init__(pos, surf, group)

		# movement
		self.pos = vector(self.rect.topleft)
		self.speed = 120
		self.collision_sprites = collision_sprites
		self.timer = timer.Timer(10000)
		self.timer.activate()
	
	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		self.frame_index = 0 if self.frame_index >= len(self.animation_frames) else self.frame_index
		self.image = self.animation_frames[int(self.frame_index)]
	
	def move(self, dt):
		self.pos.x -= self.speed * dt
		pos_y = sin((self.pos.x / 10)) * 25
		self.rect.x = round(self.pos.x)
		self.rect.y = round(self.pos.y - pos_y)
	
	def update(self, dt, player_pos):
		if abs(self.pos[0] - player_pos[0]) <= 600:
			self.animate(dt)
			self.move(dt)

			self.timer.update()
			if not self.timer.active:
				self.kill()


class WalkingEnemies(Generic):
	def __init__(self, assets, pos, group, collision_sprites):
		self.animation_frames = assets
		self.frame_index = 0
		surf = self.animation_frames[self.frame_index]
		super().__init__(pos, surf, group)
		self.rect.bottom = self.rect.top + TILE_SIZE
		self.mask = pygame.mask.from_surface(self.image)

		# movement
		self.pos = vector(self.rect.topleft)
		self.speed = 120
		self.collision_sprites = collision_sprites

		
		
	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		self.frame_index = 0 if self.frame_index >= len(self.animation_frames) else self.frame_index
		self.image = self.animation_frames[int(self.frame_index)]
	
	def move(self, dt):
		if not [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(self.rect.midbottom + vector(0, 10))]:
			self.kill()
		self.pos.x -= self.speed * dt
		self.rect.x = round(self.pos.x)

	
	def update(self, dt, player_pos):
		if abs(self.pos[0] - player_pos[0]) <= 400:
			self.animate(dt)
			self.move(dt)

class Angel(Generic):
	def __init__(self, assets, pos, group, collision_sprites):
		#  general setup
		self.animation_frames = assets
		self.frame_index = 0
		self.orientation = 'right'
		surf = self.animation_frames[f'run_{self.orientation}'][self.frame_index]
		super().__init__(pos, surf, group)
		self.rect.bottom = self.rect.top + TILE_SIZE

		# movement
		self.direction = vector(choice((1, -1)), 0)
		self.orientation = 'left' if self.direction.x < 0 else 'right'
		self.pos = vector(self.rect.topleft)
		self.speed = 120
		self.collision_sprites = collision_sprites

		if not [sprite for sprite in collision_sprites if sprite.rect.collidepoint(self.rect.midbottom + vector(0, 10))]:
			self.kill()
		
	def animate(self, dt):
		current_animation = self.animation_frames[f'run_{self.orientation}']
		self.frame_index += ANIMATION_SPEED * dt
		self.frame_index = 0 if self.frame_index >= len(current_animation) else self.frame_index
		self.image = current_animation[int(self.frame_index)]
	
	def move(self, dt):
		right_gap = self.rect.bottomright + vector(1, 1)
		right_block = self.rect.midright + vector(1, 0)
		left_gap = self.rect.bottomleft + vector(-1, 1)
		left_block = self.rect.midleft + vector(-1, 0)
		if self.direction.x > 0:
			floor_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(right_gap)]
			wall_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(right_block)]
			if wall_sprites or not floor_sprites:
				self.direction.x *= -1
				self.orientation = 'left'
		
		if self.direction.x < 0:
			floor_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(left_gap)]
			wall_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(left_block)]
			if not floor_sprites or wall_sprites:
				self.direction.x *= -1
				self.orientation = 'right'
		
		self.pos.x += self.direction.x * self.speed * dt
		self.rect.x = round(self.pos.x)
	
	def update(self, dt, player_pos):
		self.animate(dt)
		self.move(dt)

class Goat(Generic):
	def __init__(self, assets, pos, group, collision_sprites):
		self.animation_frames = assets
		self.frame_index = 0
		self.orientation = 'right'
		surf = self.animation_frames[f'run_{self.orientation}'][self.frame_index]
		super().__init__(pos, surf, group)
		self.rect.bottom = self.rect.top + TILE_SIZE

		self.direction = vector(choice((1, -1)), 0)
		self.orientation = 'left' if self.direction.x < 0 else 'right'
		self.pos = vector(self.rect.topleft)
		self.speed = 120
		self.collision_sprites = collision_sprites

		if not [sprite for sprite in collision_sprites if sprite.rect.collidepoint(self.rect.midbottom + vector(0, 10))]:
			self.kill()
	
	def animate(self, dt):
		current_animation = self.animation_frames[f'run_{self.orientation}']
		self.frame_index += ANIMATION_SPEED * dt
		self.frame_index = 0 if self.frame_index >= len(current_animation) else self.frame_index
		self.image = current_animation[int(self.frame_index)]
	
	def move(self, dt):
		right_gap = self.rect.bottomright + vector(1, 1)
		right_block = self.rect.midright + vector(1, 0)
		left_gap = self.rect.bottomleft + vector(-1, 1)
		left_block = self.rect.midleft + vector(-1, 0)
		if self.direction.x > 0:
			floor_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(right_gap)]
			wall_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(right_block)]
			if wall_sprites or not floor_sprites:
				self.direction.x *= -1
				self.orientation = 'left'
		
		if self.direction.x < 0:
			floor_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(left_gap)]
			wall_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(left_block)]
			if not floor_sprites or wall_sprites:
				self.direction.x *= -1
				self.orientation = 'right'
		
		self.pos.x += self.direction.x * self.speed * dt
		self.rect.x = round(self.pos.x)
	
	def update(self, dt, player_pos):
		self.animate(dt)
		self.move(dt)

class Harp(Generic):
	def __init__(self, assets, pos, group, arrow_surf, enemies_sprites):
		self.animation_frames = assets
		self.frame_index = 0
		pos = list(pos)
		pos[1] -= 70
		pos = tuple(pos)
		super().__init__(pos, assets[self.frame_index], group)



		# arrow
		self.arrow_surf = arrow_surf
		self.has_shot = False
		self.attack_cooldown = timer.Timer(2000)
		self.enemies_sprites = enemies_sprites
	
	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		if self.frame_index >= len(self.animation_frames):
			self.frame_index = 0
			if self.has_shot:
				self.attack_cooldown.activate()
				self.has_shot = False
		self.image = self.animation_frames[int(self.frame_index)]
		if not self.has_shot:
			arrow_direction = vector(-1, 0)
			Arrow(self.rect.center + vector(0, -30), arrow_direction, self.arrow_surf, [self.groups(), self.enemies_sprites])
			self.has_shot = True
	
	def update(self, dt, player_pos):
		self.animate(dt)
		self.attack_cooldown.update()

class Arrow(Generic):
	def __init__(self, pos, direction, surf, group):
		super().__init__(pos, surf, group)
		self.mask = pygame.mask.from_surface(self.image)
	
		#movement
		self.pos = vector(self.rect.topleft)
		self.direction = direction
		self.speed = 150

		# self destruct
		self.timer = timer.Timer(6000)
		self.timer.activate()

	def update(self, dt, player_pos):
        # movement
		self.pos.x += self.direction.x * self.speed * dt
		self.rect.x = round(self.pos.x)


        # timer
		self.timer.update()
		if not self.timer.active:
			self.kill()

class Bird(Generic):
	def __init__(self, assets, pos, group, collision_sprites):
		self.animation_frames = assets
		self.frame_index = 0
		self.orientation = 'right'
		surf = self.animation_frames[f'fly_{self.orientation}'][self.frame_index]
		super().__init__(pos, surf, group)
		self.rect.bottom = self.rect.top + TILE_SIZE

		# movement
		self.direction = vector(choice((1, -1)), 0)
		self.orientation = 'left' if self.direction.x < 0 else 'right'
		self.pos = vector(self.rect.topleft)
		self.speed = 120
		self.collision_sprites = collision_sprites

	def animate(self, dt):
		current_animation = self.animation_frames[f'fly_{self.orientation}']
		self.frame_index += ANIMATION_SPEED * dt
		self.frame_index = 0 if self.frame_index >= len(current_animation) else self.frame_index
		self.image = current_animation[int(self.frame_index)]
	
	def move(self, dt):
		right_gap = self.rect.bottomright + vector(1, 1)
		right_block = self.rect.midright + vector(1, 0)
		left_gap = self.rect.bottomleft + vector(-1, 1)
		left_block = self.rect.midleft + vector(-1, 0)
		if self.direction.x > 0:
			floor_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(right_gap)]
			wall_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(right_block)]
			if wall_sprites or floor_sprites:
				self.direction.x *= -1
				self.orientation = 'left'
		
		if self.direction.x < 0:
			floor_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(left_gap)]
			wall_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(left_block)]
			if floor_sprites or wall_sprites:
				self.direction.x *= -1
				self.orientation = 'right'
	
		self.pos.x += self.direction.x * self.speed * dt
		self.rect.x = round(self.pos.x)
	
	def update(self, dt, player_pos):
		self.animate(dt)
		self.move(dt)

