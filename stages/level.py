import pygame, sys 
from pygame.math import Vector2 as vector

from settings import *
from img_imports import *

from sprites import *

class Level:
	def __init__(self, grid, switch, asset_dict):
		self.display_surface = pygame.display.get_surface()
		self.switch = switch

		# groups 
		self.all_sprites = pygame.sprite.Group()
		self.keys_sprites = pygame.sprite.Group()
		self.gear_sprites = pygame.sprite.Group()
		self.enemies_sprites = pygame.sprite.Group()
		self.activator_sprites = pygame.sprite.Group()

		self.build_level(grid, asset_dict)

		self.taken_surf = asset_dict['taken']

	def build_level(self, grid, asset_dict):
		for layer_name, layer in grid.items():
			for pos, data in layer.items():
				if layer_name == 'common':
					Generic(pos, asset_dict['land'][data[0]][data[1]], self.all_sprites)
				match data:
					case 0: self.player = Player(pos, self.all_sprites)
					case 9: Angel(asset_dict['angel'], pos, [self.all_sprites, self.enemies_sprites])
					case 10: FlyingEnemy(asset_dict['bat'], pos, [self.all_sprites, self.enemies_sprites])
					case 11: Bird(asset_dict['bird'], pos, [self.all_sprites, self.enemies_sprites])
					case 12: FlyingEnemy(asset_dict['bug'], pos, [self.all_sprites, self.enemies_sprites])
					case 13: Camel(pos, asset_dict['camel'], self.all_sprites )
					case 14: Spikes(asset_dict['cem_spikes'], pos, [self.all_sprites, self.enemies_sprites])
					case 15: FlyingEnemy(asset_dict['disputes'], pos, [self.all_sprites, self.enemies_sprites])
					case 16: Fire(asset_dict['fire'], pos, [self.all_sprites, self.enemies_sprites])
					case 17: Spikes(asset_dict['gar_spikes'], pos, [self.all_sprites, self.enemies_sprites])
					case 18: Goat(asset_dict['goat'], pos, [self.all_sprites, self.enemies_sprites])
					case 19: Harp(asset_dict['harp'], pos, self.all_sprites)
					case 20: Spikes(asset_dict['heav_spikes'], pos, [self.all_sprites, self.enemies_sprites])
					case 21: WalkingEnemies(asset_dict['hedgehog'], pos, self.all_sprites)
					case 22: FlyingEnemy(asset_dict['scrolls'], pos, [self.all_sprites, self.enemies_sprites])
					case 23: Slime(asset_dict['slime'], pos, [self.all_sprites, self.enemies_sprites])
					case 24: Wasp(pos, asset_dict['wasp'], [self.all_sprites, self.enemies_sprites])
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
					case 69: Generic(pos, asset_dict['desert_stuff']['palm'][0], self.all_sprites)
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
					case 91: Activator(pos, asset_dict['activators']['wall'][0], [self.all_sprites, self.activator_sprites], lambda x: x)
					case 92: Activator(pos, asset_dict['activators']['blue_door_in'][0], [self.all_sprites, self.activator_sprites], lambda x: x)
					case 93: Activator(pos, asset_dict['activators']['blue_door_out'][0], [self.all_sprites, self.activator_sprites], lambda x: x)
					case 94: Activator(pos, asset_dict['activators']['cementry_gates'][0], [self.all_sprites, self.activator_sprites], lambda x: x)
					case 95: Activator(pos, asset_dict['activators']['cupboard_bed'][0], [self.all_sprites, self.activator_sprites], lambda x: x)
					case 96: Activator(pos, asset_dict['activators']['cupboard_door_in'][0], [self.all_sprites, self.activator_sprites], lambda x: x)
					case 97: Activator(pos, asset_dict['activators']['cupboard_door_out'][0], [self.all_sprites, self.activator_sprites], lambda x: x)
					case 98: Activator(pos, asset_dict['activators']['ff_bed_in'][0], [self.all_sprites, self.activator_sprites], lambda x: x)
					case 99: Activator(pos, asset_dict['activators']['green_door_in'][0], [self.all_sprites, self.activator_sprites], lambda x: x)
					case 100: Activator(pos, asset_dict['activators']['green_door_out'][0], [self.all_sprites, self.activator_sprites], lambda x: x)
					case 101: Activator(pos, asset_dict['activators']['machine'][0], [self.all_sprites, self.activator_sprites], lambda x: x)
					case 102: Activator(pos, asset_dict['activators']['pink_door_in'][0], [self.all_sprites, self.activator_sprites], lambda x: x)
					case 103: Activator(pos, asset_dict['activators']['pink_door_out'][0], [self.all_sprites, self.activator_sprites], lambda x: x)
					case 104: Activator(pos, asset_dict['activators']['sf_bed'][0], [self.all_sprites, self.activator_sprites], lambda x: x)


	def get_keys(self):
		collided_keys = pygame.sprite.spritecollide(self.player, self.keys_sprites, True)
		for sprite in collided_keys:
			match sprite.key_type:
				case 'green':
					self.player.inventory['green_key'] = True
					sprite.kill()
				case 'hammer':
					self.player.inventory['hammer'] = True
					sprite.kill()
				case 'pink':
					self.player.inventory['pink_key'] = True
					sprite.kill()
				case 'yellow':
					self.player.inventory['yellow_key'] = True
					sprite.kill()
			

	def get_gears(self):
		collided_gears = pygame.sprite.spritecollide(self.player, self.gear_sprites, True)
		for sprite in collided_gears:
			Taken(self.taken_surf, sprite.rect.center, self.all_sprites)
			self.player.inventory['gears'] += 1

	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.switch()

	def run(self, dt):
		self.event_loop()
		self.all_sprites.update(dt)
		self.get_keys()
		self.get_gears()
		self.display_surface.fill(SKY_COLOR)
		self.all_sprites.update(dt)
		self.all_sprites.draw(self.display_surface)