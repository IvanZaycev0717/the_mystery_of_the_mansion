import pygame, sys 
from pygame.math import Vector2 as vector
import os

from settings import *
from img_imports import *
import json
from sprites import *

from ui import Inventory, Helper

class Level:
	def __init__(self, grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds=True, has_horizon=True):
		self.display_surface = pygame.display.get_surface()
		self.switch = switch
		self.current_stage = 4
		self.gear_change = gear_change
		self.change_keys = change_keys
		self.hp = hp
		self.dead_time = 0
		self.current_hp = None
		self.gears_amount = 0
		self.player_stats = {}
		self.sky_color = sky_color
		self.ground_color = ground_color
		self.has_clouds = has_clouds
		self.has_horizon = has_horizon
		self.save_active = False
		self.set_prev_stage = set_prev_stage

		# groups 
		self.all_sprites = CameraGroup(self.ground_color, self.has_horizon)
		self.keys_sprites = pygame.sprite.Group()
		self.gear_sprites = pygame.sprite.Group()
		self.enemies_sprites = pygame.sprite.Group()
		self.activator_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()
		self.camel_sprites = pygame.sprite.Group()
		self.harp_sprites = pygame.sprite.Group()
		self.inventory = Inventory(self.display_surface)
		self.helper = Helper(self.display_surface)
		self.player_asset = asset_dict['player']
		self.jump_sound = audio['jump']
		self.walk_sound = audio['walk']
		self.lives_left = 3
		self.tab_pressed = False
		self.quicksave_time = timer.Timer(1500)

		self.build_level(grid, asset_dict, self.jump_sound, self.walk_sound)

		self.level_limits = {
            'left' : -WINDOW_WIDTH,
            'right': sorted(list(grid['common'].keys()), key= lambda pos: pos[0])[-1][0] + 500
        }

		self.taken_surf = asset_dict['taken']
		if self.has_clouds:
			self.cloud_surfs = asset_dict['clouds']
			self.cloud_timer = pygame.USEREVENT + 2
			pygame.time.set_timer(self.cloud_timer, 2000)
			self.startup_clouds()

		self.gear_sound = audio['gear']
		self.gear_sound.set_volume(0.3)

		self.hit_sound = audio['hit']
		self.hit_sound.set_volume(0.1)

		self.key_sound = audio['key']
		self.key_sound.set_volume(0.3)

	def show_save_message(self, dt):
		if self.save_active:
			self.save_active = False
			if self.quicksave_time.start_time:
				self.helper.show_helper('game_saved')
				self.save_active = True
			self.quicksave_time.update()

	def correct_falling(self):
		if self.player.pos[1] > 1000 and self.player.orientation == 'right':
			self.player.pos[0] -= 200
			self.player.pos[1] = 250
		elif self.player.pos[1] > 1000 and self.player.orientation == 'left':
			self.player.pos[0] += 200
			self.player.pos[1] = 250


	def build_level(self, grid, asset_dict, jump_sound, walk_sound):
		for layer_name, layer in grid.items():
			for pos, data in layer.items():
				if layer_name == 'common':
					Generic(pos, asset_dict['land'][data[0]][data[1]], [self.all_sprites, self.collision_sprites])
				match data:
					case 0: self.player = Player(pos, asset_dict['player'], self.all_sprites, self.collision_sprites, jump_sound, walk_sound)
					case 1:
						self.horizon_y = pos[1]
						self.all_sprites.horizon_y = pos[1]
					case 9: Angel(
						assets=asset_dict['angel'],
						pos=pos,
						group=[self.all_sprites, self.enemies_sprites],
						collision_sprites=self.collision_sprites)
					case 10: FlyingEnemy(
						assets=asset_dict['bat'],
						pos=pos,
						group=[self.all_sprites, self.enemies_sprites],
						collision_sprites=self.collision_sprites)
					case 11: Bird(
						assets=asset_dict['bird'],
						pos=pos,
						group=[self.all_sprites, self.enemies_sprites],
						collision_sprites=self.collision_sprites)
					case 12: WalkingEnemies(
						assets=asset_dict['bug'],
						pos=pos,
						group=[self.all_sprites, self.enemies_sprites],
						collision_sprites=self.collision_sprites)
					case 13: Camel(
						pos=pos,
						surf=asset_dict['camel'],
						splutter_surf=asset_dict['splutter'],
						group=[self.all_sprites, self.camel_sprites],
						enemy_sprites= self.enemies_sprites)
					case 14: Spikes(asset_dict['cem_spikes'], pos, [self.all_sprites, self.enemies_sprites])
					case 15: FlyingEnemy(
						assets=asset_dict['disputes'],
						pos=pos,
						group=[self.all_sprites, self.enemies_sprites],
						collision_sprites=self.collision_sprites)
					case 16: Fire(asset_dict['fire'], pos, [self.all_sprites, self.enemies_sprites])
					case 17: Spikes(asset_dict['gar_spikes'], pos, [self.all_sprites, self.enemies_sprites])
					case 18: Goat(
						assets=asset_dict['goat'],
						pos=pos,
						group=[self.all_sprites, self.enemies_sprites],
						collision_sprites=self.collision_sprites)
					case 19: Harp(
						assets=asset_dict['harp'],
						pos=pos,
						group=[self.all_sprites, self.harp_sprites],
						arrow_surf=asset_dict['arrow'],
						enemies_sprites=self.enemies_sprites)
					case 20: Spikes(asset_dict['heav_spikes'], pos, [self.all_sprites, self.enemies_sprites])
					case 21: WalkingEnemies(
						assets=asset_dict['hedgehog'],
						pos=pos,
						group=[self.all_sprites, self.enemies_sprites],
						collision_sprites=self.collision_sprites)
					case 22: FlyingEnemy(
						assets=asset_dict['scrolls'],
						pos=pos,
						group=[self.all_sprites, self.enemies_sprites],
						collision_sprites=self.collision_sprites)
					case 23: Slime(asset_dict['slime'], pos, [self.all_sprites, self.enemies_sprites])
					case 24: Wasp(
						pos=pos,
						surf=asset_dict['wasp'],
						group=[self.all_sprites, self.enemies_sprites],
						collision_sprites=self.collision_sprites)
					case 25: Key('green', asset_dict['green_key'], pos, [self.all_sprites, self.keys_sprites])
					case 26: Key('hammer', asset_dict['hammer'], pos, [self.all_sprites, self.keys_sprites])
					case 27: Key('pink', asset_dict['pink_key'], pos, [self.all_sprites, self.keys_sprites])
					case 28: Key('yellow', asset_dict['yellow_key'], pos, [self.all_sprites, self.keys_sprites])
					case 29: Gear(asset_dict['gear'], pos, [self.all_sprites, self.gear_sprites])
					case 30: Generic(pos, asset_dict['first_floor_stuff']['shelf'][0], self.all_sprites)
					case 31: Generic(pos, asset_dict['cupboard_stuff']['cauldron'][0], self.all_sprites)
					case 32: Generic(pos, asset_dict['cementry_stuff']['bush1'][0], self.all_sprites)
					case 33: Generic(pos, asset_dict['cementry_stuff']['bush2'][0], self.all_sprites)
					case 34: Generic(pos, asset_dict['cementry_stuff']['gravefence'][0], self.all_sprites)
					case 35: Animated(asset_dict['cementry_stuff']['gravetree1'], pos, self.all_sprites)
					case 36: Generic(pos, asset_dict['cementry_stuff']['gravetree2'][0], self.all_sprites)
					case 37: Generic(pos, asset_dict['first_floor_stuff']['chair'][0], self.all_sprites)
					case 38: Generic(pos, asset_dict['first_floor_stuff']['chest'][0], self.all_sprites)
					case 39: Generic(pos, asset_dict['common_stuff']['hedge'][0], self.all_sprites)
					case 40: Generic(pos, asset_dict['common_stuff']['plant1'][0], self.all_sprites)
					case 41: Generic(pos, asset_dict['common_stuff']['plant2'][0], self.all_sprites)
					case 42: Generic(pos, asset_dict['common_stuff']['plant3'][0], self.all_sprites)
					case 43: Generic(pos, asset_dict['common_stuff']['lightpost'][0], self.all_sprites)
					case 44: Generic(pos, asset_dict['common_stuff']['woodfence'][0], self.all_sprites)
					case 45: Generic(pos, asset_dict['first_floor_stuff']['couch'][0], self.all_sprites)
					case 46: Generic(pos, asset_dict['cupboard_stuff']['devil'][0], self.all_sprites)
					case 47: Generic(pos, asset_dict['floor_stuff']['door'][0], self.all_sprites)
					case 48: Generic(pos, asset_dict['desert_stuff']['dune1'][0], self.all_sprites)
					case 49: Generic(pos, asset_dict['desert_stuff']['dune2'][0], self.all_sprites)
					case 50: Generic(pos, asset_dict['desert_stuff']['dune3'][0], self.all_sprites)
					case 51: Generic(pos, asset_dict['garden_stuff']['wood_fence'][0], self.all_sprites)
					case 52: Generic(pos, asset_dict['garden_stuff']['tree1'][0], self.all_sprites)
					case 53: Animated(asset_dict['garden_stuff']['tree2'], pos, self.all_sprites)
					case 54: Generic(pos, asset_dict['cementry_stuff']['gravestone1'][0], self.all_sprites)
					case 55: Generic(pos, asset_dict['cementry_stuff']['gravestone2'][0], self.all_sprites)
					case 56: Generic(pos, asset_dict['cementry_stuff']['gravestone3'][0], self.all_sprites)
					case 57: Generic(pos, asset_dict['cementry_stuff']['gravestone4'][0], self.all_sprites)
					case 58: Generic(pos, asset_dict['heaven_stuff']['fortress'][0], self.all_sprites)
					case 59: Generic(pos, asset_dict['heaven_stuff']['gate1'][0], self.all_sprites)
					case 60: Generic(pos, asset_dict['heaven_stuff']['gate2'][0], self.all_sprites)
					case 61: Generic(pos, asset_dict['heaven_stuff']['stair1'][0], self.all_sprites)
					case 62: Generic(pos, asset_dict['heaven_stuff']['stair2'][0], self.all_sprites)
					case 63: Generic(pos, asset_dict['heaven_stuff']['stair3'][0], self.all_sprites)
					case 64: Generic(pos, asset_dict['floor_stuff']['lamp'][0], self.all_sprites)
					case 65: Generic(pos, asset_dict['common_stuff']['mansion'][0], self.all_sprites)
					case 66: Generic(pos, asset_dict['cementry_stuff']['monument'][0], self.all_sprites)
					case 67: Generic(pos, asset_dict['poison_stuff']['mush1'][0], self.all_sprites)
					case 68: Generic(pos, asset_dict['poison_stuff']['mush2'][0], self.all_sprites)
					case 69: Animated(asset_dict['desert_stuff']['palm'], pos, self.all_sprites)
					case 70: Generic(pos, asset_dict['floor_stuff']['picture1'][0], self.all_sprites)
					case 71: Generic(pos, asset_dict['floor_stuff']['picture2'][0], self.all_sprites)
					case 72: Generic(pos, asset_dict['floor_stuff']['picture3'][0], self.all_sprites)
					case 73: Generic(pos, asset_dict['floor_stuff']['picture4'][0], self.all_sprites)
					case 74: Generic(pos, asset_dict['floor_stuff']['picture5'][0], self.all_sprites)
					case 75: Generic(pos, asset_dict['first_floor_stuff']['picture1'][0], self.all_sprites)
					case 76: Generic(pos, asset_dict['first_floor_stuff']['picture2'][0], self.all_sprites)
					case 77: Generic(pos, asset_dict['first_floor_stuff']['picture3'][0], self.all_sprites)
					case 78: Generic(pos, asset_dict['garden_stuff']['plant1'][0], self.all_sprites)
					case 79: Generic(pos, asset_dict['garden_stuff']['plant2'][0], self.all_sprites)
					case 80: Generic(pos, asset_dict['common_stuff']['rockfence1'][0], self.all_sprites)
					case 81: Generic(pos, asset_dict['common_stuff']['rockfence2'][0], self.all_sprites)
					case 82: Generic(pos, asset_dict['floor_stuff']['window'][0], self.all_sprites)
					case 83: Generic(pos, asset_dict['cupboard_stuff']['shelf'][0], self.all_sprites)
					case 84: Generic(pos, asset_dict['floor_stuff']['stair'][0], self.all_sprites)
					case 85: Generic(pos, asset_dict['first_floor_stuff']['stand'][0], self.all_sprites)
					case 86: Generic(pos, asset_dict['common_stuff']['statue'][0], self.all_sprites)
					case 87: Generic(pos, asset_dict['first_floor_stuff']['table'][0], self.all_sprites)
					case 88: Generic(pos, asset_dict['first_floor_stuff']['wall'][0], self.all_sprites)
					case 89: Generic(pos, asset_dict['floor_stuff']['wardrobe'][0], self.all_sprites)
					case 90: Generic(pos, asset_dict['first_floor_stuff']['window'][0], self.all_sprites)
					case 91: Activator(pos, asset_dict['activators']['wall'][0], [self.all_sprites, self.activator_sprites], 'act_wall')
					case 92: Activator(pos, asset_dict['activators']['blue_door_in'][0], [self.all_sprites, self.activator_sprites], 'blue_door_in')
					case 93: Activator(pos, asset_dict['activators']['blue_door_out'][0], [self.all_sprites, self.activator_sprites], 'blue_door_out')
					case 94: Activator(pos, asset_dict['activators']['cementry_gates'][0], [self.all_sprites, self.activator_sprites], 'cem_gates')
					case 95: Activator(pos, asset_dict['activators']['cupboard_bed'][0], [self.all_sprites, self.activator_sprites], 'cup_bed')
					case 96: Activator(pos, asset_dict['activators']['cupboard_door_in'][0], [self.all_sprites, self.activator_sprites], 'cup_door_in')
					case 97: Activator(pos, asset_dict['activators']['cupboard_door_out'][0], [self.all_sprites, self.activator_sprites], 'cup_door_out')
					case 98: Activator(pos, asset_dict['activators']['ff_bed_in'][0], [self.all_sprites, self.activator_sprites], 'ff_bed_in')
					case 99: Activator(pos, asset_dict['activators']['green_door_in'][0], [self.all_sprites, self.activator_sprites], 'green_door_in')
					case 100: Activator(pos, asset_dict['activators']['green_door_out'][0], [self.all_sprites, self.activator_sprites], 'green_door_out')
					case 101: Activator(pos, asset_dict['activators']['machine'][0], [self.all_sprites, self.activator_sprites], 'machine')
					case 102: Activator(pos, asset_dict['activators']['pink_door_in'][0], [self.all_sprites, self.activator_sprites], 'pink_door_in')
					case 103: Activator(pos, asset_dict['activators']['pink_door_out'][0], [self.all_sprites, self.activator_sprites], 'pink_door_out')
					case 104: Activator(pos, asset_dict['activators']['sf_bed'][0], [self.all_sprites, self.activator_sprites], 'sf_bed')

	def save_the_game(self):
		save_dct = {
			'stage': self.current_stage,
			'pos_x': self.player.pos[0],
			'pos_y': self.player.pos[1],
			}
		save_to_json = json.dumps(save_dct)
		with open('quicksave.json', 'w') as file:
			json.dump(save_to_json, file)
		
	def load_the_game(self):
		if os.path.exists('quicksave.json'):
			with open('quicksave.json') as file:
				save_dct = json.load(file)
			save_dct = json.loads(save_dct)
			self.current_stage =save_dct['stage']
			self.player.pos.x = save_dct['pos_x']
			self.player.pos.y = save_dct['pos_y']

	def check_death(self, pos, dt):
		if self.player.status == 'death':
			self.dead_time += dt
			if self.dead_time >= 5:
				self.player.kill()
				pos = (pos[0] - 100, pos[1] - 100)
				self.player = Player(pos, self.player_asset, self.all_sprites, self.collision_sprites, self.jump_sound, self.walk_sound)
				self.dead_time = 0

	def get_keys(self):
		collided_keys = pygame.sprite.spritecollide(self.player, self.keys_sprites, True)
		for sprite in collided_keys:
			self.walk_sound.stop()
			self.jump_sound.stop()
			self.key_sound.play()
			self.change_keys(f'{sprite.__dict__["key_type"]}_key')
			sprite.kill()

	def get_damage(self):
		collision_sprites = pygame.sprite.spritecollide(self.player, self.enemies_sprites, False, pygame.sprite.collide_mask)
		if collision_sprites and self.player.status != 'death':
			self.walk_sound.stop()
			self.jump_sound.stop()
			self.hit_sound.play()
			self.player.damage()
			self.hp(0.2)
	

	def get_gears(self):
		collided_gears = pygame.sprite.spritecollide(self.player, self.gear_sprites, True)
		for sprite in collided_gears:
			self.gear_sound.play()
			Taken(self.taken_surf, sprite.rect.center, self.all_sprites)
			self.gear_change(1)

	

	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.switch()
			if self.has_clouds and event.type == self.cloud_timer:
				surf = choice(self.cloud_surfs)
				surf = pygame.transform.scale2x(surf) if randint(0, 5) > 3 else surf
				x = self.level_limits['right'] + randint(100, 300)
				y = self.horizon_y - randint(-50, 600)
				Cloud((x, y), surf, self.all_sprites, self.level_limits['left'])
			if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
				self.tab_pressed = True
			if event.type == pygame.KEYUP and event.key == pygame.K_TAB:
				self.tab_pressed = False
	
	def startup_clouds(self):
		for cloud in range(40):
			surf = choice(self.cloud_surfs)
			surf = pygame.transform.scale2x(surf) if randint(0, 5) > 3 else surf
			x = randint(self.level_limits['left'], self.level_limits['right'])
			y = self.horizon_y - randint(-50, 600)
			Cloud((x, y), surf, self.all_sprites, self.level_limits['left'])

	def run(self, dt, gears_amount, player_stats, current_stage):
		self.current_stage = current_stage
		self.gears_amount = gears_amount
		self.player_stats = player_stats
		self.correct_falling()
		self.event_loop()
		self.all_sprites.update(dt, self.player.pos)
		self.get_keys()
		self.get_gears()
		self.get_damage()
		self.check_death(self.player.pos, dt)
		self.display_surface.fill(self.sky_color)
		self.all_sprites.custom_draw(self.player)
		if self.tab_pressed:
			self.inventory.show_inventory(self.gears_amount, self.player_stats)

