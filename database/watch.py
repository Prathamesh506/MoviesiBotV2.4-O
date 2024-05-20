from info import  DATABASE_NAME
DATABASE_URI = "mongodb+srv://MoviesiBotV6:MoviesiBotV5@cluster0.zs9smub.mongodb.net/?retryWrites=true&w=majority"
from motor.motor_asyncio import AsyncIOMotorClient
from fuzzywuzzy import fuzz, process
client = AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]

class Movie:
    def __init__(self, title, movie_type, rating, popularity):
        self.title = title
        self.type = movie_type
        self.rating = rating
        self.popularity = popularity

async def search_movie_db(title_query):
    best_match = None
    best_score = 0
    async for movie in db.movies.find({}, {"title": 1}):
        movie_title = movie['title']
        score = fuzz.ratio(title_query, movie_title)
        if score > 80 and score > best_score:
            best_match = movie_title
            best_score = score
    return best_match
    
async def get_watch_movies(movie_type, offset=1, limit=10):
    movies_collection = db['movies']

    pipeline = [
        {'$match': {'movie_type': movie_type}},
        {'$sort': {'popularity': -1 if movie_type == 'trending' else 1}},
        {'$facet': {
            'movies': [
                {'$skip': (offset - 1) * limit},
                {'$limit': limit}
            ],
            'totalResults': [
                {'$count': 'count'}
            ]
        }}
    ]

    result = await movies_collection.aggregate(pipeline).to_list(length=None)

    # Extract movies and total results from the result
    movies = result[0]['movies']
    total_results = result[0]['totalResults'][0]['count'] if result and result[0]['totalResults'] else 0

    return movies, total_results


async def does_movie_exxists(title, category="trending"):
    movies_collection = db['movies']

    # Check if a movie with the given title and category exists
    movie = await movies_collection.find_one({'title': title, 'movie_type': category})

    return movie is not None

async def delete_category(category):
    movies_collection = db['movies']

    # Delete all movies of the given category
    result = await movies_collection.delete_many({'type': category})

    return result.deleted_count

async def get_all_movies():
    movies_collection = db['movies']

    # Retrieve all movies from the collection
    categories = await movies_collection.distinct('type')

    return categories

async def store_movies_from_text(movie_text):
    movies_collection = db['movies']

    # Split the text into lines, assuming each line represents a movie
    movie_lines = movie_text.split('\n')

    for line in movie_lines:
        # Split each line into movie attributes
        attributes = line.split(',')

        # Check if there are enough attributes for a movie
        if len(attributes) >= 4:
            movie_data = {
                'popularity': int(attributes[0].strip()),
                'title': attributes[1].strip(),
                'movie_type': attributes[2].strip(),
                'rating': float(attributes[3].strip())
            }

            # Check for repetition based on the movie title and movie type
            existing_movie = await movies_collection.find_one({
                'title': movie_data['title'],
                'movie_type': movie_data['movie_type']
            })

            # If movie type is "trending" and there is an existing movie, increment its popularity
            if existing_movie and movie_data['movie_type'].lower() == 'trending':
                existing_movie['popularity'] += 1
                await movies_collection.update_one(
                    {'title': movie_data['title'], 'movie_type': movie_data['movie_type']},
                    {'$set': {'popularity': existing_movie['popularity']}}
                )
                print(f"Popularity of movie '{movie_data['title']}' incremented to {existing_movie['popularity']}.")

            # If the movie is not "trending" or doesn't exist, insert it into the collection
            elif not existing_movie:
                await movies_collection.insert_one(movie_data)
                print(f"Movie '{movie_data['title']}' added to the collection.")
            else:
                print(f"Movie '{movie_data['title']}' alreday present.")

        else:
            print(f"Invalid movie data: {line}. Skipping.")
