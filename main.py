# Widget - A UI element (input field, label, text, button...)
# Glade - A GUI designer using the GTK framework

# Necessary imports for the GUI
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject
import utilities, page_parser

# Globals
headline_approved = False
article_fetched = False

# Create a new builder, build the GUI from the file
builder = Gtk.Builder()
builder.add_from_file("AlternativeGUI.glade")

# GTK Widgets
in_url = builder.get_object("input_url")
lbl_validurl = builder.get_object("lbl_validurl")
lbl_headline_prompt = builder.get_object("lbl_headline_prompt")
lbl_article_headline = builder.get_object("lbl_article_headline")
in_article_headline = builder.get_object("input_article_headline")
listbox_flags = builder.get_object("lbox_flags")
lbl_flags = builder.get_object("lbl_flags")
chbox_headline_correct = builder.get_object("chbox_headline_correct")
btn_fact_check = builder.get_object("btn_fact_check")


# This class will handle all widget events
class Handler():

    def on_correct_headline_chechbox_check(self, *args):
        global headline_approved

        headline_approved = True
        ui_refresh()

    def on_check_button_click(self, *args):
        pass

        ui_refresh()

    def on_fetch_button_click(self, *args):
        global article_fetched
        url = in_url.get_text()

        # Check the article for validity first
        if utilities.is_url_valid(url):
            lbl_validurl.set_text("The given URL is valid")
            article_fetched = True
            ui_refresh()
            user_validate_headline(url)
        else:
            lbl_validurl.set_text("The given URL is invalid!")
        print(url)

        ui_refresh()

    def on_main_window_quit(self, window):
        Gtk.main_quit(main_window)


def user_validate_headline(url):
    page_parser.website(url)
    in_article_headline.set_text(page_parser.article_title)

def ui_refresh():
    if article_fetched:
        in_article_headline.set_editable(True)
        lbl_article_headline.set_visible(True)
        in_article_headline.set_visible(True)
        lbl_headline_prompt.set_visible(True)
        chbox_headline_correct.set_visible(True)
    else:
        in_article_headline.set_editable(False)
        lbl_article_headline.set_visible(False)
        in_article_headline.set_visible(False)
        lbl_headline_prompt.set_visible(False)
        chbox_headline_correct.set_visible(False)

    if article_fetched and headline_approved:
        btn_fact_check.set_sensitive(True)
    else:
        btn_fact_check.set_sensitive(False)



# Start the GUI
if __name__ == "__main__":
    builder.connect_signals(Handler())  # Connect Gtk.Builder with the Handler class to handle widget callbacks
    main_window = builder.get_object("main_window")
    main_window.show_all()

    lbl_headline_prompt.set_text("Is this the correct article headline? If not, please correct it.")
    lbl_headline_prompt.set_visible(False)
    chbox_headline_correct.set_visible(False)
    lbl_article_headline.set_visible(False)
    in_article_headline.set_visible(False)

    ui_refresh()

    #lbl_flags.set_visible(False)
    #listbox_flags.set_visible(False)

    Gtk.main()