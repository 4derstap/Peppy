# Copyright 2020-2021 Peppy Player peppy.player@gmail.com
# 
# This file is part of Peppy Player.
# 
# Peppy Player is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Peppy Player is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Peppy Player. If not, see <http://www.gnu.org/licenses/>.

from ui.menu.multipagemenu import MultiPageMenu
from ui.factory import Factory
from ui.state import State
from util.config import COLOR_DARK, COLORS, HORIZONTAL_LAYOUT, COLOR_MEDIUM, COLOR_BRIGHT, COLOR_CONTRAST, WRAP_LABELS
from ui.layout.gridlayout import GridLayout
from util.keys import TRACK_MENU
from ui.button.button import Button

TRACK_ROWS = 6
TRACK_COLUMNS = 2
TRACKS_PER_PAGE = TRACK_ROWS * TRACK_COLUMNS
LABEL_HEIGHT_PERCENT = 42
PADDING = 5

class CollectionTrackMenu(MultiPageMenu):
    """ Collection tracks menu """
    
    def __init__(self, util, next_page, previous_page, set_title, reset_title, go_to_page, play_track, bgr=None, bounding_box=None):
        """ Initializer
        
        :param util: utility object
        :param next_page: next page callback
        :param previous_page: previous page callback
        :param set_title: set title callback
        :param reset_title: reset title callback
        :param go_to_page: go to page callback
        :param play_track: play track callback
        :param bgr: menu background
        :param bounding_box: bounding box
        """ 
        self.factory = Factory(util)
        self.util = util
        self.next_page = next_page
        self.previous_page = previous_page
        self.bb = bounding_box
        m = self.create_collection_track_menu_button
        h = self.util.config[HORIZONTAL_LAYOUT]
        MultiPageMenu.__init__(self, util, next_page, previous_page, set_title, reset_title, go_to_page, m, TRACK_ROWS, TRACK_COLUMNS, None, bgr, bounding_box, horizontal=h)
        self.config = util.config
        self.play_track = play_track
        self.tracks = None
    
    def create_collection_track_menu_button(self, s, constr, action, show_img=True, show_label=True):
        """ Create Collection Track Menu button

        :param s: button state
        :param constr: scaling constraints
        :param action: button event listener
        :param show_img: True - show button image, False - not
        :param show_label: True - show button label, False - not

        :return: menu button
        """
        s.bounding_box = constr
        s.img_x = None
        s.img_y = None
        s.auto_update = True
        s.show_bgr = True
        s.show_img = show_img
        s.show_label = show_label
        s.source = TRACK_MENU
        s.text_color_normal = self.config[COLORS][COLOR_BRIGHT]
        s.text_color_selected = self.config[COLORS][COLOR_CONTRAST]
        s.text_color_disabled = self.config[COLORS][COLOR_MEDIUM]
        s.text_color_current = s.text_color_normal
        s.wrap_labels = self.config[WRAP_LABELS]

        button = Button(self.util, s)
        button.bgr = self.config[COLORS][COLOR_DARK]
        button.add_release_listener(action)

        return button

    def set_tracks(self, tracks, page):
        """ Set tracks in menu
        
        :param tracks: list of tracks
        :param page: page number
        """
        if tracks == None:
            return
        self.tracks = tracks
        items = {}
        start_index = TRACKS_PER_PAGE * (page - 1)
        end_index = start_index + TRACKS_PER_PAGE
        
        layout = GridLayout(self.bb)
        layout.set_pixel_constraints(TRACK_ROWS, TRACK_COLUMNS, 1, 1)
        constr = layout.get_next_constraints()        
        fixed_height = int((constr.h * LABEL_HEIGHT_PERCENT)/100.0)
         
        for i, a in enumerate(self.tracks[start_index : end_index]):
            state = State()
            state.name = a.file_name
            state.l_name = state.name
            state.bgr = self.config[COLORS][COLOR_DARK]
            state.img_x = None
            state.img_y = None
            state.auto_update = True
            state.show_bgr = True
            state.show_img = False
            state.show_label = True
            state.comparator_item = state.name
            state.index = i
            state.fixed_height = fixed_height
            state.file_name = a.file_name
            state.folder = a.folder
            state.file_name = a.file_name
            state.url = a.url
            state.padding = PADDING
            items[state.name] = state
        self.set_items(items, 0, self.play_track, False)
        
    def select_track(self, state):
        """ Select track on page
        
        :param state: new track state object
        """
        if self.get_selected_item() == None: # navigator selected
            return

        max_index = item_index = 0
        for button in self.buttons.values():
            if button.state.index > max_index:
                max_index = button.state.index
            if button.state.name == state.file_name:
                self.unselect()
                self.select_by_index(button.state.index)
                return
            
        for i, s in enumerate(self.tracks):
            if s.file_name == state.file_name:
                item_index = i
                break
        
        if item_index > max_index:
            self.next_page(state)
        else:
            self.previous_page(state)
        