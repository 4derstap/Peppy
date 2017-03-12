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

import time
import math
import pygame

from threading import Thread

class CircularAnimator(Thread):
    """ Provides needle circular animation in a separate thread """
    
    def __init__(self, channel, component, base, ui_refresh_period, needle_rects):
        """ Initializer
        
        :param channel: number of channels
        :param component: UI component
        :param base: meter base
        :param ui_refresh_period: animation interval 
        :param needle_rects: list of sprite rectangles
        """
        Thread.__init__(self)             
        self.channel = channel
        self.component = component
        self.run_flag = True
        self.base = base
        self.ui_refresh_period = ui_refresh_period
        self.previous_index = 0
        self.needle_rects = needle_rects
        self.mask = None
        if base.rect.w != base.meter_bounding_box.x:
            mask_w = 130
            mask_h = 52
            mask_x = base.rect.w/2 - mask_w/2
            mask_y = base.rect.h - (base.rect.h - base.meter_bounding_box.h)/2        
            self.mask = pygame.Rect(mask_x, mask_y, mask_w, mask_h)
        
    def run(self):
        """ Thread method. Converts volume value into the needle angle and displays corresponding sprite. """
        
        while self.run_flag:            
            volume = self.channel.get()            
            self.channel.task_done()
            n = (volume * self.base.max_volume * self.base.incr) / 100.0
            if n >= len(self.base.needle_sprites): n = len(self.base.needle_sprites) - 1
            
            if self.previous_index == int(n):
                time.sleep(self.ui_refresh_period)
                continue
            
            diff = n - self.previous_index
            sub_steps = range(int(abs(diff)) * self.base.steps_per_degree)
            sign = int(math.copysign(1, diff))
            for m in sub_steps:
                if not self.run_flag:
                    break
                
                previous_rect = self.component.bounding_box
                self.base.draw_bgr_fgr(previous_rect, self.base.bgr)  
                next_index = (self.previous_index * self.base.steps_per_degree) + (m * sign)
                if next_index >= len(self.base.needle_sprites): next_index = len(self.base.needle_sprites) - 1
                
                sprite = self.base.needle_sprites[next_index]
                self.component.content = ("", sprite)
                r = self.needle_rects[next_index]
                self.component.content_x = r.x
                self.component.content_y = r.y
                r.x = 0
                r.y = 0
                self.component.bounding_box = r
                self.component.draw()
                r.x = self.component.content_x
                r.y = self.component.content_y

                a = previous_rect.union(r)
                if self.base.fgr:
                    self.base.draw_bgr_fgr(a, self.base.fgr)
                
                if self.mask:
                    pygame.draw.rect(self.component.screen, (0, 0, 0), self.mask)
                    a = a.union(self.mask)
                    
                self.base.update_rectangle(a)
                time.sleep(self.ui_refresh_period)
            self.previous_index = int(n)
