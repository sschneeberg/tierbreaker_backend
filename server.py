# Imports
from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine
from datetime import datetime, date
from uuid import uuid4
from math import log2
from models import Bracket, BracketOptions, Keys, Round

# Set Up
app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'tb_test',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)


@app.route('/', methods=['GET'])
def ping_server():
    # check if server is running
    return { "ping" : "pong" }


######### BRACKET ROUTES #########

@app.route('/brackets', method=['GET'])
def all_public_brackets():
    # query db and find everything that is marked public
    public_brackets = Bracket.objects(private=False)
    return { "public_brackets" : public_brackets}

@app.route('/bracket/<bracket_key>', method=['GET'])
def show_bracket(bracket_key):
    # query db for specific bracket to vote
    # either end display or voting options
    bracket = Bracket.objects(key=bracket_key)
    return bracket.to_json()

@app.route('/bracket/<bracket_key>/vote', method=['PUT'])
def add_vote(bracket_key):
    # query db for bracket key, request.json['option']
    option = request.json['option']
    bracket = Bracket.objects(key=bracket_key)
    round_votes = bracket.voting_options__votes
    round_votes[-1][option] += 1
    total_votes = bracket.voting_options__totals
    total_votes[option] += 1
    bracket.update_one(set__voting_options__votes=round_votes, set__voting_options__totals=total_votes)
    return

@app.route('/bracket/create', method=['POST'])
def create_bracket():
    # bracket = Bracket(key, title, time_duration, num_rounds, round_duration,created_at, end_display_formation, private, voting_options)
    
    def gen_key():
        key = uuid4().hex[:8]
        if Keys.objects(key=key): return gen_key()
        return key

    bracket = Bracket()
    bracket.title = request.json['title']
    bracket.key = gen_key()
    bracket.num_rounds = log2(request.json['num_options'])
    bracket.time_duration = request.json['duration']
    bracket.round_duration = bracket.time_duration/bracket.num_rounds
    bracket.created_at = datetime.now()
    bracket.end_display_format = request.json['end_display']
    bracket.private = request.json['private']

    def gen_votes(options):
        init_options = {}
        for option in options:
            init_options[option] = 0
        return init_options

    bracket.voting_options.init_options = request.json['options_list']
    bracket.voting_options.votes = [gen_votes(request.json['options_list'])]
    bracket.voting_options.totals = gen_votes(request.json['options_list'])
    bracket.save()
    return { "msg" : "bracket created", "bracket" : bracket }

@app.route('/bracket/<bracket_key>/edit', method=['PUT'])
def update_duration(bracket_key):
    new_dur = request.json['duration']
    bracket = Bracket.objects(key=bracket_key)
    # if not working just make it total rounds
    new_round_dur = new_dur // (bracket.num_rounds - len(bracket.voting_options.votes))
    bracket.update_one(set__time_duration=new_dur, set__round_duration=new_round_dur)
    return { "msg" : "duration updated"}

@app.route('/bracket/<bracket_key>/tally', method=['PUT'])
def tally_votes(bracket_key):
    # set up next round
    return

@app.route('/bracket/<bracket_key>/', method=['DELETE'])
def delete_bracket(bracket_key):
    # delete bracket
    bracket = Bracket.objects(key=bracket_key)
    bracket.delete()
    return 



if __name__ == '__main__':
    app.run(port=8000, debug=True)


    