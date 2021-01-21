# Imports
from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine
from datetime import datetime, date
from uuid import uuid4
from math import log2
from random import randint
from models import Bracket, BracketOptions, Keys

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

@app.route('/brackets', methods=['GET'])
def all_public_brackets():
    # query db and find everything that is marked public
    public_brackets = Bracket.objects(private=False)
    return { "public_brackets" : public_brackets}

@app.route('/bracket/<bracket_key>', methods=['GET'])
def show_bracket(bracket_key):
    # query db for specific bracket to vote
    # either end display or voting options
    bracket = Bracket.objects(key=bracket_key)[0]
    return jsonify(bracket)

@app.route('/bracket/<bracket_key>/vote', methods=['PUT'])
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

@app.route('/bracket/create', methods=['POST'])
def create_bracket():
    # bracket = Bracket(key, title, time_duration, num_rounds, round_duration,created_at, end_display_formation, private, voting_options)
    
    def gen_key():
        key = uuid4().hex[:8]
        if Keys.objects(key=key): return gen_key()
        return key

    bracket = Bracket()
    bracket.title = request.json['title']
    bracket.key = gen_key()
    bracket.num_rounds = log2(int(request.json['num_options']))
    bracket.time_duration = int(request.json['duration'])
    bracket.round_duration = bracket.time_duration/bracket.num_rounds
    bracket.created_at = datetime.now()
    bracket.end_display_format = request.json['end_display']
    bracket.private = request.json['private']

    def gen_votes(options):
        init_options = {}
        for option in options:
            init_options[option] = 0
        return init_options

    options = BracketOptions()

    options.round_options = request.json['options_list']
    options.votes = [gen_votes(request.json['options_list'])]
    options.totals = gen_votes(request.json['options_list'])

    bracket.voting_options = options

    bracket.save()
    return { "msg" : "bracket created", "bracket" : bracket }

@app.route('/bracket/<bracket_key>/edit', methods=['PUT'])
def update_duration(bracket_key):
    new_dur = request.json['duration']
    bracket = Bracket.objects(key=bracket_key)
    # if not working just make it total rounds
    new_round_dur = new_dur // (bracket.num_rounds - len(bracket.voting_options.votes))
    bracket.update_one(set__time_duration=new_dur, set__round_duration=new_round_dur)
    return { "msg" : "duration updated"}

@app.route('/bracket/<bracket_key>/tally', methods=['PUT'])
def tally_votes(bracket_key):
    # set up next round
    bracket = Bracket.objects(key=bracket_key)
    # find the winners from each match up of the previous round
    prev_round = bracket.voting_options.votes
    prev_matchups = bracket.voting_options.round_options

    def tally_round(matches, votes):
        next_round = {}
        next_matches = []
        for i in range(0, len(matches), 2):
            if votes[matches[i]] > votes[matches[i+1]]: 
                next_matches.append(matches[i])
                next_round[matches[i]] = 0
            elif votes[matches[i]] < votes[matches[i+1]]:
                next_matches.append(matches[i+1])
                next_round[matches[i+1]] = 0
            else: # in case of tie, randomize which advances
                ind = randint(i, i+1)
                next_matches.append(matches[ind])
                next_round[matches[ind]] = 0
        return next_matches, next_round
    
    next_matchups, next_round = tally_round(prev_matchups, prev_round)
    bracket.update_one(push__voting_options__votes=next_round, set__voting_options__round_options=next_matchups)
    bracket.reload()
    return { "msg" : "bracket rounds updated", "bracket" : bracket.to_json() }

@app.route('/bracket/<bracket_key>/', methods=['DELETE'])
def delete_bracket(bracket_key):
    # delete bracket
    bracket = Bracket.objects(key=bracket_key)
    bracket.delete()
    return { "msg" : "bracket deleted" }



if __name__ == '__main__':
    app.run(port=8000, debug=True)


    