import os
import sys
from columnar import columnar
from cmd import Cmd
import qrcode
from PIL import ImageDraw
from PIL import ImageFont
import os
import io
import time
import shlex


def console_print(io_string, time_delay=0.05):
    for char in io_string:
        time.sleep(time_delay)
        print(char, end='', flush=True)


def console_list_print(io_list, time_delay=0.05):
    for each in io_list:
        print()
        console_print(each, time_delay)


def color_green(inp):
    os.system('color 0A')


def color_yellow(inp):
    os.system('color 0E')


def color_red(inp):
    os.system('color 0C')


def color_white(inp):
    os.system('color 0F')


def color_blue(inp):
    os.system('color 1F')


def color_bsod(inp):
    os.system('color 9F')


def color_default(inp):
    console_print(f'This color {inp} does not exist!'
                  f'\nType [HELP COLORS] to show which colors are available.')


def gen_qrcode(data, title, image, b_color, f_color):
    try:
        qr = qrcode.QRCode(box_size=20)
        qr.add_data(data)
        # img = qr.make_image()
        img = qr.make_image(back_color=b_color, fill_color=f_color)
        f = io.StringIO()
        qr.print_ascii(out=f)
        f.seek(0)
        print(f.read())
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 30)
        draw.text((300, 520), title, font=font)
        img.save(image)

    except Exception:
        raise Exception("Error occured in gen_qrcode func in genqr.py")


class MyPrompt(Cmd):
    COLOR_SELECTIONS = {
        'green': color_green,
        'yellow': color_yellow,
        'red': color_red,
        'white': color_white,
        'blue': color_blue,
        'bsod': color_bsod
    }
    HEADER = f'\n\n=================================================\n' \
             f'ROBCO INDUSTRIES\n' \
             f'=================================================\n'
    HEADER_CMDS = 'Press [EXIT] to exit. Type [HELP] to get help using the terminal.'
    PROMPT_STR = '\n\n \\Root\\ >  '

    BACK_COLOR = (36, 41, 46)
    FRONT_COLOR = (225, 228, 232)

    IMAGE = 'qrcode-test.png'

    prompt = f'{PROMPT_STR}'
    intro = f'{HEADER}\n{HEADER_CMDS}'

    def do_os_system(self, inp):
        os.system(inp)

    def do_qr(self, inp):
        args = shlex.split(inp.upper())

        if args[0] == 'COLOR':
            if args[1] == 'RESET':
                self.BACK_COLOR = (36, 41, 46)
                self.FRONT_COLOR = (225, 228, 232)
                console_print(f'\nSET QR-CODE RGB TO F:{self.FRONT_COLOR} B:{self.BACK_COLOR}')

            elif args[1] == 'SET':
                try:

                    console_print('\n< FRONT FILL >')
                    console_print('\nENTER [R G B] > ')
                    f_r, f_g, f_b = input().split()
                    self.FRONT_COLOR = (int(f_r), int(f_g), int(f_b))

                    console_print('\n< BACK FILL >')
                    console_print('\nENTER [R G B] > ')
                    b_r, b_g, b_b = input().split()
                    self.BACK_COLOR = (int(b_r), int(b_g), int(b_b))

                except TypeError:
                    console_print('INVALID RGB VALUES ...')

        elif args[0] == 'MAKE':
            data = args[1]

            if len(args) >= 3:
                title = args[2]
            else:
                title = ''

            gen_qrcode(data, title, self.IMAGE, self.BACK_COLOR, self.FRONT_COLOR)

        elif args[0] == 'OPEN':
            console_print(f'OPENING {self.IMAGE}')
            os.startfile(self.IMAGE)

        elif args[0] == 'SAVEAS':
            self.IMAGE = str(input('\nSAVE NEW QR-CODE IMAGE AS > '))

    def do_clear(self, inp):
        os.system("cls")

    def do_colors(self, inp):
        COLOR_CHOICE = self.COLOR_SELECTIONS.get(inp, color_default)
        COLOR_CHOICE(inp)

    def do_exit(self, inp):
        console_print(self.HEADER)
        return True  # sys.exit()

    # ------------------------------------------------------------------------------------------------

    def help_qr(self):
        hlp = 'Generate or configure a QR-code. Input options are:\n' \
              '\nqr [COLOR] [SET/RESET]' \
              '\nqr [MAKE] [DATA] [TITLE]' \
              '\nqr [OPEN]' \
              '\nqr [SAVEAS]'
        console_print(hlp)

    def help_os_system(self):
        hlp = 'Use this to input valid CMD Prompts.'
        console_print(hlp)

    def help_clear(self):
        hlp = 'Clears the terminal interface.'
        console_print(hlp)

    def help_colors(self):
        hlp = 'Changes CLI w/ new terminal color.\n' \
              'Available colors include:\n'
        console_print(hlp)
        console_list_print(self.COLOR_SELECTIONS.keys())

    def help_exit(self):
        print('Exit the application. Shorthand: [X] [Q] Ctrl-D.')

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
        print(f"'{inp}' is not a recognized command.")


if __name__ == '__main__':
    MyPrompt().cmdloop()
