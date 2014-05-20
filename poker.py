'''
Created on May 19, 2014

@author: pavan
'''

import copy

def main():
	card_test()
	hand_test()
	poker_test()
	
	print('round 1')	
	h1 = Hand('AH 4H 2H 3H 5H')
	h2 = Hand('JH 4D 7H 6D 5D')
	h3 = Hand('TD TC TH 7C 7D')
	h4 = Hand('2C 3C 4C 5C 6S')
	h5 = Hand('AS 4S 5S 3S 2S')
	hands = [h1,h2,h3,h4,h5]
	poker = Poker(hands)
	print poker.get_winning_hand()
	
	print('round 2')	
	h1 = Hand('2S 5S 4H 6C 3D')
	h2 = Hand('AC 3H 4S KD 6D')
	h3 = Hand('AH AS JS KH KS')
	h4 = Hand('5C 4D 3S 2C AD')
	h5 = Hand('7H 7C JD 5H 2D')
	hands = [h1,h2,h3,h4,h5]
	poker = Poker(hands)
	print poker.get_winning_hand()
	
	print('round 3')	
	h1 = Hand('6H 6S KD KH KS')
	h2 = Hand('JH JS JD TH TS')
	h3 = Hand('5H 4H 3S 2S AH')
	h4 = Hand('AD KC JC 5C 2D')
	h5 = Hand('AC QH QD QS QC')
	hands = [h1,h2,h3,h4,h5]
	poker = Poker(hands)
	print poker.get_winning_hand()

