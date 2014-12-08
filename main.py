import urwid
import commands


class MenuButton(urwid.Button):
    def __init__(self, caption, callback):
        super(MenuButton, self).__init__("")
        urwid.connect_signal(self, 'click', callback)
        self._w = urwid.AttrMap(urwid.SelectableIcon(
            [u'  \N{BULLET} ', caption], 2), None, 'selected')


class SubMenu(urwid.WidgetWrap):
    def __init__(self, caption, choices):
        super(SubMenu, self).__init__(MenuButton(
            [caption, u"\N{HORIZONTAL ELLIPSIS}"], self.open_menu))
        line = urwid.Divider(u'\N{LOWER ONE QUARTER BLOCK}')
        listbox = urwid.ListBox(urwid.SimpleFocusListWalker([
            urwid.AttrMap(urwid.Text([u"\n  ", caption]), 'heading'),
            urwid.AttrMap(line, 'line'),
            urwid.Divider()] + choices + [urwid.Divider()]))
        self.menu = urwid.AttrMap(listbox, 'options')

    def open_menu(self, button):
        top.open_box(self.menu)


class Choice(urwid.WidgetWrap):
    def __init__(self, caption):
        super(Choice, self).__init__(
            MenuButton(caption, self.item_chosen))
        self.caption = caption

    def item_chosen(self, button):
        response = None
        if self.caption == 'check elasticsearch':
            if _check_es():
                response = urwid.Text([' elasticsearch is running \n'])
            else:
                response = urwid.Text([' elasticsearch is not running \n'])
        elif self.caption == 'check redis-server':
            if _check_redis():
                response = urwid.Text([' redis-server is running \n'])
            else:
                response = urwid.Text([' redis-server is not running \n'])
        if not response:
            response = urwid.Text([' quit? \n'])
        done = MenuButton(u'Ok', exit_program)
        response_box = urwid.Filler(urwid.Pile([response, done]))
        top.open_box(urwid.AttrMap(response_box, 'options'))


def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()


def exit_program(key):
    raise urwid.ExitMainLoop()


def _check_es():
    output = commands.getoutput('ps -A')
    return 'elasticsearch' in output


def _check_redis():
    output = commands.getoutput('ps -A')
    return 'redis-server' in output


def _on_off(check):
    if check:
        return 'ON'
    else:
        return 'OFF'


menu_top = SubMenu(u'Main Menu', [
    SubMenu(u'code repos', [
        SubMenu(u'be-core', [
            Choice(u'open'),
            ]),
    ]),
    SubMenu(u'System Services', [
        SubMenu(u'redis', [
            Choice(u'check redis-server'),
            Choice(u'start'),
            Choice(u'stop'),
            Choice(u'restart'),
            ]),
        SubMenu(u'elasticsearch', [
            Choice(u'check elasticsearch'),
            Choice(u'start'),
            Choice(u'stop'),
            Choice(u'restart'),
        ]),
    ]),
    Choice(u'redis-server %s' % _on_off(_check_redis())),
    Choice(u'elasticsearch %s' % _on_off(_check_es())),
    Choice(u'quit'),
])

palette = [
    (None, 'light gray', 'black'),
    ('heading', 'black', 'light gray'),
    ('line', 'black', 'light gray'),
    ('options', 'dark gray', 'black'),
    ('focus heading', 'white', 'dark red'),
    ('focus line', 'black', 'dark red'),
    ('focus options', 'black', 'light gray'),
    ('selected', 'white', 'dark blue')]
focus_map = {
    'heading': 'focus heading',
    'options': 'focus options',
    'line': 'focus line'}


class HorizontalBoxes(urwid.Columns):
    def __init__(self):
        super(HorizontalBoxes, self).__init__([], dividechars=1)

    def open_box(self, box):
        if self.contents:
            del self.contents[self.focus_position + 1:]
        self.contents.append(
            (
                urwid.AttrMap(box, 'options', focus_map),
                self.options('given', 24)
            )
        )
        self.focus_position = len(self.contents) - 1

top = HorizontalBoxes()
top.open_box(menu_top.menu)
urwid.MainLoop(urwid.Filler(top, 'middle', 10), palette).run()
