from rest_framework import serializers
from SleeperApp.models import Departments, Employees, Gamelogs


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ('DepartmentId',
                  'DepartmentName')


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ('EmployeeId',
                  'EmployeeName',
                  'Department',
                  'DateOfJoining',
                  'PhotoFileName')


class GamelogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gamelogs
        fields = ('gamelog_id',
                  'player_id',
                  'year_id',
                  'game_date',
                  'game_num',
                  'week_num',
                  'age',
                  'team',
                  'game_location',
                  'opp',
                  'game_result',
                  'gs',
                  'pass_cmp',
                  'pass_att',
                  'pass_cmp_perc',
                  'pass_yds',
                  'pass_td',
                  'pass_int',
                  'pass_rating',
                  'pass_sacked',
                  'pass_sacked_yds',
                  'pass_yds_per_att',
                  'pass_adj_yds_per_att',
                  'rush_att',
                  'rush_yds',
                  'rush_yds_per_att',
                  'rush_td',
                  'targets',
                  'rec',
                  'rec_yds',
                  'rec_yds_per_rec',
                  'rec_td',
                  'catch_pct',
                  'rec_yds_per_tgt',
                  'two_pt_md',
                  'all_td',
                  'scoring',
                  'fumbles',
                  'fumbles_lost',
                  'fumbles_forced',
                  'fumbles_rec',
                  'fumbles_rec_yds',
                  'fumbles_rec_td',
                  'safety_md',
                  'sacks',
                  'tackles_solo',
                  'tackles_assists',
                  'tackles_combined',
                  'tackles_loss',
                  'qb_hits',
                  'def_int',
                  'def_int_yds',
                  'def_int_td',
                  'pass_defended',
                  'kick_ret',
                  'kick_ret_yds',
                  'kick_ret_yds_per_ret',
                  'kick_ret_td',
                  'punt_ret',
                  'punt_ret_yds',
                  'punt_ret_yds_per_ret',
                  'punt_ret_td',
                  'xpm',
                  'xpa',
                  'xp_perc',
                  'fgm',
                  'fga',
                  'fg_perc',
                  'punt',
                  'punt_yds',
                  'punt_yds_per_punt',
                  'punt_blocked',
                  'offense',
                  'off_pct',
                  'defense',
                  'def_pct',
                  'special_teams',
                  'st_pct')
