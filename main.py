# Widget - A UI element (input field, label, text, button...)
# Glade - A GUI designer using the GTK framework

# Necessary imports for the GUI
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject
import utilities, page_parser

# Globals
headline_approved = False

# Create a new builder, build the GUI from the file
builder = Gtk.Builder()
builder.add_from_file("AlternativeGUI.glade")

# GTK Widgets
in_url = builder.get_object("input_url")
lbl_result = builder.get_object("lbl_result")
lbl_headline_prompt = builder.get_object("lbl_headline_prompt")
in_article_headline = builder.get_object("input_article_headline")

# This class will handle all widget events
class Handler():

    def on_check_button_click(self, *args):
        url = in_url.get_text()

        # Check the article for validity first
        if utilities.is_url_valid(url):
            lbl_result.set_text("Valid URL")
        else:
            lbl_result.set_text("Invalid URL")
        print(url)

        page_parser.website(url)

        if not headline_approved:
            in_article_headline.set_text(page_parser.article_title)
            lbl_headline_prompt.set_text("Is this not the article headline? If so, please correct it.")


        print page_parser.article_title



    def on_main_window_quit(self, window):
        Gtk.main_quit(main_window)


# Start the GUI
if __name__ == "__main__":
    builder.connect_signals(Handler())  # Connect Gtk.Builder with the Handler class to handle widget callbacks
    main_window = builder.get_object("main_window")
    main_window.show_all()

    Gtk.main()