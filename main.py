import random
from flask import Flask, render_template, request
import cohere
from cohere.classify import Example
import os


categories = ["blabbermouth", "coward", "liar", "stupid", "ugly", "unlikeable", "useless", "general", "offensive"]

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")


def read_file(filename, multi):
    f = open(filename, "r", encoding='utf-8')
    data_list = []
    for line in f:
        data = line
        if multi:
            d_list = data.split("~")
            data_list.append(d_list)
        else:
            data_list.append(data)
        # print(d_list[1])
    f.close()
    return data_list


def write_file(filename, data_list):
    f = open(filename, 'w', encoding='utf-8')
    for s in data_list:
        s = s.rstrip()
        f.write("\"" + s + "\"" + "\n")
    f.close()


def add_categories(i_filename, o_filename):
    input_f = open(i_filename, 'r', encoding='utf-8')
    output_f = open(o_filename, 'w', encoding='utf-8')
    for s in input_f:
        s = s.rstrip()
        print(s)
        cat = input("What category does this insult fit in (blabbermouth, coward, liar, stupid, ugly, unlikeable, "
                    "useless, general, offensive)")
        cat = cat.lower()
        if cat == "done":
            break
        while cat not in categories and cat != "skip":
            cat = input("What category does this insult fit in (blabbermouth, coward, liar, stupid, ugly, unlikeable, "
                        "useless, general, offensive)")
            cat = cat.lower()
        output_f.write(s + "," + cat + "\n")
    output_f.close()
    input_f.close()


def classify_insults(filename):

    data_list = read_file(filename, False)
    cropped_list = data_list[7:]

    co = cohere.Client('GrQHcfdmGkhOW3Q3Mmeo7WXAeCIWPoVj0xnIFBkc')  # api key
    response = co.classify(
        model='multilingual-22-12',
        inputs=cropped_list,
        examples=[Example("More of your conversation would infect my brain.", "blabbermouth"), Example(
            "Thine forward voice, now, is to speak well of thine friend; thine backward voice is to utter foul speeches and to detract.",
            "blabbermouth"), Example("Thy tongue outvenoms all the worms of Nile.", "blabbermouth"), Example(
            "Foul spoken coward, that thund’rest with thy tongue, and with thy weapon nothing dares perform.",
            "blabbermouth"), Example("Go, prick thy face, and over-red thy fear, Thou lily-liver’d boy.", "coward"),
                  Example("You are pigeon-liver’d and lack gall.", "coward"),
                  Example("There’s no more faith in thee than in a stewed prune.", "coward"),
                  Example("I scorn you, scurvy companion.", "general"),
                  Example("You, minion, are too saucy.", "general"), Example("Threadbare juggler!", "general"),
                  Example("Eater of broken meats!", "general"), Example("Bottled spider!", "general"),
                  Example("Thou subtle, perjur’d, false, disloyal man!", "liar"),
                  Example("Heaven truly knows that thou art false as hell.", "liar"),
                  Example("You are not worth another word, else I’d call you knave.", "liar"),
                  Example("Thou subtle, perjur’d, false, disloyal man!", "liar"),
                  Example("Dissembling harlot, thou art false in all.", "liar"), Example(
                "Away, you starvelling, you elf-skin, you dried neat’s-tongue, bull’s-pizzle, you stock-fish!",
                "offensive"), Example(
                "That trunk of humours, that bolting-hutch of beastliness, that swollen parcel of dropsies, that huge bombard of sack, that stuffed cloak-bag of guts, that roasted Manningtree ox with pudding in his belly, that reverend vice, that grey Iniquity, that father ruffian, that vanity in years?",
                "offensive"),
                  Example("Thou clay-brained guts, thou knotty-pated fool, thou whoreson obscene greasy tallow-catch!",
                          "offensive"), Example(
                "Thou leathern-jerkin, crystal-button, knot-pated, agatering, puke-stocking, caddis-garter, smooth-tongue, Spanish pouch!",
                "offensive"), Example(
                "You starvelling, you eel-skin, you dried neat’s-tongue, you bull’s-pizzle, you stock-fish–O for breath to utter what is like thee!-you tailor’s-yard, you sheath, you bow-case, you vile standing tuck!",
                "offensive"), Example(
                "A most notable coward, an infinite and endless liar, an hourly promise breaker, the owner of no one good quality.",
                "offensive"), Example("Your wit’s as thick as a Tewkesbury mustard.", "stupid"),
                  Example("Your brain is as dry as the remainder biscuit after voyage.", "stupid"), Example(
                "Four of his five wits went halting off, and now is the whole man governed with one: so that if he have wit enough to keep himself warm, let him bear it for a difference between himself and his horse; for it is all the wealth that he hath left, to be known a reasonable creature.",
                "stupid"), Example("You have a plentiful lack of wit.", "stupid"),
                  Example("His wit’s as thick as a Tewkesbury mustard", "stupid"),
                  Example("Your abilities are too infant-like for doing much alone.", "stupid"),
                  Example("If you spend word for word with me, I shall make your wit bankrupt.", "stupid"),
                  Example("Thou art the cap of all the fools.", "stupid"),
                  Example("I am sick when I do look on thee.", "ugly"), Example("Peace, ye fat guts!", "ugly"),
                  Example("The rankest compound of villainous smell that ever offended nostril", "ugly"),
                  Example("The tartness of his face sours ripe grapes.", "ugly"),
                  Example("Thine face is not worth sunburning.", "ugly"), Example("Thou art as fat as butter.", "ugly"),
                  Example("Like the toad; ugly and venomous.", "ugly"),
                  Example("Here is the babe, as loathsome as a toad.", "unlikeable"),
                  Example("Thou art unfit for any place but hell.", "unlikeable"),
                  Example("Thy sin’s not accidental, but a trade.", "unlikeable"),
                  Example("I do desire that we may be better strangers.", "unlikeable"), Example(
                "Drunkenness is his best virtue, for he will be swine drunk, and in his sleep he does little harm, save to his bedclothes about him.",
                "unlikeable"), Example("I do wish thou were a dog, that I might love thee something.", "unlikeable"),
                  Example("She hath more hair than wit, and more faults than hairs, and more wealth than faults.",
                          "unlikeable"),
                  Example("Thou art a boil, a plague sore, an embossed carbuncle in my corrupted blood.", "unlikeable"),
                  Example("Come, come, you froward and unable worms!", "useless"),
                  Example("Thou whoreson zed, thou unnecessary letter!", "useless"),
                  Example("Away thou rag, thou quantity, thou remnant.", "useless"),
                  Example("Come, come, you froward and unable worms!", "useless")])
    return cropped_list, response.classifications


