from config import *
import pygame as pg

class Button():
    """Button with different textures when Idle, Hovered Over, or Pressed.

    In order for the button to work as intended, the following must be done in the game loop:
    - Include the button in `listener_mouse_button` to make sure all mouse button events are handled by the button
    - Similary, removing the button from `listener_mouse_button` effectively disables the button
    """
    IDLE = 0
    HOVER = 1
    PRESSED = 2

    def __init__(self, imgs, offset=(0, 0), funcs=None, on_surface=None, surface_abs_pos=(0, 0), *, center=False):
        """Creates a Button object at `offset` on `on_surface` that executes `func` when clicked.
    
        Args:
            imgs (Tuple[pg.Surface] | Tuple[str] | pg.Surface | str):
                Tuple of 3 surfaces - (Idle, Hover, Pressed) Hover/Pressed can be None (to auto-generate)
                Can also be paths (str) to images, the tuple will be auto-generated
            offset ((int, int)): (x, y) offset from top-left of `on_surface` (x, y) will be the top-left of the button, unless `centre=True`
            funcs (function | Dict[int:function]):
                The callback function, MUST accept exactly 1 argument (the instance of the button that called it)
                Triggered by default when a button is left-clicked,
                To override / multiple functions, use a dictionary with KEY being button num, VAL being function
            on_surface (pg.Surface): The surface to render the button on (default to the game display surface)
            surface_abs_pos ((int, int)): (x, y) absolute coordinate of `on_surface`, used for calculation of mouse coordinates

            centre (bool): True to set `offset` (x, y) to mean the centre of the button (instead of top-left)
        
        Examples:
            - Create a button with top-left at (100, 100) of the screen, calls `my_func` with `self` when left-clicked
                - Provide all images as paths  
                    - `button1 = Button(("idle.png", "hover.png", "pressed.png"), (100, 100), my_func)`
                - Hover and Pressed images can be None (will be auto-generated by darkening)
                    - `button1 = Button(("idle.png", None, "pressed.png"), (100, 100), my_func)`
                - If only Idle image provided, can pass without a Tuple
                    - `button1 = Button("idle.png", (100, 100), my_func)`
                - Pygame Surfaces can be passed directly instead of paths
                    - `button1 = Button((surface1, surface2, surface3), (100, 100), my_func)`

            - Create a button with it's centre at (100, 100)
                - `button1 = Button("idle.png", (100, 100), my_func, center=True)`

            - Button that runs `func_L(self)` when left-clicked and `func_R(self)` when right-clicked
                - `button1 = Button("idle.png", (100, 100), {1: func_L, 3: func_R})`
        """

        # Initialise imgs
        self.imgs = self.to_surface_none_list(imgs)  # Get self.imgs containing [Surface/None, Surface/None, Surface/None]
        self.imgs = self.complete_imgs(self.imgs)  # We have self.imgs containing [Surface, Surface, Surface]

        # If no on_surface specified, we will default to the button being blitted onto the game screen
        if on_surface is None:
            on_surface = pg.display.get_surface()
        self.on_surface = on_surface
        self.on_surface_abs_pos = surface_abs_pos
        
        if center:
            self.rect = self.imgs[self.IDLE].get_rect(center=offset)
        else:
            self.rect = self.imgs[self.IDLE].get_rect(topleft=offset)

        # Initialise funcs
        if funcs is None:   # If no trigger specified, "Clicked <Button>" function will be assigned
            funcs = lambda x: print("Clicked", x)
        if callable(funcs): # Create the function dictionary if only given a function (more specifically a callable)
            funcs = {1: funcs}  # Defaults to a left-click triggered button
        elif not isinstance(funcs, dict):   # Error check
            raise TypeError("funcs not a function or dictionary of functions!")
        assert all(isinstance(k, int) for k in funcs), "Dictionary keys should be int mouse buttons"
        self.funcs = funcs

        self.await_release = None   # The button that is currently awaiting release
        self._img_ind = self.IDLE   # The button's image state is based on this

    def _on_mouse_button(self, event):
        """Updates button status based on mouse
        
        Called with just mouse position to check for hovering
        Can also be called with a MOUSEBUTTONUP or MOUSEBUTTONDOWN event for handling
        """
        # We need the mouse's relative position to on_surface to check if it's hovering over the button
        abs_pos = event.pos
        rel_pos = (abs_pos[0] - self.on_surface_abs_pos[0], abs_pos[1] - self.on_surface_abs_pos[1])

        # Mouse Button Event while outside button, we just reset
        if not self.rect.collidepoint(rel_pos):
            self._img_ind = self.IDLE
            self.await_release = None
            return False

        # Hovering over button
        if event.type == pg.MOUSEBUTTONDOWN:
            self._img_ind = self.PRESSED
            self.await_release = event.button
        elif event.type == pg.MOUSEBUTTONUP:
            if self.await_release == event.button:  # Button only triggers if the mouse button has been held
                self._img_ind = self.IDLE
                if event.button in self.funcs:
                    self.funcs[event.button](self)  # Class the attached Callback function with self
            self.await_release = None
        return True
        
    def hover_check(self):
        """Checks if this button is currently being hovered on, then assigned the appropriate img"""
        abs_pos = pg.mouse.get_pos()
        rel_pos = (abs_pos[0] - self.on_surface_abs_pos[0], abs_pos[1] - self.on_surface_abs_pos[1])

        if self.rect.collidepoint(rel_pos): # Hovering over button
            if not self.await_release:      # Only goes back to HOVER state if it's not being pressed
                self._img_ind = self.HOVER
        else:
            self._img_ind = self.IDLE

    def draw(self):
        """Blits the button onto it's on_surface
        
        Always call `check_mouse` before this to make sure the correct button state is drawn
        """
        self.hover_check()
        self.on_surface.blit(self.imgs[self._img_ind], self.rect)

    @staticmethod
    def to_surface_none_list(imgs):
        """Returns a List of Surfaces/None (Idle, Hover, Pressed)
        
        Accepts `imgs` as either a Surface, a Path (str), a Tuple of Surfaces/Paths/None
        """
        # Create an Tuple if surfaces not given in a Tuple
        if isinstance(imgs, str):
            imgs = (imgs,)
        try:
            iter(imgs)
        except TypeError:
            imgs = (imgs,)

        res = [None, None, None]
        try:
            for i, img in enumerate(imgs):
                if isinstance(img, str):    # User provided a path instead of surface
                    img = pg.image.load(img).convert_alpha()
                elif not (isinstance(img, pg.Surface) or img is None):
                    raise TypeError("Button img not a pg.Surface or Path (str)", imgs)
                res[i] = img
        except IndexError:
            raise Exception("Too many images, only 3 required (Idle, Hover, Pressed)")
        # We have res containing [Surface/None, Surface/None, Surface/None]
        return res

    @staticmethod
    def complete_imgs(surface_none_list):
        """Returns a List of pg.Surface, where all None imgs[i] is replaced with a darker version of imgs[i-1]

        imgs can contain pg.Surface / None
        imgs[0] must be a pg.Surface and not None
        Intended to be used to generate hover/pressed pg.Surface for Buttons
        """
        complete_imgs = list(surface_none_list)
        if complete_imgs[0] is None:
            raise Exception("Idle Button Img not provided")
        for i in range(1, len(complete_imgs)):
            if complete_imgs[i] is None:
                complete_imgs[i] = complete_imgs[i-1].copy()
                complete_imgs[i].fill((20, 20, 20), special_flags=pg.BLEND_SUB)
        return complete_imgs


