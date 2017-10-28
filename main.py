# Widget - A UI element (input field, label, text, button...)
# Glade - A GUI designer using the GTK framework

# Necessary imports for the GUI
import gi, threading
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject
import utilities, page_parser, headline_summarise, fake_checker

# Globals
headline_approved = False
article_fetched = False
article_url = ""
article_headline = ""
article_headline_keywords = ""

# Create a new builder, build the GUI from the file
builder = Gtk.Builder()
builder.add_from_file("AlternativeGUI.glade")

# GTK Widgets
in_url = builder.get_object("input_url")
lbl_headline_prompt = builder.get_object("lbl_headline_prompt")
lbl_article_headline = builder.get_object("lbl_article_headline")
in_article_headline = builder.get_object("input_article_headline")
listbox_flags = builder.get_object("lbox_flags")
lbl_flags = builder.get_object("lbl_flags")
chbox_headline_correct = builder.get_object("chbox_headline_correct")
btn_fact_check = builder.get_object("btn_fact_check")
lbox_console = builder.get_object("lbox_console")


# This class will handle all widget events
class Handler():

    def on_correct_headline_chechbox_check(self, *args):
        global headline_approved

        headline_approved = True
        ui_refresh()

    def on_check_button_click(self, *args):
        global article_headline

        console_write("Fact checking started...")

        # Get the article headline keywords (used in Snopes search)
        console_write("Extracting article headline keywords")
        article_headline = in_article_headline.get_text()
        get_headline_keywords(article_headline)

        # Search for the keywords on Snopes.com
        console_write("Article headline keywords: [" + ", ".join(article_headline_keywords) + "]")
        scan_thread = threading.Thread(target=stage1,args=article_headline_keywords,name="MainCheckThread")
        scan_thread.start()

        ui_refresh()

    def on_fetch_button_click(self, *args):
        global article_fetched, article_url
        url = in_url.get_text()

        # Check the article for validity first
        if utilities.is_url_valid(url):
            article_fetched = True
            article_url = url
            console_write("The given URL is valid!")

            ui_refresh()
            user_validate_headline(url)
        else:
            console_write("The given URL is invalid! Please enter a valid URL")
        print(url)

        ui_refresh()

    def on_main_window_quit(self, window):
        Gtk.main_quit(main_window)

"""
In the first stage we take the keywords from the headline of the checked article and we try to figure out whether
the article has been fact checked at Snopes.com
"""
def stage1(*keywords):
    keywords_reduced = False

    console_write("STAGE 1", True)
    browser = fake_checker.initialize_browser()

    console_write("Searching for article references at Snopes.com")
    while (True):
        search_terms = "+".join(keywords)
        search_url = "https://www.snopes.com/?s=" + search_terms
        print search_url
        most_relevant_result = fake_checker.find_snopes_reference(browser, search_url)

        if most_relevant_result:
            break
        else:
            if (not keywords_reduced):
                console_write("Could not find anything. Trying to use fewer keywords...")
                keywords = keywords[::2]
                keywords_reduced = True
                console_write("New article headline keywords: [" + ", ".join(keywords) + "]")
            else:
                console_write("Could not find a Snopes reference even with fewer keywords")
                console_write("STAGE 1 END", True)
                return False

    console_write("Looking for the Snopes reference article URL")
    factchecking_url = fake_checker.find_factchecking_url(most_relevant_result)

    matching_words = fake_checker.find_matching_search_result_words(most_relevant_result)

    console_write("Found the best search result, calculating relevance")
    relevance = fake_checker.calculate_relevance(keywords, matching_words)
    if relevance > 0.3:
        console_write("The search result is relevant enough, fetching the article truth rating")
        rating = fake_checker.fetch_rating(browser, factchecking_url)

        console_write("-------------------")
        console_write("The article is... " + rating)
        console_write("See %s for more information" % factchecking_url)
        return True
    else:
        console_write("The best result is not relevant enough, the article is not likely fact checked at Snopes.com")
        console_write("STAGE 1 END", True)
        return False

def stage2():


def user_validate_headline(url):
    global article_headline

    page_parser.website(url)
    article_headline = page_parser.article_title
    in_article_headline.set_text(page_parser.article_title)

def get_headline_keywords(headline):
    global article_headline_keywords

    print headline_summarise.summarise(headline)
    article_headline_keywords = headline_summarise.summarise(headline)


def get_headline_keywords(headline):
    global article_headline_keywords

    print headline_summarise.summarise(headline)
    article_headline_keywords = headline_summarise.summarise(headline)


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

def console_write(message, *important):
    consoleMessage = Gtk.Label();
    if important:
        consoleMessage.set_text("-----------------%s------------------" % message)
        consoleMessage.set_halign(Gtk.Align(3))
    else:
        consoleMessage.set_text("> %s" % message)
        consoleMessage.set_halign(Gtk.Align(1))
    consoleMessage.set_visible(True)

    lbox_console.add(consoleMessage)

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

    Gtk.main()