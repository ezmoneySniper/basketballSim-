from getData import *
from Team_class import *
import os
from helper import *
from PlayerManager import *
from Database import *
from PlayerFactory import *
from TeamFactory import *

NBA_teams_checklist={}
NBA_teams={}
Ranking={}
offensive_efficiency={}
defensive_efficiency={}


dir = os.path.dirname(__file__)+'/results/'
active_players_json=open(dir+'active_players-nba-2016-2017-regular.json').read()
conference_team_standing_json=open(dir+"conference_team_standings-nba-2016-2017-regular.json").read()
cumulative_player_stats_json=open(dir+"cumulative_player_stats-nba-2016-2017-regular.json").read()
division_team_standings_json=open(dir+"division_team_standings-nba-2016-2017-regular.json").read()
full_game_schedule_json=open(dir+"full_game_schedule-nba-2016-2017-regular.json").read()
overall_team_standings_json=open(dir+"overall_team_standings-nba-2016-2017-regular.json").read()
player_injuries_json=open(dir+"player_injuries-nba-2016-2017-regular.json").read()
playoff_team_standings_json=open(dir+"playoff_team_standings-nba-2016-playoff.json").read()
team_gamelogs_base=dir+"team_gamelogs-nba-2016-2017-regular-"

active_players=json.loads(active_players_json)
conference_team_standing=json.loads(conference_team_standing_json)
cumulative_player_stats=json.loads(cumulative_player_stats_json)
division_team_standings=json.loads(division_team_standings_json)
full_game_schedule=json.loads(full_game_schedule_json)
overall_team_standings=json.loads(overall_team_standings_json)
player_injuries=json.loads(player_injuries_json)
playoff_team_standings=json.loads(playoff_team_standings_json)
player_list = []
active_players_list = {}
player_manager = PlayerManager()
more_data=input("Enter data(Y/N): ")
if more_data.lower() == 'y':
    more_data=True
else:
    more_data=None
#populate the team check list to get a complete team abbre
for a in range(0,len(active_players['activeplayers']['playerentry'])):
    base = active_players['activeplayers']['playerentry'][a]
    if "team" in base:
        team_name_abbr = str(base['team']['Abbreviation'])
        team_name_and_city = str(base['team']['City']+" " + base['team']['Name'])
        ID = base['player']['ID']
        FirstName = base['player']['FirstName']
        LastName = base['player']['LastName']
        nameFormat =  FirstName + '-' + LastName + '-' + ID

        if team_name_abbr not in NBA_teams_checklist.keys():
            NBA_teams_checklist[team_name_abbr]=team_name_and_city
        else:
            pass
        if nameFormat not in player_list:
            player_list.append(nameFormat)
            active_players_list[ID] = nameFormat
    else:
        pass
#check for more data
while more_data:
    print("Enter 'general' for data contain \ncumulative player stats\nfull game schedule\nactive player\noverall team standings\nconference team standings\ndivision team standings\nplayoff team standings\nplayer injuries\nlatest updates\n\n")
    print("Or enter 'daily'  for \ndaily_game_schedule\ndaily_player_stats three\nscoreboard\nroster_player\n\n")
    print("or enter 'gamelogs' for \nplayer game logs\nteam game logs\n\n")
    print("or enter 'game' for \ngame_playbyplay\ngame_boxscore\ngame_startinglineup\n\n")

    request_type=input("Enter the data type: ")
    if request_type=="general":
        request_general()
    elif request_type=="daily":
        request_daily()
    elif request_type=="gamelogs":
        gamelogs_type=input("Requesting for all team gamelogs?(y/n): ")
        if gamelogs_type.lower()=="y":
            request_all_team_gamelogs(NBA_teams_checklist)
        else:
            gamelogs_type=input("Requesting for all players gamelogs?(y/n): ")
            if gamelogs_type.lower()=="y":
                request_all_player_gamelogs(player_list)
                #pass #alex put your player requesting here
            else:
                request_gamelogs()
    elif request_type=="game":
        request_game()
    else:
        print("Wrong input try again")
    
    more=input("More data?: (Y/N)")
    if more.lower() =="y":
        more_data=True
        clear_input()
    else:
        more_data=None
        
        clear_input()
##################################populates the roster list as well as creating the team class(including all attributes within the team class)######################
#create classes for each team
create_table_year()
create_table_teams()
#temp_method()
create_table_player()

