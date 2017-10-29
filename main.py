# Widget - A UI element (input field, label, text, button...)
# Glade - A GUI designer using the GTK framework

# Necessary imports for the GUI
import gi, threading
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject
import article_parser, headline_summarise, stage1utils, stage2utils, validators, watson_utils

# Globals
headline_approved = False
article_fetched = False
article_url = ""
article_headline = ""
article_headline_keywords = ""
finish_at_stage1 = False
finish_at_stage2 = False
finish_at_stage3 = False


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
console_window = builder.get_object("console_scrolled_window")


# This class will handle all widget events
class Handler():

    def on_correct_headline_chechbox_check(self, *args):
        global headline_approved

        headline_approved = True
        ui_refresh()

    def on_check_button_click(self, *args):
        global article_headline, finish_at_stage3, finish_at_stage2, finish_at_stage1
        finish_at_stage1 = False
        finish_at_stage2 = False
        finish_at_stage3 = False

        console_write("Fact checking started...")

        # Get the article headline keywords (used in Snopes search)
        console_write("Extracting article headline keywords")
        article_headline = in_article_headline.get_text()
        get_headline_keywords(article_headline)

        # Search for the keywords on Snopes.com
        console_write("Article headline keywords: [" + ", ".join(article_headline_keywords) + "]")
        stage_thread = threading.Thread(target=stage_manager,args=article_headline_keywords,name="StageThread")
        stage_thread.start()

        ui_refresh()

    def on_fetch_button_click(self, *args):
        global article_fetched, article_url
        url = in_url.get_text()

        # Check the article for validity first
        if validators.url(url):
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

def stage_manager(*keywords):
    stage1(keywords)
    if finish_at_stage1: return

    stage2()
    if finish_at_stage2: return

    stage3()


def stage1(keywords):
    print keywords, type(keywords)
    global finish_at_stage1

    keywords_reduced = False

    console_write("", False)
    console_write("STAGE 1", True)
    browser = stage1utils.initialize_browser()

    console_write("Searching for article references at Snopes.com")
    while (True):
        search_terms = "+".join(keywords)
        search_url = "https://www.snopes.com/?s=" + search_terms
        print search_url
        most_relevant_result = stage1utils.find_snopes_reference(browser, search_url)

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
                finish_at_stage1 = False
                return

    console_write("Looking for the Snopes reference article URL")
    factchecking_url = stage1utils.find_factchecking_url(most_relevant_result)

    matching_words = stage1utils.find_matching_search_result_words(most_relevant_result)

    console_write("Found the best search result, calculating relevance")
    relevance = stage1utils.calculate_relevance(keywords, matching_words)
    if relevance > 0.3:
        console_write("The search result is relevant enough, fetching the article truth rating")
        rating = stage1utils.fetch_rating(browser, factchecking_url)

        console_write("VERDICT", True)
        console_write("The article is... " + rating)
        console_write("See %s for more information" % factchecking_url)
        finish_at_stage1 = True
    else:
        console_write("The best result is not relevant enough, the article is not likely fact checked at Snopes.com")
        console_write("STAGE 1 END", True)
        finish_at_stage1 = False

def stage2():
    global finish_at_stage2

    console_write("", False)
    console_write("STAGE 2", True)
    console_write("Extracting site name")
    site_name = stage2utils.isolate_domain_name(article_url)
    console_write("Site name - %s" % site_name)

    if stage2utils.fake_news_sites_match(site_name):
        console_write("The site matches our database of known fake news sites")
        console_write("VERDICT", True)
        console_write("The article is very likely to be FAKE or INACCURATE due to the site being known for creating and spreading fake news")
        finish_at_stage2 = True
        return
    elif stage2utils.real_news_sites_match(site_name):
        console_write("The site matches our database of known reputable news sites")
        console_write("VERDICT", True)
        console_write("The article is most likely REAL due to the site being recognized as a reputable news site")
        finish_at_stage2 = True
        return
    elif stage2utils.satire_news_sites_match(site_name):
        console_write("The site matches our database of known SaTiRe news sites")
        console_write("VERDICT", True)
        console_write("It's just a JOKE bro!")
        finish_at_stage2 = True
        return
    else:
        console_write("The site has not been found in our database of fake/reputable news sources")
        console_write("STAGE 2 END", True)
        return

def stage3():
    global finish_at_stage3

    console_write("", False)
    console_write("STAGE 3", True)
    console_write("At this point, we cannot reliably detect whether the article is fake or real news.")
    console_write("We present a list of flags that may indicate which is more likely.")
    console_write("TEXT EMOTION ANALYSIS", True)

    real_emotions = {"Analytical" : "ANALYTIC",
                     "Tentative" : "TENTATIVE"}
    fake_emotions = {"Sadness" : "expressing SADNESS",
                     "Disgust" : "expressing DISGUST",
                     "Confident" : "expressing CONFIDENCE",
                     "Anger" : "expressing ANGER",
                     "Fear" : "expressing FEAR"}

    article_emotions = watson_utils.get_article_emotions(article_url)
    for emotion, value in article_emotions.items():
        if emotion in real_emotions:
            if value > 0.75:
                console_write("It is very likely that the text is %s, which s usually associated with REAL NEWS" % real_emotions[emotion])
            elif value > 0.5:
                console_write("It is likely that the text is %s, which is usually associated with REAL NEWS" % real_emotions[emotion])
        elif emotion in fake_emotions:
            if value > 0.75:
                console_write("It is very likely that the text is %s, which is usually associated with FAKE NEWS" % fake_emotions[emotion])
            elif value > 0.5:
                console_write("It is likely that the text is %s, which is usually associated with FAKE NEWS" % fake_emotions[emotion])

def user_validate_headline(url):
    global article_headline

    in_article_headline.set_text(article_parser.get_article_headline(url))

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

def console_write(message, important=None):
    consoleMessage = Gtk.Label();
    if important == True:
        GObject.idle_add(consoleMessage.set_text, "-----------------%s------------------" % message)
        GObject.idle_add(consoleMessage.set_halign, Gtk.Align(3))
    elif important == False:
        GObject.idle_add(consoleMessage.set_text, message)
    else:
        GObject.idle_add(consoleMessage.set_text, "> %s" % message)
        GObject.idle_add(consoleMessage.set_halign, Gtk.Align(1))

    GObject.idle_add(consoleMessage.set_visible, True)
    GObject.idle_add(lbox_console.add, consoleMessage)

    adjustment = console_window.get_vadjustment()
    adjustment.set_value(adjustment.get_upper())
    adjustment.set_page_size(0.0)
    GObject.idle_add(console_window.set_vadjustment, adjustment)



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