class Poker(object):
	'''
	poker constructor
	''' 
	def __init__(self,hands = []):
		self.hands = hands

	def get_highest_rank_card_hand(self,hands):
		'''
		find hand with the highest rank card among all hands
		''' 
		maxrank = 0
		high_hand = ''
		for hand in hands:
			if(max(hand.ranks) > maxrank):
				maxrank = max(hand.ranks)
		for hand in hands:
			if max(hand.ranks) == maxrank:
				high_hand = high_hand + hand.cardlist + ','		#comma separated if more than one
		if high_hand[-1] == ',':
			high_hand = high_hand[:-1]		#remove trailing comma, if exists
		return high_hand

	def break_tie(self,hands):
		'''
		break tie and compute winning hand
		''' 
		winning_hand = ''
		card_type = hands[0].handtype
		if(card_type == 1):			#royal flush. All royal flush(s) are winning hands
			for hand in hands:
				winning_hand = winning_hand + hand.cardlist + ','
				
		elif(card_type == 2):		#straight flush
			maxrank = 0
			winning_hand = ''
			for hand in hands:
				if(max(hand.ranks) > maxrank and max(hand.ranks) != 14):	#A has value 1, if A = 14 it's a royal flush
					maxrank = max(hand.ranks)
				else:
					maxrank = sorted(hand.ranks)[-2]	#choose second highest rank i.e. consider A = 1
			for hand in hands:
				if (max(hand.ranks) == maxrank and max(hand.ranks) != 14) or ((sorted(hand.ranks)[-2] == maxrank and max(hand.ranks) == 14)) :
					winning_hand = winning_hand + hand.cardlist + ','		#highest ranked straight flush, all having highest ranked s.flush
					
		elif(card_type in [3,4,9]):		#Four or a kind, full house, one pair
			#highest ranked group1 cards as winning hand
			#if group1 tied, highest ranked group2 cards as winning hand
			#group1 - four of a kind ranks, 3 of a kind rank in full house, one pair rank
			#group2 - fifth card rank, pair in full house rank, highest ranked card in remaining cards
			max_group1_card = 0
			max_group2_card = 0
			for hand in hands:
				if hand.info['group1'] > max_group1_card:
					max_group1_card = hand.info['group1']
				if hand.info['group2'] > max_group2_card:
					max_group2_card = hand.info['group2']
			cnt = 0
			winning_hand = ''
			for hand in hands:
				if hand.info['group1'] == max_group1_card:
					cnt += 1
					if cnt > 1:
						winning_hand = ''
						break;					
					winning_hand = hand.cardlist	
			if cnt > 1:	
				for hand in hands:
					if hand.info['group2'] == max_group2_card and hand.info['group1'] == max_group1_card:
						winning_hand = winning_hand + hand.cardlist + ','
						
		elif(card_type in [5,10]): 		#Flush, high card
			winning_hand = self.get_highest_rank_card_hand(hands)
			
		elif(card_type == 6):		#straight
			maxrank = 0			
			for hand in hands:				
				mx = max(hand.ranks)
				if hand.info['A_val'] == 1:		#value of A in hand
					mx  = sorted(hand.ranks)[-2]	#second highest rank in hand, i.e. consider A = 1
				if(mx > maxrank):
					maxrank = mx
			for hand in hands:
				mx = max(hand.ranks)
				if hand.info['A_val'] == 1:
					mx  = sorted(hand.ranks)[-2]
				if mx == maxrank:
					winning_hand = winning_hand + hand.cardlist + ','		#hand(s) with highest ranked hand 
					
		elif(card_type == 7):		#three of a kind
			max_group1_card = 0			
			for hand in hands:
				if hand.info['group1'] > max_group1_card:	
					max_group1_card = hand.info['group1']				
			for hand in hands:
				if hand.info['group1'] == max_group1_card:
					winning_hand = winning_hand + hand.cardlist + ','     #highest ranked three of a kind rank as winning hand(s)
					
		elif(card_type == 8):		#Two pair
			#highest ranked first pair card ranks (group1) as winning hand
			#if first pair tied, second highest ranked second pair card ranks (group2) cards as winning hand
			#if first and second pair tied, highest fifth card rank as winning hand(s)
			max_group1_card = 0
			max_group2_card = 0
			max_group3_card = 0
			for hand in hands:
				if hand.info['group1'] > max_group1_card:
					max_group1_card = hand.info['group1']
				if hand.info['group2'] > max_group2_card:
					max_group2_card = hand.info['group2']
				if hand.info['group3'] > max_group3_card:
					max_group3_card = hand.info['group3']
			cnt1 = 0
			winning_hand = ''
			for hand in hands:
				if hand.info['group1'] == max_group1_card:
					cnt1 += 1
					if cnt1 > 1:
						winning_hand = ''
						break;					
					winning_hand = hand.cardlist
			cnt2 = 0	
			if cnt1 > 1:	
				for hand in hands:
					if hand.info['group2'] == max_group2_card and hand.info['group1'] == max_group1_card:
						cnt2 += 1
						if cnt2 > 1:
							winning_hand = ''
							break;					
						winning_hand = hand.cardlist
				if cnt2 > 1:		
					for hand in hands:
						if hand.info['group3'] == max_group3_card and hand.info['group2'] == max_group2_card and hand.info['group1'] == max_group1_card:
							winning_hand = winning_hand + hand.cardlist + ','
							
		else:
			winning_hand = ','		
			
		if winning_hand[-1] == ',':
			winning_hand = winning_hand[:-1]	#removing trailing comma
		return winning_hand

	def get_winning_hand(self):
		'''
		compute the winning hand among all hands
		''' 
		handtypes = []
		hands_tied = []
		for hand in self.hands:
			handtypes.append(hand.handtype)
		mintype = min(handtypes)
		for hand in self.hands:
			if(hand.handtype == mintype):
				hands_tied.append(hand)
		if(len(hands_tied) == 1):
			return hands_tied[0].cardlist		#only one highest hand type, wins
		else:
			return self.break_tie(hands_tied)		#break tie of highest hand type if more than one hand of certain hand type						

