from dataclasses import dataclass
from copy import deepcopy
import pygame as pg
import random, os, io, requests
os.environ["SDL_AUDIODRIVER"] = "dummy"
pg.init()
def get_image(url: str) -> pg.surface.Surface:
    return pg.image.load(io.BytesIO(requests.get(url, stream=True).content))
RCS = {"LOGO": get_image("https://codehs.com/uploads/1ba906464685a4b47d94ce59a0b62c3a"),
                   "LOGOTEXT": get_image("https://codehs.com/uploads/96b8568b78f4fcae1f76ca9ae2efe3f7"),
                   "MENUICON": get_image("https://codehs.com/uploads/a631c25c3cfeedc54cbcefa3cbce665c"),
                   "CLOSEAPP": get_image("https://codehs.com/uploads/4c93a70e584949208c0f37927f16de3e"),
                   "BG": pg.transform.scale(get_image("https://codehs.com/uploads/e6c0b6b6bddf7e3675c3ef12d3ca61b2"), (400,400)),
                   "font": pg.font.SysFont(None, 24)
}
@dataclass
class DietaryRestrictions:
    vegan: bool
    iron_rich: bool
    egg: bool
    nuts: bool
    dairy: bool
    meat: bool
    low_sugar: bool
    high_fiber: bool
    gluten_free: bool
    max_cal: bool
    budget: int
    meals: int
    special_occasion: bool
    
    def is_meal_compatible(self, meal, calorie_limit, allotted_money) -> bool:
        # Using comparing to make things concise
        return not(self.vegan > meal['vegan'] #If you are vegan, but meal is not
                    or self.iron_rich > meal['iron_rich'] #If you need iron, but meal doesn't have
                    or self.egg < meal['has_egg'] #If you can't eat egg, but meal has
                    or self.nuts < meal['has_nuts'] #If you can't eat nuts, but meal has
                    or self.dairy < meal['has_dairy'] #If you can't eat dairy, but meal has'
                    or self.meat < meal['has_meat'] #If you can't eat meat, but meal has
                    or self.low_sugar == meal['high_sugar'] == 1 #If you don't want a lot of sugar, but meal has 
                    or self.high_fiber > meal['high_fibre'] #If you need fiber, but meal doesn't have
                    or self.gluten_free > meal['gluten_free'] #If you can't eat gluten, but meal has
                    or calorie_limit < meal['calories'] #If the meal is too many calories
                    or allotted_money < meal['cost'] #If meal is too expensive
                    )
    #Get a meal given parameters
    def get_meal(self, meal: dict, amount_allotted: float, num_items: int):
        # self -> The dietary info
        # meal -> The food options read from the json
        # amount_allotted -> The factor deciding how much of the budget and calories can be used per meal
        # num_items -> The amount of items eaten at the meal
        if amount_allotted == 0.40:
            print(meal)
        cal_lim = self.max_cal * amount_allotted // num_items
        print("CALLIM",cal_lim)
        money_lim = self.budget * amount_allotted // num_items
        options = list(filter(lambda i: self.is_meal_compatible(i[1], cal_lim, money_lim), meal.items()))
        if amount_allotted == 0.40:
            print(options)
        try:
            try:
                chosen_options = random.sample(options, num_items)
            except:
                chosen_options = deepcopy(options)
                while len(chosen_options) < num_items:
                    chosen_options.append(random.choice(options))
        except:
            return []
        return chosen_options
        
    def get_foods(self, breakfast: dict, lunch: dict, dinner: dict, grander_food:dict):
        # self -> The dietary info
        meals_list = {"breakfast":None, "lunch":None, "dinner":None, "grand":None}
        if self.meals == 3: #Only have breakfast if having 3 meals
           print("BREAKFAST")
           meals_list["breakfast"] = self.get_meal(breakfast, 0.25, 1)
           print("*********************\n\n\n")
        if self.meals >= 2: #Have lunch if having 2 or 3 meals
            print("LUNCH")
            meals_list["lunch"] = self.get_meal(lunch, 0.35, 2)
            print("*********************\n\n\n")
        if self.meals > 0 and not self.special_occasion: # Have dinner if eating that day
            print("DINNER")
            meals_list["dinner"] = self.get_meal(dinner, 0.40, 3)
            if not meals_list["dinner"]:
                meals_list["dinner"] = self.get_meal(dinner, 0.40, 2)
            if not meals_list["dinner"]:
                meals_list["dinner"] = self.get_meal(dinner, 0.40, 1)
            if not meals_list["dinner"]:
                meals_list["dinner"] = result
            
            print("*********************\n\n\n")
        elif self.meals > 0 and self.special_occasion: # Have grand food for an occasion
            print("GRANDER")
            #TODO: Calorie counting here
            meals_list["grand"] = self.get_meal(grander_food, 0.50, 1)
            print("*********************\n\n\n")
        else:
            print("Good Job! Not eating today!")
            print("*********************\n\n\n")
        
        return meals_list

