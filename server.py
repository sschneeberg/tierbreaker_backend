# Imports
from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from datetime import datetime, date
from uuid import uuid4
from math import log2
from random import randint
from models import Bracket, BracketOptions, Keys
from middleware import quick_sort
from credentials import MONGO_URI
# Set Up
app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:8000' 
CORS(app)
socket = SocketIO(app, cors_allowed_origins="*")
# to use mongo atlas:
app.config['MONGODB_HOST'] = MONGO_URI 
# to use local db: 
# app.config['MONGODB_SETTINGS'] = {
#     'db' : 'tb_test',
#     'host' : '127.0.0.1',
#     'port' :  27017
# }
db = MongoEngine()
db.init_app(app)

@app.route('/', methods=['GET'])
def ping_server():
    # check if server is running
    return { "ping" : "pong" }

######### SOCKET LISTENERS #########

@socket.on('connect')
def confirm_connect():
    print('client connected')

@socket.on('disconnect')
def confirm_disconnect():
    print('client disconnected')

# @socket.on('vote')
# def vote_cast(key):
#     emit('vote_cast', key, broadcast=True)
#alternatively, this could be in the vote route?


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
    bracket = Bracket.objects(key=bracket_key) # returns only one 
    if len(bracket) == 0: return { "msg" : "no bracket found" } 
    bracket = bracket[0]
    return jsonify(bracket)

@app.route('/bracket/<bracket_key>/vote', methods=['PUT'])
def add_vote(bracket_key):
    # query db for bracket key, request.json['option']
    option = request.json['option']
    bracket = Bracket.objects(key=bracket_key)[0]
    round_votes = bracket.voting_options.votes
    round_votes[-1][option] += 1
    total_votes = bracket.voting_options.totals
    total_votes[option] += 1
    Bracket.objects(id=bracket.id).update_one(set__voting_options__votes=round_votes, set__voting_options__totals=total_votes)
    bracket.reload()
    socket.emit('vote_cast', { "key" : bracket.key })
    return { "vote": f"bracket option: {option} updated", "bracket": bracket}

@app.route('/bracket/create', methods=['POST'])
def create_bracket():
    # bracket = Bracket(key, title, time_duration, num_rounds, round_duration,created_at, end_display_formation, private, voting_options)
    
    def gen_key():
        poll_key = uuid4().hex[:8]
        if Keys.objects(key=poll_key): return gen_key()
        new_key = Keys(key=poll_key)
        new_key.save()
        return poll_key

    bracket = Bracket()
    bracket.title = request.json['title']
    bracket.key = gen_key()
    bracket.num_rounds = log2(int(request.json['num_options']))
    bracket.time_duration = int(request.json['duration'])*bracket.num_rounds
    bracket.round_duration = int(request.json['duration'])
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
def update_bracket(bracket_key):
    bracket = Bracket.objects(key=bracket_key)[0]
    # STRETCH GOAL: Reinstate this, proving unnecessarily complicated on front end
    # if request.json['duration']:
    #     new_round_dur = int(request.json['duration'])
    #     new_dur = new_round_dur * (bracket.num_rounds - (len(bracket.voting_options.votes)-1))
    #     Bracket.objects(id=bracket.id).update_one(set__time_duration=new_dur, set__round_duration=new_round_dur)
    if request.json['title']:
        Bracket.objects(id=bracket.id).update_one(set__title=request.json['title'])
    if request.json['private'] or request.json['private'] == False:
        print('PRIVATE')
        Bracket.objects(id=bracket.id).update_one(set__private=request.json['private'])
    bracket.reload()
    return { "msg" : "bracket updated" , "bracket": bracket }

@app.route('/bracket/<bracket_key>/tally', methods=['PUT'])
def tally_votes(bracket_key):
    # set up next round
    bracket = Bracket.objects(key=bracket_key)[0]
    # find the winners from each match up of the previous round
    prev_round = bracket.voting_options.votes[-1]
    prev_matchups = bracket.voting_options.round_options
    print(prev_matchups)

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
    
    if len(prev_matchups) == 1: return { "msg" :  "cannot tally completed brackets"}
    next_matchups, next_round = tally_round(prev_matchups, prev_round)
    Bracket.objects(id=bracket.id).update_one(push__voting_options__votes=next_round, set__voting_options__round_options=next_matchups)
    bracket.reload()

    def gen_winner(bracket):
        if bracket.end_display_format.lower() == 'winner': 
            Bracekt(id=bracket.id).update_one(set__end_display__winner={ bracket.voting_options.round_options[0] : bracket.voting_options.totals[bracket.voting_options.round_options[0]]})
        else: 
            sorted_totals = quick_sort.quick_sort(bracket.voting_options.totals)
            if bracket.end_display_format.lower() == 'top': Bracket.objects(id=bracket.id).update_one(set__end_display__top_three=sorted_totals[:3])
            if bracket.end_display_format.lower() == 'full': Bracket.objects(id=bracket.id).update_one(set__end_display__full_bracket=sorted_totals)
        return

    if len(next_round) == 1: 
        gen_winner(bracket)
        bracket.reload()
    
    return { "msg" : "bracket rounds updated", "bracket" : bracket }

@app.route('/bracket/<bracket_key>/delete', methods=['DELETE'])
def delete_bracket(bracket_key):
    # delete bracket
    bracket = Bracket.objects(key=bracket_key)[0]
    bracket.delete()
    # LATER : delete keys from master list of deleted brackets ??? this may be a security issue to discuss
    return { "msg" : "bracket deleted" }



if __name__ == '__main__':
    socket.run(app)


    