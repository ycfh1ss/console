# -*- coding: future_fstrings -*-
'''
    .. console - Comprehensive utility library for ANSI terminals.
    .. © 2018, Mike Miller - Released under the LGPL, version 3+.

    Demos showing what the library and terminal combo can do.
'''

if __name__ == '__main__':

    import sys, os
    import logging
    import env

    log = logging.getLogger(__name__)
    _DEBUG = '-d' in sys.argv
    if os.name == 'nt':
        try:  # wuc must come before colorama.init() for detection to work.
            import win_unicode_console as wuc
            wuc.enable()
        except ImportError:
            pass
        try:
            if not env.ANSICON:  # TODO: detect Win10 support
                import colorama
                colorama.init()
        except ImportError:
            pass

    # this sucks, what needs to be done to get demos to run:
    import console
    from importlib import reload
    reload(console)
    pal = console._CHOSEN_PALETTE

    if _DEBUG:
        from . import _set_debug_mode
        _set_debug_mode(_DEBUG)

        fmt = '  %(levelname)-7.7s %(module)s/%(funcName)s:%(lineno)s %(message)s'
        logging.basicConfig(level=logging.DEBUG, format=fmt)
        # detection already happened - need to run this again to log. :-/
        from .detection import choose_palette
        pal = choose_palette()

    # try some stuff out
    from . import fg, bg, fx, defx
    from . import style
    from .constants import BEL, ALL_PALETTES
    from .detection import is_a_tty, query_terminal_color, get_theme
    from .screen import screen
    from .utils import set_title, strip_ansi, cls

    # util functions
    def make_header(i):
        return f'  {fx.dim}{i+1:02d}{fx.end} '

    def build_demos(caption, obj, extra_style=''):
        ''' Iterate over a Palette container and collect the items to add to
            demos.
        '''
        items = []
        for name in dir(obj):
            if not name.startswith('_') and not name == 'clear':  # types !work
                attr = getattr(obj, name)
                if extra_style:
                    items.append(f'{attr + extra_style}{attr.name}{fx.end}')
                else:
                    items.append(f'{attr}{attr.name}{fx.end}')
        return caption + ' '.join(items)

    def run():
        ''' Run the demos. '''
        print('\nConsole - ANSI lib demos, here we go:\n')
        hello_world = f'''Greetings: {fx.bold + fg.blue}Hello {fx.reverse +
                        fg.yellow}World{fg.default + defx.reverse}!{fx.end}'''

        demos = [
            hello_world,
            f'↑ Title: {set_title("Console FTW! 🤣")!r} (gone in a µs.)',
            f'Combined, bold + underline + red: {fx.bold + fx.underline + fg.red}' +
                f'Merry {fg.green}X-Mas{fg.default}!{fx.end}',
            f'Cursor right → : [{screen.right}] (<-- one space between brackets)',
            f'Cursor down ↓ 2: {screen.down(2)}',

            'Text wrap: ' + fg.purple('Fill my eyes with that Double Vision…'
                                + BEL, fx.underline, fx.italic, fx.overline),
        ]

        demos.append(build_demos('FG:   ', fg))
        demos.append(build_demos('Bold: ', fg, extra_style=fx.bold))
        demos.append(build_demos('BG:   ', bg))
        demos.append(build_demos('FX:   ', fx))
        demos.append('Stripped: %r' % strip_ansi(hello_world))

        for i, demo in enumerate(demos):
            print(make_header(i), demo)
            if _DEBUG:
                log.debug('%r\n' % demo)

        print()
        print(make_header(i+1), 'with bg:')
        try:
            with bg.cornflowerblue:
                print('\tCan I get the icon in Cornflower Blue?\n\t'
                      'Absolutely. :-D')
        except AttributeError as err:
            with bg.blue:
                print('\tCan I get the icon in Cornflower Blue?\n\t'
                      'Absolutely. :-D')
        print('\n')

        print(make_header(i+2), 'Foreground - 256 indexed colors:\n      ',
              end='')
        for j in range(256):
            attr = getattr(fg, f'i{j}')
            print(attr, '%4.4s' % attr.name, fx.end, end=' ')

            # newline every 16 columns :-/
            if not (j + 1) % 16:
                print('\n      ', end='')
        print()

        print(make_header(i+3), 'Background - 256 indexed colors:\n      ',
              end='')
        for j in range(256):

            attr = getattr(bg, f'i{j}')
            print(attr, '%4.4s' % attr.name, fx.end, end=' ')

            # NL every 16 columns :-/
            if not (j + 1) % 16:
                print('\n      ', end='')
        print()

        print(make_header(i+4), 'Foreground - Millions of colors: 24-bit:')
        print('      fg:', fg.tFF00BB, 'text_FF00BB', fx.end)
        print('      fg:', fg.tB0B,    'text_BOB', fx.end)
        print('      fg:', fg.tff00bb, 'text_FF00BB', fx.end)
        try:
            print('      fg:', fg.tFF00B, 'text_FF00B', fx.end)
        except AttributeError as err:
            print('      ', fg.red, fx.reverse, 'Error:', fx.end, ' ', err,
                  '\n', sep='')

        print(make_header(i+5), 'Background - 24-bit, Millions of colors:')
        step = 3  # length of bar 256/3 = ~86

        # draw rounded box around gradients
        print('      ╭' + '─' * 86, '╮\n      │', sep='', end='')   # RED
        for val in range(0, 256, step):
            code = format(val, '02x')
            print(getattr(bg, 't%s0000' % code), fx.end, end='')
        print('│')

        print('      │', sep='', end='')                            # GREEN
        for val in range(255, -1, -step):
            code = format(val, '02x')
            #~ print(code, end =' ')
            print(getattr(bg, 't00%s00' % code), fx.end, end='')
        print('│')

        print('      │', sep='', end='')                            # BLUE
        for val in range(0, 256, step):
            code = format(val, '02x')
            print(getattr(bg, 't0000%s' % code), fx.end, end='')
        print('│')
        print('      ╰' + '─' * 86, '╯\n', sep='', end='')
        print()

        print(make_header(i+5), 'Test color downgrade support '
                                '(True ⏵ Indexed ⏵ Basic):')
        try:
            import webcolors
        except ImportError as err:
            print('      Test not available without webcolors installed.')
            sys.exit()

        if 'pal' in globals() and pal:
            bgall = style.BackgroundPalette(palettes=ALL_PALETTES);
            bge =   style.BackgroundPalette(palettes=('basic', 'extended'))
            bgb =   style.BackgroundPalette(palettes='basic')
            print()

            colors = (
                't_222',            # grey
                't_808080',         # grey
                't_ccc',            # grey
                't_ddd',            # grey
                't_eee',            # grey
                't_e95420',         # ubuntu orange
                'coral',            # wc
                't_ff00ff',         # grey
                't_bb00bb',         # magenta
                'x_bisque',
                'x_dodgerblue',     # lighter blue
                'w_cornflowerblue', # lighter blue
                'w_navy',           # dark blue
                'w_forestgreen',    # dark/medium green
                'i_28',
                'i_160',
                'n_a08',
                'n_f0f',
                't_deadbf',
            )

            for i, color_key in enumerate(colors):
                full = getattr(bgall, color_key)
                dwne = getattr(bge, color_key)
                dwnb = getattr(bgb, color_key)

                print('      ', '%-18.18s' % (color_key + ':'),
                      full, ' t   ', bgall.default,
                      dwne, ' i   ', bgall.default,
                      dwnb, ' b   ', bgall.default,
                sep='', end=' ')
                if i % 2 == 1:
                    print()

            fgall = style.ForegroundPalette(palettes=ALL_PALETTES);
            fge =   style.ForegroundPalette(palettes=('basic', 'extended'))
            fgb =   style.ForegroundPalette(palettes='basic')
            print('      FG t_deadbf:      ',
                fgall.t_deadbf('▉▉▉▉▉'),
                fge.t_deadbf('▉▉▉▉▉'),
                fgb.t_deadbf('▉▉▉▉▉'),
            sep='')
        else:
            print('      Term support not available.')
        print()

        if is_a_tty():
            try:
                print('       theme:', get_theme(), '\n')
                print('       color scheme:', query_terminal_color('fg'), 'on',
                                              query_terminal_color('bg'), end=' ')
            except ModuleNotFoundError:
                pass  # termios - Windows

            import time
            try:
                print('       About to clear terminal, check title above. ☝  '
                      ' (Ctrl+C exits first.) ', end='', flush=True)
                time.sleep(10)     # wait to see terminal title
                cls()
            except KeyboardInterrupt:
                pass

        print()
        print()
        print('      ☛ Done, should be normal text. ☚  ')
        print()

    run()
