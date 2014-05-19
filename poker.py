
def main():
	card_test()
	hand_test()

class Poker(object):
	def __init__(self,hands = []):
		self.hands = hands

	def get_winning_hand():
		pass

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
	h1 = ['AH','4H','2H','3H','5H']
	h2 = ['JH','4D','7H','6D','5D']
	h3 = ['TD','TC','TH','7C','7D']
	h4 = ['2C','3C','4C','5C','6S']
	h5 = ['AS','4S','5S','3S','2S']
	
	hands = [h1,h2,h3,h4,h5]	
	poker = Poker(hands)	

	#assert poker.get_winning_hand() == ''	
	
if __name__ == "__main__":
	main()