def get_insult(filename, category):
    insults, classifications = classify_insults(filename)
    index = 0
    insult = ""
    classification = ""
    while True:
        index = random.randint(0, 95)
        classification = classifications[index].prediction
        if classification == category:
            break
    insult = insults[index]
    print(insult)
    return insult


@app.route('/generateInsult', methods=["POST"])
def generate_insult():
    path = os.getcwd()
   # get_insult(path + "/venv/files/new_insults.csv", "general")

    user_input = request.form['user-input']
    category = ""
    if len(user_input) > 100:
        category = "blabbermouth"
    else:
        co = cohere.Client('GrQHcfdmGkhOW3Q3Mmeo7WXAeCIWPoVj0xnIFBkc')  # This is your trial API key
        response = co.classify(
            model='large',
            inputs=[user_input],
            examples=[Example("Give me an insult for my friend who is a coward", "coward"),
                      Example("I\'m not feeling very confident", "coward"), Example("This chatbot is scary", "coward"),
                      Example("I\'m scared", "coward"), Example("I don\'t know what to put", "coward"),
                      Example("I am a liar", "liar"), Example("My friend doesn\'t tell the truth", "liar"),
                      Example("What I say is false", "liar"), Example("This is a lie", "liar"),
                      Example("Insult my dishonest buddy", "liar"), Example("My friend betrayed me", "liar"),
                      Example("I am a disloyal person", "liar"), Example("You suck and are awful", "offensive"),
                      Example("Shakespeare is the worst author!", "offensive"),
                      Example("You are a terrible playwright!", "offensive"),
                      Example("I hate you and your books", "offensive"),
                      Example("I really dislike William Shakespeare", "offensive"),
                      Example("Help me insult my stupid friend", "stupid"), Example("I am an idiot", "stupid"),
                      Example("I failed my math exam", "stupid"), Example("My brain hurts", "stupid"),
                      Example("I don\'t really know what I\'m doing?", "stupid"), Example("Huh?", "stupid"),
                      Example("My friends is very ugly, insult them", "ugly"), Example("I am not very attractive", "ugly"),
                      Example("I didn\'t shower today", "ugly"), Example("My hair is a mess", "ugly"),
                      Example("He has a horrible face", "ugly"), Example("I hate my friend", "unlikeable"),
                      Example("Everyone dislikes me", "unlikeable"), Example("I don\'t have any friends", "unlikeable"),
                      Example("I think I\'m better than everyone", "unlikeable"),
                      Example("Other people hate me and I also hate them", "unlikeable"),
                      Example("I have nothing to offer to society", "useless"),
                      Example("My friend isn\'t doing anything with their life", "useless"),
                      Example("There\'s nothing to say", "useless"), Example("This is boring", "useless"),
                      Example("I have no job and live in my parent\'s basement all day", "useless")])
        category = response.classifications[0].prediction

        if response.classifications[0].confidence < 0.2:
            category = "general"

        print('The confidence levels of the labels are: {}'.format(response.classifications))

    insult = get_insult(path + "/files/new_insults.csv", category)
    author = "unknown"
    insult_data = read_file(path + "/files/insults.txt", True)
    for entry in insult_data:
        source, quote = entry
        quote = quote.rstrip()
        # print(quote)
        # print(insult[1:-2])
        if quote == insult[1:-2]:
            author = source
            break
    return render_template("index.html", insult=insult, author=author)

@app.route('/generateCustomInsult', methods=["POST"])
def get_custom_insult():
    path = os.getcwd()
    file = open(path + "/files/custom_insults.txt", 'r')
    insults = []
    for line in file:
        insults.append(line)

    insult = random.choice(insults).lower()
    is_vowel = insult[0] in 'aeiou'
    if is_vowel:
        insult = "Thou art an " + insult.rstrip()
    else:
        insult = "Thou art a " + insult.rstrip()
    insult += "!"
    author = "Custom-generated"
    return render_template("index.html", insult =insult, author=author)

def main():

    path = os.getcwd()
    # data_list = read_file(path + "/venv/files/insults.txt", True)
    # write_file(path + "/venv/files/new_insults.csv", data_list)
    get_insult(path + "/files/new_insults.csv", "general")
    # add_categories(path + "/venv/files/new_insults.txt", path + "/venv/files/insults_training_examples.csv")


if __name__ == "__main__":
    #main()
    #print(get_custom_insult())
    app.run()
