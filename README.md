# Tier Breaker (Backend Repository)

Find the front end repository at [github.com/NikkiHmltn/tier-breaker](https://github.com/NikkiHmltn/tier-breaker)

This is a Flask API, using MongoDB through MonogEngine.

The app is deployed on heroku at [tierbreaker.herokuapp.com](https://tierbreaker.herokuapp.com)

## Installation

1. `Fork` and `Clone` this repository to your local machine.
2. Install Pyhton3 dependencies:
    - flask
    - flask_mongoengine
    - flask_cors
    - flask-socketio
3. Set up connection to MongoDB:
   This app is set up to access a remote Monog Atlas Cluster. To connect to your own, create a `credentials.py` file with a `MONOG_URI` variable containing your remote URI.

    To use MongoDb on your lcoal machine, do the following in server.py:

    - Comment out or remove line 11 and line 19 (which connect to credentials.py and configure the URI)

    - Uncomment lines 21 to 25, and confirm the db name, host, and port align with your desired local connection

4. In terminal, run `python3 server.py` to start the api on port 8000

## Using the API

### Models:

The main model is the tournament bracket:

```python
class Bracket(Document):
    key = StringField()
    title = StringField() # question for poll
    time_duration = IntField() # number in days
    num_rounds = IntField() # log2(options)
    round_duration = IntField() # number in days
    created_at = DateField()
    end_display_format = StringField() # how to show the results: Top, winner, or Full
    private = BooleanField() # if public, anyone can vote
    voting_options = EmbeddedDocumentField(BracketOptions)
    end_display = EmbeddedDocumentField(EndDisplay)
```

The two embedded documents dictate how votes are stored and displayed and expect data in specific ways (seen in the comments after each line):

```python
class BracketOptions(EmbeddedDocument):
    round_options = ListField(StringField())
    # [match1opt1, match1op2, match2opt1, match2opt2, etc.]
    votes = ListField(DictField(), blank=True)
    # example:
    # [ {round1opt1: round_votes, round1opt2: round_votes, round1opt3: round_votes, round1opt4: round_votes}, {round2opt1: round_votes, round2opt2: round_votes}, {winning_opt: round_votes}]
    totals = DictField()
    # {option1: total_votes, option2: total_votes, etc.}
```

```python
class EndDisplay(EmbeddedDocument):
    winner = DictField() # {winning_option: total_votes}
    top_three = ListField(DictField())
    # [{winning_option: total_votes}, {second_place_option: total_votes}, {third_place_option: total_votes}]
    full_bracket = ListField(DictField())
    # [ sorted array of all options from winner to loser ] where each element is {option: total_votes}
```

when brackets are created, they are given a unique, concise key to make user access easier. This key is a slice of an uuid (v4).  
In testing potential avenues for short key generation, this 8 character slice showed the fewest collisions, but they still exist.
To ensure we do not assign repeated keys, all keys are stored in the database. Before saving a new bracket, we check to make sure the newly generated key is not already stored and therefore not already assigned.  
This key testing process can be seen in the `scratch work` directory.

### Routes

| Method | Endpoint                      | Data expected                                                                                    | Data Returned                      | Purpose                                                      |
| ------ | ----------------------------- | ------------------------------------------------------------------------------------------------ | ---------------------------------- | ------------------------------------------------------------ |
| GET    | /                             | N/A                                                                                              | Message                            | Ping route to confirm connection to server                   |
| GET    | /brackets                     | N/A                                                                                              | List of all bracket objects        | Get all public tournament brackets                           |
| GET    | /bracket/<bracket_key>        | Bracket key in url parameters                                                                    | Full bracket object                | Get a single bracket's information                           |
| POST   | /bracket/create               | Request body: 'title', 'num_options', 'duration', 'end_display', 'private', 'options_list'       | Message and created bracket        | Create new bracket, initialize voting structures             |
| PUT    | /bracket/<bracket_key>/vote   | Bracket key in url parameters, 'option' in request body                                          | Message and updated bracket object | Add vote to specific option for specific bracket             |
| PUT    | /bracket/<bracket_id>/edit    | Bracket id in url parameters, updated fields in request body ('title', 'duration', or 'private') | Message and updated bracket object | Edit certain tournament parameters                           |
| PUT    | /bracket/<bracket_key>/tally  | Bracket key in url parameters                                                                    | Message and updated bracket object | Tally votes and set up next round or generate winner display |
| DELETE | /bracket/<bracket_key>/delete | Bracket key in url parameters                                                                    | Message                            | Delete tournament from database                              |

## Testing

This API was tested using Mocha.js on the principle that an API does not have restrictions on what kind of application can access it provided the protocols are correct and the conversation is held in JSON.
As I was more familiar with Mocha, time was limited, and Flask was entirely new when the project started, I decided to test with Javascript.

### Setting up testing

1. `cd` into the `testing` directory in terminal
2. Run `npm i` to get the required javascript dependencies
3. Ensure the API server is running (start it with `python3 server.py` from the root directory in a separate terminal window)
4. Use `mocha` to run all tests from the `testing` directory

### Testing Protocol

These tests rely on database information to run successfully and therefore must be run in a specific order.
The test file, when first cloned down, will have only the "ping" test uncommented. To test follow these steps:

1. Run `mocha` to test your server connection
2. On all passing, uncomment line 25 and it's closing brackets on line 226. Then begin for the first test within that section, and uncomment the POST test.
3. After running again, find the key for the bracket you just created in MongoDB.  
   Change opts, duration, and private in the POST test to the following values to test another set of inputs:

    - opts = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']

    - duration = '4' - private = false

    Uncomment the GET /bracket and GET /bracket/<bracket_key> tests, add the key you got from MONGO to the latter.

    Uncomment the Put /bracket/<brackey_key>/vote test and add the key to the key variable here as well.

    Run `mocha` again

4. Grab the id for your newly created bracket and comment out the POST test. Uncomment the edit test and add this id.
5. After running, uncomment the DELETE test, add the same key and comment out the edit test.  
   Change the option in the PUT vote test to "one" before running again.
6. Comment out the delete and vote tests. Uncomment the tally test and add the same key as in the vote test. Run this final test with `mocha`.

Please note, these tests are not all inclusive. Due to time constraints, this api was tested with a combination of these written tests and visual confirmation in Mongo and in Postman.

As an educational project and as an opportunity to learn Flask, emphasis was put on testing enough to confirm functionality.
Should we continue to build out this project, tests and logic will be added to address edge cases and errors rahter than relying on only the front end structure to filter this out.
