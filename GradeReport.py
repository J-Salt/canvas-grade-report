import requests
import json
import PySimpleGUI as sg
import time
import credentials


def main(grades, text_colors):
    background_color = '#212121'

    title_bar_background_color = '#1c1c1c'
    inner_elements = [
        [sg.Text(grades[0], background_color=text_colors[0], k='grade0', expand_x=True, text_color='#000000')],
        [sg.Text(grades[1], background_color=text_colors[1], k='grade1', expand_x=True, text_color='#000000')],
        [sg.Text(grades[2], background_color=text_colors[2], k='grade2', expand_x=True, text_color='#000000')],
        [sg.Text(grades[3], background_color=text_colors[3], k='grade3', expand_x=True, text_color='#000000')],
        [sg.Button(button_text='Close', key='Exit', button_color='#4D4D4D', border_width=0)]
    ]
    layout = [
        [sg.Frame(title='Grades', layout=[
            [sg.Frame(title='', layout=inner_elements, background_color=background_color, border_width=0)]
        ], background_color=title_bar_background_color, border_width=0)]
    ]
    window = sg.Window(title='', layout=layout, margins=(0, 0), background_color=background_color,
                       grab_anywhere=True, auto_size_buttons=False, no_titlebar=True, element_padding=(0, 0), border_depth=3)
    start_time = int(round(time.time()))
    while True:

        current_time = int(round(time.time())) - start_time
        if current_time >= 360:
            start_time = int(round(time.time()))
            grades, text_colors = get_grades()
            for i in range(0, len(grades)):
                window['grade' + str(i)].update(grades[i])
                window['grade' + str(i)].update(background_color=text_colors[i])
        else:
            event, values = window.read(timeout=5000)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break


def get_grades():
    bright_green = '#89f94f'
    green = '#7bb88e'
    green_yellow = '#b3c781'
    yellow = '#f3d678'
    orange = '#e0ac77'
    red = '#d08277'
    bright_red = '#dd3721'
    colors = []
    url = credentials.credentials['url']
    access_token = credentials.credentials['api_access_token']
    response = requests.get(url + '/users/self/enrollments' + access_token)
    parsed = json.loads(response.text)
    formatted_file = json.dumps(parsed, indent=4, sort_keys=True)
    with open('data.txt', 'w') as f:
        f.write(formatted_file)
        f.close()

    data = open('data.txt', 'r')
    data_list = data.readlines()
    grades = []
    for line in data_list:
        if 'current_score' in line:
            if 'null' in line:
                continue
            temp_line = line.replace('            "current_score": ', '')
            temp_line2 = temp_line.replace(',\n', '')
            grades.append(temp_line2)
            grade = float(temp_line2)
            if grade > 92.59:
                colors.append(bright_green)
            elif 92.59 >= grade > 89.59:
                colors.append(green)
            elif 89.59 >= grade > 86.59:
                colors.append(green_yellow)
            elif 86.59 >= grade > 83.59:
                colors.append(yellow)
            elif grade > 79.59:
                colors.append(orange)
            elif 79.59 >= grade > 76.59:
                colors.append(red)
            elif grade <= 76.59:
                colors.append(bright_red)

    print(grades)
    return grades, colors


if __name__ == '__main__':
    grades, colors = get_grades()
    main(grades, colors)