class Hand(object):
	
	def is_royal_flush(self):
		return min(self.ranks) == 10 and max(self.ranks) == 14 and len(set(self.suits)) == 1 and len(set(self.ranks)) == 5

	def is_straight_flush(self):
		mx = max(self.ranks)
		mn = min(self.ranks)
		if(mx == 14):	#A cannot be 14 in straight flush, if it does it will be a royal flush
			mn = 1
		mx = sorted(self.ranks)[-2]
		return (abs(mx-mn)) == 4 and len(set(self.suits)) == 1 and len(set(self.ranks)) == 5 

	def is_kind(self,n):
   		for r in self.ranks:
			if self.ranks.count(r) == n: 
				return True
		return False

	def is_full_house(self):
		return self.is_kind(3) and self.is_kind(2)

	def is_flush(self):
		return len(set(self.suits)) == 1

	def is_straight(self):
		rks =  copy.deepcopy(self.ranks)
		self.info['A_val'] = 14 	#value of A 
		if(2 in rks):	#A can have value 1 only if 2 exists in a straight
			rks.append(1)  		
			if 14 in rks: rks.remove(14)
			self.info['A_val'] = 1		#value of A in the hand e.g A=1 in 5H, 4A, 3S, 2S, AC 			
		return (max(rks) - min(rks)) == 4 and len(set(rks)) == 5

	def is_two_pair(self):
		return self.is_kind(2) and len(set(self.ranks)) == 3
	
	def is_one_pair(self):
		return self.is_kind(2) and len(set(self.ranks)) != 3	

	def get_hand_type(self):
		'''
		compute the type of hand e.g. full house - 4, flush - 5 etc.
		''' 
		if(self.is_royal_flush()):
			return 1
		elif(self.is_straight_flush()):
			return 2
		elif(self.is_kind(4)):
			for r in self.ranks:
				if self.ranks.count(r) == 4: 
					self.info['group1'] = r		#rank of four of a kind card
				elif self.ranks.count(r) == 1:
					self.info['group2'] = r		#rank of fifth card
			return 3
		elif(self.is_full_house()):
			for r in self.ranks:
				if self.ranks.count(r) == 3: 
					self.info['group1'] = r		#rank of 3 cards of same rank
				elif self.ranks.count(r) == 2:
					self.info['group2'] = r		#rank of remaining 2 cards of same rank
			return 4
		elif(self.is_flush()):
			return 5
		elif(self.is_straight()):
			return 6
		elif(self.is_kind(3)):
			for r in self.ranks:
				if self.ranks.count(r) == 3: 
					self.info['group1'] = r		#rank of three of a kind cards
			return 7
		elif(self.is_two_pair()):
			rks = sorted(copy.deepcopy(self.ranks), reverse=True)
			for r in rks:
				if rks.count(r) == 2: 
					self.info['group1'] = r		#rank of first pair
					break	
			rks.remove(r)
			rks.remove(r)
			for r in rks:
				if rks.count(r) == 2: 
					self.info['group2'] = r		#rank of second pair
					break
			rks.remove(r)
			rks.remove(r)
			self.info['group3'] = max(rks)		#rank of fifth card
			return 8
		elif(self.is_one_pair()):
			rks = copy.deepcopy(self.ranks)
			for r in rks:
				if self.ranks.count(r) == 2: 
					self.info['group1'] = r		#rank of pair
					break
			rks.remove(r)
			rks.remove(r)
			self.info['group2'] = max(rks)		#highest rank of remaining cards		
			return 9
		else:
			return 10		

	'''
	hand constructor
	''' 
	def __init__(self,cards = ''):
		self.cards = []
		self.info = {}	#additional information about the hand, optional
		self.cardlist = cards	
		for c in cards.split():
			self.cards.append(Card(c))		
		self.ranks = []
		self.suits = []
		for c in self.cards:
			self.ranks.append(c.rank)
			self.suits.append(c.suit)
		self.handtype = self.get_hand_type()	#type of hand e.g. full house, flush