class CameraGroup(pygame.sprite.Group):
    def __init__(self, custom_sea, has_horizon):
        super().__init__()
        self.dispay_surface = pygame.display.get_surface()
        self.offset = vector()
        self.custom_sea = custom_sea
        self.has_horizon = has_horizon

    def draw_horizon(self):
        horizon_pos = self.horizon_y - self.offset.y
        if horizon_pos < WINDOW_HEIGHT:
            sea_rect = pygame.Rect(0, horizon_pos, WINDOW_WIDTH, WINDOW_HEIGHT - horizon_pos)
            pygame.draw.rect(self.dispay_surface, self.custom_sea, sea_rect)

            # horizon line
            horizon_rect1 = pygame.Rect(0,horizon_pos - 10,WINDOW_WIDTH,10)
            horizon_rect2 = pygame.Rect(0,horizon_pos - 16,WINDOW_WIDTH,4)
            horizon_rect3 = pygame.Rect(0,horizon_pos - 20,WINDOW_WIDTH,2)
            pygame.draw.rect(self.dispay_surface, HORIZON_TOP_COLOR, horizon_rect1)
            pygame.draw.rect(self.dispay_surface, HORIZON_TOP_COLOR, horizon_rect2)
            pygame.draw.rect(self.dispay_surface, HORIZON_TOP_COLOR, horizon_rect3)
            pygame.draw.line(self.dispay_surface, HORIZON_COLOR, (0,horizon_pos), (WINDOW_WIDTH, horizon_pos), 3)

        if horizon_pos < 0:
            self.dispay_surface.fill((100, 100, 100))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 1.4
        for sprite in self:
            if sprite.z == LEVEL_LAYERS['clouds']:
                offset_rect = sprite.rect.copy()
                offset_rect.center -= self.offset
                self.dispay_surface.blit(sprite.image, offset_rect)
        
        if self.has_horizon:
            self.draw_horizon()
        for sprite in self:
            for layer in LEVEL_LAYERS.values():
                if sprite.z == layer and sprite.z != LEVEL_LAYERS['clouds']:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.dispay_surface.blit(sprite.image, offset_rect)

