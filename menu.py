import pygame
import classes
import game
import others
import random
import os
import sys

def menu(window):
    """Főképernyő"""
    disp = classes.Screen

    # felhasznált elemek és pozícióik betöltése
    arial_50 = pygame.font.Font("Files/arial.ttf", 50)
    arial_20 = pygame.font.Font("Files/arial.ttf", 20)

    game_button = classes.DisplayItems([pygame.image.load("Files/jatek.jpg").convert(), pygame.image.load("Files/jatek_lenyomva.jpg").convert()], (disp.get_screenx() // 2, 2 * disp.get_screeny() // 3), "center", "center")
    x_button = classes.DisplayItems([pygame.image.load("Files/x.jpg").convert(), pygame.image.load("Files/x_lenyomva.jpg").convert()], (5, disp.get_screeny() - 5), "left", "bottom")
    help_button = classes.DisplayItems([pygame.image.load("Files/sugo.jpg").convert(), pygame.image.load("Files/sugo_lenyomva.jpg").convert()], (disp.get_screenx() - 5, disp.get_screeny() - 5), "right", "bottom")
    minesweeper = classes.DisplayItems(arial_50.render("Aknakereső", True, disp.color_black()), (disp.get_screenx() // 2, disp.get_screeny() // 10), "center", "top")

    # használt változók
    mottos = [ "Aki másnak vermet ás, maga esik bele. Ez nagyon mély volt.",
               "Az Aknavető című játék folytatása.",
               "Üdvözlöm, tanár úr! :D",
               " - Közlegény, mi a teendő, ha aknára lépünk?\n - 50 méter magasra felrepülni és nagy területen szétszóródni, uram!",
               "A 90-es és a 2000-es évek kedvence.",
               "\"Boom, Boom, Boom, Boom!!\" - Vengaboys",
               "Ha még most kilépsz, nem fogsz veszíteni!",
               "Tudta? Egy éles robbanószerkezet veszélyt jelent ön és a környezete egészsége számára. Ha robbanásveszély gyanúja áll fenn, haladéktalanul hívja a 112-t!",
               "/valami random generált hülyeség helye/",
               "Szia, uram! Aknakereső okosba' érdekel?" ]
    random_motto = random.randint(0, len(mottos) - 1)
    
    # eseményhurok
    clock = pygame.time.Clock()
    run = True
    while run:
        event = pygame.event.wait()
        if event.type == pygame.QUIT: # kilépés
            run = False
        elif game_button.is_button_left_clicked(event, window): # beállítások menü
            settings(window)
            random_motto = random.randint(0, len(mottos) - 1)
        elif x_button.is_button_left_clicked(event, window): # kilépés
            run = False
        elif help_button.is_button_left_clicked(event, window): # súgó
            help_screen(window)
            random_motto = random.randint(0, len(mottos) - 1)
        
        # kirajzolás
        window.fill(pygame.Color(disp.color_bgcolor()))
        minesweeper.draw(window)
        others.multiple_lines_center(mottos[random_motto], arial_20, disp.get_screenx(), window, minesweeper.getpos()[1] + minesweeper.getsize().height * 2, 10)
        game_button.draw(window)
        x_button.draw(window)
        help_button.draw(window)

        clock.tick(disp.get_fps())
        pygame.display.update()

def settings(window):
    """Játék beállításai vagy mentett játékállás megtalálása, majd játék indítása."""
    disp = classes.Screen

    if os.path.exists("Data/save.txt"):
        user_choice = others.universal_window(window, "Mentett játékállást találtam. Szeretnéd folytatni? (A nem választása esetén törlődik a mentés!)", classes.WindowType.YES_NO)
        if user_choice == classes.ReturnType.YES:
            game.game(None, None, None, None, True)
        else:
            os.remove("Data/save.txt")

    # felhasznált elemek és pozícióik betöltése
    arial_40 = pygame.font.Font("Files/arial.ttf", 40)
    arial_50 = pygame.font.Font("Files/arial.ttf", 50)

    field1 = classes.DisplayItems(pygame.image.load("Files/mezo.jpg").convert(), (disp.get_screenx() // 2, 2 * disp.get_screeny() // 10), "center", "center")
    user = classes.DisplayItems(pygame.image.load("Files/user.png").convert_alpha(), (field1.getpos()[0] // 2, 2 * disp.get_screeny() // 10), "center", "center")
    down1 = classes.DisplayItems([pygame.image.load("Files/le.png").convert_alpha(), pygame.image.load("Files/le_lenyomva.png").convert_alpha()], (field1.getpos()[0] + field1.getsize().width + 20, 2 * disp.get_screeny() // 10), "left", "center")
    up1 = classes.DisplayItems([pygame.image.load("Files/fel.png").convert_alpha(), pygame.image.load("Files/fel_lenyomva.png").convert_alpha()], (field1.getpos()[0] + field1.getsize().width + down1.getsize().width + 30, 2 * disp.get_screeny() // 10), "left", "center")

    field2 = classes.DisplayItems(pygame.image.load("Files/mezo.jpg").convert(), (disp.get_screenx() // 2, 4 * disp.get_screeny() // 10), "center", "center")
    field_resize = classes.DisplayItems(pygame.image.load("Files/atmeretez.png").convert_alpha(), (field2.getpos()[0] // 2, 4 * disp.get_screeny() // 10), "center", "center")
    down2 = classes.DisplayItems([pygame.image.load("Files/le.png").convert_alpha(), pygame.image.load("Files/le_lenyomva.png").convert_alpha()], (field2.getpos()[0] + field2.getsize().width + 20, 4 * disp.get_screeny() // 10), "left", "center")
    up2 = classes.DisplayItems([pygame.image.load("Files/fel.png").convert_alpha(), pygame.image.load("Files/fel_lenyomva.png").convert_alpha()], (field2.getpos()[0] + field2.getsize().width + down2.getsize().width + 30, 4 * disp.get_screeny() // 10), "left", "center")

    field3 = classes.DisplayItems(pygame.image.load("Files/mezo.jpg").convert(), (disp.get_screenx() // 2, 6 * disp.get_screeny() // 10), "center", "center")
    bomb = classes.DisplayItems(pygame.transform.scale(pygame.image.load("Files/bomba.png").convert_alpha(), (70, 70)), (field3.getpos()[0] // 2, 6 * disp.get_screeny() // 10), "center", "center")
    down3 = classes.DisplayItems([pygame.image.load("Files/le.png").convert_alpha(), pygame.image.load("Files/le_lenyomva.png").convert_alpha()], (field3.getpos()[0] + field3.getsize().width + 20, 6 * disp.get_screeny() // 10), "left", "center")
    up3 = classes.DisplayItems([pygame.image.load("Files/fel.png").convert_alpha(), pygame.image.load("Files/fel_lenyomva.png").convert_alpha()], (field3.getpos()[0] + field3.getsize().width + down3.getsize().width + 30, 6 * disp.get_screeny() // 10), "left", "center")

    field4 = classes.DisplayItems(pygame.image.load("Files/mezo.jpg").convert(), (disp.get_screenx() // 2, 8 * disp.get_screeny() // 10), "center", "center")
    stopwatch = classes.DisplayItems(pygame.transform.scale(pygame.image.load("Files/ido.png").convert_alpha(), (70, 70)), (field4.getpos()[0] // 2, 8 * disp.get_screeny() // 10), "center", "center")
    down4 = classes.DisplayItems([pygame.image.load("Files/le.png").convert_alpha(), pygame.image.load("Files/le_lenyomva.png").convert_alpha()], (field4.getpos()[0] + field4.getsize().width + 20, 8 * disp.get_screeny() // 10), "left", "center")
    up4 = classes.DisplayItems([pygame.image.load("Files/fel.png").convert_alpha(), pygame.image.load("Files/fel_lenyomva.png").convert_alpha()], (field4.getpos()[0] + field4.getsize().width + down4.getsize().width + 30, 8 * disp.get_screeny() // 10), "left", "center")

    back_button = classes.DisplayItems([pygame.image.load("Files/nyil.jpg").convert(), pygame.image.load("Files/nyil_lenyomva.jpg").convert()], (5, disp.get_screeny() - 5), "left", "bottom")
    start_button = classes.DisplayItems([pygame.image.load("Files/start_gomb.jpg").convert(), pygame.image.load("Files/start_gomb_lenyomva.jpg").convert()], (disp.get_screenx() // 2, disp.get_screeny() - 5), "center", "bottom")
    scoreboard_botton = classes.DisplayItems([pygame.image.load("Files/kupa.jpg").convert(), pygame.image.load("Files/kupa_lenyomva.jpg").convert()], (disp.get_screenx() - 5, disp.get_screeny() - 5), "right", "bottom")

    settings_text = classes.DisplayItems(arial_50.render("Beállítások:", True, disp.color_black()), (disp.get_screenx() // 2, 1 * disp.get_screeny() // 40), "center", "top")

    # használt változók
    num_of_players = 1
    mines = 15
    field_size = 6
    field_sizes = [ [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9], [10, 10], [11, 11], [12, 12], [13, 13], [14, 14], [15, 15], [20, 15], [30, 15], [40, 15] ]
    time = 7
    time_options = [ 0, 5, 10, 15, 30, 60, 120, 300, 600, 900, 1800, 3600, 5400, 7200 ]

    # eseményhurok
    clock = pygame.time.Clock()
    run = True
    while run:
        event = pygame.event.wait()
        if event.type == pygame.QUIT: # kilépés
            sys.exit()
        elif back_button.is_button_left_clicked(event, window): # vissza
            run = False
        elif start_button.is_button_left_clicked(event, window): # start
            game.game(field_sizes[field_size], mines, time_options[time], num_of_players)
        elif scoreboard_botton.is_button_left_clicked(event, window):
            scoreboard_menu(window, field_sizes[field_size], mines, time_options[time])
        elif down1.is_button_left_clicked(event, window): # játékosok számának csökkentése
            if not num_of_players - 1 < 1:
                num_of_players -= 1
        elif up1.is_button_left_clicked(event, window): # játékosok számának növelése
            if not num_of_players + 1 > 4:
                num_of_players += 1
        elif down2.is_button_left_clicked(event, window): # mező csökkentés
            if not field_size - 1 < 0:
                field_size -= 1
                mines = int(field_sizes[field_size][0] * field_sizes[field_size][1] * 0.15)
        elif up2.is_button_left_clicked(event, window): # mező növelés
            if not field_size + 1 > len(field_sizes) - 1:
                field_size += 1
                mines = int(field_sizes[field_size][0] * field_sizes[field_size][1] * 0.15)
        elif down3.is_button_left_clicked(event, window): # akna csökkentés
            if not mines - 1 < 1:
                mines -= 1
        elif up3.is_button_left_clicked(event, window): # akna növelés
            if not mines + 1 > field_sizes[field_size][0] * field_sizes[field_size][1]:
                mines += 1
        elif down4.is_button_left_clicked(event, window): # idő csökkentés
            if not time - 1 < 0:
                time -= 1
        elif up4.is_button_left_clicked(event, window): # idő növelés
            if not time + 1 > len(time_options) - 1:
                time += 1

        # változó szövegek kiszámítása
        players_text = classes.DisplayItems(arial_40.render(f"{num_of_players}", True, disp.color_black()), (disp.get_screenx() // 2, field1.getpos()[1] + field1.getsize().height // 2), "center", "center")
        field_text = classes.DisplayItems(arial_40.render(str(field_sizes[field_size][0]) + "*" + str(field_sizes[field_size][1]), True, disp.color_black()), (disp.get_screenx() // 2, field2.getpos()[1] + field2.getsize().height // 2), "center", "center")
        mines_text = classes.DisplayItems(arial_40.render(str(mines), True, disp.color_black()), (disp.get_screenx() // 2, field3.getpos()[1] + field3.getsize().height // 2), "center", "center")
        if time == 0:
            time_text = classes.DisplayItems(arial_40.render("∞", True, disp.color_black()), (disp.get_screenx() // 2, field4.getpos()[1] + field4.getsize().height // 2), "center", "center")
        else:
            time_text = classes.DisplayItems(arial_40.render(str(f"{time_options[time] // 60}:{time_options[time] % 60:02d}"), True, disp.color_black()), (disp.get_screenx() // 2, field4.getpos()[1] + field4.getsize().height // 2), "center", "center")
        
        # elemek kirajzolása
        window.fill(disp.color_bgcolor())
        settings_text.draw(window)

        field1.draw(window)
        up1.draw(window)
        down1.draw(window)
        players_text.draw(window)
        user.draw(window)

        field2.draw(window)
        up2.draw(window)
        down2.draw(window)
        field_text.draw(window)
        field_resize.draw(window)

        field3.draw(window)
        up3.draw(window)
        down3.draw(window)
        mines_text.draw(window)
        bomb.draw(window)

        field4.draw(window)
        up4.draw(window)
        down4.draw(window)
        time_text.draw(window)
        stopwatch.draw(window)

        back_button.draw(window)
        start_button.draw(window)
        scoreboard_botton.draw(window)

        clock.tick(disp.get_fps())
        pygame.display.update()

def lost_screen(window, text):
    """Vesztes játék utáni képernyő"""
    disp = classes.Screen

    arial_50 = pygame.font.Font("Files/arial.ttf", 50)

    # használt elemek betöltése
    arrow_button = classes.DisplayItems([pygame.image.load("Files/nyil.jpg").convert(), pygame.image.load("Files/nyil_lenyomva.jpg").convert()], (pygame.display.get_window_size()[0] - 5, pygame.display.get_window_size()[1] - 5), "right", "bottom")
    lost_text = classes.DisplayItems(arial_50.render(text, True, disp.color_black()), (pygame.display.get_window_size()[0] // 2, pygame.display.get_window_size()[1] // 4), "center", "center")

    click = False

    # kirajzolás
    window.fill(disp.color_bgcolor())
    lost_text.draw(window)
    arrow_button.draw(window)
    pygame.display.update()

    # eseményhurok
    clock = pygame.time.Clock()
    run = True
    while run:
        event = pygame.event.wait()
        if event.type == pygame.QUIT: # ablak bezárása
            raise ValueError("exit-gameover")
        elif arrow_button.is_button_left_clicked(event, window): # visszanyíl kattintása (játék befejezése)
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # egérgomb lenyomva
            click = True
        elif click and event.type == pygame.MOUSEBUTTONUP and event.button == 1: # egérgomb felengedve, eseményhurok vége
            run = False

        clock.tick(disp.get_fps())
    return True

def pause_screen(window):
    """Játék közbeni szünet képernyő"""
    disp = classes.Screen

    arial_50 = pygame.font.Font("Files/arial.ttf", 50)

    # használt elemek betöltése
    pause_text = classes.DisplayItems(arial_50.render("Szünet.", True, disp.color_black()), (pygame.display.get_window_size()[0] // 2, pygame.display.get_window_size()[1] // 4), "center", "center")
    play_button = classes.DisplayItems([pygame.image.load("Files/play.jpg").convert(), pygame.image.load("Files/play_lenyomva.jpg").convert()], (5, pygame.display.get_window_size()[1] - 5), "left", "bottom")
    arrow_button = classes.DisplayItems([pygame.image.load("Files/nyil.jpg").convert(), pygame.image.load("Files/nyil_lenyomva.jpg").convert()], (pygame.display.get_window_size()[0] - 5, pygame.display.get_window_size()[1] - 5), "right", "bottom")

    # kirajzolás
    window.fill(disp.color_bgcolor())
    pause_text.draw(window)
    play_button.draw(window)
    arrow_button.draw(window)
    pygame.display.update()

    # eseményhurok
    clock = pygame.time.Clock()
    run = True
    while run:
        event = pygame.event.wait()
        if event.type == pygame.QUIT: # ablak bezárása
            raise ValueError("exit")
        elif play_button.is_button_left_clicked(event, window): # játék folytatása; eseményhurok vége
            run = False
        elif arrow_button.is_button_left_clicked(event, window): # játék befejezése
            return False

    clock.tick(disp.get_fps())
    return True

def win_screen(window, scoreboard, user_time, field_size, num_of_mines, set_time):
    """Nyertes játék utáni képernyő, illetve szükséges esetben ranglista frissítése."""
    disp = classes.Screen

    arial_50 = pygame.font.Font("Files/arial.ttf", 50)

    # használt elemek betöltése
    arrow_button = classes.DisplayItems([pygame.image.load("Files/nyil.jpg").convert(), pygame.image.load("Files/nyil_lenyomva.jpg").convert()], (pygame.display.get_window_size()[0] - 5, pygame.display.get_window_size()[1] - 5), "right", "bottom")
    win_text = classes.DisplayItems(arial_50.render("Nyertél!", True, disp.color_black()), (pygame.display.get_window_size()[0] // 2, pygame.display.get_window_size()[1] // 4), "center", "center")

    click = False

    # kirajzolás
    window.fill(disp.color_bgcolor())
    win_text.draw(window)
    arrow_button.draw(window)
    pygame.display.update()

    # eseményhurok
    clock = pygame.time.Clock()
    run = True
    while run:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            raise ValueError("exit-gameover") # itt az user túl aggresszívan lép ki ahhoz, hogy felvegyük a ranglistára :,( túl sok "nyaggatás" lenne kilépés helyett
        elif arrow_button.is_button_left_clicked(event, window):
            try:
                if set_time == 0:
                    if len(scoreboard) < 10 or user_time < scoreboard[len(scoreboard) - 1].time:
                        user_name = others.universal_window(window, "Gratulálok! Az eredményed alapján felkerültél a ranglistára! Írd be a neved!", classes.WindowType.INPUTBOX, True)
                        others.save_scoreboard(field_size, num_of_mines, set_time, scoreboard, classes.ScoreboardData(user_name, user_time))
                else:
                    if len(scoreboard) < 10 or user_time > scoreboard[len(scoreboard) - 1].time:
                        user_name = others.universal_window(window, "Gratulálok! Az eredményed alapján felkerültél a ranglistára! Írd be a neved!", classes.WindowType.INPUTBOX, True)
                        others.save_scoreboard(field_size, num_of_mines, set_time, scoreboard, classes.ScoreboardData(user_name, user_time))
            except: # ha bezárják az input ablakot, jelezzük felfelé
                raise ValueError("exit-gameover")
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True
        elif click and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            run = False

    clock.tick(disp.get_fps())
    return True

def help_screen(window):
    """Súgó képernyő"""
    disp = classes.Screen

    arial_50 = pygame.font.Font("Files/arial.ttf", 50)
    arial_20 = pygame.font.Font("Files/arial.ttf", 17)

    # használt elemek betöltése
    arrow = classes.DisplayItems([pygame.image.load("Files/nyil.jpg").convert(), pygame.image.load("Files/nyil_lenyomva.jpg").convert()], (5, disp.get_screeny() - 5), "left", "bottom")
    help = classes.DisplayItems(arial_50.render("Súgó", True, disp.color_black()), (disp.get_screenx() // 2, disp.get_screeny() // 10), "center", "top")

    # használt változók
    help_text = "Aknakereső 1.0\n\nKattints a bal egérgombbal egy mezőre, hogy felfedd a vele összefüggő üres mezőket! Kattints a jobb egérgombbal, hogy megjelölj egy piros zászlóval egy olyan cellát, ami szerinted aknát tartalmaz! A felfedett mezőkben lévő szám azt jelöli, hogy a szomszédos cellái közül hány tartalmaz aknát. Ha kifutsz az időből vagy olyan cellát nyitsz fel, ami alatt akna van, vesztettél. Ha minden aknát tartalmazó cellát megjelöltél, nyertél!\n\nKészült a BME-VIK üzemmérnök-informatikus BProf képzésén lévő A programozás alapjai nevű tárgy nagy házi feladataként 2021-ben.\nKészítette: Gyenes Dávid"

    # kirajzolás, csak egyszer tesszük meg, mert ebben a menüben nem változik a képernyő tartalma
    window.fill(disp.color_bgcolor())
    help.draw(window)
    others.multiple_lines_center(help_text, arial_20, disp.get_screenx(), window, help.getpos()[1] + help.getsize().height * 2, 10)
    arrow.draw(window)
    pygame.display.update()

    # eseményhurok
    clock = pygame.time.Clock()
    run = True
    while run:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            sys.exit()
        elif arrow.is_button_left_clicked(event, window):
            run = False

        clock.tick(disp.get_fps())

def scoreboard_menu(window, field_size, num_of_mines, time):
    """Ranglista képernyő"""
    disp = classes.Screen
    window.fill(disp.color_bgcolor()) # háttér letörlése a hívó függvény után
    
    # használt elemek betöltése
    scoreboard = others.load_scoreboard(field_size, num_of_mines, time)

    arial_20 = pygame.font.Font("Files/arial.ttf", 20)
    arial_50 = pygame.font.Font("Files/arial.ttf", 50)

    scoreboard_text = classes.DisplayItems(arial_50.render("Ranglista", True, disp.color_black()), (disp.get_screenx() // 2, 1 * disp.get_screeny() // 40), "center", "top")
    back_button = classes.DisplayItems([pygame.image.load("Files/nyil.jpg").convert(), pygame.image.load("Files/nyil_lenyomva.jpg").convert()], (5, disp.get_screeny() - 5), "left", "bottom")
    
    # kirajzolás (nem változik a képernyő tartalma ebben a menüben, elég egyszer megtenni)
    scoreboard_text.draw(window)
    if time == 0:
        time_text = "∞"
    else:
        time_text = f"{time // 60}:{time % 60:02d}"
    others.multiple_lines_center(f"Mezőméret: {field_size[0]}*{field_size[1]}, aknák száma: {num_of_mines}, idő: {time_text}", arial_20, disp.get_screenx(), window, scoreboard_text.getpos()[1] + scoreboard_text.getsize().height + 50, 20)
    if len(scoreboard) == 0:
        display_text = classes.DisplayItems(arial_20.render("Még nincs adat. Legyél te az első!", True, disp.color_black()), (disp.get_screenx() // 2, disp.get_screeny() // 2), "center", "center")
        display_text.draw(window)
    else:
        top_px = 200 # az adott sor teteje ennyi pixelre van az ablak tetejétől
        for i in range(len(scoreboard)):
            name_text = classes.DisplayItems(arial_20.render(f"{i + 1}.: {scoreboard[i].name}", True, disp.color_black()), (20, top_px), "left", "top")
            record_time = classes.DisplayItems(arial_20.render(f"{scoreboard[i].time // 60}:{scoreboard[i].time % 60:02d}", True, disp.color_black()), (disp.get_screenx() - 20, top_px), "right", "top")
            name_text.draw(window)
            record_time.draw(window)
            top_px += name_text.getsize().height
    back_button.draw(window)

    pygame.display.update()
    
    # eseményhurok
    clock = pygame.time.Clock()
    run = True
    while run:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            sys.exit()
        elif back_button.is_button_left_clicked(event, window):
            run = False
        
        clock.tick(disp.get_fps())
