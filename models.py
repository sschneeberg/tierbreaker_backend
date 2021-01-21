from mongoengine import *

class Keys(Document):
    key = StringField()

class BracketOptions(EmbeddedDocument):
    round_options = ListField(StringField()) # [match1opt1, match1op2, match2opt1, match2opt2, etc.]
    votes = ListField(DictField(), blank=True) 
    # [ {option1: total_votes, option2: total_votes, etc.}, {option1: total_votes, option2: total_votes, etc.}, etc.]
    totals = DictField()
    # {option1: total_votes, option2: total_votes, etc.}

class EndDisplay(EmbeddedDocument):
    winner = DictField() # {option: total_votes}
    top_three = ListField(DictField()) 
    # [{option: total_votes}, {option: total_votes}, {option: total_votes}]
    full_bracket = ListField(DictField()) 
    # [top_tier(winner), second_tier, etc. ] where each is {option: total_votes}



class Bracket(Document):
    key = StringField()
    title = StringField() # question for poll
    time_duration = IntField() # number in days
    num_rounds = IntField() # log2(options)
    round_duration = IntField() # number in days
    created_at = DateField() 
    end_display_format = StringField() # how to show the results: Top, winner, or Full
    private = BooleanField() # if public, anyone can vote
    active = BooleanField() # if winner chosen, active if false
    voting_options = EmbeddedDocumentField(BracketOptions)
    end_display = EmbeddedDocumentField(EndDisplay)

    def __str__(self):
        return self.title
