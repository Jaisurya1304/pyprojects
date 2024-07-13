import pandas as pd
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Use a pipeline as a high-level helper
from transformers import pipeline

classifier= pipeline("text-classification", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
# Perform sentiment analysis using pre-trained model from Hugging Face
# classifier = pipeline("sentiment-analysis")


# Web scraping CNBC website for headlines
def scrape_cnbc_headlines():
    url = "https://www.cnbc.com/search/?query=green%20hydrogen&qsearchterm=green%20hydrogen"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []
    dates = []
    sources = []
    for article in soup.find_all("div", class_="Card-titleContainer"):
        headline = article.find("a").text.strip()
        headlines.append(headline)
        date = article.find("time")["datetime"]
        dates.append(date)
        sources.append("CNBC")
    return headlines, dates, sources


# Fetching news headlines from Google News RSS feed
def fetch_google_news_headlines():
    url = "https://news.google.com/rss/search?q=green%20hydrogen&hl=en-IN&gl=IN&ceid=IN:en"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "xml")
    headlines = []
    dates = []
    sources = []
    for item in soup.find_all("item"):
        headline = item.find("title").text.strip()
        headlines.append(headline)
        date = item.find("pubDate").text
        dates.append(date)
        sources.append("Google News")
    return headlines, dates, sources


# Perform sentiment analysis using pre-trained model from Hugging Face
def get_sentiment_score(text):
    result = classifier(text)
    return result[0]["label"], result[0]["score"]


# Extract organization names using NER
def extract_organization_names(text):
    classifier = pipeline(
        "ner",
        model="dbmdz/bert-large-cased-finetuned-conll03-english",
        aggregation_strategy="simple",
    )
    entities = classifier(text)
    org_names = [entity["word"] for entity in entities if entity["entity"] == "ORG"]
    return org_names


def create_dataframe(headlines, dates, sources):
    df = pd.DataFrame({"Headline": headlines, "Date": dates, "Source": sources})
    return df


def export_to_csv(df):
    df.to_csv("news_headlines.csv", index=False)


def generate_sentiment_scores(df):
    df["Sentiment"] = df["Headline"].apply(lambda x: get_sentiment_score(x)[1])


def generate_wordcloud(df):
    all_org_names = []
    for headline in df["Headline"]:
        org_names = extract_organization_names(headline)
        all_org_names.extend(org_names)
    word_freq = Counter(all_org_names)
    wordcloud = WordCloud(
        width=800, height=400, background_color="white"
    ).generate_from_frequencies(word_freq)
    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Organization Names Word Cloud")
    plt.show()


def main():
    cnbc_headlines, cnbc_dates, cnbc_sources = scrape_cnbc_headlines()
    google_news_headlines, google_news_dates, google_news_sources = (
        fetch_google_news_headlines()
    )
    headlines = cnbc_headlines + google_news_headlines
    dates = cnbc_dates + google_news_dates
    sources = cnbc_sources + google_news_sources

    df = create_dataframe(headlines, dates, sources)
    export_to_csv(df)

    generate_sentiment_scores(df)

    # Convert Date column to datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # Group by week and calculate average sentiment score
    df["Week"] = df["Date"].dt.to_period("W")
    weekly_sentiment = df.groupby("Week")["Sentiment"].mean()

    # Plot week-wise trend of average sentiment score
    weekly_sentiment.plot(kind="line", marker="o", figsize=(10, 6))
    plt.title("Week-wise Trend of Average Sentiment Score")
    plt.xlabel("Week")
    plt.ylabel("Average Sentiment Score")
    plt.grid(True)
    plt.show()

    # Generate organization word cloud
    generate_wordcloud(df)


if __name__ == "__main__":
    main()
