import pygame
import math

class DayNightCycle:
    def __init__(self, screen):
        self.screen = screen
        self.time = 0  # 0 to 2π represents a full day
        self.day_duration = 60  # seconds for a full day cycle
        
        # Colors for different times of day
        self.day_sky = (20, 80, 140)  # Blue
        self.night_sky = (10, 10, 30)  # Dark blue
        self.sunset_sky = (255, 165, 0)  # Orange
        
        # Celestial body properties
        self.sun_img = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.sun_img, (255, 255, 0), (15, 15), 15)  # Yellow sun
        self.moon_img = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.moon_img, (200, 200, 200), (15, 15), 15)  # Gray moon
        
    def update(self, dt):
        # Update time (0 to 2π)
        self.time = (self.time + (2 * math.pi * dt / self.day_duration)) % (2 * math.pi)
        
    def lerp_color(self, color1, color2, t):
        """Linear interpolation between two colors"""
        return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))
        
    def get_sky_color(self):
        # Define transition periods
        morning_start = 0
        morning_end = math.pi/2
        sunset_start = math.pi/2
        sunset_end = math.pi
        night_start = math.pi
        night_end = 3*math.pi/2
        sunrise_start = 3*math.pi/2
        sunrise_end = 2*math.pi
        
        # Calculate transition progress (0 to 1)
        if morning_start <= self.time < morning_end:
            # Morning transition (night to day)
            progress = (self.time - morning_start) / (morning_end - morning_start)
            return self.lerp_color(self.night_sky, self.day_sky, progress)
        elif sunset_start <= self.time < sunset_end:
            # Sunset transition (day to night)
            progress = (self.time - sunset_start) / (sunset_end - sunset_start)
            return self.lerp_color(self.day_sky, self.night_sky, progress)
        elif night_start <= self.time < night_end:
            # Night transition (sunset to night)
            progress = (self.time - night_start) / (night_end - night_start)
            return self.lerp_color(self.sunset_sky, self.night_sky, progress)
        else:
            # Sunrise transition (night to day)
            progress = (self.time - sunrise_start) / (sunrise_end - sunrise_start)
            return self.lerp_color(self.night_sky, self.sunset_sky, progress)
            
    def draw(self):
        # Draw sky
        self.screen.fill(self.get_sky_color())
        
        # Calculate celestial body position
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2
        radius = min(self.screen.get_width(), self.screen.get_height()) // 3
        
        # Calculate position based on time
        x = center_x + radius * math.cos(self.time)
        y = center_y - radius * math.sin(self.time)
        
        # Draw sun or moon based on time
        if 0 <= self.time < math.pi:  # Day
            self.screen.blit(self.sun_img, (x - 15, y - 15))
        else:  # Night
            self.screen.blit(self.moon_img, (x - 15, y - 15)) 