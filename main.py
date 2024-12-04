import eel
import expence_tracker
import expence



# name of folder where the html, css, js, image files are located

eel.init('templates')



@eel.expose

def demo(x):
    print(f'This is a test from python {x}')


    return x**2



# 1000 is width of window and 600 is the height

eel.start('index.html', size=(1000, 600))