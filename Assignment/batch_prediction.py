def batch_predict_sentiment(reviews):
    """
    Simulates batch prediction for sentiment analysis.
    Categorizes reviews as 'positive' if they contain the word 'good', 
    otherwise 'negative'.
    """
    predictions = []
    for index, review in enumerate(reviews, start=1):
        # Basic case-insensitive string search
        if 'good' in review.lower():
            sentiment = 'positive'
        else:
            sentiment = 'negative'
        predictions.append((review, sentiment))
    return predictions

# Sample list of 10 user reviews for a restaurant
reviews = [
    "The food was really good and fresh.",
    "Worst service ever, totally disappointed.",
    "Ambience was nice and staff was very polite.",
    "The pizza tasted good, but it was cold.",
    "Extremely slow delivery and cold food.",
    "A good place to hang out with friends and family.",
    "Not worth the price, quality was poor.",
    "Desserts were amazingly good!",
    "Average taste, nothing special.",
    "Great presentation and good value for money."
]

if __name__ == "__main__":
    results = batch_predict_sentiment(reviews)
    print(f"{'No.':<4} | {'Review':<50} | {'Predicted Sentiment'}")
    print("-" * 75)
    for idx, (review, sentiment) in enumerate(results, start=1):
        print(f"{idx:<4} | {review:<50} | {sentiment}")
