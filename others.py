import pygame
import classes
import os
import sys

def is_field_leftclicked(size, event, winsize):
    """Megadja, hogy a felhasználó a játékmezőre kattintott-e bal egérgombbal, feltételezve, hogy a játékmező az ablak közepén van."""
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] - ((winsize[0] // 2) - (size[0] // 2)) >= 0 and event.pos[0] - ((winsize[0] // 2) - (size[0] // 2)) <= size[0] and event.pos[1] - ((winsize[1] // 2) - (size[1] // 2)) >= 0 and event.pos[1] - ((winsize[1] // 2) - (size[1] // 2)) <= size[1]:
        return True
    else:
        return False

def is_field_rightclicked(size, event, winsize):
    """Megadja, hogy a felhasználó a játékmezőre kattintott-e jobb egérgombbal, feltételezve, hogy a játékmező az ablak közepén van."""
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and event.pos[0] - ((winsize[0] // 2) - (size[0] // 2)) >= 0 and event.pos[0] - ((winsize[0] // 2) - (size[0] // 2)) <= size[0] and event.pos[1] - ((winsize[1] // 2) - (size[1] // 2)) >= 0 and event.pos[1] - ((winsize[1] // 2) - (size[1] // 2)) <= size[1]:
        return True
    else:
        return False

def field_coordinates(size, tile_size, event, winsize):
    """Visszaadja, hogy a felhasználó a játékmező melyik cellájára kattintott, feltételezve, hogy a játékmező az ablak közepén van."""
    return [ ( event.pos[0] - ((winsize[0] // 2) - (size[0] // 2))) // tile_size.width, (event.pos[1] - ((winsize[1] // 2) - (size[1] // 2))) // tile_size.height ]

def gameover_common():
    """A játék lezárulását követő képernyők közös része. Az időszámlálót kikapcsolja, és kattintásra vár bárhol az ablakban."""
    pygame.time.set_timer(pygame.USEREVENT, 0)
    wait_for_click = pygame.event.wait()
    while not (wait_for_click.type == pygame.MOUSEBUTTONDOWN and wait_for_click.button == 1):
        if wait_for_click.type == pygame.QUIT:
            raise ValueError("exit-gameover")
        wait_for_click = pygame.event.wait()

def uncover_all(game_field):
    for i in game_field:
        for j in i:
            j.uncover()

def reset_field(game_field):
    """A játékmező alapra állítása, az aknák helye és a mezők számossága marad."""
    for i in game_field:
        for j in i:
            j.cover()
            j.take_flag()

def multiple_lines_center(text, font, screen_x, window, top, margin):
    """Többsoros szöveg automatikus tördelése és kiíratása középre igazítva a képernyőn."""
    disp = classes.Screen

    lines = text.split("\n")
    
    for i in range(len(lines)):
        lines[i] = lines[i].split(" ")
        row_begin = 0
        j = 0
        while j < len(lines[i]):
            while font.render(" ".join(lines[i][row_begin:j + 1]), True, disp.color_black()).get_rect().width < screen_x - 2 * margin and j < len(lines[i]): # növeljük a sorban a szavak számát, amíg kiférnek
                j += 1
            if row_begin == j: # a szöveg nem fér ki, de azért inkább kiiratjuk, különben végtelen ciklus lenne
                row = font.render(" ".join(lines[i][row_begin:j + 1]), True, disp.color_black())
                j += 1
            else:
                row = font.render(" ".join(lines[i][row_begin:j]), True, disp.color_black())
            window.blit(row, (screen_x // 2 - row.get_rect().width // 2, top))
            row_begin = j
            top += row.get_rect().height

def universal_window(window, text, type, in_game = False):
    """Újrahasználható, paraméterezhető párbeszédablak."""
    disp_size = pygame.display.get_window_size()
    
    arial_30 = pygame.font.Font("Files/arial.ttf", 30)

    window.fill(pygame.Color(classes.Screen.color_bgcolor()))
    multiple_lines_center(text, arial_30, disp_size[0], window, disp_size[1] // 6, 30)

    if type == classes.WindowType.OK:
        ok_button = classes.DisplayItems([pygame.image.load("Files/oke.jpg").convert(), pygame.image.load("Files/oke_lenyomva.jpg").convert()], (disp_size[0] // 2, 2 * disp_size[1] // 3), "center", "center")
        ok_button.draw(window)
    elif type == classes.WindowType.YES_NO:
        yes_button = classes.DisplayItems([pygame.image.load("Files/igen.jpg").convert(), pygame.image.load("Files/igen_lenyomva.jpg").convert()], (disp_size[0] // 2 - 3, 2 * disp_size[1] // 3), "right", "center")
        no_button = classes.DisplayItems([pygame.image.load("Files/nem.jpg").convert(), pygame.image.load("Files/nem_lenyomva.jpg").convert()], (disp_size[0] // 2 + 3, 2 * disp_size[1] // 3), "left", "center")
        yes_button.draw(window)
        no_button.draw(window)
    elif type == classes.WindowType.INPUTBOX:
        ok_button = classes.DisplayItems([pygame.image.load("Files/oke.jpg").convert(), pygame.image.load("Files/oke_lenyomva.jpg").convert()], (disp_size[0] // 2, 4 * disp_size[1] // 5), "center", "center")
        ok_button.draw(window)
        input_field = classes.DisplayItems(pygame.image.load("Files/input_mezo.jpg").convert(), (disp_size[0] // 2, disp_size[1] // 2), "center", "center")
        input_field.draw(window)
        userinput = ""
        cursor = True
        pygame.time.set_timer(pygame.USEREVENT + 1, 500)

    pygame.display.update()
    clock = pygame.time.Clock()
    run = True
    while run:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            if in_game:
                raise ValueError("exit")
            else:
                sys.exit()
        elif type == classes.WindowType.OK:
            if ok_button.is_button_left_clicked(event, window):
                run = False
        elif type == classes.WindowType.YES_NO:
            if yes_button.is_button_left_clicked(event, window):
                return classes.ReturnType.YES
            elif no_button.is_button_left_clicked(event, window):
                return classes.ReturnType.NO
        elif type == classes.WindowType.INPUTBOX:
            if event.type == pygame.USEREVENT + 1:
                cursor = not cursor
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    userinput = userinput[0:len(userinput) - 1]
                elif not event.key in ( pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_TAB, pygame.K_KP_ENTER, pygame.K_DELETE ): # próba alapján problémát okozó whitespace karakterek
                    if not arial_30.render(userinput + event.unicode + "|", True, classes.Screen.color_black()).get_width() >= input_field.getsize().width - 15: # nincs karakterlimit, csak férjen bele a mezőbe
                        userinput += event.unicode
                elif event.key == pygame.K_RETURN:
                    run = False
            elif ok_button.is_button_left_clicked(event, window):
                run = False

            input_field.draw(window)
            if cursor:
                input_text = classes.DisplayItems(arial_30.render(userinput + "|", True, classes.Screen.color_black()), (input_field.getpos()[0] + 10, input_field.getpos()[1] + input_field.getsize().height // 2), "left", "center")
                input_text.draw(window)
            else:
                input_text = classes.DisplayItems(arial_30.render(userinput, True, classes.Screen.color_black()), (input_field.getpos()[0] + 10, input_field.getpos()[1] + input_field.getsize().height // 2), "left", "center")
                input_text.draw(window)
            pygame.display.update()
            clock.tick(60) # a gyorsabban írók miatt növelni kell a képfrissítést
    if type == classes.WindowType.INPUTBOX:
        pygame.time.set_timer(pygame.USEREVENT + 1, 0)
        return userinput
    else:
        return None

def save_game(game_data, player):
    """Játékállás elmentése"""
    if not os.path.exists("Data"):
        os.mkdir("Data")
    with open("Data/save.txt", "wt", encoding="utf-8") as f:
        f.write(f"{game_data.set_time}\n")
        f.write(f"{game_data.num_of_players}\n")
        f.write(f"{player}\n")
        f.write(f"{game_data.flags_left}\n")
        f.write(f"{game_data.num_of_mines}\n")
        f.write(f"{game_data.mines_to_flag}\n")
        f.write(f"{game_data.field_elements[0]}:{game_data.field_elements[1]}\n")
        for i in game_data.player_data:
            f.write(f"{i.time}:{i.won}\n")
        f.write("END-OF-PLAYER-DATA\n")
        for i in game_data.game_field:
            for j in i:
                item = j.get_status()
                for k in item:
                    f.write(f"{k},")
                f.write(":")
            f.write("\n")

def load_game():
    """Játékállás betöltése"""
    loaded_data = classes.GameData()
    loaded_data.game_field = []
    with open("Data/save.txt", "rt", encoding="utf-8") as f:
        loaded_data.set_time = int(f.readline().rstrip("\n"))
        loaded_data.num_of_players = int(f.readline().rstrip("\n"))
        loaded_data.player_start_from = int(f.readline().rstrip("\n"))
        loaded_data.flags_left = int(f.readline().rstrip("\n"))
        loaded_data.num_of_mines = int(f.readline().rstrip("\n"))
        loaded_data.mines_to_flag = int(f.readline().rstrip("\n"))
        field_elements_temp = f.readline().rstrip("\n").split(":")
        loaded_data.field_elements = [ int(field_elements_temp[0]), int(field_elements_temp[1]) ]
        loaded_data.player_data = []
        read_line = f.readline().rstrip("\n")
        while not read_line == "END-OF-PLAYER-DATA": # egyes játékosok adatai
            current_line = read_line.split(":")
            current_data = classes.PlayerData()
            current_data.time = int(current_line[0])
            if current_line[1] == "True":
                current_data.won = True
            else:
                if not current_line[1] == "False":
                    raise ValueError # csak egy kis hibakeresés
                current_data.won = False
            loaded_data.player_data.append(current_data)
            read_line = f.readline().rstrip("\n")
        for i in f: # mező állapota
            line = i.rstrip(",:\n").split(":")
            row = []
            for j in line:
                row.append(classes.Tile())
                item = j.rstrip(",").split(",")
                if item[0] == "True":
                    row[len(row) - 1].uncover()
                elif not item[0] == "False":
                    raise ValueError
                if item[1] == "True":
                    row[len(row) - 1].give_mine()
                elif not item[1] == "False":
                    raise ValueError
                if item[2] == "True":
                    row[len(row) - 1].give_flag()
                elif not item[2] == "False":
                    raise ValueError
                row[len(row) - 1].set_num_to(int(item[3]))
            loaded_data.game_field.append(row)
    return loaded_data

def load_scoreboard(field_size, mines, time):
    """Ranglista betöltése paraméterek alapján"""
    filename = f"{field_size[0]}-{field_size[1]}-{mines}-{time}.txt"
    loaded_data = []
    if os.path.exists(f"Data/{filename}"):
        try:
            with open(f"Data/{filename}", "rt", encoding="utf8") as f:
                for i in f:
                    line = i.rstrip("\n").split("\t")
                    loaded_data.append(classes.ScoreboardData(line[0], line[1]))
        except:
            os.remove(f"Data/{filename}")
            return []
    return loaded_data

def save_scoreboard(field_size, mines, time, scoreboard, record):
    """Ranglista frissítése és mentése a paraméterek alapján"""
    filename = f"{field_size[0]}-{field_size[1]}-{mines}-{time}.txt"
    scoreboard.append(record)
    if not time == 0:
        record.time = time - record.time # a felhasznált időre vagyunk kíváncsiak, nem a fennmaradóra
    scoreboard.sort(key=classes.ScoreboardData.sort_key)
    with open(f"Data/{filename}", "wt", encoding="utf-8") as f:
        if len(scoreboard) < 10:
            length = len(scoreboard)
        else:
            length = 10
        for i in range(length):
            f.write(f"{scoreboard[i].name}\t{scoreboard[i].time}\n")