class Card(object):
	'''
	compute rank of card
	''' 
	def rank(self,char):
		cards = '2 3 4 5 6 7 8 9 T J Q K A'.split()
		return cards.index(char) + 2 #0 based index
	
	'''
	card constructor
	''' 
	def __init__(self, val=''):
		self.val = val
		self.rank = self.rank(val[0])
		self.suit = val[1]

def card_test():
	c = Card('AH')
	assert c.rank == 14
	assert c.suit == 'H'	

	c = Card('4D')
	assert c.rank == 4
	assert c.suit == 'D'

def hand_test():
	royal_flush = Hand('AS KS QS JS TS')
	straight_flush = Hand('5S 4S 3S 2S AS')
	four_of_kind = Hand('AH AS AD AC KH')
	full_house = Hand('AH AS AD KH KS')
	flush = Hand('AS TS 2S 5S 6S')
	straight = Hand('5H 4A 3S 2S AC')
	three_of_kind = Hand('AH AS AC KH QC')
	two_pair = Hand('AH AC KH KS QC')
	one_pair = Hand('AH AS KH QS JD')
	high_card = Hand('AH KS JD 5H 2D')

	#tests for hand types
	assert royal_flush.is_royal_flush() == True
	assert straight_flush.is_straight_flush() == True
	assert four_of_kind.is_kind(4) == True
	assert full_house.is_full_house() == True
	assert flush.is_flush() == True
	assert straight.is_straight() == True
	assert three_of_kind.is_kind(3) == True
	assert two_pair.is_two_pair() == True
	assert one_pair.is_one_pair() == True

	#tests for computing hand types e.g. royal flush, full house
	assert royal_flush.get_hand_type() == 1
	assert straight_flush.get_hand_type() == 2
	assert four_of_kind.get_hand_type() == 3
	assert full_house.get_hand_type() == 4
	assert flush.get_hand_type() == 5
	assert straight.get_hand_type() == 6
	assert three_of_kind.get_hand_type() == 7
	assert two_pair.get_hand_type() == 8
	assert one_pair.get_hand_type() == 9

