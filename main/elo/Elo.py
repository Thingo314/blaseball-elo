class Elo:
	def __init__(self, k=5, default_rating=1500):
		self.ratings = {}
		self.k = k
		self.default_rating = default_rating
	
	def add_player(self, name):
		self.ratings[name] = self.default_rating
	
	def run_game(self, a, b, a_score, b_score):
		if a_score < b_score:
			self.update(b, a)
		else:
			self.update(a, b)

	def update(self, winner, loser):
		expectation = self.expected_result(winner, loser)
		self.ratings[winner] += self.k * (1 - expectation)
		self.ratings[loser] += self.k * (expectation - 1)
	
	def expected_result(self, a, b):
		exponent = (self.ratings[b] - self.ratings[a])/400.0
		return 1/(1+10**exponent)
