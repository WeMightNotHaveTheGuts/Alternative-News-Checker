# Widget - A UI element (input field, label, text, button...)
# Glade - A GUI designer using the GTK framework

# Necessary imports for the GUI
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject

# Create a new builder, build the GUI from the file
builder = Gtk.Builder()
builder.add_from_file("AlternativeGUI.glade")

# This class will handle all widget events
class Handler():
    pass

# Start the GUI
if __name__ == "__main__":
    builder.connect_signals(Handler())  # Connect Gtk.Builder with the Handler class to handle widget callbacks
    main_window = builder.get_object("main_window")
    main_window.show_all()

    Gtk.main()