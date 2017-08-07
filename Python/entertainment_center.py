import media
import fresh_tomatoes

"""Creates instances of media.Movie and passes them to fresh_tomatoes"""

godspell = media.Movie(
    "Godspell",
    "https://upload.wikimedia.org/wikipedia/en/2/28/Godspellmoviep.jpg",
    "https://www.youtube.com/watch?v=bJ9X7OHAMs0")
  
montypythonholygrail = media.Movie(
    "Monty Python and the Holy Grail",
    "https://upload.wikimedia.org/wikipedia/en/0/08/Monty-Python-1975-poster.png",
    "https://www.youtube.com/watch?v=RDM75-oXGmQ")

lordoftheringsrotk = media.Movie(
    "The Lord of the Rings: The Return of the King",
    "https://upload.wikimedia.org/wikipedia/en/9/9d/Lord_of_the_Rings_-_The_Return_of_the_King.jpg",
    "https://www.youtube.com/watch?v=r5X-hFf6Bwo")

movies = [godspell, montypythonholygrail, lordoftheringsrotk]

fresh_tomatoes.open_movies_page(movies)

                     
