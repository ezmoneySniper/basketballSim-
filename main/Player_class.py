class Player:
	'''Instances of this class hold data from the players table for easier interaction'''
	def __init__(self, FirstName, LastName, Position, points_per_game):
		self.player_id = 0
		self.team_id = 0
		self.team_abbr = ""
		self.FirstName = FirstName
		self.LastName = LastName
		self.FullName = FirstName + " " + LastName
		self.Position = Position
		self.points_per_game = points_per_game
		self.assists_per_game = 0
		self.effective_field_goal_percentage = 0
		self.true_shooting_percentage = 0
		self.field_goal_attempts = 0
		self.field_goals_made = 0
		self.free_throw_attempts = 0
		self.free_throws_made = 0
		self.treys_made = 0
		self.off_reb_per_game = 0
		self.def_reb_per_game = 0
		self.points_produced = 0
		self.tov_per_game = 0
		self.offensive_win_share = 0
		self.defensive_win_share = 0
		self.total_win_share = 0
		self.player_usage = 0
		self.turnover = 0
		self.minutes = 0
		self.steals = 0
		self.blocks = 0
		self.fouls = 0
		self.win_share_normalized = 0

	def print_name(self):
		print (self.FullName)

	def print_points_per_game(self):
		print (self.points_per_game)

	def print_position(self):
		print (self.Position)

	#getters
	def get_player_id(self):
		return self.player_id

	def get_team_id(self):
		return self.team_id

	def get_team_abbr(self):
		return self.team_abbr

	def get_points(self):
		return self.points_per_game

	def get_assists_per_game(self):
		return self.assists_per_game

	def get_full_name(self):
		return self.FullName

	def get_field_goal_attempts(self):
		return self.field_goal_attempts

	def get_field_goals_made(self):
		return self.field_goals_made

	def get_free_throw_attempts(self):
		return self.free_throw_attempts

	def get_free_throws_made(self):
		return self.free_throws_made

	def get_treys_made(self):
		return self.treys_made

	def get_effective_field_goal_percentage(self):
		return self.effective_field_goal_percentage

	def get_true_shooting_percentage(self):
		return self.true_shooting_percentage

	def get_off_reb_per_game(self):
		return self.off_reb_per_game

	def get_def_reb_per_game(self):
		return self.def_reb_per_game

	def get_points_produced(self):
		return self.points_produced

	def get_tov_per_game(self):
		return self.tov_per_game

	def get_offensive_win_share(self):
		return self.offensive_win_share

	def get_defensive_win_share(self):
		return self.defensive_win_share

	def get_total_win_share(self):
		return self.total_win_share

	def get_player_usage(self):
		return self.player_usage

	def get_player_turnover(self):
		return self.turnover

	def get_player_minutes(self):
		return self.minutes

	def get_steals(self):
		return self.steals

	def get_blocks(self):
		return self.blocks

	def get_fouls(self):
		return self.fouls

	def get_win_share_normalized(self):
		return self.win_share_normalized

	#setters
	def set_player_id(self, value):
		self.player_id = value

	def set_team_id(self, value):
		self.team_id = value

	def set_team_abbr(self, value):
		self.team_abbr = value

	def set_true_shooting_percentage(self, value):
		self.true_shooting_percentage = value

	def set_effective_field_goal_percentage(self, value):
		self.effective_field_goal_percentage = value

	def set_field_goal_attempts(self, value):
		self.field_goal_attempts = value

	def set_field_goals_made(self, value):
		self.field_goals_made = value

	def set_free_throw_attempts(self, value):
		self.free_throw_attempts = value

	def set_free_throws_made(self, value):
		self.free_throws_made = value

	def set_treys_made(self, value):
		self.treys_made = value

	def set_points_per_game(self, value):
		self.points_per_game = value

	def set_assists_per_game(self, value):
		self.assists_per_game = value

	def set_off_reb_per_game(self, value):
		self.off_reb_per_game = value

	def set_def_reb_per_game(self, value):
		self.def_reb_per_game = value

	def set_points_produced(self, value):
		self.points_produced = value

	def set_tov_per_game(self, value):
		self.tov_per_game = value

	def set_offensive_win_share(self, value):
		self.offensive_win_share = value

	def set_defensive_win_share(self, value):
		self.defensive_win_share = value

	def set_total_win_share(self, value):
		self.total_win_share = value

	def set_player_usage(self,value):
		self.player_usage = value

	def set_turnover(self,value):
		self.turnover = value

	def set_minutes(self,value):
		self.minutes = value

	def set_steals(self, value):
		self.steals = value
	
	def set_blocks(self, value):
		self.blocks = value

	def set_fouls(self, value):
		self.fouls = value

	def set_win_share_normalized(self,value):
		self.win_share_normalized = value

	@classmethod
	def alt_init(cls, FirstName, LastName, Position):
		return cls(FirstName, LastName, Position, 0)
