from os import listdir
import pickle
import nltk
import progressbar
#import nltk
#nltk.download('reuters')


# RETURN ARTICLE TEXT FROM CORRESPONDING FILE
def article_text(file_name):
    with open(file_name, encoding='cp437', errors='ignore') as f:
        text = f.read()

    return text



# SPLIT ARTICLE TEXT INTO STORY AND HIGHLIGHTS SECTION
def split_highlights(article):
    pos = article.find('@highlight')
    story, highlights = article[:pos], article[pos:].split('@highlight')
    highlights = [h.strip() for h in highlights if len(h) > 0]
    return story, highlights



# SAVE ARTICLES AS DICTIONARY OF STORIES AND HIGHLIGHTS
def load_folder(folder):
    bar = progressbar.ProgressBar(max_value = progressbar.UnknownLength)
    i = 0
    articles = list()

    for _file in listdir(folder):
        file_name = folder + '/' + _file
        article = article_text(file_name)
        story, highlights = split_highlights(article)
        articles.append({'story': story, 'highlights': highlights})
        i += 1
        bar.update(i)

    return articles




# BASIC CLEAN UP (LOWER CASE AND REMOVE PUNCTUATION)
def clean_article_story(story):
    words = nltk.word_tokenize(story)
    words = [word.lower() for word in words if word.isalpha()]

    return ' '.join(word for word in words)



def clean_article_highlights(highlights):
    return_highlights = list()
    for highlight in highlights:
        words = nltk.word_tokenize(highlight)
        words = [word.lower() for word in words if word.isalpha()]
        return_highlights.append(' '.join(word for word in words))

    return return_highlights



# SAVE ARTICLES AS PICKLE FILE
def save_articles(articles):
    with open('cnn_articles.pkl', 'wb') as f:
        pickle.dump(articles, f, pickle.HIGHEST_PROTOCOL)


# LOAD ARTICLE PICKLE FILE
def load_articles():
    return pickle.load(open('cnn_articles.pkl', 'rb'))



if __name__ == '__main__':


    articles = load_folder('stories')
    # print(articles[27]['highlights'])
    # print(clean_article_highlights(articles[27]['highlights']))


    # CLEAN UP TEXT BEFORE SAVING TO PICKLE FILE
    for article in articles:
        article['story'] = clean_article_story(article['story'])
        article['highlights'] = clean_article_highlights(article['highlights'])


    save_articles(articles)

    articles = load_articles()
    print(len(articles))
    print(articles[27]['highlights'])