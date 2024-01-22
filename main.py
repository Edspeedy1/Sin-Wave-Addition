'''
Eric De Leenheer 100869527
Assignment 3 - Graphing Sine Functions
I did my best not to use any obscure libraries and tried to avoid
"magic numbers" but alas, there is only so much i can do.
Also, I created a window to do all of the inputs which i think looks
a little nicer than the terminal, so i've tried to comment everything
to make the pygame portions easier to read.
I used some map and lambda functions to make the code more compact
though not to the extent of my other one-line projects
'''

# import necessary moduals
import pygame
import matplotlib.pyplot as plt
import numpy as np
pygame.init()   # initialize pygame

# set up the window
SCREEN = pygame.display.set_mode((1200, 800))
COMP_FUNCTION = lambda x: x     # default function, will be changed
SAMPLE_RANGE = 5    # number of periods of sine wave with frequency 1
SAMPLE_FREQUENCY = 0.01  # 100 samples per unit (recommended)
FONT_SIZE = 40


boxList = []    # store input boxes
# class for input boxes
class InputBox:
    # initialize the input box
    def __init__(self, x, y, w, h, index, value=1):
        self.index = index
        self.w = w
        self.x = x
        self.y = y
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)
        self.color = [70,120,150]
        self.text = str(value)
        self.txt_surface = pygame.font.Font(None, h).render(self.text, True, self.color)
        self.active = False
        boxList.append(self)
    
    # takes an event and sees if it collides with the input box
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:    # if it got clicked on
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                if self.active:
                    self.deselect()
            self.color = [70,170,240] if self.active else [70,120,150] # change the color

        if event.type == pygame.KEYDOWN:    # if a key is pressed
            if self.active:                 # and the input box is selected
                if event.key == pygame.K_RETURN:
                    self.deselect()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode  # add the pressed key to the text
                self.txt_surface = pygame.font.Font(None, self.h).render(self.text, True, self.color)   # recreate the text surface

    def deselect(self):
        self.active = False
        self.color = [70,120,150]
    
        # set the sample range
        if self.index == 7:
            global SAMPLE_RANGE
            SAMPLE_RANGE = float(self.text)

        remakeGraphs()

    def update(self):
        width = max(self.w, self.txt_surface.get_width()+10)    # extends the textbox if needed
        self.rect.w = width

    def draw(self, screen):  # Draws inputbox to the screen
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)



def makeFunction(amplitude, frequency, phase):
    # creates a sine wave function with the given parameters
    domain = np.arange(0.0, SAMPLE_RANGE, SAMPLE_FREQUENCY)
    function = amplitude * np.sin(2 * np.pi * frequency * domain + phase)

    return function, domain


def makeComboFunction(amplitude1, frequency1, phase1, amplitude2, frequency2, phase2):
    # exactly the same as the previous function, but with two sine waves
    global COMP_FUNCTION    # also sets the global function
    domain = np.arange(0.0, SAMPLE_RANGE, SAMPLE_FREQUENCY)
    function = amplitude1 * np.sin(2 * np.pi * frequency1 * domain + phase1) + amplitude2 * np.sin(2 * np.pi * frequency2 * domain + phase2)
    COMP_FUNCTION = lambda x: amplitude1 * np.sin(2 * np.pi * frequency1 * x + phase1) + amplitude2 * np.sin(2 * np.pi * frequency2 * x + phase2)   # with the power of math I command thee!!

    return function, domain


def makeGraph(function, t, num=1):
    fig, ax = plt.subplots()    # creates a new figure and axis of said figure
    ax.plot(t, function)   # sets the axis to the function and domain
    plt.xticks([0])   # removes the ticks on the x axis
    ax.set(xlabel='time', title=f'graph {num}', xlim=(0, SAMPLE_RANGE))  # sets the labels and limits
    ax.axhline(0, color='black')    # adds a horizontal line

    # adjusts the figure's size
    fig.set_figwidth(10)
    fig.set_figheight(3)

    # saves the figure
    fig.savefig(f"images\\graph{num}.png", bbox_inches='tight', pad_inches=0)
    plt.close(fig)


def remakeGraphs():
    for i, j in zip([(0,1,2), (3,4,5), (0,1,2,3,4,5)], (1,2,3)):    # magic numbers :P
        # sets i to a list of the box numbers contiaining the parameters and j is simply the current graph number
        parameters = map(lambda x: float(boxList[x].text), i) # extracts the parameters from the boxes and places them in a list
        s, t = makeFunction(*parameters) if j != 3 else makeComboFunction(*parameters)  # *args unpack notation
        makeGraph(s, t, num=j) # makes the graph with the function and domain