class Common(Level):
	def __init__(self, grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds=True, has_horizon=True):
		super().__init__(grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds=True, has_horizon=True)
		self.door_in = False
		self.gate_active = False
		self.current_stage = 4
		self.prev_stage = 3
		self.main_menu = False

		self.bg_music = audio['common_theme']
		self.bg_music.set_volume(0.2)
		self.is_music_playing = False

	def play_sound(self):
		if not self.is_music_playing:
			self.bg_music.play(loops=-1)
			self.is_music_playing = True

	def get_activator(self, dt=0):
		collision_sprites = pygame.sprite.spritecollide(self.player, self.activator_sprites, False)
		self.gate_active = False
		self.door_in = False
		if collision_sprites:
			for sprite in collision_sprites:
				if sprite.__dict__['id'] == 'blue_door_in' and not self.player_stats['yellow_key']:
					self.helper.show_helper('yellow_not')
				if sprite.__dict__['id'] == 'blue_door_in' and self.player_stats['yellow_key']:
					self.helper.show_helper('has_item')
					self.door_in = True
				if sprite.__dict__['id'] == 'cem_gates':
					self.helper.show_helper('has_item')
					self.gate_active = True
	
	def event_loop(self, dt):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.bg_music.stop()
				self.set_prev_stage(self.current_stage, self.prev_stage)
				self.current_stage = self.prev_stage
				self.is_music_playing = False
			if self.has_clouds and event.type == self.cloud_timer:
				surf = choice(self.cloud_surfs)
				surf = pygame.transform.scale2x(surf) if randint(0, 5) > 3 else surf
				x = self.level_limits['right'] + randint(100, 300)
				y = self.horizon_y - randint(-50, 600)
				Cloud((x, y), surf, self.all_sprites, self.level_limits['left'])
			if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
				self.tab_pressed = True
			if event.type == pygame.KEYUP and event.key == pygame.K_TAB:
				self.tab_pressed = False
			if event.type == pygame.KEYDOWN and event.key in (pygame.K_x, pygame.K_UP) and self.gate_active:
				self.bg_music.stop()
				self.current_stage = 5
				self.gate_active = False
				self.is_music_playing = False
			if event.type == pygame.KEYDOWN and event.key in (pygame.K_x, pygame.K_UP) and self.door_in:
				self.bg_music.stop()
				self.current_stage = 6
				self.door_in = False
				self.is_music_playing = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
				self.save_active = True
				self.quicksave_time.activate()
				self.save_the_game()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F9:
				self.load_the_game()
			

	def run(self, dt, gears_amount, player_stats, current_stage, prev_stage):
		self.current_stage = current_stage
		self.gears_amount = gears_amount
		self.player_stats = player_stats
		self.prev_stage = prev_stage
		self.play_sound()
		self.correct_falling()
		self.event_loop(dt)
		
		self.all_sprites.update(dt, self.player.pos)
		self.get_keys()
		self.get_gears()
		self.get_damage()
	
		self.check_death(self.player.pos, dt)
		self.display_surface.fill(self.sky_color)
		self.all_sprites.custom_draw(self.player)
		if self.tab_pressed:
			self.inventory.show_inventory(self.gears_amount, self.player_stats)
		self.get_activator()
		self.show_save_message(dt)
		return self.current_stage


