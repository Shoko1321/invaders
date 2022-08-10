import PySimpleGUI as sg

layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button('NOU')]]
#Create the window
window = sg.Window('Demo', layout)

#create an event loop
while True:
    event, values = window.read()
    #end program if user closes window or presses ok button
    if event == 'NOU' or event == sg.WIN_CLOSED:
        break

window.close