def updateWindow():
    global SAMPLE_RANGE
    # handels drawing all the text boxes and graphs
    SCREEN.fill((255,255,255)) # clear the screen
    pygame.draw.rect(SCREEN, '#002135', (0, 0, 320, 800))
    for i in range(3):
        try:    # try to draw each graph
            img = pygame.image.load(f"images\\graph{i+1}.png")
            SCREEN.blit(pygame.transform.scale(img, (800, 220)), (350, 800*i/3))
        except:
            pass
    
    # write all the text elements to the screen
    SCREEN.blit(pygame.font.Font(None, FONT_SIZE).render('Amplitude', True, (120,220,250)),(10,20))
    SCREEN.blit(pygame.font.Font(None, FONT_SIZE).render('Frequency', True, (120,220,250)),(10,80))
    SCREEN.blit(pygame.font.Font(None, FONT_SIZE).render('Offset', True, (120,220,250)),(10,140))
    SCREEN.blit(pygame.font.Font(None, FONT_SIZE).render('Amplitude', True, (120,220,250)),(10,320))
    SCREEN.blit(pygame.font.Font(None, FONT_SIZE).render('Frequency', True, (120,220,250)),(10,380))
    SCREEN.blit(pygame.font.Font(None, FONT_SIZE).render('Offset', True, (120,220,250)),(10,440))
    SCREEN.blit(pygame.font.Font(None, FONT_SIZE).render('Sample @', True, (120,220,250)),(10,600))
    SCREEN.blit(pygame.font.Font(None, FONT_SIZE-10).render('Sample range', True, (120,220,250)),(10,740))

    # calculate the value of the function at the sample point
    sampleVal = float(boxList[6].text) if boxList[6].text != '' else 0
    value = COMP_FUNCTION(sampleVal/(2*np.pi))
    SCREEN.blit(pygame.font.Font(None, FONT_SIZE).render('= ' + str(round(value, 5)) , True, (120,220,250)),(20,650))

    # draw all the input boxes
    for box in boxList:
        box.draw(SCREEN)
    
    # this was supposed to draw a vertical line on the composite sine wave where you were sampling at but
    # this code doesn't work because the image sizes change and thus the coordinates change for where the line should be drawn.
    # it would tke a lot more work than i'm willing to put in to get it to work with all cases (not even worth marks)
    # if you're curious, uncomment it and test it out but keep the amplitude of both sine waves constant at 1
    # plus, the zero line isn't always in the middle so if you use the change the offset of the second wave to be 1.57 it breaks again

    # maxSinValue = (float(boxList[0].text) if boxList[0].text != '' else 0) + (float(boxList[3].text) if boxList[3].text != '' else 0)
    # xvalue = 392 + 756*sampleVal/(SAMPLE_RANGE*2*np.pi)
    # yStart = 634
    # pygame.draw.line(SCREEN, '#e8a23c', (xvalue, yStart), (xvalue, yStart - 90*value/maxSinValue), 2)
    # pygame.draw.circle(SCREEN, '#e8423c', (xvalue, yStart - 90*value/maxSinValue), 2.5)
    
    pygame.display.update()  # update the screen


def main():
    # the main draw and event handling loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # close the window

            for box in boxList: # update the input boxes
                box.handle_event(event)

        updateWindow()


if __name__ == '__main__':
    # create input boxes
    InputBox(200, 10, 90, 50, 0)
    InputBox(200, 70, 90, 50, 1)
    InputBox(200, 130, 90, 50, 2, value=0)
    InputBox(200, 310, 90, 50, 3)
    InputBox(200, 370, 90, 50, 4, value=2)
    InputBox(200, 430, 90, 50, 5, value=0)
    InputBox(200, 590, 90, 50, 6)
    InputBox(200, 730, 90, 50, 7, value=5)
    remakeGraphs() # make default graphs

    # create the icon
    icon = pygame.image.load('images\\graph1.png').subsurface((50, 25, 300, 200))
    pygame.display.set_icon(pygame.transform.scale(icon, (32,32)))
    pygame.display.set_caption('Assignment 3 - Graphing Sine Functions')

    main()