class Cementry(Level):
	def __init__(self, grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds=True, has_horizon=True):
		super().__init__(grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds=True, has_horizon=True)
		self.current_stage = 5
		self.gate_active = False
		self.prev_stage = 3

		self.bg_music = audio['cementry_theme']
		self.bg_music.set_volume(0.2)
		self.is_music_playing = False
	
	def play_sound(self):
		if not self.is_music_playing:
			self.bg_music.play(loops=-1)
			self.is_music_playing = True

	def get_activator(self):
		collision_sprites = pygame.sprite.spritecollide(self.player, self.activator_sprites, False)
		self.gate_active = False
		if collision_sprites:
			for sprite in collision_sprites:
				if sprite.__dict__['id'] == 'cem_gates':
					self.helper.show_helper('has_item')
					self.gate_active = True
	
	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if self.has_clouds and event.type == self.cloud_timer:
				surf = choice(self.cloud_surfs)
				surf = pygame.transform.scale2x(surf) if randint(0, 5) > 3 else surf
				x = self.level_limits['right'] + randint(100, 300)
				y = self.horizon_y - randint(-50, 600)
				Cloud((x, y), surf, self.all_sprites, self.level_limits['left'])
			if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
				self.tab_pressed = True
			if event.type == pygame.KEYUP and event.key == pygame.K_TAB:
				self.tab_pressed = False
			if event.type == pygame.KEYDOWN and event.key in (pygame.K_x, pygame.K_UP) and self.gate_active:
				self.bg_music.stop()
				self.current_stage = 4
				self.gate_active = False
				self.is_music_playing = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
				self.save_active = True
				self.quicksave_time.activate()
				self.save_the_game()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F9:
				self.load_the_game()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.bg_music.stop()
				self.set_prev_stage(self.current_stage, self.prev_stage)
				self.current_stage = self.prev_stage
				self.is_music_playing = False
	
	def run(self, dt, gears_amount, player_stats, current_stage):
		self.current_stage = current_stage
		self.gears_amount = gears_amount
		self.player_stats = player_stats
		self.correct_falling()
		self.play_sound()
		self.event_loop()
		self.all_sprites.update(dt, self.player.pos)
		self.get_keys()
		self.get_gears()
		self.get_damage()
		
		self.check_death(self.player.pos, dt)
		self.display_surface.fill(self.sky_color)
		self.all_sprites.custom_draw(self.player)
		if self.tab_pressed:
			self.inventory.show_inventory(self.gears_amount, self.player_stats)
		self.get_activator()
		self.show_save_message(dt)
		return self.current_stage


