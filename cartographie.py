import turtle

# Configuration de l'écran
screen = turtle.Screen()
screen.title("Simulation de cartographie en temps réel")
screen.bgcolor("white")
screen.setup(width=600, height=600)

# Création des limites de la pièce
walls = turtle.Turtle()
walls.penup()
walls.goto(-250, -250)
walls.pendown()
walls.pensize(3)
for i in range(4):
    walls.forward(500)
    walls.left(90)
walls.hideturtle()

# Création du robot (turtle mobile)
robot = turtle.Turtle()
robot.shape("circle")
robot.color("blue")
robot.penup()
robot.speed(1)

# Création du traceur de carte
map_drawer = turtle.Turtle()
map_drawer.shape("square")
map_drawer.color("gray")
map_drawer.penup()
map_drawer.hideturtle()

# Liste des obstacles (coordonnées x, y)
obstacles = [(-100, 100), (50, -50), (150, 150), (-150, -100)]

# Dessin des obstacles sur la carte
obstacle_drawer = turtle.Turtle()
obstacle_drawer.shape("square")
obstacle_drawer.color("red")
obstacle_drawer.penup()
for obs in obstacles:
    obstacle_drawer.goto(obs)
    obstacle_drawer.stamp()
obstacle_drawer.hideturtle()

# Liste des positions explorées
explored_positions = set()

# Vérifie si le robot rencontre un obstacle
def is_collision(x, y):
    for obs in obstacles:
        if abs(x - obs[0]) < 20 and abs(y - obs[1]) < 20:
            return True
    return False

# Ajoute une position explorée sur la carte
def update_map(x, y):
    pos = (round(x), round(y))
    if pos not in explored_positions:
        explored_positions.add(pos)
        map_drawer.goto(pos)
        map_drawer.stamp()  # Ajoute une trace sur la carte

# Déplacement du robot avec mise à jour de la carte
def move_right():
    new_x = robot.xcor() + 20
    if new_x < 240 and not is_collision(new_x, robot.ycor()):
        update_map(new_x, robot.ycor())
        robot.setx(new_x)
    else:
        print("Obstacle détecté ou mur atteint !")

def move_left():
    new_x = robot.xcor() - 20
    if new_x > -240 and not is_collision(new_x, robot.ycor()):
        update_map(new_x, robot.ycor())
        robot.setx(new_x)
    else:
        print("Obstacle détecté ou mur atteint !")

def move_up():
    new_y = robot.ycor() + 20
    if new_y < 240 and not is_collision(robot.xcor(), new_y):
        update_map(robot.xcor(), new_y)
        robot.sety(new_y)
    else:
        print("Obstacle détecté ou mur atteint !")

def move_down():
    new_y = robot.ycor() - 20
    if new_y > -240 and not is_collision(robot.xcor(), new_y):
        update_map(robot.xcor(), new_y)
        robot.sety(new_y)
    else:
        print("Obstacle détecté ou mur atteint !")
        
"""
def autonomous():
    droite = True
    gauche = True
    haut = True
    pas_bloque = droite | gauche | haut
    
    pos_rob_x = robot.xcor()
    pos_rob_y = robot.ycor()
    
    while(pas_bloque):
        if pos_rob_x < 240 and not is_collision(pos_rob_x, robot.ycor()): #aller à droite
            pos_rob_x = robot.xcor() + 20
        else:
            droite = False
    
        if pos_rob_x > -240 and not is_collision(pos_rob_x, robot.ycor()): #aller à gauche
            pos_rob_x = robot.xcor() - 20
            update_map(pos_rob_x, robot.ycor())
            robot.setx(pos_rob_x)
    
autonomous()
"""

# Assignation des touches de contrôle
screen.listen()
screen.onkey(move_right, "Right")  # Flèche droite
screen.onkey(move_left, "Left")  # Flèche gauche
screen.onkey(move_up, "Up")  # Flèche haut
screen.onkey(move_down, "Down")  # Flèche bas

screen.mainloop()