class CellButtonStyle():
    """Needs to be provided to `CellButton` to stylize the Buttons
    
    Attributes:
        normal_button_imgs ([pg.Surface, pg.Surface, pg.Surface]): The list of [Idle, Hover, Pressed] Surfaces for the Normal Button
        flag_button_imgs ([pg.Surface, pg.Surface, pg.Surface]): The list of [Idle, Hover, Pressed] Surfaces for the Flagged Button
        mine_img (pg.Surface): The surface for the Mine's image
        num_imgs ([pg.Surface, pg.Surface, ...]): The list of surfaces for the numbers. Where num_imgs[i] = Surface for i, (i = 0 to 8)
    """
    def __init__(self, normal_button_imgs, flag_img, mine_img, num_imgs_dir):
        """
        CellButtonStyle objects have attributes that aids in creating the various Buttons
        
        Args:
            normal_button_imgs (List[pg.Surface] | List[str] | pg.Surface | str): (Idle, Hover, Pressed) Surfaces/Paths, can contain `None`
            flag_img (str | Pygame.Surface):  The Flag Img that will be overlayed on top of the button
            mine_img (str | Pygame.Surface):  The Mine Img that will be overlayed on top of the button
            num_imgs_dir (str): (eg. "assets/cell/"), the directory to find the files 0.png, 1.png, ...
        """
        # Create the (Idle, Hover, Pressed) Surfaces for Normal Buttons
        normal_button_imgs = Button.to_surface_none_list(normal_button_imgs)
        normal_button_imgs = Button.complete_imgs(normal_button_imgs)

        if isinstance(flag_img, str):
            flag_img = pg.image.load(flag_img)
        flag_img = flag_img.convert_alpha()
        assert isinstance(flag_img, pg.Surface)

        if isinstance(mine_img, str):
            mine_img = pg.image.load(mine_img)
        mine_img = mine_img.convert_alpha()
        assert isinstance(mine_img, pg.Surface)

        # Create the (Idle, Hover, Pressed) Surfaces for Flag Buttons
        flag_button_imgs = [None, None, None]
        for i, normal_img in enumerate(normal_button_imgs):
            flag_button_imgs[i] = normal_img.copy() # Flag Button Imgs are generated by overlaying the flag over Normal Imgs
            flag_button_imgs[i].blit(flag_img, (0,0))
        # Now flag_imgs = [Surface, Surface, Surface]

        # Numbers will be images stored as 0.png, 1.png, ... in num_imgs_dir (eg. assets/cell/)
        num_imgs = [pg.image.load(num_imgs_dir + f"{i}.png").convert_alpha() for i in range(9)]
        # Now nums_imgs = [Surface for 0, Surface for 1, ...]

        self.normal_button_imgs = normal_button_imgs
        self.flag_button_imgs = flag_button_imgs
        self.mine_img = mine_img
        self.num_imgs = num_imgs

