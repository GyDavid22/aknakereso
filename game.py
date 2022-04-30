import pygame
import classes
import others
import random
import menu
import os
import sys

def game(field_elements, num_of_mines, set_time, num_of_players, loaded_game = False):
    """A játékmenetet lebonyolító függvény."""
    disp = classes.Screen

    if loaded_game:
        try:
            game_data = others.load_game()
        except:
            others.universal_window(pygame.display.set_mode(disp.get_size()), "A talált játékállás sérült, így nem sikerült betölteni, és törlésre került. Kérlek, kezdj új játékot!", classes.WindowType.OK)
            pygame.display.set_mode(classes.Screen.get_size())
            return
        finally:
            os.remove("Data/save.txt")
    else: # ha nem betöltjük, létre kell hozni újakat
        game_data = classes.GameData(set_time=set_time, num_of_players=num_of_players, num_of_mines=num_of_mines, flags_left=num_of_mines, player_start_from=0, field_elements=field_elements, player_data=[])
        game_data.game_field = prepare_game(game_data.field_elements, game_data.num_of_mines)
        for _ in range(game_data.num_of_players):
            game_data.player_data.append(classes.PlayerData(game_data.set_time))

    scoreboard = others.load_scoreboard(game_data.field_elements, game_data.num_of_mines, game_data.set_time)
    
    # használt elemek betöltése
    arial_40 = pygame.font.Font("Files/arial.ttf", 40)
    arial_20 = pygame.font.Font("Files/arial.ttf", 20)
    tiles = classes.DisplayItems([pygame.image.load("Files/fedett.jpg").convert(), pygame.image.load("Files/fedett_zaszlo.jpg").convert(), pygame.image.load("Files/felfedett.jpg").convert(), pygame.image.load("Files/felfedett_akna.jpg").convert(), pygame.image.load("Files/felfedett_akna_kritikus.jpg").convert()])

    field_size = (game_data.field_elements[0] * tiles.getsize().width, game_data.field_elements[1] * tiles.getsize().height)

    # kijelző mezőhöz igazítása
    screen_x = disp.get_screenx()
    screen_y = disp.get_screeny()
    if field_size[0] > disp.get_screenx():
        screen_x = field_size[0] + 100
    if field_size[1] > disp.get_screeny() - 220: # kell a hely még alatta és felette is
        screen_y = field_size[1] + 200
    window = pygame.display.set_mode((screen_x, screen_y))

    # használt elemek betöltésének folytatása
    pause = classes.DisplayItems(pygame.image.load("Files/szunet.jpg").convert(), (5, screen_y - 5), "left", "bottom")
    if game_data.num_of_players > 1:
        field = classes.DisplayItems(pygame.image.load("Files/mezo.jpg").convert(), (screen_x // 2 - 5, screen_y // 40), "right", "top")
    else:
        field = classes.DisplayItems(pygame.image.load("Files/mezo.jpg").convert(), (screen_x // 2, screen_y // 40), "center", "top")
    faces = classes.DisplayItems([pygame.image.load("Files/default.jpg").convert(), pygame.image.load("Files/sad.jpg").convert(), pygame.image.load("Files/won.jpg").convert(), pygame.image.load("Files/blown.jpg").convert()], (pause.getpos()[0] + pause.getsize().width + 5, screen_y - 5), "left", "bottom")
    field_mini = classes.DisplayItems(pygame.image.load("Files/mezo_mini.jpg").convert(), (screen_x - 5, screen_y - 5), "right", "bottom")
    big_flag = classes.DisplayItems(pygame.image.load("Files/zaszlo_nagy.png").convert_alpha(), (field_mini.getpos()[0] - 5, screen_y - 5), "right", "bottom")
    
    # játék előkészítése
    if game_data.set_time == 0:
        countdown = False
    else:
        countdown = True
         
    # eseményhurok
    clock = pygame.time.Clock()

    end = False # a szünet menüből visszalépés is megszakítja a ciklust
    player = game_data.player_start_from
    while player < game_data.num_of_players and not end: # játékosonként iterál
        critical = False # ha a felhasználó aknára lépett
        criticalpos = [] # hol lépett aknára

        if loaded_game: # betöltött játéknál nem a 0-ról indítjuk az else ágban lévő adatokat, de csak az aktuális körben
            loaded_game = False
        else:
            game_data.flags_left = game_data.num_of_mines
            game_data.mines_to_flag = game_data.num_of_mines
        timeisup = False
        
        face_index = 0

        field_changed = True # optimalizáció része, nagy játékmezőkre indokolatlanul nagy a CPU fogyasztás enélkül
        try:
            if game_data.num_of_players > 1:
                others.universal_window(window, f"Felkészül: {player+1}. játékos. A játék megkezdéséhez kattints a gombra!", classes.WindowType.OK, True)
                player_text = classes.DisplayItems(arial_20.render(f"{player + 1}/{game_data.num_of_players}. játékos", True, disp.color_black()), (screen_x // 2 + 5, field.getpos()[1] + field.getsize().height // 2), "left", "center")
            pygame.time.set_timer(pygame.USEREVENT, 1000) # idő számolása

            run = True
            while run: # egy kört vezényel le
                # játékmenet felügyelete
                if critical: # aknára léptünk
                    others.gameover_common()
                    run = menu.lost_screen(window, "Aknára léptél.")
                    field_changed = True
                elif timeisup: # letelt az idő
                    others.gameover_common()
                    run = menu.lost_screen(window, "Letelt az idő")
                    field_changed = True
                elif game_data.mines_to_flag == 0: # nyertünk
                    if game_data.num_of_players > 1:
                        game_data.player_data[player].won = True
                    others.gameover_common()
                    run = menu.win_screen(window, scoreboard, game_data.player_data[player].time, game_data.field_elements, game_data.num_of_mines, game_data.set_time)
                    field_changed = True

                # események kezelése
                for event in pygame.event.get(): # bizonyos esetekben nagyobb reszponzivitást ad
                    if event.type == pygame.QUIT: # kilépés
                        raise ValueError("exit")
                    elif pause.is_button_left_clicked(event): # szünet menü
                        run = menu.pause_screen(window)
                        if not run:
                            end = True
                            raise ValueError("save")
                        field_changed = True
                    elif others.is_field_leftclicked(field_size, event, (screen_x, screen_y)): # bal kattintás egy cellára
                        cord = others.field_coordinates(field_size, tiles.getsize(), event, (screen_x, screen_y))
                        if game_data.game_field[cord[0]][cord[1]].get_status()[1]: # aknára kattintottunk
                            critical = True
                            criticalpos = cord
                            others.uncover_all(game_data.game_field)
                            face_index = 3
                        else: # nem akna, felfedjük a környéket
                            game_data.flags_left = discover(cord, game_data.game_field, game_data.flags_left)
                        field_changed = True
                    elif others.is_field_rightclicked(field_size, event, (screen_x, screen_y)): # zászlók
                        cord = others.field_coordinates(field_size, tiles.getsize(), event, (screen_x, screen_y))
                        if not game_data.game_field[cord[0]][cord[1]].get_status()[0] and not game_data.game_field[cord[0]][cord[1]].get_status()[2] and not game_data.flags_left == 0: # zászlót szúrunk le
                            game_data.game_field[cord[0]][cord[1]].give_flag()
                            game_data.flags_left -= 1
                            if game_data.game_field[cord[0]][cord[1]].get_status()[1]: # aknára került a zászló
                                game_data.mines_to_flag -=1
                            if game_data.mines_to_flag == 0:
                                face_index = 2
                        elif game_data.game_field[cord[0]][cord[1]].get_status()[2]: # felvesszük a zászlót
                            game_data.game_field[cord[0]][cord[1]].take_flag()
                            game_data.flags_left += 1
                            if game_data.game_field[cord[0]][cord[1]].get_status()[1]:
                                game_data.mines_to_flag +=1
                        field_changed = True
                    elif event.type == pygame.USEREVENT: # idő
                        if countdown:
                            game_data.player_data[player].time -= 1
                            if game_data.player_data[player].time == 0:
                                timeisup = True
                                others.uncover_all(game_data.game_field)
                                field_changed = True
                                face_index = 1
                        elif not countdown:
                            game_data.player_data[player].time += 1

                # változó szövegek kiszámítása
                time_text = classes.DisplayItems(arial_40.render(f"{game_data.player_data[player].time//60}:{game_data.player_data[player].time % 60:02d}", True, disp.color_black()), (field.getpos()[0] + field.getsize().width // 2, field.getpos()[1] + field.getsize().height // 2), "center", "center")
                flags_left_text = classes.DisplayItems(arial_40.render(str(game_data.flags_left), True, disp.color_black()), (field_mini.getpos()[0] + field_mini.getsize().width // 2, field_mini.getpos()[1] + field_mini.getsize().height // 2), "center", "center")
                
                # mező és egyéb elemek kirajzolása
                if field_changed:
                    window.fill(disp.color_bgcolor())
                    if game_data.num_of_players > 1:
                        player_text.draw(window)
                    pause.draw(window)
                    faces.draw(window, face_index)
                    field_mini.draw(window)
                    big_flag.draw(window)
                    flags_left_text.draw(window)

                    for i in range(len(game_data.game_field)):
                        for j in range(len(game_data.game_field[i])):
                            pos = ((screen_x - field_size[0]) // 2 + i * tiles.getsize().width, (screen_y - field_size[1]) // 2 + j * tiles.getsize().height)
                            if game_data.game_field[i][j].get_status()[0] and game_data.game_field[i][j].get_status()[1]:
                                if critical and [i, j] == criticalpos:
                                    tiles.draw(window, 4, pos)
                                else:
                                    tiles.draw(window, 3, pos)
                            elif game_data.game_field[i][j].get_status()[0]:
                                tiles.draw(window, 2, pos)
                            elif game_data.game_field[i][j].get_status()[2]:
                                tiles.draw(window, 1, pos)
                            else:
                                tiles.draw(window, 0, pos)
                            if game_data.game_field[i][j].get_status()[0] and not game_data.game_field[i][j].get_status()[3] == 0 and not game_data.game_field[i][j].get_status()[1]:
                                cellnumber = classes.DisplayItems(arial_20.render(str(game_data.game_field[i][j].get_status()[3]), True, disp.color_black()), (pos[0] + tiles.getsize().width // 2, pos[1] + tiles.getsize().height // 2), "center", "center")
                                cellnumber.draw(window)
                    field_changed = False
                field.draw(window)
                time_text.draw(window)
                
                # kijelző frissítése
                clock.tick(disp.get_fps())
                pygame.display.update()
        except ValueError as e: # a program ezen részén előfordulhat, hogy függvényhívás belsejében lép ki a felhasználó, ilyen esetekben is meg kell kérdezni, hogy szeretne-e menteni, és így nem kell a játék összes adatát továbbadni olyan függvényeknek, amiknek semmi dolga nincs velük
            if str(e) == "exit" or str(e) == "exit-gameover" or str(e) == "save":
                user_choice = others.universal_window(window, "Szeretnéd elmenteni az aktuális játékállást?", classes.WindowType.YES_NO)
                if user_choice == classes.ReturnType.YES:
                    if str(e) == "exit-gameover": # a következő játékos jön, olyan ablakról léptek ki, ami egy játékot zár le
                        others.reset_field(game_data.game_field)
                        player += 1
                    others.save_game(game_data, player)
                if not str(e) == "save":
                    sys.exit()
        
        others.reset_field(game_data.game_field)
        player += 1
    
    if not end: # játék végi összegzés, hogy melyik játékos nyert
        if game_data.num_of_players > 1:
            winner = -1
            best_time = game_data.player_data[0].time
            for i in range(len(game_data.player_data)):
                if game_data.player_data[i].won:
                    if countdown:
                        if game_data.player_data[i].time >= best_time:
                            winner = i + 1
                    else:
                        if game_data.player_data[i].time <= best_time:
                            winner = i + 1
            if winner == -1:
                others.universal_window(window, "Sajnos senki sem nyert.", classes.WindowType.OK)
            else:
                others.universal_window(window, f"A győztes: {winner}. játékos!", classes.WindowType.OK)
    pygame.display.set_mode(classes.Screen.get_size())

def prepare_game(field_elements, num_of_mines):
    """A játékmezőt teljesen létrehozó függvény."""
    game_field = []
    for _ in range(field_elements[0]):
        temp = []
        for _ in range(field_elements[1]):
            temp.append(classes.Tile())
        game_field.append(temp)

    # aknák random elhelyezése
    numbers_list = []
    for i in range(field_elements[0] * field_elements[1]):
        numbers_list.append(i)
    for _ in range(num_of_mines):
        number = random.randint(0, len(numbers_list) - 1)
        generated = numbers_list.pop(number)
        game_field[generated // field_elements[1]][generated % field_elements[1]].give_mine()
    numbers_list.clear()

    numbers(game_field)

    return game_field

def discover(pos, field, flags_left):
    """Egybefüggő üres cellák felderítése."""
    if pos[0] < 0 or pos[0] > len(field) - 1 or pos[1] < 0 or pos[1] > len(field[0]) - 1: # ha kilóg a tábláról, nem foglalkozunk vele
        return flags_left
    elif field[pos[0]][pos[1]].get_status()[0]: # ha már nyitva van, nem foglalkozunk vele
        return flags_left
    field[pos[0]][pos[1]].uncover()
    if field[pos[0]][pos[1]].get_status()[3] == 0: # rekurzív meghívás szomszédos cellákra
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                flags_left = discover([pos[0] + i, pos[1] + j], field, flags_left)
    if field[pos[0]][pos[1]].get_status()[2]: # automatikusan felszedett zászlók kezelése
        flags_left += 1
        field[pos[0]][pos[1]].take_flag()

    return flags_left

def numbers(field):
    """A mező celláiban lévő szám meghatározása."""
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j].get_status()[1]: # ha aknát találtunk, frissítjük a szomszédos cellákat
                for k in range(-1, 2, 1):
                    for l in range(-1, 2, 1):
                        if not (i + k < 0 or i + k >= len(field) or j + l < 0 or j + l >= len(field[i])):
                            field[i + k][j + l].set_num()