class Hall(Level):
	def __init__(self, grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds=True, has_horizon=True):
		super().__init__(grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds, has_horizon)
		self.current_stage = 6
		self.prev_stage = 3
		self.door_out = False
		self.pink_door = False
		self.green_door = False
		self.cupboard_door = False

		self.bg_music = audio['inside_theme']
		self.bg_music.set_volume(0.2)
		self.is_music_playing = False


	def play_sound(self):
		if not self.is_music_playing:
			self.bg_music.play(loops=-1)
			self.is_music_playing = True

	def get_activator(self):
		collision_sprites = pygame.sprite.spritecollide(self.player, self.activator_sprites, False)
		self.door_out = False
		self.pink_door = False
		self.green_door = False
		self.cupboard_door = False
		if collision_sprites:
			for sprite in collision_sprites:
				if sprite.__dict__['id'] == 'blue_door_out' and self.player_stats['yellow_key']:
					self.helper.show_helper('has_item')
					self.door_out = True
				if sprite.__dict__['id'] == 'cup_door_in':
					self.helper.show_helper('has_item')
					self.cupboard_door = True
				if sprite.__dict__['id'] == 'green_door_out' and self.player_stats['green_key']:
					self.helper.show_helper('has_item')
					self.green_door = True
				elif sprite.__dict__['id'] == 'green_door_out' and not self.player_stats['green_key']:
					self.helper.show_helper('green_not')
				if sprite.__dict__['id'] == 'pink_door_out' and self.player_stats['pink_key']:
					self.helper.show_helper('has_item')
					self.pink_door = True
				elif sprite.__dict__['id'] == 'pink_door_out' and not self.player_stats['pink_key']:
					self.helper.show_helper('pink_not')
	
	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if self.has_clouds and event.type == self.cloud_timer:
				surf = choice(self.cloud_surfs)
				surf = pygame.transform.scale2x(surf) if randint(0, 5) > 3 else surf
				x = self.level_limits['right'] + randint(100, 300)
				y = self.horizon_y - randint(-50, 600)
				Cloud((x, y), surf, self.all_sprites, self.level_limits['left'])
			if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
				self.tab_pressed = True
			if event.type == pygame.KEYUP and event.key == pygame.K_TAB:
				self.tab_pressed = False
			if event.type == pygame.KEYDOWN and event.key in (pygame.K_x, pygame.K_UP) and self.door_out:
				self.bg_music.stop()
				self.current_stage = 4
				self.door_out = False
				self.is_music_playing = False
				self.is_music_playing = False
			if event.type == pygame.KEYDOWN and event.key in (pygame.K_x, pygame.K_UP) and self.cupboard_door:
				self.bg_music.stop()
				self.current_stage = 7
				self.cupboard_door = False
				self.is_music_playing = False
			if event.type == pygame.KEYDOWN and event.key in (pygame.K_x, pygame.K_UP) and self.green_door:
				self.bg_music.stop()
				self.current_stage = 9
				self.green_door = False
				self.is_music_playing = False
			if event.type == pygame.KEYDOWN and event.key in (pygame.K_x, pygame.K_UP) and self.pink_door:
				self.bg_music.stop()
				self.current_stage = 11
				self.pink_door = False
				self.is_music_playing = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
				self.save_active = True
				self.quicksave_time.activate()
				self.save_the_game()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F9:
				self.load_the_game()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.bg_music.stop()
				self.set_prev_stage(self.current_stage, self.prev_stage)
				self.current_stage = self.prev_stage
				self.is_music_playing = False
	
	def run(self, dt, gears_amount, player_stats, current_stage):
		self.current_stage = current_stage
		self.gears_amount = gears_amount
		self.player_stats = player_stats
		self.play_sound()
		self.correct_falling()
		self.event_loop()
		self.all_sprites.update(dt, self.player.pos)
		self.get_keys()
		self.get_gears()
		self.get_damage()
		self.check_death(self.player.pos, dt)
		self.display_surface.fill(self.sky_color)
		self.all_sprites.custom_draw(self.player)
		if self.tab_pressed:
			self.inventory.show_inventory(self.gears_amount, self.player_stats)
		self.get_activator()
		self.show_save_message(dt)
		return self.current_stage