#old nba_teams filling method
#use this for the initiall load
for key,value in NBA_teams_checklist.items():
    NBA_teams[key]=Team(key,value)


#use this when database is full
teams = TeamFactory.teams_from_db()
for team in teams:
    NBA_teams[team.get_team_name_abbr()] = team

get_each_team_schedule(NBA_teams,full_game_schedule) #needs to run before team_entry()
# team_entry(NBA_teams)
# player_entry(active_players_list)
# UNCOMMENT THIS LOADING FROM DB METHOD TO TEST WIN SHARES
# populate each team with a complete roster FROM API (need to find way to use this if DB is empty)
for x in range(0,len(cumulative_player_stats['cumulativeplayerstats']['playerstatsentry'])):
    base = cumulative_player_stats['cumulativeplayerstats']['playerstatsentry'][x]
    raw_player = base['player']
    playerID = raw_player['ID']

    if playerID in active_players_list:
        raw_stats = base['stats']

        team_name_abbr = str(base['team']['Abbreviation'])
        team_id = base['team']['ID']
        #generate the player object and relevant stats
        player = PlayerFactory.make_player(raw_player)
        PlayerFactory.stats_filler(raw_stats, player)
        PlayerFactory.stat_calculator(player)
        TeamFactory.team_basic_stats_filler(NBA_teams, overall_team_standings)
        PlayerFactory.usage(player,raw_stats,NBA_teams,team_name_abbr)
        player.set_team_id(team_id)
        player.set_team_abbr(team_name_abbr)
        #populate the roster
        NBA_teams[team_name_abbr].add_players_roster(player.FullName)
        #populate the player class
        NBA_teams[team_name_abbr].add_player(player)
    else:
        pass

assign_teamid(NBA_teams,overall_team_standings)
NBA_teams['GSW'].print_roster()   #//print roster
#NBA_teams['CLE'].print_player_points_helper("Kevin Love")      //print points by passing a name
#NBA_teams['GSW'].team_theoretical_points() 
#####################################################################################################################
###########################test###############################################

#trade_player(NBA_teams,NBA_teams_checklist)
TeamFactory.off_and_deff_efficiency_rating(overall_team_standings,offensive_efficiency,defensive_efficiency,NBA_teams,NBA_teams_checklist)
#NBA_teams['BOS'].change_effeiciency()
TeamFactory.four_factors(NBA_teams,NBA_teams_checklist, overall_team_standings)
#access players
#NBA_teams['LAL'].roster_class["IvicaZubac"].set_points_per_game(999999999)
#NBA_teams['LAL'].roster_class["IvicaZubac"].print_points_per_game()
TeamFactory.winning_percentage(NBA_teams,NBA_teams_checklist,overall_team_standings)
#pprint(NBA_teams['HOU'].roster_class["JamesHarden"].get_points_produced())
# print(len(cumulative_player_stats['cumulativeplayerstats']['playerstatsentry']))

#database test





#uncomment the next line to test reading teams from DB
TeamFactory.teams_from_db()
player_manager.load_players(NBA_teams, NBA_teams_checklist)
Ranking_wins = {}
ranking_win_share(NBA_teams, NBA_teams_checklist, Ranking_wins)


#testing PPG after loading players
print("\nPoints per game ranking after loading players from DB:")
ranking_points_per_game(NBA_teams,NBA_teams_checklist,Ranking)
print("\n")

print("\n")
player_manager.rank_by_win_shares()
player_manager.player_win_share_percentage(NBA_teams)

sim(NBA_teams,NBA_teams_checklist,Ranking,overall_team_standings)
ranking_by_sim(Ranking)
# @ERICK: uncomment later to test trade and re-ordering of teams
trade_player(NBA_teams,NBA_teams_checklist,Ranking)
ranking_by_sim(Ranking)
#ranking_points_per_game(NBA_teams,NBA_teams_checklist,Ranking)

################factory reset###############
# all_team = TeamFactory.teams_from_db()
# for team in all_team:
#     print (team.team_name_abbr + ": " + str(team.teamid))
#uncomment the lines below to test PlayerFactory
# all_players = PlayerFactory.players_from_db()
# for player in all_players:
#     print (player.FullName + ": " + str(player.team_id))
