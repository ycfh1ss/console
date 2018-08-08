'''
    console - An easy to use ANSI escape sequence library.
    © 2018, Mike Miller - Released under the LGPL, version 3+.

    Complicated Gobbyldegook providing the simple interface,
    is located here.

    Classes here not meant to be instantiated by client code.
'''
import sys
import logging

from .constants import CSI
from .disabled import dummy, empty


ALL_PALETTES = ('basic', 'extended', 'truecolor')
log = logging.getLogger(__name__)
chosen_palette = None


class _BasicPaletteBuilder:
    ''' ANSI code container for styles, fonts, etc.

        A base-class that modifies the attributes of child container classes on
        initialization.  Integer attributes are recognized as ANSI codes to be
        wrapped with a manager object to provide mucho additional
        functionality.  Most useful for the basic 8/16 color palette.
    '''
    def __new__(cls, autodetect=True, palettes=None):
        ''' Override new() to replace the class entirely on deactivation.

            Arguments:
                autodetect  - Attempt to detect palette support.
                palettes    - If autodetect disabled, set palette support
                              explicitly.  str, seq, or None
        '''
        self = super().__new__(cls)
        if autodetect:
            # defer loading detection so logging can start before demo
            from .detection import choose_palette
            global chosen_palette  # check once only
            chosen_palette = chosen_palette or choose_palette()

            if chosen_palette:  # enable "up to" the chosen palette level:
                palettes = ALL_PALETTES[:ALL_PALETTES.index(chosen_palette)+1]
            else:
                self = dummy    # None, deactivate completely
                palettes = ()                       # skipen-Sie

        else:  # set palette manually
            if type(palettes) in (list, tuple):     # carry on
                pass
            elif type(palettes) is str:             # make iterable
                palettes = (palettes,)
            elif type(palettes) is None:            # Ah, Shaddap-a ya face
                self = dummy
                palettes = ()                       # skipen-Sie
            else:
                raise TypeError('%r not in type (str, list, tuple)' % palettes)

        self._palette_support = palettes
        return self

    def __init__(self, **kwargs):
        # look for integer attributes to wrap in a basic palette:
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                if type(value) is int:
                    if 'basic' in self._palette_support:
                        attr = _PaletteEntry(self, name.upper(), value)
                    else:
                        attr = empty
                    setattr(self, name, attr)


class _HighColorPaletteBuilder(_BasicPaletteBuilder):
    ''' Container/Router for ANSI extended & truecolor palettes. '''

    def __getattr__(self, name):
        ''' Traffic cop - called only when an attribute is missing, so once per
            palette entry attribute.
        '''
        # route on first letter - must have length one to be called:
        first_letter, digits = name[0], name[1:]

        if first_letter == 'i':
            if not digits or len(digits) > 3:     # bdsm
                raise AttributeError('index %r not found. Check length of '
                                     'numeric portion, must be from 1 to 3 '
                                     'digits only.' % name)
            if not digits.isdigit():
                raise AttributeError('index %r not found. i+digits, holmes.' %
                                     name)

            if 'extended' in self._palette_support:  # build entry
                return self._get_extended_palette_entry(name, digits)
            else:
                return empty

        elif first_letter == 't':
            dig_len = len(digits)
            if dig_len == 6:
                pass
            elif dig_len == 3:  # double chars:  b0b -> bb00bb
                digits = ''.join([ch*2 for ch in digits])
            else:
                raise AttributeError('%r not found. Check length, hex portion '
                                     'must be 3 or 6 characters only.' % name)
            try:
                int(digits, 16)  # poor-man's ishexdigit()
            except ValueError:
                raise AttributeError('%r not found---not hex digits.' % name)

            if 'truecolor' in self._palette_support:  # build entry
                return self._get_true_palette_entry(name, digits)
            else:
                return empty

        else:
            raise AttributeError('%r is not a recognized attribute name '
                                 'format.' % name)

    def _get_extended_palette_entry(self, name, index):
        ''' Compute extended entry, once on the fly. '''
        attr = _PaletteEntry(self, name.upper(), index)
        attr._codes.insert(0, self._start_codes_extended)  # short for a deque
        setattr(self, name, attr)  # cached for later
        return attr

    def _get_true_palette_entry(self, name, hexdigits):
        ''' Compute truecolor entry, once on the fly. '''
        values = [self._start_codes_true]
        # convert hex attribute name, ex 'tBB00BB', to ints to 'R', 'G', 'B':
        values.extend(str(int(hexdigits[idx:idx+2], 16)) for idx in (0, 2 ,4))

        # Render first values as one string and place as first code:
        attr = _PaletteEntry(self, name.upper(), ';'.join(values))
        setattr(self, name, attr)  # cached for later
        return attr

    def clear(self):
        ''' Clears the palette, to save memory.
            Useful for truecolor palette, perhaps.
        '''
        self.__dict__.clear()


class _PaletteEntry:
    ''' Palette Entry Attribute

        Enables:

        - Rendering to an escape sequence string.
        - Addition of attributes, to create a combined, single sequence.
        - Allows entry attributes to be called, for use as a text wrapper.
        - Use as a Context Manager via the "with" statement.

        Arguments:
            parent  - Parent palette
            name    - Display name, used in demos.
            code    - Associated ANSI code number.
            out     - Stream to print to, when using a context manager.
    '''
    def __init__(self, parent, name, code, out=sys.stdout):
        self.parent = parent
        self.default = (parent.default if hasattr(parent, 'default')
                                       else parent.end)
        self.name = name
        self._codes = [str(code)]           # the initial code
        self._out = out                     # for redirection

    def __add__(self, other):
        ''' Add: self + other '''
        if isinstance(other, str):
            return str(self) + other

        elif isinstance(other, _PaletteEntry):
            # Make copy, so codes don't pile up after each addition:
            # Render first values once as one string and place as first code:
            return _PaletteEntry(self.parent, self.name,
                                  ';'.join(self._codes + other._codes))
        else:
            raise TypeError('Addition to type %r not supported.' % type(other))

    def __radd__(self, other):
        ''' Reverse add: other + self '''
        return other + str(self)

    def __bool__(self):
        return bool(self._codes)

    def __enter__(self):
        log.debug(repr(str(self)))
        print(self, file=self._out, end='')

    def __exit__(self, type, value, traceback):
        # self.default is not ready yet:
        log.debug(repr(str(self.parent.default)))
        print(self.parent.default, file=self._out, end='')

    def __call__(self, text, *styles):
        if hasattr(self, 'end'):
            end = self.end
        else:
            end = self.end = CSI + '0m'     # cache on 1st access

        for attr in styles:
            self += attr

        return f'{self}{text}{end}'

    def __str__(self):
        return f'{CSI}{";".join(self._codes)}m'

    def __repr__(self):
        return repr(self.__str__())
