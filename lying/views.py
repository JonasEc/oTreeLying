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
	def vars_for_template(self):
		return {"extra": Constants.maxBonus + Constants.extraBonus}

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
		if values["truefalse3"] != True:
			summand += 1
		if values["truefalse4"] != 12:
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
class rule1(Page):
	def is_displayed(self):
		return Constants.First
	def vars_for_template(self):
		alloc = self.player.participant.vars.get("allocation")
		threshold = Constants.treatmentDict[alloc[self.round_number-1]]
		if alloc[self.round_number-1] == 4:
			bonusThresh = True
		else:
			bonusThresh = False 
		return {"BonusShare": Constants.maxBonus/len(threshold), "thresholds": threshold, "BonusThresh": bonusThresh }
	
class rule2(Page):
	def is_displayed(self):
		return not Constants.First
	def vars_for_template(self):
		alloc = self.player.participant.vars.get("allocation")
		threshold = Constants.treatmentDict[alloc[self.round_number-1]]
		if alloc[self.round_number-1] == 4:
			bonusThresh = True
		else:
			bonusThresh = False 
		return {"BonusShare": Constants.maxBonus/len(threshold), "thresholds": threshold, "BonusThresh": bonusThresh }




class throwDice(Page):
	form_model = models.Player
	def get_form_fields(self):
		fields_to_show=[]
		for die in range(1,Constants.numberOfDice+1):
			fields_to_show.append('die{}'.format(die))
		return fields_to_show
	def before_next_page(self):
		a = [self.player.die1,self.player.die2,self.player.die3,self.player.die4,self.player.die5,self.player.die6,self.player.die7,self.player.die8,self.player.die9,self.player.die10]
		if all(a):
			self.player.sumOfThrows = sum(a)

class outcomeCalc(Page):
	def is_displayed(self):
		return self.player.sumOfThrows
	def vars_for_template(self):
		return {"result": self.player.sumOfThrows}



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

class done(Page):
	pass

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
	welcome,
	IRB,
	instructions,
	quizz,
	rule1,
	throwDice,
	outcomeCalc,
	rule2,
	report,
	done,
	survey1,
	survey2,
	payment
]
