"""Player Manager module"""
from Player_class import Player
from Team_class import Team

class PlayerManager:
    """Contains methods that create and modify player objects"""

    @classmethod
    def make_player(cls, raw_player):
        """create and return a new player from the given info"""
        first_name = raw_player['FirstName']
        last_name = raw_player['LastName']
        position = raw_player['Position']
        player_id = raw_player['ID']

        player = Player.alt_init(first_name, last_name, position)
        player.set_player_id(player_id)

        return player

    @classmethod
    def stats_filler(cls, raw_stats, player):
        """grab statistics from 2016-2017 season for the given player"""
        points_per_game = float(raw_stats['PtsPerGame']['#text'])
        assists_per_game = float(raw_stats['AstPerGame']['#text'])
        field_goal_attempts = float(raw_stats['FgAttPerGame']['#text'])
        field_goals_made = float(raw_stats['FgMadePerGame']['#text'])
        free_throw_attempts = float(raw_stats['FtAttPerGame']['#text'])
        free_throws_made = float(raw_stats['FtMadePerGame']['#text'])
        treys_made = float(raw_stats['Fg3PtMadePerGame']['#text'])
        off_reb_per_game = float(raw_stats['OffRebPerGame']['#text'])
        tov_per_game = float(raw_stats['TovPerGame']['#text'])
        player_minutes = float(raw_stats['MinSecondsPerGame']['#text'])/60.0
        turnover = float(raw_stats['TovPerGame']['#text'])

        player.set_points_per_game(points_per_game)
        player.set_assists_per_game(assists_per_game)
        player.set_field_goal_attempts(field_goal_attempts)
        player.set_field_goals_made(field_goals_made)
        player.set_free_throw_attempts(free_throw_attempts)
        player.set_free_throws_made(free_throws_made)
        player.set_treys_made(treys_made)
        player.set_off_reb_per_game(off_reb_per_game)
        player.set_tov_per_game(tov_per_game)
        player.set_minutes(player_minutes)
        player.set_turnover(turnover)


    @classmethod
    def stat_calculator(cls, player):
        """calculate any dependent statistics for the player"""

        # Effective Field Goal Percentage = (Field Goals Made) + 0.5*3P Field Goals Made))/(Field Goal Attempts)
        # True Shooting Percentage = (Player's Total Points)/[(2*(Player's Field Goal Attempts+ 0.44*Player's Free Throw Attempts)]
        if player.get_field_goal_attempts() > 0:
            #obtain all required totals from the player
            field_goal_attempts = player.get_field_goal_attempts()
            field_goals_made = player.get_field_goals_made()
            treys_made = player.get_treys_made()
            free_throw_attempts = player.get_free_throw_attempts()
            points_per_game = player.get_points()

            #calculate the necessary statistic and update the player accordingly
            effective_field_goal_percentage = ((field_goals_made + (0.5 * treys_made)) / field_goal_attempts) * 100.0
            true_shooting_percentage = points_per_game / (2.0 * (field_goal_attempts + 0.44 * free_throw_attempts)) * 100.0
            player.set_effective_field_goal_percentage(effective_field_goal_percentage)
            player.set_true_shooting_percentage(true_shooting_percentage)

            #find the number of points produced per game
            cls.points_produced(player)

        else:
            #avoid division errors, simply set the values to 0
            player.set_effective_field_goal_percentage(0)
            player.set_true_shooting_percentage(0)

    @classmethod
    def points_produced(cls, player):
        """ uses per-game averages to calculate points produced per game """

        #Points Produced = (1.45 x FGM) + (2.2 x 3PTM) + FTM + (0.6 * Off. Reb.) + (0.6 * Ast)
        points_produced = ((1.45 * player.get_field_goals_made()) +
                           (2.2 * player.get_treys_made()) + player.get_free_throws_made() +
                           (0.6 * player.get_off_reb_per_game()) +
                           (0.6 * player.get_assists_per_game()))

        player.set_points_produced(points_produced)

    @classmethod
    def win_shares(cls, player, NBA_teams, NBA_teams_checklist):
        """uses per-game averages to determine a player's 'win share'"""
        cls.off_win_shares(player, NBA_teams, NBA_teams_checklist)
        cls.def_win_shares(player, NBA_teams, NBA_teams_checklist)


    @classmethod
    def off_win_shares(cls, player, NBA_teams, NBA_teams_checklist):
        """handles offensive win share calculations"""
        team_abbr = player.get_team_abbr()
        fg_attempts = player.get_field_goal_attempts()
        turnovers = player.get_tov_per_game()
        free_throw_attempts = player.get_free_throw_attempts()
        offensive_rebounds = player.get_off_reb_per_game()
        pts_produced = player.get_points_produced()

        possessions = 0.96 * (fg_attempts + turnovers + 0.44 * free_throw_attempts - offensive_rebounds)

        league_avg_poss = 0.96 * (7004 + 1144 + 0.44 * 1895 - 831)
        league_pts_per_poss = 8658 / league_avg_poss

        team_pace = NBA_teams[team_abbr].get_possessions()
        league_pace = 0

        for key, value in NBA_teams_checklist:
            league_pace += NBA_teams[key].get_possessions()

        marginal_offense = pts_produced - (0.92 * league_pts_per_poss * possessions)

        marginal_pts_per_win = 0.32 * 105.6 * (team_pace / league_pace)

        off_win_share = marginal_offense / marginal_pts_per_win

        player.set_offensive_win_share(off_win_share)

    @classmethod
    def def_win_shares(cls, player, NBA_teams, NBA_teams_checklist):
        """handles defensive win share calculations"""
        team_abbr = player.get_team_abbr()
        team = NBA_teams[team_abbr]

        schedule = team.game_schedule
        total_opponent_poss = 0
        pts_allowed = team.get_points_allowed()
        for a in range(0, len(team.game_schedule)):
            total_opponent_poss += NBA_teams[a].get_possessions()

        team_rating = team.defensive_efficiency
        def_pts_per_scoring_poss = pts_allowed / total_opponent_poss
        #Stops = STL + BLK + FMwt * (1 - 1.07 * DOR%) + DREB * (1 - FMwt)
        

        #individual_def_rating = team_rating + 0.2 * (100 * def_pts_per_scoring_poss * (1 - ))
    @classmethod
    def usage(cls,player,raw_stats,NBA_teams,team_name_abbr):
        """Usage rate, a.k.a., usage percentage is an estimate of the percentage of team plays used by a player while he was on the floor."""

        #Usage Rate Formula=100*((FGA+0.44*FTA+TO)*(TMP/5))/(MP*(TFGA+0.44*TFTA+TTO))
        team_minutes = 48*5
        player_minutes = player.get_player_minutes()
        field_goal_attempts = player.get_field_goal_attempts()
        free_throw_attempts = player.get_free_throw_attempts()
        turnover = player.get_player_turnover()
        team_field_goal_attempts = NBA_teams[team_name_abbr].get_field_goal_attempts()
        team_free_throw_attempts = NBA_teams[team_name_abbr].get_free_throw_attempts()
        team_turnover = NBA_teams[team_name_abbr].get_turnover()


        #Calculation
        if player_minutes == 0:
            usage_rate = 0
        else:
            usage_rate = 100 * ((field_goal_attempts + 0.44 * free_throw_attempts + turnover) * (team_minutes / (5))) / (player_minutes * (team_field_goal_attempts + 0.44 * team_free_throw_attempts + team_turnover))
            usage_rate = round(usage_rate,1)
            print(player.FullName,usage_rate)
            player.set_player_usage(usage_rate)



      

