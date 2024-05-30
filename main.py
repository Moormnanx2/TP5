
import random, arcade, game_state, attack_animation

class MyGame(arcade.Window):
    def __init__ (self):
        self.compy_score = 0
        self.you_score = 0
        self.sprite_list = arcade.SpriteList()
        self.reset_round()
        self.sprite_list.append(arcade.Sprite("compy.png", scale= 2, center_x=650, center_y=350))
        self.sprite_list.append(arcade.Sprite("faceBeard.png", scale= 0.4, center_x=200, center_y=350))
        super().__init__(800, 800, "TP5")
        self.game_state = game_state.GameState.GAME_NOT_STARTED

    def reset_round(self):
        self.paper = attack_animation.AttackAnimation(attack_type=attack_animation.AttackType.PAPER, pos_x=100, pos_y=200)
        self.scissors = attack_animation.AttackAnimation(attack_type=attack_animation.AttackType.SCISSOR, pos_x=200, pos_y=200)
        self.rock = attack_animation.AttackAnimation(attack_type=attack_animation.AttackType.ROCK, pos_x=300, pos_y=200)
        self.compy_attack = attack_animation.AttackAnimation(attack_type=attack_animation.AttackType.COMPUTER, pos_x=650, pos_y=200)
        

        self.update_paper = True
        self.update_scissors = True
        self.update_rock = True
        self.draw_paper = True
        self.draw_scissors = True
        self.draw_rock = True
        self.draw_compy_attack = False
        self.update_compy_attack = False
        self.draw_the_attacks = True
        self.has_chosen_attack = False
        self.chosen_attack = None
        self.computer_attack_type = None
        self.chosen_attack_nbr = -1
        self.pc_attack = -1

    def on_update(self, delta_time):
        if self.game_state == game_state.GameState.ROUND_ACTIVE and self.has_chosen_attack == True:
            if self.compy_attack.nbr_swaps == 6:
                self.update_compy_attack = False
            self.pc_attack = random.randint(0, 2)
            if self.pc_attack == 0:
                self.computer_attack_type = attack_animation.AttackType.PAPER
            elif self.pc_attack == 1:
                self.computer_attack_type = attack_animation.AttackType.SCISSOR
            else:
                self.computer_attack_type = attack_animation.AttackType.ROCK
            
            
            self.game_state = game_state.GameState.ROUND_DONE
            self.game_result()
            


    def game_result(self):
        if self.game_state == game_state.GameState.ROUND_DONE:
            
            if self.chosen_attack_nbr == self.pc_attack:
                pass
            elif self.chosen_attack_nbr == 0 and self.pc_attack == 1:
                self.compy_score +=1
                if self.compy_score == 3:
                    self.game_state = game_state.GameState.GAME_OVER
                    
            elif self.chosen_attack_nbr == 0 and self.pc_attack == 2:
                self.you_score +=1
                if self.you_score == 3:
                    self.game_state = game_state.GameState.GAME_OVER
                    
            elif self.chosen_attack_nbr == 1 and self.pc_attack == 0:
                self.you_score +=1
                if self.you_score == 3:
                    self.game_state = game_state.GameState.GAME_OVER
                    
            elif self.chosen_attack_nbr == 1 and self.pc_attack == 2:
                self.compy_score +=1
                if self.compy_score == 3:
                    self.game_state = game_state.GameState.GAME_OVER

            elif self.chosen_attack_nbr == 2 and self.pc_attack == 0:
                self.compy_score +=1
                if self.compy_score == 3:
                    self.game_state = game_state.GameState.GAME_OVER

            elif self.chosen_attack_nbr == 2 and self.pc_attack == 1:
                self.you_score +=1
                if self.you_score == 3:
                    self.game_state = game_state.GameState.GAME_OVER



                


    def draw_attacks(self):
        if self.update_paper: self.paper.on_update()
        if self.update_scissors: self.scissors.on_update()
        if self.update_rock: self.rock.on_update()
        if self.draw_paper: self.paper.draw()
        if self.draw_scissors: self.scissors.draw()
        if self.draw_rock: self.rock.draw()
        if self.computer_attack_type == attack_animation.AttackType.PAPER:
            paper = arcade.Sprite("spaper.png", center_x=650, center_y=200)
            paper.draw()
        elif self.computer_attack_type == attack_animation.AttackType.SCISSOR:
            scissor = arcade.Sprite("scissors.png", center_x=650, center_y=200)
            scissor.draw()
        elif self.computer_attack_type == attack_animation.AttackType.ROCK: 
            rock = arcade.Sprite("srock.png", center_x=650, center_y=200)
            rock.draw()
      
        
    
    def on_key_press(self, symbol, key_modifiers):
        if symbol == 32 and self.game_state == game_state.GameState.GAME_NOT_STARTED:
            self.game_state = game_state.GameState.ROUND_ACTIVE
        if symbol == 32 and self.game_state == game_state.GameState.ROUND_DONE:
            self.reset_round()
            self.game_state = game_state.GameState.ROUND_ACTIVE
        if symbol == 32 and self.game_state == game_state.GameState.GAME_OVER:
            self.you_score = 0
            self.compy_score = 0
            self.reset_round()
            self.game_state = game_state.GameState.ROUND_ACTIVE

    def on_mouse_press(self, x, y, button, modifiers):
        if self.has_chosen_attack == False and self.game_state == game_state.GameState.ROUND_ACTIVE and (self.paper.collides_with_point((x,y)) or self.scissors.collides_with_point((x,y)) or self.rock.collides_with_point((x,y))):
            self.has_chosen_attack = True
            if self.paper.collides_with_point((x,y)): 
                self.draw_rock = False
                self.draw_scissors = False
                self.update_paper = False
                self.chosen_attack = attack_animation.AttackType.PAPER
                self.chosen_attack_nbr = 0
            if self.scissors.collides_with_point((x,y)): 
                self.draw_rock = False
                self.draw_paper = False
                self.update_scissors = False
                self.chosen_attack = attack_animation.AttackType.SCISSOR
                self.chosen_attack_nbr = 1
            if self.rock.collides_with_point((x,y)): 
                self.draw_scissors = False
                self.draw_paper = False
                self.update_rock = False
                self.chosen_attack = attack_animation.AttackType.ROCK
                self.chosen_attack_nbr = 2
            self.draw_compy_attack = True
            self.update_compy_attack = True
            
            

    def draw_immobile_images(self):
        arcade.draw_rectangle_outline(center_x= 100, center_y= 200, width=75, height=75, color=arcade.color.BLACK)
        arcade.draw_rectangle_outline(center_x= 200, center_y= 200, width=75, height=75, color=arcade.color.BLACK)
        arcade.draw_rectangle_outline(center_x= 300, center_y= 200, width=75, height=75, color=arcade.color.BLACK)
        arcade.draw_rectangle_outline(center_x= 650, center_y= 200, width=75, height=75, color=arcade.color.BLACK)
        arcade.draw_text("Pointage usager: "+str(self.you_score), start_x=-200, start_y=120, color=arcade.color.BLACK, font_size=17, align="center", width=800, font_name="calibri")
        arcade.draw_text("Pointage ordinateur: "+str(self.compy_score), start_x=250, start_y=120, color=arcade.color.BLACK, font_size=17, align="center", width=800, font_name="calibri")
        self.sprite_list.draw()
        


    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.AFRICAN_VIOLET)
        if self.game_state == game_state.GameState.GAME_NOT_STARTED:
            arcade.draw_text("Roche Papier Ciseaux", start_x=0, start_y=700, color=arcade.color.BLACK, font_size=40, align="center", width=800)
            arcade.draw_text("Appuyez sur 'ESPACE' pour commencer.", start_x=0, start_y=600, color=arcade.color.BLACK, font_size=20, align="center", width=800, font_name="calibri")
        if self.game_state == game_state.GameState.ROUND_ACTIVE:
            self.draw_immobile_images()
            arcade.draw_text("Roche Papier Ciseaux", start_x=0, start_y=700, color=arcade.color.BLACK, font_size=40, align="center", width=800)
            arcade.draw_text("Appuyez sur une image pour faire une attaque.", start_x=0, start_y=600, color=arcade.color.BLACK, font_size=20, align="center", width=800, font_name="calibri")
            if self.draw_the_attacks: self.draw_attacks()
        if self.game_state == game_state.GameState.ROUND_DONE:
            arcade.draw_text("Roche Papier Ciseaux", start_x=0, start_y=700, color=arcade.color.BLACK, font_size=40, align="center", width=800)
            arcade.draw_text("Résultats...", start_x=0, start_y=600, color=arcade.color.BLACK, font_size=20, align="center", width=800, font_name="calibri")
            #print(self.compy_score)
            #print(self.you_score)
            self.draw_attacks()
            self.draw_immobile_images()
        if self.game_state == game_state.GameState.GAME_OVER:
            if self.compy_score == 3:
                arcade.draw_text("Roche Papier Ciseaux", start_x=0, start_y=700, color=arcade.color.BLACK, font_size=40, align="center", width=800)
                arcade.draw_text("L'ordinateur gagne!", start_x=0, start_y=600, color=arcade.color.BLACK, font_size=30, align="center", width=800, font_name="Times")
                self.list_compy = arcade.SpriteList()
                self.list_compy.append(arcade.Sprite("compy.png", scale= 4, center_x=400, center_y=350))
                self.list_compy.draw()
                arcade.draw_text("Appuyez sur 'ESPACE' pour recommencer.", start_x=0, start_y=500, color=arcade.color.BLACK, font_size=20, align="center", width=800, font_name="calibri")
                


            if self.you_score == 3:
                arcade.draw_text("Roche Papier Ciseaux", start_x=0, start_y=700, color=arcade.color.BLACK, font_size=40, align="center", width=800)
                arcade.draw_text("Tu gagne!", start_x=0, start_y=600, color=arcade.color.BLACK, font_size=30, align="center", width=800, font_name="Times")
                self.list_you = arcade.SpriteList()
                self.list_you.append(arcade.Sprite("faceBeard.png", scale= 0.8, center_x=400, center_y=350))
                self.list_you.draw()
                arcade.draw_text("Appuyez sur 'ESPACE' pour recommencer.", start_x=0, start_y=500, color=arcade.color.BLACK, font_size=20, align="center", width=800, font_name="calibri")
                 
                
                



                



def main():
    mygame = MyGame()
    mygame.on_draw()
    arcade.run()

main()