class Cupboard(Level):
	def __init__(self, grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds=True, has_horizon=True):
		super().__init__(grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds, has_horizon)
		self.current_stage = 6
		self.prev_stage = 3
		self.cupboard_door = False
		self.cupboard_bed = False

		self.bg_music = audio['inside_theme']
		self.bg_music.set_volume(0.2)
		self.is_music_playing = False

	def play_sound(self):
		if not self.is_music_playing:
			self.bg_music.play(loops=-1)
			self.is_music_playing = True

	def get_activator(self):
		collision_sprites = pygame.sprite.spritecollide(self.player, self.activator_sprites, False)
		self.cupboard_door = False
		self.cupboard_bed = False
		if collision_sprites:
			for sprite in collision_sprites:
				if sprite.__dict__['id'] == 'cup_door_out':
					self.helper.show_helper('has_item')
					self.cupboard_door = True
				if sprite.__dict__['id'] == 'cup_bed' and not self.player_stats['green_key']:
					self.helper.show_helper('sleep_well')
					self.cupboard_bed = True
	
	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if self.has_clouds and event.type == self.cloud_timer:
				surf = choice(self.cloud_surfs)
				surf = pygame.transform.scale2x(surf) if randint(0, 5) > 3 else surf
				x = self.level_limits['right'] + randint(100, 300)
				y = self.horizon_y - randint(-50, 600)
				Cloud((x, y), surf, self.all_sprites, self.level_limits['left'])
			if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
				self.tab_pressed = True
			if event.type == pygame.KEYUP and event.key == pygame.K_TAB:
				self.tab_pressed = False
			if event.type == pygame.KEYDOWN and event.key in (pygame.K_x, pygame.K_UP) and self.cupboard_door:
				self.bg_music.stop()
				self.current_stage = 6
				self.cupboard_door = False
				self.is_music_playing = False
			if event.type == pygame.KEYDOWN and event.key in (pygame.K_x, pygame.K_UP) and self.cupboard_bed:
				self.bg_music.stop()
				self.current_stage = 8
				self.cupboard_bed = False
				self.is_music_playing = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
				self.save_active = True
				self.quicksave_time.activate()
				self.save_the_game()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F9:
				self.load_the_game()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.bg_music.stop()
				self.set_prev_stage(self.current_stage, self.prev_stage)
				self.current_stage = self.prev_stage
				self.is_music_playing = False
	
	def run(self, dt, gears_amount, player_stats, current_stage):
		self.current_stage = current_stage
		self.gears_amount = gears_amount
		self.player_stats = player_stats
		self.play_sound()
		self.correct_falling()
		self.event_loop()
		self.all_sprites.update(dt, self.player.pos)
		self.get_keys()
		self.get_gears()
		self.get_damage()
		
		self.check_death(self.player.pos, dt)
		self.display_surface.fill(self.sky_color)
		self.all_sprites.custom_draw(self.player)
		if self.tab_pressed:
			self.inventory.show_inventory(self.gears_amount, self.player_stats)
		self.get_activator()
		self.show_save_message(dt)
		return self.current_stage

class Heaven(Level):
	def __init__(self, grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds=True, has_horizon=True):
		super().__init__(grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds, has_horizon)
		self.current_stage = 8
		self.prev_stage = 3

		self.bg_music = audio['heaven_theme']
		self.bg_music.set_volume(0.2)
		self.is_music_playing = False
	
	def check_green_key(self):
		if self.player_stats['green_key']:
			self.bg_music.stop()
			self.current_stage = 7
			self.is_music_playing = False
	def play_sound(self):
		if not self.is_music_playing:
			self.bg_music.play(loops=-1)
			self.is_music_playing = True

	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if self.has_clouds and event.type == self.cloud_timer:
				surf = choice(self.cloud_surfs)
				surf = pygame.transform.scale2x(surf) if randint(0, 5) > 3 else surf
				x = self.level_limits['right'] + randint(100, 300)
				y = self.horizon_y - randint(-50, 600)
				Cloud((x, y), surf, self.all_sprites, self.level_limits['left'])
			if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
				self.tab_pressed = True
			if event.type == pygame.KEYUP and event.key == pygame.K_TAB:
				self.tab_pressed = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
				self.save_active = True
				self.quicksave_time.activate()
				self.save_the_game()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F9:
				self.load_the_game()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.bg_music.stop()
				self.set_prev_stage(self.current_stage, self.prev_stage)
				self.current_stage = self.prev_stage
				self.is_music_playing = False
	
	def run(self, dt, gears_amount, player_stats, current_stage):
		self.current_stage = current_stage
		self.gears_amount = gears_amount
		self.player_stats = player_stats
		self.play_sound()
		self.correct_falling()
		self.event_loop()
		self.check_green_key()
		self.all_sprites.update(dt, self.player.pos)
		self.get_keys()
		self.get_gears()
		self.get_damage()
		self.check_death(self.player.pos, dt)
		self.display_surface.fill(self.sky_color)
		self.all_sprites.custom_draw(self.player)
		if self.tab_pressed:
			self.inventory.show_inventory(self.gears_amount, self.player_stats)
		self.show_save_message(dt)
		return self.current_stage

