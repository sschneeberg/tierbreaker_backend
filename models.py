from mongoengine import *

class Keys(Document):
    key = StringField()

class BracketOptions(EmbeddedDocument):
    round_options = ListField(StringField()) # [match1opt1, match1op2, match2opt1, match2opt2, etc.]
    votes = ListField(DictField(), blank=True) 
    # example: 
    # [ {round1opt1: round_votes, round1opt2: round_votes, round1opt3: round_votes, round1opt4: round_votes}, {round2opt1: round_votes, round2opt2: round_votes}, {winner: round_votes}]
    totals = DictField()
    # {option1: total_votes, option2: total_votes, etc.}

class EndDisplay(EmbeddedDocument):
    winner = DictField() # {winning_option: total_votes}
    top_three = ListField(DictField()) 
    # [{winning_option: total_votes}, {second_place_option: total_votes}, {third_place_option: total_votes}]
    full_bracket = ListField(DictField()) 
   # [ sorted array of all options from winner to loser ] where each element is {option: total_votes}



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

    def __str__(self):
        return self.title
