import pygame

class DisplayItems:
    def __init__(self, texture, pos = None, h_align = "left", v_align = "top"):
        self.__texture = texture
        if pos == None:
            self.__pos = None
        else:
            if isinstance(self.__texture, list):
                temp_texture = self.__texture[0]
            else:
                temp_texture = self.__texture
            temp_pos = []
            if h_align == "left":
                temp_pos.append(pos[0])
            elif h_align == "center":
                temp_pos.append(pos[0] - temp_texture.get_width() // 2)
            else: # hivatalosan "right", de kerüljük el a hibákat
                temp_pos.append(pos[0] - temp_texture.get_width())
            if v_align == "top":
                temp_pos.append(pos[1])
            elif v_align == "center":
                temp_pos.append(pos[1] - temp_texture.get_height() // 2)
            else: # mint az előbb, csak "bottom"
                temp_pos.append(pos[1] - temp_texture.get_height())
            self.__pos = tuple(temp_pos)
    
    def draw(self, window, index = 0, pos = None):
        """Az objektumban tárolt elem kirajzolása a képernyőre."""
        if not pos == None:
            draw_pos = pos
        else:
            draw_pos = self.__pos
        if isinstance(self.__texture, list):
            window.blit(self.__texture[index], draw_pos)
        else:
            window.blit(self.__texture, draw_pos)

    def is_button_left_clicked(self, event, window = None):
        """Logikai értékkel tér vissza annak megfelelően, hogy az elemre kattintottak-e bal egérgombbal, illetve a gombrakattintás meganimálása, ha lehetséges. (Fontos: az animálás nem használható olyan programrészben, ahol fontos, hogy ne veszítsünk eventet!)"""
        if isinstance(self.__texture, list):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.__texture[0].get_rect().collidepoint((event.pos[0] - self.__pos[0], event.pos[1] - self.__pos[1])):
                window.blit(self.__texture[1], self.__pos)
                pygame.display.update()
                clickend = pygame.event.wait()
                while not (clickend.type == pygame.MOUSEBUTTONUP and clickend.button == 1):
                    clickend = pygame.event.wait()
                window.blit(self.__texture[0], self.__pos)
                pygame.display.update()
                return True
            else:
                return False
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.__texture.get_rect().collidepoint((event.pos[0] - self.__pos[0], event.pos[1] - self.__pos[1])):
                return True
            else:
                return False

    def getpos(self):
        return self.__pos

    def getsize(self):
        if isinstance(self.__texture, list):
            return self.__texture[0].get_rect()
        else:
            return self.__texture.get_rect()

class Screen:
    __size = (400, 600)
    __bg_color = (96, 96, 96)
    __black = (0, 0, 0)
    __fps = 30

    def __init__(self): # példányosítható, de nem kötelező, hiszen konstansokat tárol, fölösleges külön példányokat létrehozni
        pass

    def get_size(self = None):
        return Screen.__size
    
    def get_screenx(self = None):
        return Screen.__size[0]

    def get_screeny(self = None):
        return Screen.__size[1]

    def color_bgcolor(self = None):
        return Screen.__bg_color
    
    def color_black(self = None):
        return Screen.__black

    def get_fps(self = None):
        return Screen.__fps

class Tile:
    def __init__(self):
        self.__is_uncovered = False
        self.__is_mine = False
        self.__is_flagged = False
        self.__number = 0

    def uncover(self):
        self.__is_uncovered = True
    
    def cover(self):
        self.__is_uncovered = False

    def give_mine(self):
        self.__is_mine = True

    def give_flag(self):
        self.__is_flagged = True
    
    def take_flag(self):
        self.__is_flagged = False

    def set_num(self):
        self.__number += 1

    def set_num_to(self, num):
        self.__number = num

    def get_status(self):
        """0: fel van-e fedve, 1: akna-e, 2: meg van-e jelölve, 3: a cella száma"""
        return [ self.__is_uncovered, self.__is_mine, self.__is_flagged, self.__number ]

class WindowType: # others.universal_window() használja
    OK = 1
    YES_NO = 2
    INPUTBOX = 3

class ReturnType: # others.universal_window() használja
    YES = 1
    NO = 2

class PlayerData:
    def __init__(self, time = 0):
        self.time = time
        self.won = False

class GameData:
    def __init__(self, game_field = None, set_time = None, num_of_players = None, player_start_from = None, flags_left = None, num_of_mines = None, mines_to_flag = None, player_data = None, field_elements = None):
        # a későbbiek miatt lesz praktikus, ha a konstruktor paraméterezhető, de nem kötelező
        self.game_field = game_field
        self.set_time = set_time
        self.num_of_players = num_of_players
        self.player_start_from = player_start_from
        self.flags_left = flags_left
        self.num_of_mines = num_of_mines
        self.mines_to_flag = mines_to_flag
        self.player_data = player_data
        self.field_elements = field_elements

class ScoreboardData:
    def __init__(self, name, time):
        self.name = name
        self.time = int(time)

    def sort_key(self):
        return self.time