class FirstFloor(Level):
	def __init__(self, grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds=True, has_horizon=True):
		super().__init__(grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds, has_horizon)
		self.current_stage = 9
		self.prev_stage = 3
		self.green_door = False
		self.green_bed = False

		self.bg_music = audio['inside_theme']
		self.bg_music.set_volume(0.2)
		self.is_music_playing = False
	
	def play_sound(self):
		if not self.is_music_playing:
			self.bg_music.play(loops=-1)
			self.is_music_playing = True
	
	def get_activator(self):
		collision_sprites = pygame.sprite.spritecollide(self.player, self.activator_sprites, False)
		self.green_door = False
		self.green_bed = False
		if collision_sprites:
			for sprite in collision_sprites:
				if sprite.__dict__['id'] in ('green_door_in', 'green_door_out'):
					self.helper.show_helper('has_item')
					self.green_door = True
				if sprite.__dict__['id'] == 'ff_bed_in' and not self.player_stats['pink_key']:
					self.helper.show_helper('sleep_well')
					self.green_bed = True
	
	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if self.has_clouds and event.type == self.cloud_timer:
				surf = choice(self.cloud_surfs)
				surf = pygame.transform.scale2x(surf) if randint(0, 5) > 3 else surf
				x = self.level_limits['right'] + randint(100, 300)
				y = self.horizon_y - randint(-50, 600)
				Cloud((x, y), surf, self.all_sprites, self.level_limits['left'])
			if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
				self.tab_pressed = True
			if event.type == pygame.KEYUP and event.key == pygame.K_TAB:
				self.tab_pressed = False
			if event.type == pygame.KEYDOWN and event.key in (pygame.K_x, pygame.K_UP) and self.green_door:
				self.bg_music.stop()
				self.current_stage = 6
				self.green_door = False
				self.is_music_playing = False
			if event.type == pygame.KEYDOWN and event.key in (pygame.K_x, pygame.K_UP) and self.green_bed:
				self.bg_music.stop()
				self.current_stage = 10
				self.green_bed = False
				self.is_music_playing = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
				self.save_active = True
				self.quicksave_time.activate()
				self.save_the_game()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F9:
				self.load_the_game()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.bg_music.stop()
				self.set_prev_stage(self.current_stage, self.prev_stage)
				self.current_stage = self.prev_stage
				self.is_music_playing = False
	
	def run(self, dt, gears_amount, player_stats, current_stage):
		self.current_stage = current_stage
		self.gears_amount = gears_amount
		self.player_stats = player_stats
		self.play_sound()
		self.correct_falling()
		self.event_loop()
		self.all_sprites.update(dt, self.player.pos)
		self.get_keys()
		self.get_gears()
		self.get_damage()
		self.get_activator()
		self.check_death(self.player.pos, dt)
		self.display_surface.fill(self.sky_color)
		self.all_sprites.custom_draw(self.player)
		if self.tab_pressed:
			self.inventory.show_inventory(self.gears_amount, self.player_stats)
		self.get_activator()
		self.show_save_message(dt)
		return self.current_stage

class Desert(Level):
	def __init__(self, grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds=True, has_horizon=True):
		super().__init__(grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds, has_horizon)
		self.current_stage = 10
		self.prev_stage = 3

		self.bg_music = audio['desert_theme']
		self.bg_music.set_volume(0.2)
		self.is_music_playing = False

	def play_sound(self):
		if not self.is_music_playing:
			self.bg_music.play(loops=-1)
			self.is_music_playing = True
	
	def check_green_key(self):
		if self.player_stats['pink_key']:
			self.bg_music.stop()
			self.current_stage = 9
			self.is_music_playing = False

	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if self.has_clouds and event.type == self.cloud_timer:
				surf = choice(self.cloud_surfs)
				surf = pygame.transform.scale2x(surf) if randint(0, 5) > 3 else surf
				x = self.level_limits['right'] + randint(100, 300)
				y = self.horizon_y - randint(-50, 600)
				Cloud((x, y), surf, self.all_sprites, self.level_limits['left'])
			if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
				self.tab_pressed = True
			if event.type == pygame.KEYUP and event.key == pygame.K_TAB:
				self.tab_pressed = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
				self.save_active = True
				self.quicksave_time.activate()
				self.save_the_game()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F9:
				self.load_the_game()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.bg_music.stop()
				self.set_prev_stage(self.current_stage, self.prev_stage)
				self.current_stage = self.prev_stage
				self.is_music_playing = False
	
	def run(self, dt, gears_amount, player_stats, current_stage):
		self.current_stage = current_stage
		self.gears_amount = gears_amount
		self.player_stats = player_stats
		self.play_sound()
		self.correct_falling()
		self.event_loop()
		self.check_green_key()
		self.all_sprites.update(dt, self.player.pos)
		self.get_keys()
		self.get_gears()
		self.get_damage()
		self.check_death(self.player.pos, dt)
		self.display_surface.fill(self.sky_color)
		self.all_sprites.custom_draw(self.player)
		if self.tab_pressed:
			self.inventory.show_inventory(self.gears_amount, self.player_stats)
		return self.current_stage

class SecondFloor(Level):
	def __init__(self, grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds=True, has_horizon=True):
		super().__init__(grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds, has_horizon)
		self.current_stage = 11
		self.prev_stage = 3
		self.pink_door = False
		self.pink_bed = False
		self.wall = False

		self.bg_music = audio['inside_theme']
		self.bg_music.set_volume(0.2)
		self.is_music_playing = False

	def play_sound(self):
		if not self.is_music_playing:
			self.bg_music.play(loops=-1)
			self.is_music_playing = True

	def get_activator(self):
		collision_sprites = pygame.sprite.spritecollide(self.player, self.activator_sprites, False)
		self.pink_door = False
		self.pink_bed = False
		self.wall = False
		if collision_sprites:
			for sprite in collision_sprites:
				if sprite.__dict__['id'] == 'pink_door_in':
					self.helper.show_helper('has_item')
					self.pink_door = True
				if sprite.__dict__['id'] == 'sf_bed' and not self.player_stats['hammer_key']:
					self.helper.show_helper('sleep_well')
					self.pink_bed = True
				if sprite.__dict__['id'] == 'act_wall' and not self.player_stats['hammer_key']:
					self.helper.show_helper('hammer_not')
				if sprite.__dict__['id'] == 'act_wall' and self.player_stats['hammer_key']:
					self.helper.show_helper('hammer_yes')
					self.wall = True
	
	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if self.has_clouds and event.type == self.cloud_timer:
				surf = choice(self.cloud_surfs)
				surf = pygame.transform.scale2x(surf) if randint(0, 5) > 3 else surf
				x = self.level_limits['right'] + randint(100, 300)
				y = self.horizon_y - randint(-50, 600)
				Cloud((x, y), surf, self.all_sprites, self.level_limits['left'])
			if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
				self.tab_pressed = True
			if event.type == pygame.KEYUP and event.key == pygame.K_TAB:
				self.tab_pressed = False
			if event.type == pygame.KEYDOWN and event.key in (pygame.K_x, pygame.K_UP) and self.pink_door:
				self.bg_music.stop()
				self.current_stage = 6
				self.pink_door = False
				self.is_music_playing = False
			if event.type == pygame.KEYDOWN and event.key in (pygame.K_x, pygame.K_UP) and self.pink_bed:
				self.bg_music.stop()
				self.current_stage = 12
				self.pink_bed = False
				self.is_music_playing = False
			if event.type == pygame.KEYDOWN and event.key in (pygame.K_x, pygame.K_UP) and self.wall:
				self.bg_music.stop()
				self.current_stage = 13
				self.wall = False
				self.is_music_playing = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
				self.save_active = True
				self.quicksave_time.activate()
				self.save_the_game()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F9:
				self.load_the_game()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.bg_music.stop()
				self.set_prev_stage(self.current_stage, self.prev_stage)
				self.current_stage = self.prev_stage
				self.is_music_playing = False
	
	def run(self, dt, gears_amount, player_stats, current_stage):
		self.current_stage = current_stage
		self.gears_amount = gears_amount
		self.player_stats = player_stats
		self.play_sound()
		self.correct_falling()
		self.event_loop()
		self.all_sprites.update(dt, self.player.pos)
		self.get_keys()
		self.get_gears()
		self.get_damage()
		self.get_activator()
		self.check_death(self.player.pos, dt)
		self.display_surface.fill(self.sky_color)
		self.all_sprites.custom_draw(self.player)
		if self.tab_pressed:
			self.inventory.show_inventory(self.gears_amount, self.player_stats)
		self.get_activator()
		self.show_save_message(dt)
		return self.current_stage

