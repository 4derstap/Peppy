# Copyright 2016-2017 Peppy Player peppy.player@gmail.com
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

from ui.menu.menu import Menu
from ui.factory import Factory
from util.keys import CURRENT, KEY_SCREENSAVER, KEY_SCREENSAVER_DELAY, ORDER_SCREENSAVER_DELAY_MENU

class SaverDelayMenu(Menu):
    """ Screensaver Delay Menu class. Extends base Menu class """
    
    def __init__(self, util, bgr=None, bounding_box=None):
        """ Initializer
        
        :param util: utility object
        :param bgr: menu background
        :param bounding_box: bounding box
        """
        self.factory = Factory(util)
        m = self.factory.create_saver_delay_menu_button
        Menu.__init__(self, util, bgr, bounding_box, 1, 3, create_item_method=m)
        self.config = util.config
        current_delay_name = self.config[KEY_SCREENSAVER][KEY_SCREENSAVER_DELAY]
        self.delays = util.get_screensaver_delays()
        self.set_items(self.delays, 0, self.change_delay, False, self.config[ORDER_SCREENSAVER_DELAY_MENU])
        current_delay = self.delays[current_delay_name]
        self.item_selected(current_delay)
        
    def change_delay(self, state):
        """ Change delay event listener
        
        :param state: button state
        """
        self.config[KEY_SCREENSAVER][KEY_SCREENSAVER_DELAY] = state.name        
        self.notify_listeners(state)
        