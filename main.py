import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import cairo

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, resizable=False)
        self.set_default_size(1000, 700)
        self.brush = {'width':10, 'color':(1, 1, 1)}
        self.strokes = []
        self.written_strokes = []
        self.drawing_init()
        self.colors = {}


    def change_color(self, button, color):
        self.brush['color'] = color
    
    
    def drawing_init(self):
        vbox = Gtk.VBox()
        vbox.set_homogeneous(False)
        hbox = Gtk.HBox()
        vbox.pack_start(hbox, True, True, 0)
        red_button = Gtk.Button(name="r-btn")
        blue_button = Gtk.Button(name="b-btn")
        green_button = Gtk.Button(name="g-btn")
        white_button = Gtk.Button(name="w-btn")
        hbox.pack_end(red_button, True, True, 0)
        hbox.pack_end(blue_button, True, True, 0)
        hbox.pack_end(white_button, True, True, 0)
        hbox.pack_end(green_button, True, True, 0)
        

        area = Gtk.DrawingArea(name = 'area')
        area.set_property("width-request", 1000)
        area.set_property("height-request", 600)
        area.connect("draw", self.draw)
        area.connect('motion-notify-event', self.mouse_move)
        area.connect("button-press-event", self.mouse_press)
        area.connect("button-release-event", self.mouse_release)
        area.set_events(area.get_events() |
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK)
        fixed = Gtk.Fixed()
        fixed.put(area, 0, 0)
        fixed.set_property("width-request", 1000)
        fixed.set_property("height-request", 550)
        vbox.pack_end(fixed, False, False, 0)
        white_button.connect("clicked", self.change_color, (1, 1, 1))
        red_button.connect("clicked", self.change_color, (1, 0, 0))
        blue_button.connect("clicked", self.change_color, (0, 0, 1))
        green_button.connect("clicked", self.change_color, (0, 1, 0))
        self.add(vbox)
        self.show_all()
    

    def draw(self, widget, cr):
        cr.set_source_rgb(0.2, 0.2, 0.2)
        cr.paint()
        for i in range(len(self.strokes)):
            stroke = self.strokes[i]
            if stroke not in self.written_strokes:
                self.colors[i] = [self.brush['color'][0], self.brush['color'][1], self.brush['color'][2]]
            cr.set_source_rgb(self.colors[i][0], self.colors[i][1], self.colors[i][2])
            cr.set_line_width(self.brush['width'])
            cr.set_line_cap(1)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.new_path()
            for x, y in stroke:
                cr.line_to(x, y) 
            cr.stroke()
            self.written_strokes.append(stroke)


    def mouse_press(self, widget, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            self.strokes.append(list())
            self.strokes[-1].append((event.x, event.y))
            widget.queue_draw()
        elif event.button == Gdk.BUTTON_SECONDARY:
            self.strokes.clear()


    def mouse_move(self, widget, event):
        if event.state:
            self.strokes[-1].append((event.x, event.y))
            widget.queue_draw()


    def mouse_release(self, widget, event):
        widget.queue_draw()


def main():
    cssProvider = Gtk.CssProvider()
    cssProvider.load_from_path('style.css')
    screen = Gdk.Screen.get_default()
    styleContext = Gtk.StyleContext()
    styleContext.add_provider_for_screen(screen, cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    win = MyWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == "__main__":    
    main()