def poker_test():
	royal_flush = Hand('AS KS QS JS TS')
	straight_flush = Hand('5S 4S 3S 2S AS')
	four_of_kind = Hand('AH AS AD AC KH')
	full_house = Hand('AH AS AD KH KS')
	flush = Hand('AS TS 2S 5S 6S')
	straight = Hand('5H 4A 3S 2S AC')
	three_of_kind = Hand('AH AS AC KH QC')
	two_pair = Hand('AH AC KH KS QC')
	one_pair = Hand('AH AS KH QS JD')
	high_card = Hand('AH KS JD 5H 2D')		

	#get highest ranked card test
	straight_flush1 = Hand('6S 5S 4S 3S 2S')
	hands = [straight_flush, straight_flush1]
	poker = Poker(hands)
	assert poker.get_highest_rank_card_hand(hands) == '5S 4S 3S 2S AS'

	#royal flush tie test
	royal_flush1 = Hand('AH KH QH JH TH')
	hands = [royal_flush,royal_flush1]
	poker = Poker(hands)
	assert poker.break_tie(hands) == 'AS KS QS JS TS,AH KH QH JH TH'

	#straight flush tie test
	straight_flush1 = Hand('6S 5S 4S 3S 2S')
	hands = [straight_flush, straight_flush1]
	poker = Poker(hands)
	assert poker.break_tie(hands) == '6S 5S 4S 3S 2S'

	#four of a kind test - four of a kind card tie
	four_of_kind1 = Hand('2H 2S 2D 2C 3H')
	hands = [four_of_kind,four_of_kind1]
	poker = Poker(hands)
	assert poker.break_tie(hands) == 'AH AS AD AC KH'
	
	#four of a kind test - fifth card tie
	four_of_kind1 = Hand('AH AS AD AC 3H')
	hands = [four_of_kind,four_of_kind1]
	poker = Poker(hands)
	assert poker.break_tie(hands) == 'AH AS AD AC KH'	

	#full house test - three of a kind card tie
	full_house1 = Hand('KH, KS, KD, AH, AS')
	hands = [full_house, full_house1]
	poker = Poker(hands)
	assert poker.break_tie(hands) == 'AH AS AD KH KS'
	
	#full house test - pair tie
	full_house1 = Hand('AH, AS, AD, 3H, 3S')
	hands = [full_house, full_house1]
	poker = Poker(hands)
	assert poker.break_tie(hands) == 'AH AS AD KH KS'

	#flush  tie test - highest rank
	flush1 = Hand('4S 6S 2S 5S 6S')
	hands = [flush, flush1]
	poker = Poker(hands)
	assert poker.break_tie(hands) == 'AS TS 2S 5S 6S'
	
	#flush  tie test - same highest rank hands
	flush1 = Hand('AH TH 2H 5H 6H')
	hands = [flush, flush1]
	poker = Poker(hands)
	assert poker.break_tie(hands) == 'AS TS 2S 5S 6S,AH TH 2H 5H 6H'

	#straight  tie test - Ace as 1
	straight1 = Hand('7H 6A 5S 4S 3C')
	hands = [straight, straight1]
	poker = Poker(hands)
	assert poker.break_tie(hands) == '7H 6A 5S 4S 3C'

	#straight  tie test - Ace as 14
	straight1 = Hand('AH KS QS JS TC')
	hands = [straight, straight1]
	poker = Poker(hands)
	assert poker.break_tie(hands) == 'AH KS QS JS TC'

	#three of a kind  tie test - highest three of a kind card rank 
	three_of_kind1 = Hand('2H 2S 2C KH QC')
	hands = [three_of_kind,three_of_kind1]
	poker = Poker(hands)
	assert poker.break_tie(hands) == 'AH AS AC KH QC'
	
	#three of a kind  tie test - three of a kind card rank tie (rules not specified, assumption all highest hands win)
	three_of_kind1 = Hand('AH AS AC 2H 3C')
	hands = [three_of_kind,three_of_kind1]
	poker = Poker(hands)
	assert poker.break_tie(hands) == 'AH AS AC KH QC,AH AS AC 2H 3C'

	#two pair tie test - highest first pair hand wins
	two_pair1 = Hand('2H 2C TH TS QC')
	hands = [two_pair,two_pair1]
	poker = Poker(hands)
	assert poker.break_tie(hands) == 'AH AC KH KS QC'
	
	#two pair tie test - first pair tie, highest second pair hand wins
	two_pair1 = Hand('AH AC 2H 2S QC')
	hands = [two_pair,two_pair1]
	poker = Poker(hands)
	assert poker.break_tie(hands) == 'AH AC KH KS QC'

	#two pair tie test - first and second pair tie, highest fifth card hand wins
	two_pair1 = Hand('AH AC KH KS 4C')
	hands = [two_pair,two_pair1]
	poker = Poker(hands)
	assert poker.break_tie(hands) == 'AH AC KH KS QC'
	
	#high card tie test - highest ranked hand wins
	high_card1 = Hand('QH KS JD 5H 2D')		
	hands = [high_card,high_card1]
	poker = Poker(hands)
	assert poker.break_tie(hands) == 'AH KS JD 5H 2D'

	#one pair tie test - highest ranked pair wins
	one_pair1 = Hand('2H 2S KH QS JD')
	hands = [one_pair,one_pair1]
	poker = Poker(hands)
	assert poker.break_tie(hands) == 'AH AS KH QS JD'
	
	#one pair tie test - highest ranked pair tie, highest ranked remaining cards win
	one_pair1 = Hand('AH AS 2H 3S 4D')
	hands = [one_pair,one_pair1]
	poker = Poker(hands)
	assert poker.break_tie(hands) == 'AH AS KH QS JD'

	#winning hand test - without ties
	hands = [full_house,flush,straight]	
	poker = Poker(hands)	
	assert poker.get_winning_hand() == 'AH AS AD KH KS'	
	
if __name__ == "__main__":
	main()