class Mealy:
    def __init__(self):
        pg.init()
        self.dimensions = (400, 400)
        self.surface = pg.display.set_mode(self.dimensions, pg.HWSURFACE | pg.DOUBLEBUF)
        self.effects_surf = pg.surface.Surface(self.dimensions, pg.SRCALPHA)
        self.is_running = True
        self.scene_locals = {"scale_factor": 0.5, "scale_change": -0.005, "progress": 0} #Change to ZERO
        self.transition_fade = 0
        self.scene = "loading"
        self.clock = pg.time.Clock()
        self.close_icon = pg.transform.scale(RCS["CLOSEAPP"], (30,30))
        self.menu = False
    def logic(self):
        #Get mouse status
        mp = pg.mouse.get_pos()
        mpressed = pg.mouse.get_pressed()
        
        #If quit button, quit
        if mp[0] >= 370 and mp[1] <= 30 and mpressed[0]:
            quit()
            
        #If menu button, open menu
        if self.scene == "main_app":
            if mp[0] <= 60 and mp[1] <= 45 and mpressed[0] and not self.scene_locals["menu_mouse_release_wait"]:
                self.scene_locals["menu_mouse_release_wait"] = True
            elif mp[0] <= 60 and mp[1] <= 45 and not mpressed[0] and self.scene_locals["menu_mouse_release_wait"]:
                self.scene_locals["menu_mouse_release_wait"] = False
                self.menu = not self.menu
            
        
        
        
        
    def render(self):
        if self.scene == "loading":
            
            #Do the calculations for bouncing logo
            self.scene_locals['scale_factor'] += self.scene_locals['scale_change']
            if self.scene_locals['scale_factor'] < 0.4 or self.scene_locals['scale_factor'] > 0.6:
                self.scene_locals['scale_change'] *= -1
            
            #Draw Background
            self.surface.blit(RCS['BG'], (0,0))
            
            #Draw Text Logo
            self.surface.blit(RCS["LOGOTEXT"], (102 , 5))
            
            #Use scale calculations to create scaled copy of bouncing logo surface
            #   This creates bouncing effect
            image = pg.transform.scale_by(RCS["LOGO"], self.scene_locals['scale_factor'])
            
            #Draw bouncing logo centered horizontally
            self.surface.blit(image, (200 - (171 * self.scene_locals['scale_factor']) , 225 - (146 * self.scene_locals['scale_factor'])))
            
            #Draw Progress
            pg.draw.rect(self.surface, (25, 25, 25), (75, 330, 250, 30))
            pg.draw.rect(self.surface, (0, 143, 190), (75, 330, min(2.5 * self.scene_locals['progress'], 250), 30))
            
            #Fake Loading Effect
            if self.scene_locals['progress'] < 100:
                self.scene_locals['progress'] += (random.random() / random.randint(1, 6))
            #Activate Fade
            elif self.transition_fade < 255:
                self.transition_fade += 5
                self.effects_surf.fill((0,0,0, min(self.transition_fade, 255)))
            #Switch to next scene
            else:
                self.transition_fade = 255
                self.scene = "main_app"
                self.scene_locals = {"logotext_cache": pg.transform.scale_by(RCS["LOGOTEXT"], 0.3), "menu_mouse_release_wait": False}
            self.surface.blit(self.effects_surf, (0,0))
            
        if self.scene == "main_app":
            #Draw background
            self.surface.blit(RCS['BG'], (0,0))
            pg.draw.rect(self.surface, (255, 255, 150), (0, 0, 400, 45))
            if self.menu:
                pg.draw.rect(self.surface, (255, 255, 180), (0, 0, 250, 400))
                self.surface.blit(RCS['font'].render('Vegan?', True, (0,0,0)), (20, 50))
                self.surface.blit(RCS['font'].render('Can have egg?', True, (0,0,0)), (20, 80))
                self.surface.blit(RCS['font'].render('Should food be iron rich?', True, (0,0,0)), (20, 110))
                self.surface.blit(RCS['font'].render('Can have nuts?', True, (0,0,0)), (20, 140))
                self.surface.blit(RCS['font'].render('Can have dairy?', True, (0,0,0)), (20, 170))
                self.surface.blit(RCS['font'].render('Can have meat?', True, (0,0,0)), (20, 200))
                self.surface.blit(RCS['font'].render('Higher sugar okay?', True, (0,0,0)), (20, 230))
                self.surface.blit(RCS['font'].render('High fiber needed?', True, (0,0,0)), (20, 260))
                self.surface.blit(RCS['font'].render('Must be gluten-free?', True, (0,0,0)), (20, 290))
                self.surface.blit(RCS['font'].render('Maximum calories:', True, (0,0,0)), (20, 320))
                self.surface.blit(RCS['font'].render('Budget:', True, (0,0,0)), (20, 350))
                self.surface.blit(RCS['font'].render('Special Occasion?', True, (0,0,0)), (20, 380))
                
            self.surface.blit(RCS["MENUICON"], (10, -2))
            self.surface.blit(self.scene_locals["logotext_cache"], (65, 6))
            #Bring fade back in
            if self.transition_fade > 0:
                self.effects_surf.fill((0,0,0, max(0, self.transition_fade)))
                self.transition_fade -= 3
                self.surface.blit(self.effects_surf, (0,0))
            
        
        pg.draw.rect(self.surface, (220, 0, 0), (370, 0, 30, 30))
        self.surface.blit(self.close_icon, (370, 0))

    def handle_event(self, e):
        if e.type == pg.QUIT:
            self.is_running = False

    def run(self):
        while self.is_running:
            for event in pg.event.get():
                self.handle_event(event)
            self.logic()
            self.render()
            pg.display.flip()
            self.clock.tick(60)
        pg.quit()
