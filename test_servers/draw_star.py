import turtle

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("white")

# Create a turtle
t = turtle.Turtle()
t.speed(1)

# Draw a filled red star
t.begin_fill()
t.fillcolor("red")
for _ in range(5):
    t.forward(100)
    t.right(144)
t.end_fill()

# Hide the turtle and display
t.hideturtle()
turtle.done()
