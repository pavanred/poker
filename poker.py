
def main():
	card_test()
	hand_test()
	poker_test()

class Poker(object):
	def __init__(self,hands = []):
		self.hands = hands

	def get_highest_rank_card_hand(self,hands):
		maxrank = 0
		high_hand = ''
		for hand in hands:
			if(max(hand.ranks) > maxrank):
				maxrank = max(hand.ranks)
		for hand in hands:
			if max(hand.ranks) == maxrank:
				high_hand = high_hand + hand.cardlist + ','
		if high_hand[-1] == ',':
			high_hand = high_hand[:-1]
		return high_hand

	def break_tie(self,hands):
		winning_hand = ''
		card_type = hands[0].handtype
		if(card_type in [1]):
			for hand in hands:
				winning_hand = winning_hand + hand.cardlist + ','
		elif(card_type in [2]):
			winning_hand = self.get_highest_rank_card_hand(hands)
		elif(card_type == 3):
			max_four_card = 0
			max_fifth_card = 0
			for hand in hands:
				if hand.info['four_card_rank'] > max_four_card:
					max_four_card = hand.info['four_card_rank']
				if hand.info['fifth_card_rank'] > max_fifth_card:
					max_fifth_card = hand.info['fifth_card_rank']
			cnt = 0
			winning_hand = ''
			for hand in hands:
				if hand.info['four_card_rank'] == max_four_card:
					if cnt > 1:
						break;
					cnt += 1
					winning_hand = hand.cardlist		
			for hand in hands:
				if hand.info['fifth_card_rank'] == max_fifth_card and hand.info['four_card_rank'] == max_four_card:
					winning_hand = winning_hand + hand.cardlist + ','
		if winning_hand[-1] == ',':
			winning_hand = winning_hand[:-1]
		return winning_hand

	def get_winning_hand(self):
		handtypes = []
		hands_tied = []
		for hand in self.hands:
			handtypes.append(hand.handtype)
		mintype = min(handtypes)
		for hand in self.hands:
			if(hand.handtype == mintype):
				hands_tied.append(hand)
		if(len(hands_tied) == 1):
			return hands_tied[0].cardlist
		else:
			return self.break_tie(hands_tied)							

class Hand(object):
	
	def is_royal_flush(self):
		return min(self.ranks) == 10 and max(self.ranks) == 14 and len(set(self.suits)) == 1 and len(set(self.ranks)) == 5

	def is_straight_flush(self):
		rks = self.ranks
		for i in range(0,5):
			rks[i] = rks[i]%13
		return (max(rks)-min(rks)) == 4 and len(set(self.suits)) == 1 and len(set(self.ranks)) == 5 

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
		rks = self.ranks
		if(14 in rks):
			rks.append(1)
		return (max(rks) - min(rks)) == 4 and len(set(rks)) == 5

	def is_two_pair(self):
		return self.is_kind(2) and len(set(self.ranks)) == 3
	
	def is_one_pair(self):
		return self.is_kind(2) and len(set(self.ranks)) != 3	

	def get_hand_type(self):
		if(self.is_royal_flush()):
			return 1
		elif(self.is_straight_flush()):
			return 2
		elif(self.is_kind(4)):
			for r in self.ranks:
				if self.ranks.count(r) == 4: 
					self.info['four_card_rank'] = r
				elif self.ranks.count(r) == 1:
					self.info['fifth_card_rank'] = r	
			return 3
		elif(self.is_full_house()):
			return 4
		elif(self.is_flush()):
			return 5
		elif(self.is_straight()):
			return 6
		elif(self.is_kind(3)):
			return 7
		elif(self.is_two_pair()):
			return 8
		elif(self.is_one_pair()):
			return 9
		else:
			return 10		

	def __init__(self,cards = ''):
		self.cards = []
		self.info = {}
		self.cardlist = cards
		for c in cards.split():
			self.cards.append(Card(c))		
		self.ranks = []
		self.suits = []
		for c in self.cards:
			self.ranks.append(c.rank)
			self.suits.append(c.suit)
		self.handtype = self.get_hand_type()

class Card(object):
	def rank(self,char):
		cards = '2 3 4 5 6 7 8 9 T J Q K A'.split()
		return cards.index(char) + 2 #0 based index
	
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

	assert royal_flush.is_royal_flush() == True
	assert straight_flush.is_straight_flush() == True
	assert four_of_kind.is_kind(4) == True
	assert full_house.is_full_house() == True
	assert flush.is_flush() == True
	assert straight.is_straight() == True
	assert three_of_kind.is_kind(3) == True
	assert two_pair.is_two_pair() == True
	assert one_pair.is_one_pair() == True

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

	straight_flush1 = Hand('6S 5S 4S 3S 2S')
	hands = [straight_flush, straight_flush1]
	poker = Poker(hands)
	assert poker.get_highest_rank_card_hand(hands) == '6S 5S 4S 3S 2S'

	royal_flush1 = Hand('AH KH QH JH TH')
	hands = [royal_flush,royal_flush1]
	poker = Poker(hands)
	assert poker.break_tie(hands) == 'AS KS QS JS TS,AH KH QH JH TH'

	straight_flush1 = Hand('6S 5S 4S 3S 2S')
	hands = [straight_flush, straight_flush1]
	poker = Poker(hands)
	assert poker.break_tie(hands) == '6S 5S 4S 3S 2S'

	four_of_kind1 = Hand('AH AS AD AC 3H')
	hands = [four_of_kind,four_of_kind1]
	poker = Poker(hands)
	print poker.break_tie(hands)
	assert poker.break_tie(hands) == 'AH AS AD AC KH'

	four_of_kind1 = Hand('2H 2S 2D 2C 3H')
	hands = [four_of_kind,four_of_kind1]
	poker = Poker(hands)
	print poker.break_tie(hands)
	assert poker.break_tie(hands) == 'AH AS AD AC KH'

	
	

	hands = [full_house,flush,straight]	
	poker = Poker(hands)	
	assert poker.get_winning_hand() == 'AH AS AD KH KS'
	
if __name__ == "__main__":
	main()

