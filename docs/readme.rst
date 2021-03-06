
.. role:: mod
   :class: mod

.. role:: reverse
   :class: reverse

.. raw:: html

    <pre id='logo' class='center'>
    ┌───────────────────────────┐
    │   ┏━╸┏━┓┏┓╻┏━┓┏━┓╻  ┏━╸   │
    │   ┃  ┃ ┃┃┗┫┗━┓┃ ┃┃  ┣╸    │
    │   ┗━╸┗━┛╹ ╹┗━┛┗━┛┗━╸┗━╸   │
    └───────────────────────────┘
    </pre>

    <p class='center'><i>Tonight we're gonna party like it's 1979…</i></p>
    <p class='center'>╰─(˙𝀓˙)─╮  ╭─(＾0＾)─╯</p>



Console
============

Yet another package that makes it easy to generate the inline codes used to
display colors and character styles in ANSI-compatible terminals and emulators,
as well as other functionality such clearing screens,
moving cursors,
setting title bars,
and detecting capabilities.
A bit more comprehensive than most.
How does it work?

    *"Piece of cake?
    Oh, I wish somebody would tell me what that means." — Dr. Huer*


:reverse:`␛`\ [1;3m\ *Hello World* :reverse:`␛`\ [0m
----------------------------------------------------------

Adding a little color with console might look like this:

.. code-block:: python

    >>> from console import fg, bg, fx

    >>> fg.green + 'Hello World!' + fg.default
    '\x1b[32mHello World!\x1b[39m'

FYI, the string  ``'\x1b'`` represents the ASCII Escape character
(27 in decimal, ``1b`` hex).
Command 32 turns the text green
and 39 back to the default color,
but there's no need to worry about that.
Printing to a supporting terminal from Python might look like this:

.. raw:: html

    <pre>
    &gt;&gt;&gt; print(fg.red, fx.italic, '♥ Heart', fx.end,
              ' of Glass…', sep='')
    <span style="color:red; font-style: italic">♥ Heart</span> of Glass…
    </pre>

Above, ``fx.end`` is a convenient object to note---\
it ends all styles and fore/background colors at once,
where as ``bg.default`` for example,
resets only the background to its default color.
This need not be your responsibility however,
one may use the call form instead: ``fg.yellow('Woot!')``
More on that later.

.. raw:: html

    <p>But wait!&nbsp;  There's a
    <s><span style="opacity: .9">shitload,</span></s>
    <s><span style="opacity: .9">crapton,</span></s>
    err…
    <i>lot</i> more!</p>


Installen-Sie, Bitte
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    ⏵ pip3 install --user console

Suggested additional support packages,
some of which may be installed automatically if needed:

.. code-block:: shell

    webcolors             # More color names
    future_fstrings       # Needed: Python Version < 3.6

    colorama              # Needed: Windows Version < 10
    win_unicode_console   # Useful: for Python < 3.6


Jah!
While console is cross-platform,
`colorama <https://pypi.python.org/pypi/colorama>`_
will need to be installed and .init() run beforehand to view these examples
under the lame (no-ANSI support) versions of Windows < 10.

.. note::

    ``console`` supports Python 3.6 and over by default.
    However!  It is trying out
    `"future-fstrings" <https://github.com/asottile/future-fstrings>`_
    for experimental support under Python versions 3.5 and 3.4,
    perhaps earlier.
    Keep an eye peeled for oddities under older Pythons.
    Sorry, neither 2.X, nor 1.X is not supported. ``:-P``


``console`` has recently been tested on:

- Ubuntu 18.04 - Python 3.6

  - xterm, mate-terminal, linux, fbterm

- FreeBSD 11 - Python 3.7
- MacOS 10.13 - Python 3.6

  - Terminal.app, iTerm2

- Windows XP - Python 3.4 - 32 bit + colorama, ansicon
- Windows 7 - Python 3.6 - 32 bit + colorama
- Windows 10 - Python 3.7 - 64bit

  - Conhost, WSL

::

    ¸¸.·´¯`·.¸¸.·´¯`·.¸¸.·´¯`·.¸¸.·´¯`·.¸¸¸.·´¯`·.¸¸¸


Overview
------------------

As mentioned,
console handles lots more than color and styles.

.. rubric:: **Utils**

:mod:`console.utils`
includes a number of nifty functions:

.. code-block:: python

    >>> from console.utils import cls, set_title

    >>> cls()  # whammo! a.k.a. reset terminal
    >>> set_title('Le Freak')  # c'est chic
    '\x1b]2;Le Freak\x07'

It can also ``strip_ansi`` from strings,
wait for keypresses,
clear a line or the screen (with or without scrollback),
and easily ``pause`` a script like the old DOS commands of yesteryear.

.. rubric:: **Screen**

With :mod:`console.screen` you can
save or restore it,
move the cursor around,
get its position,
and enable
`bracketed paste <https://cirw.in/blog/bracketed-paste>`_
if any of that floats your boat. 
`Blessings <https://pypi.org/project/blessings/>`_-\
compatible context managers are also available for full-screen fun.


.. rubric:: **Detection**

Detect the terminal environment with
:mod:`console.detection`:

    - Determine palette support, load definitions.
    - Check relevant environment variables, such as
      `TERM <https://www.gnu.org/software/gettext/manual/html_node/The-TERM-variable.html>`_,
      `NO_COLOR <http://no-color.org/>`_,
      `COLORFGBG <https://unix.stackexchange.com/q/245378/159110>`_,
      and
      `CLICOLOR <https://bixense.com/clicolors/>`_,
      etc.
    - Query terminal colors and themes---light or dark?
    - Redirection---is this an interactive "``tty``" or not?
    - Get titles, and more.

Console does its best to figure out what your terminal supports on startup
and will configure its convenience objects
(we imported above)
to do the right thing.
They will deactivate themselves at startup when output is redirected into a
pipe, for example.

Detection can be bypassed and handled manually when needed however.
Simply use the detection functions in the module or write your own as desired,
then create your own objects from the classes in the
:mod:`console.style` and
:mod:`console.screen`
modules.

There's also logging done—\
enable the debug level before loading the console package and you'll see the
results of the queries from the detection module.

.. rubric:: **Constants**

A number of useful constants are provided in
:mod:`console.constants`,
such as
`CSI <https://en.wikipedia.org/wiki/ANSI_escape_code#Escape_sequences>`_
and
`OSC <https://en.wikipedia.org/wiki/ANSI_escape_code#Escape_sequences>`_
for building your own apps.
You can:

.. code-block:: python

    from console.constants import BEL
    print(f'Ring my {BEL}… Ring my {BEL}')  # ring-a-ling-a-ling…


Extended Palettes
~~~~~~~~~~~~~~~~~~~

The palettes break down into three main categories.
Unleash your inner
`Britto <https://www.art.com/gallery/id--a266/romero-britto-posters.htm>`_
below:

- Basic, the original 8/16 named colors
- Extended, 256 indexed colors
- "True", a.k.a. 16 million colors, consisting of:

  - RGB specified colors
  - X11-named colors, or
  - Webcolors-named colors

As mentioned,
the original palette,
X11,
and Webcolor palettes
may be accessed directly by name:

.. code-block:: python

    # Basic                Comment
    fg.red                # Original 8 colors
    fg.lightred           # Another 8 brighter colors w/o bold

    # Truecolor variants
    fg.bisque             # Webcolors or X11 color name, if avail
    fg.navyblue           # Webcolors takes precedence, if installed


Additional palettes are accessed via a prefix letter and a number of
digits (or name) to specify the color:

.. code-block:: python

    # Extended     Format  Comment
    bg.i_123       iDDD   # Extended/indexed 256-color palette
    bg.n_f0f       nHHH   # Hex to nearest indexed color

    # Truecolor
    bg.t_ff00bb    tHHH   # Truecolor, 3 or 6 digits
    bg.x_navyblue  x_NM   # Force an X11 color name, if available
    bg.w_bisque    w_NM   # Force Webcolors, if installed

**The underscores are optional.**
Choose depending whether brevity or readability are more important to you.
The assorted true color forms are useful to choose one explicitly without
ambiguity.
(X11 and Webcolors
`differ <https://en.wikipedia.org/wiki/X11_color_names#Clashes_between_web_and_X11_colors_in_the_CSS_color_scheme>`_
on a few colors.)
An unrecognized color name or index will result in an ``AttributeError``.


Composability++
~~~~~~~~~~~~~~~~

    *Dy-no-mite!! — J.J.*

Console's palette entry objects are meant to be highly composable and useful in
multiple ways.
For example,
you might like to create your own compound styles to use over and over again.

They can also be called as functions if desired and have "mixin" styles added
in as well.
The callable form also automatically resets styles to their defaults at the end
of each line in the string (to avoid breaking pagers),
so those tasks no longer need to be managed manually:

.. raw:: html

    <pre>
    &gt;&gt;&gt; muy_importante = fg.white + fx.bold + bg.red

    &gt;&gt;&gt; print(muy_importante('AHORITA!', fx.underline))  # ← mixin
    <div style="display: inline-block; background: #d00; color: white; font-weight: bold; text-decoration: underline">AHORITA!</div>
    </pre>

When palette objects are combined together as done above,
the list of codes to be rendered to is kept on ice until final output as a
string.
Meaning, there won't be redundant escape sequences in the output.
No sirree !

.. code-block:: python

    '\x1b[37;1;41;4mAHORITA!\x1b[0m'

Styles can be built on the fly as well:

.. raw:: html

    <pre>
    &gt;&gt;&gt; print(
        f'{fg.i208 + fx.reverse}Tangerine Dream{fx.end}',  # or
        (fg.i208 + fx.reverse)('Tangerine Dream'),
    )
    <span style="color: #222; background-color:#ff8700">Tangerine Dream</span>
    </pre>

.. rubric:: **Templating**

To build templates,
call a palette entry with placeholder strings,
with or instead of text:

.. code-block:: python

    >>> template = bg.i22('{}')  # dark green

.. raw:: html

    <pre>
    &gt;&gt;&gt; print(template.format(' GREEN Eggs… '))
    <div style="display: inline-block; background: #040;"> GREEN Eggs… </div>
    </pre>

Other template formats are no problem either, ``%s`` or ``${}``.

Console is lightweight,
but perhaps you'd like a pre-rendered string to be used in a tight loop for
performance reasons.
Simply use ``str()`` to finalize the output then use it in the loop.

Palette entries work as context-managers as well:

.. code-block:: python

    with bg.dodgerblue:
        print('Infield: Garvey, Lopes, Russel, Cey, Yeager')
        print('Outfield: Baker, Monday, Smith')
        print('Coach: Lasorda')


::

                                ⚾
    ¸¸.·´¯`·.¸¸.·´¯`·.¸¸.·´¯`·.⫽⫽¸¸.·´¯`·.¸¸¸.·´¯`·.¸¸¸
                              ⫻⫻


Demos and Tests
------------------

    *Outta Sight!*

A series of positively jaw-dropping demos (haha, ok maybe not) may be run at
the command-line with::

    ⏵ python3 -m console.demos

If you have pytest installed,
tests can be run from the install folder.

.. code-block:: shell

    ⏵ pytest -s

The Makefile at github has more details on such topics.


Contributions
------------------

Could use some help on Windows and MacOS as my daily driver is a 🐧 Tux racer.


Legalese
----------------

    *"Stickin' it to the Man"*

- Copyright 2018, Mike Miller
- Released under the LGPL, version 3+.
- Enterprise Pricing:

  | 6 MEEllion dollars!
  | *Bwah-haha-ha!*
  | (only have to sell *one* copy!)