class Garden(Level):
	def __init__(self, grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds=True, has_horizon=True):
		super().__init__(grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds, has_horizon)
		self.current_stage = 12
		self.prev_stage = 3

		self.bg_music = audio['garden_theme']
		self.bg_music.set_volume(0.2)
		self.is_music_playing = False
	
	def play_sound(self):
		if not self.is_music_playing:
			self.bg_music.play(loops=-1)
			self.is_music_playing = True
	
	def check_green_key(self):
		if self.player_stats['hammer_key']:
			self.bg_music.stop()
			self.current_stage = 11
			self.is_music_playing = False

	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if self.has_clouds and event.type == self.cloud_timer:
				surf = choice(self.cloud_surfs)
				surf = pygame.transform.scale2x(surf) if randint(0, 5) > 3 else surf
				x = self.level_limits['right'] + randint(100, 300)
				y = self.horizon_y - randint(-50, 600)
				Cloud((x, y), surf, self.all_sprites, self.level_limits['left'])
			if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
				self.tab_pressed = True
			if event.type == pygame.KEYUP and event.key == pygame.K_TAB:
				self.tab_pressed = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
				self.save_active = True
				self.quicksave_time.activate()
				self.save_the_game()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F9:
				self.load_the_game()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.bg_music.stop()
				self.set_prev_stage(self.current_stage, self.prev_stage)
				self.current_stage = self.prev_stage
				self.is_music_playing = False
			
	
	def run(self, dt, gears_amount, player_stats, current_stage):
		self.current_stage = current_stage
		self.gears_amount = gears_amount
		self.player_stats = player_stats
		self.play_sound()
		self.correct_falling()
		self.event_loop()
		self.check_green_key()
		self.all_sprites.update(dt, self.player.pos)
		self.get_keys()
		self.get_gears()
		self.get_damage()
		self.check_death(self.player.pos, dt)
		self.display_surface.fill(self.sky_color)
		self.all_sprites.custom_draw(self.player)
		if self.tab_pressed:
			self.inventory.show_inventory(self.gears_amount, self.player_stats)
		self.show_save_message(dt)
		return self.current_stage

class Poison(Level):
	def __init__(self, grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds=True, has_horizon=True):
		super().__init__(grid, switch, asset_dict, audio, gear_change, hp, change_keys, sky_color, ground_color, set_prev_stage, has_clouds, has_horizon)
		self.current_stage = 13
		self.prev_stage = 3
		self.machine = False

		self.bg_music = audio['poison_theme']
		self.bg_music.set_volume(0.2)
		self.is_music_playing = False
	
	def play_sound(self):
		if not self.is_music_playing:
			self.bg_music.play(loops=-1)
			self.is_music_playing = True

	def get_activator(self):
		collision_sprites = pygame.sprite.spritecollide(self.player, self.activator_sprites, False)
		self.machine = False
		if collision_sprites:
			for sprite in collision_sprites:
				if sprite.__dict__['id'] == 'machine':
					self.helper.show_helper('machine')
					self.machine = True
	
	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if self.has_clouds and event.type == self.cloud_timer:
				surf = choice(self.cloud_surfs)
				surf = pygame.transform.scale2x(surf) if randint(0, 5) > 3 else surf
				x = self.level_limits['right'] + randint(100, 300)
				y = self.horizon_y - randint(-50, 600)
				Cloud((x, y), surf, self.all_sprites, self.level_limits['left'])
			if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
				self.tab_pressed = True
			if event.type == pygame.KEYUP and event.key == pygame.K_TAB:
				self.tab_pressed = False
			if event.type == pygame.KEYDOWN and event.key in (pygame.K_x, pygame.K_UP) and self.machine:
				self.bg_music.stop()
				if self.gears_amount < 10:
					print('Sad Ending')
				else:
					print('Happy Ending')
				self.machine = False
				self.current_stage = 3
				self.is_music_playing = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
				self.save_active = True
				self.quicksave_time.activate()
				self.save_the_game()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F9:
				self.load_the_game()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.bg_music.stop()
				self.set_prev_stage(self.current_stage, self.prev_stage)
				self.current_stage = self.prev_stage
				self.is_music_playing = False

	
	def run(self, dt, gears_amount, player_stats, current_stage):
		self.current_stage = current_stage
		self.gears_amount = gears_amount
		self.player_stats = player_stats
		self.play_sound()
		self.correct_falling()
		self.event_loop()
		self.all_sprites.update(dt, self.player.pos)
		self.get_keys()
		self.get_gears()
		self.get_damage()
		self.get_activator()
		self.check_death(self.player.pos, dt)
		self.display_surface.fill(self.sky_color)
		self.all_sprites.custom_draw(self.player)
		if self.tab_pressed:
			self.inventory.show_inventory(self.gears_amount, self.player_stats)
		self.get_activator()
		self.show_save_message(dt)
		return self.current_stage