import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import cairo

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, resizable=False)
        self.set_default_size(1000, 700)
        fixed = Gtk.fixed()
        self.add(fixed)
        self.brush = {'width':10, 'color':(1, 1, 1)}
        self.strokes = []
        self.drawing_init()


    def drawing_init(self):
        vbox = Gtk.VBox()
        vbox.set_homogeneous(False)
        area = Gtk.DrawingArea(name = 'area')
        area.set_property("width-request", 500)
        area.set_property("height-request", 500)
        area.connect("draw", self.draw)
        area.connect('motion-notify-event', self.mouse_move)
        area.connect("button-press-event", self.mouse_press)
        area.connect("button-release-event", self.mouse_release)
        area.set_events(area.get_events() |
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK)
        fixed = Gtk.Fixed()
        fixed.put(area, 250, 0)
        fixed.set_property("width-request", 1000)
        fixed.set_property("height-request", 550)
        vbox.pack_end(fixed, False, False, 0)
        self.add(vbox)
        self.show_all()
    

    def draw(self, widget, cr):
        cr.set_source_rgb(0.2, 0.2, 0.2)
        cr.paint()
        for stroke in self.strokes:
            cr.set_source_rgb(self.brush['color'][0], self.brush['color'][1], self.brush['color'][2])
            cr.set_line_width(self.brush['width'])
            cr.set_line_cap(1)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.new_path()
            for x, y in stroke:
                cr.line_to(x, y) 
            cr.stroke()


    def mouse_press(self, widget, event):
        if event.button == Gdk.BUTTON_SECONDARY:
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

