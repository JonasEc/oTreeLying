from __future__ import division

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import mathfilters

import os
import random	 
import numpy as np

import csv



from math import ceil

author = 'Jonas Mueller-Gastell'

doc = """
This is the main part of the experiment.
"""



class Constants(BaseConstants):
### Randomness	
	seeder = os.urandom(4)
	random.seed(seeder)


### Base constants
	name_in_url = 'Experiment'
	players_per_group = None
	num_rounds = 4

### TREATMENT:
	# manySteps = True
	# equalSpacing = True
	numberunderstandingquestions = 5
	numberOfDice = 10

### Money
	HIT = c(2)
	maxBonus = c(4)
	extraBonus = c(2)


## THRESHOLDS ARE UP TO AND INCLUDING!!!! NEED TO B E A T THE THRESHOLD TO GET HIGHER PRIZE

	thresholdsES = [20, 30, 40, 50]
	thresholdsRS = [30,33,36,39]
	thresholdsSB = [39]
	thresholdBonus = 60

	treatmentDict = {1:thresholdsES, 2:thresholdsRS, 3: thresholdsSB, 4: thresholdsES}
	# if equalSpacing == True:
	# 	thresholds = [20, 30, 40, 50]
	# else:
	# 	# with open('lying/probs.csv') as f:
	# 	# 	probs = csv.DictReader(f)

	# 	# 	counter = 1
	# 	# 	cumsum = 0
	# 	# 	thresholds = []
	# 	# 	for row in probs:
	# 	# 		cumsum += float(row["prob"])
	# 	# 		if cumsum > counter/5:
	# 	# 			thresholds.append(row["throw"])
	# 	# 			counter += 1

	# 	thresholds = [30,33,36,39]

#	paymentDict = {thresholds[k] : k/maxBonus for k in range(4)}

class Subsession(BaseSubsession):
	def before_session_starts(self):
	### randomize to treatments
		for player in self.get_players():
			allocation = [1, 2, 3, 4]
			allocation = np.random.permutation(allocation)
			player.participant.vars['allocation'] = list(allocation)
	## and the payment round
			payment = random.randint(1,4)
			player.participant.vars["paymentRound"] = payment

class Group(BaseGroup):
	pass

class Player(BasePlayer):
####### QUIZZ 
	truefalse1 = models.PositiveIntegerField(verbose_name="How many of your decisions, at most, will count for payment?")
	truefalse2 = models.BooleanField(choices=[[1, 'True'],[0, 'False']],widget=widgets.RadioSelect(),verbose_name="I can report any number ")
	truefalse3 = models.BooleanField(choices=[[1, 'True'],[0, 'False']],widget=widgets.RadioSelect(),verbose_name="")
	truefalse4 = models.BooleanField(choices=[[1, 'True'],[0, 'False']],widget=widgets.RadioSelect(),verbose_name="")
	truefalse5 = models.BooleanField(choices=[[1, 'True'],[0, 'False']],widget=widgets.RadioSelect(),verbose_name="")
	

######## ACTUAL DATA COLLECTED
	report = models.PositiveIntegerField(min=Constants.numberOfDice,max=Constants.numberOfDice*6)

	belief = models.PositiveIntegerField(min=Constants.numberOfDice,max=Constants.numberOfDice*6)


######## Survey
	impactBelief   = models.PositiveIntegerField(verbose_name="My choices were impacted by what I THOUGHT other participants chose.", choices=[[1,"Strongly Disagree"],[2, "Disagree"],[3, "Neutral"],[4, "Agree"],[5,"Strongly Agree"]], widget=widgets.RadioSelectHorizontal())
	impactFair     = models.PositiveIntegerField(verbose_name="My choices were impacted by what I thought was fair.", choices=[[1,"Strongly Disagree"],[2, "Disagree"],[3, "Neutral"],[4, "Agree"],[5,"Strongly Agree"]], widget=widgets.RadioSelectHorizontal())
	impactNice     = models.PositiveIntegerField(verbose_name="My choices were impacted by what I thought was nice.", choices=[[1,"Strongly Disagree"],[2, "Disagree"],[3, "Neutral"],[4, "Agree"],[5,"Strongly Agree"]], widget=widgets.RadioSelectHorizontal())
	impactGoodLook = models.PositiveIntegerField(verbose_name="My choices were impacted by what I thought looked good to others.", choices=[[1,"Strongly Disagree"],[2, "Disagree"],[3, "Neutral"],[4, "Agree"],[5,"Strongly Agree"]], widget=widgets.RadioSelectHorizontal())

	sex = models.PositiveIntegerField(verbose_name="What is your sex?", choices=[[0,"Female"], [1,"Male"], [2, "Decline To State or Other"]], widget=widgets.RadioSelect())
	age = models.PositiveIntegerField(verbose_name="What is your age (in years)?")
	school = models.PositiveIntegerField(verbose_name="If you have a bachelor's degree or are pursuing one, in what school was your degree program (or will your expected degree program be)?", choices=[[1, "School of Business"],[2, "School of Eath Sciences"], [3,"School of Education"],[4, "School of Engineering"], [5,"School of Humanities & Sciences"], [6,"School of Law"], [7,"School of Medicine"], [8 ,"Unknown"]], widget=widgets.RadioSelect())
	income = models.CurrencyField(verbose_name="What is your household income?")




	# def set_threshold(self):
	# 	alloc = self.participant.vars.get("allocation")
	# 	thresholds = Constants.TreatmentDic[alloc[self.round_number-1]]
	# 	if alloc[self.round_number] == 4:
	# 		self.bonusThresh = Constants.thresholdBonus
	# 	# else:
	# 	# 	self.bonusThresh = False
	# 	return thresholds#, self.bonusThresh

### SET PAYOFF
	totalPayoff = models.CurrencyField()

	def set_payoffs(self):
		if self.participant.vars.get("paymentRound") == self.round_number:
			alloc = self.participant.vars.get("allocation")
			thresholds = Constants.treatmentDict[alloc[self.round_number-1]]
			if self.participant.vars.get("allocation") in [1,2,4]:
				if self.report <= thresholds[0]:
					bonus = c(0)
				elif self.report <= thresholds[1] and self.report > thresholds[0]:
					bonus = Constants.maxBonus/4
				elif self.report <= thresholds[2] and self.report > thresholds[1]:
					bonus = 2*Constants.maxBonus/4
				elif self.report <= thresholds[3] and self.report > thresholds[2]:
					bonus = 3*Constants.maxBonus/4
				elif self.report <= self.report > thresholds[3]:
					bonus = 4*Constants.maxBonus/4
			else:
				if self.report <= thresholds[0]:
					bonus = c(0)
				elif self.report > thresholds[0]:
					bonus = Constants.maxBonus

			if self.participant.vars.get("allocation") == 4 and self.report >= Constants.thresholdBonus:
				bonusExtra = Constants.bonusExtra
			else:
				bonusExtra = c(0)

			self.payoff = bonus + bonusExtra	
			
		else:	
			self.payoff = c(0)


		return self.payoff

	def set_total_payoff(self):
		self.totalPayoff = sum([p.payoff for p in self.in_all_rounds()])
		return self.totalPayoff

