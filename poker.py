
def main():
	card_test()

class Poker(object):
	def __init__(self,hands = []):
		self.hands = hands

	def get_winning_hand():
		return 1

class Hand(object):
	
	def is_royal_flush():
		return min(self.ranks) == 10 and max(self.ranks) == 14 and len(set(self.suits)) == 1

	def is_straight_flush():
		return (max(self.ranks) - min(self.ranks) == 4) and len(set(self.suits)) == 1 and max(self.ranks) != 14

	def is_kind(n):
   		for r in self.ranks:
			if self.ranks.count(r) == n: 
				return True
		return False

	def is_full_house():
		return is_kind(3) and is_kind(2)

	def is_flush():
		return len(set(self.suits)) == 1

	def is_straight():
		minrank = min(self.ranks)
		for r in sorted(self.ranks):
			if minrank != minrank: 
				return False
			minrank = minrank + 1
		return True

	def is_two_pair():
		return is_kind(2) and len(set(self.ranks)) == 3
	
	def is_one_pair():
		return is_kind(2) and len(set(self.ranks)) != 3	

	def get_hand_type():
		if(is_royal_flush()):
			return 1
		elif(is_straight_flush()):
			return 2
		elif(is_kind(4)):
			return 3
		elif(is_full_house()):
			return 4
		elif(is_flush()):
			return 5
		elif(is_straight()):
			return 6
		elif(is_kind(3)):
			return 7
		elif(is_two_pair()):
			return 8
		elif(is_one_pair()):
			return 9
		else:
			return 10		

	def __init__(self,cards = '',ranks='',suits='',handtype=''):
		self.cards = []
		for c in cards.split():
			self.cards.append(Card(c))
		
		self.ranks = []
		self.suits = []
		for c in cards:
			self.ranks.append(c.rank)
			self.suits.append(c.suit)
		self.handtype = get_hand_type()

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
	handt = Hand('AS KS QS JS TS')
	handf = Hand('AH KS QS JS TS')
	assert handt.is_royal_flush() == True
	assert handf.is_royal_flush() == False
	
	handt = Hand('5S 4S 3S 2S AS')
	handf = Hand('5H 4S 3S 2S AS')
	assert handt.is_straight_flush() == True
	assert handf.is_straight_flush() == False

	hand = Hand('AH AS AD AC KH')
	assert hand.is_kind(4) == True

	hand = Hand('AH AS AD AC KH')
	assert hand.is_kind(4) == True
	
		

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

