# Widget - A UI element (input field, label, text, button...)
# Glade - A GUI designer using the GTK framework

# Necessary imports for the GUI
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject
import utilities

# Create a new builder, build the GUI from the file
builder = Gtk.Builder()
builder.add_from_file("AlternativeGUI.glade")

# GTK Widgets
in_url = builder.get_object("input_url")
lbl_result = builder.get_object("lbl_result")

# This class will handle all widget events
class Handler():

    def on_check_button_click(self, *args):
        url = in_url.get_text()
        if utilities.is_url_valid(url): lbl_result.set_text("Valid URL")
        else: lbl_result.set_text("Invalid URL")
        print(url)

    def on_main_window_quit(self, window):
        Gtk.main_quit(main_window)


# Start the GUI
if __name__ == "__main__":
    builder.connect_signals(Handler())  # Connect Gtk.Builder with the Handler class to handle widget callbacks
    main_window = builder.get_object("main_window")
    main_window.show_all()

    Gtk.main()