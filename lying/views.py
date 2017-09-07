from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

import mathfilters

### INTRO PAGES

class welcome(Page):
	def is_displayed(self):
		return self.round_number == 1

class IRB(Page):
	def is_displayed(self):
		return self.round_number == 1

class instructions(Page):
	def is_displayed(self):
		return self.round_number == 1

class quizz(Page):
	def is_displayed(self):
		return self.round_number == 1

	form_model = models.Player
	def get_form_fields(self):
		fields_to_show=[]
		for key in range(1,Constants.numberunderstandingquestions+1):
			fields_to_show.append('truefalse{}'.format(key))
		return fields_to_show
	def error_message(self, values):
		summand = 0
		if values["truefalse1"] != 1:
			summand += 1
		if values["truefalse2"] != True:
			summand += 1
		if values["truefalse3"] != False:
			summand += 1
		if values["truefalse4"] != False:
			summand += 1
		if values["truefalse5"] != False:
			summand += 1		
		if summand > 1:	
			return 'Sorry, you got ' + str(summand) + " questions wrong."
			summand = 0
		elif summand == 1:
			summand = 0
			return 'Almost there! You just got one question wrong!'
		
		

#### MAIN PAGES

class report(Page):
	form_model = models.Player 
	form_fields = ['report', 'belief']
	def vars_for_template(self):
		alloc = self.player.participant.vars.get("allocation")
		threshold = Constants.treatmentDict[alloc[self.round_number-1]]
		if alloc[self.round_number-1] == 4:
			bonusThresh = True
		else:
			bonusThresh = False 
		return {"BonusShare": Constants.maxBonus/len(threshold), "thresholds": threshold, "BonusThresh": bonusThresh }
	
	def before_next_page(self):
		self.player.set_payoffs()


##### SURVEY PAGES

class survey1(Page):
	def is_displayed(self):
		return self.round_number == Constants.num_rounds

	form_model = models.Player
	form_fields = ['impactBelief', 'impactFair', 'impactNice', 'impactGoodLook']


class survey2(Page):
	def is_displayed(self):
		return self.round_number == Constants.num_rounds

	form_model = models.Player
	form_fields = [ 'sex', 'age', 'school', 'income']




class payment(Page):
	def is_displayed(self):
		return self.round_number == Constants.num_rounds
	def vars_for_template(self):
		total = self.player.set_total_payoff()
		if total > c(0):
			postivieBonus = True
		else:
			postivieBonus = False

		return {"payoff": self.player.payoff, "paymentTotal": self.player.totalPayoff + Constants.HIT, "postivieBonus": postivieBonus}




page_sequence = [
	# welcome,
	# IRB,
	# instructions,
	# quizz,
	report,
	survey1,
	survey2,
	payment
]
