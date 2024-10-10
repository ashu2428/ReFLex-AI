from bs4 import BeautifulSoup
from bson import ObjectId
from bson.regex import Regex
import re
from datetime import datetime
from transformers import pipeline

# Load the previously trained model for prediction
emotion_model = pipeline("text-classification", model="arpanghoshal/EmoRoBERTa")

def search_entries_by_keyword(db, keyword):
	# Build the regex pattern with case-insensitivity
	regex_pattern = f"(?i){re.escape(keyword)}"

	# Use the $match stage in the aggregation pipeline to filter entries
	pipeline = [
		{
			"$match": {
				"$or": [
					{"diary_title": {"$regex": Regex(regex_pattern)}},
					{"diary_content": {"$regex": Regex(regex_pattern)}},
				]
			}
		}
	]

	# Execute the aggregation pipeline and retrieve the matching entries
	matching_entries = list(db.diary.aggregate(pipeline))
	return matching_entries


# to extract plaintext from formatted text with html tags
def extract_plaintext(html_content):
	soup = BeautifulSoup(html_content, 'html.parser')
	plaintext = soup.get_text()
	return plaintext


# to save books in db for specified author if not already recommended
def save_books(db, recommended_books, author_id):
	existing_books = [book['title'] for book in db.books.find({'author_id': ObjectId(author_id)}, {'title': 1})]
	new_books = [book for book in recommended_books if book['title'] not in existing_books]

	if new_books:
		for book in new_books:
			book['author_id'] = ObjectId(author_id)
		db.books.insert_many(new_books, ordered=False)

def save_movies(db, recommended_movies, author_id):
	existing_movies = [movie['movie_id'] for movie in db.movies.find({'author_id': ObjectId(author_id)}, {'movie_id': 1})]
	new_movies = [movie for movie in recommended_movies if movie['movie_id'] not in existing_movies]

	if new_movies:
		for movie in new_movies[:5]:
			movie['author_id'] = ObjectId(author_id)
		db.movies.insert_many(new_movies, ordered=False)


# Function to extract emotion from text
def extract_emotion(text):
	emotion_labels = emotion_model(text)
	print(emotion_labels)
	return emotion_labels[0]['label']


# extract emotions and their respective counts from start date to end date
def fetch_data(db, author_id, start_date, end_date):
	counts = []
	emotions = []

	start_datetime = datetime.combine(start_date, datetime.min.time())
	end_datetime = datetime.combine(end_date, datetime.max.time())
	
	pipeline = [
		{"$match": {
			"author_id": author_id,
			"diary_created": {"$gte": start_datetime, "$lte": end_datetime}
		}},
		{"$group": {
			"_id": "$emotion",
			"count": {"$sum": 1}
		}},
		{"$project": {
			"emotion": "$_id",
			"count": 1,
			"_id": 0
		}}
	]
	
	result = db.diary.aggregate(pipeline)
	
	for entry in result:
		counts.append(entry['count'])
		emotions.append(entry['emotion'])
	
	print("From fetch data of emotions:")
	print(counts, emotions)
	return counts, emotions

# general interests for user to choose from during profile and as tags during writing diary entry
interests = [
	"Coding",
	"Study",
	"Space",
	"Art",
	"Reading",
	"Music",
	"Travel",
	"Fitness",
	"Cooking",
	"Photography",
	"Gaming",
	"Writing",
	"Technology",
	"Nature",
	"Movies",
	"Sports",
	"Science",
	"Fashion",
	"History",
	"DIY Projects"
]