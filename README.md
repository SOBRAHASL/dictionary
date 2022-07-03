# __*The Dictionary*__

## *Description*

As an english learner, one of the tools I use everyday is dictionary. So I came up with the idea of creating a dictionary for myself.

One of the problems I have been facing using other dictionaries is for some of the words you cannot find the best definition in one source and you have to search various sources.

So, it would be great if we can combine all of those sources in one place.

__*Warning:*__ For now the dictionary only uses one source.

__*Note:*__ This project was built for [CS50 final project](https://cs50.harvard.edu/x/).

[Website Demo](https://dictionarybeta.herokuapp.com)

[Video Demo](https://youtube.com)

## *Contents*

### *app.py*

Contains the configurations' of flask application, app routes and implementing session cookies

### *helpers.py*

Contains helper functions including lookup, load, suggest, accent

| Function | Operation |
| -------  | --------- |
| Lookup   | Searches for the meaning using [free dictionary API](https://github.com/meetDeveloper/freeDictionaryAPI). |
| Suggest  | Suggest words based on incomplete word |
| Load  | Open and load word list text file
| Accent  | Determines which accent is used in the audio file based on the audio name |

### *wordlist directory*
  
  Contains english.txt file including most of the English words.

### *templates directory*
  
  Contains templates which are rendered by app.py

| File | Usage |
| ---- | ----- |
| history.html | Showing the history of searches |
| index.html | Welcome page and some instructions |
| layout.html | The base file in all templates including meta tags, nav and header |
| login.html | Form for logging in the user |
| message.html | Uses for showing errors to the user |
| register.html | Form for registering the user |
| search.html | Visualize the API information |

### *static directory*

  Contains static flies including styles.css, fonts and images.

### *dictionary.db*

  Contains an english dictionary sqlite3 database, in addition to users and history tables.