class CellButton():
    """A CellButton is made up of 3 Buttons (Normal, Flagged, Revealed)
    
    Attributes:
        normal_button (Button): The `Button` that is activated by default
        flagged_button (Button): The `Button` that is activated when cell is flagged
        revealed_button (Button): The `Button` that is activated when cell is exposed
        
        active_button (Button): The `Button` that is currently activated
    """
    def __init__(self, cell, style):
        """
        Creates a CellButton that is associated with a Cell

        A CellButton is made up of 3 `Button`s (Normal, Flagged, Revealed),
        but only 1 is active at any 1 time.

        Args:
            cell (Cell)
            style (CellButtonStyle)
        """
        
        normal_button_imgs = style.normal_button_imgs
        flag_button_imgs = style.flag_button_imgs
        if cell.is_mine:
            reveal_button_imgs = (style.mine_img, style.mine_img, style.mine_img)
        else:
            reveal_button_imgs = (style.num_imgs[cell.val], style.num_imgs[cell.val])
        
        row, col = cell.coord
        offset = ((CELLSIZE+GAP)*col, (CELLSIZE+GAP)*row)

        self.normal_button = Button(normal_button_imgs, offset, funcs={1: self.expose, 3: self.flag}, on_surface=cell.minefield.board, surface_abs_pos=cell.minefield.board_abs_pos)
        self.flagged_button = Button(flag_button_imgs, offset, funcs={3: self.flag}, on_surface=cell.minefield.board, surface_abs_pos=cell.minefield.board_abs_pos)
        self.revealed_button = Button(reveal_button_imgs, offset, funcs={1: self.attempt_expose_around}, on_surface=cell.minefield.board, surface_abs_pos=cell.minefield.board_abs_pos)
        self.active_button = self.normal_button

        self.cell = cell

    def expose(self, _):
        self.cell.expose()

    def flag(self, _):
        self.cell.flag()

    def attempt_expose_around(self, _):
        self.cell.expose_around()

    def _on_mouse_button(self, event):
        self.active_button._on_mouse_button(event)

    def draw(self):
        cell = self.cell
        if cell.is_exposed:
            self.active_button = self.revealed_button
        elif cell.is_flagged:
            self.active_button = self.flagged_button
        else:
            self.active_button = self.normal_button
        self.active_button.draw()