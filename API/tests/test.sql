USE test;
DELETE FROM `match_leaderboards` WHERE 1=1;
DELETE FROM `matches` WHERE 1=1;
DELETE FROM `brackets` WHERE 1=1;
DELETE FROM `organizers_teams` WHERE 1=1;
DELETE FROM `tournaments` WHERE 1=1;
DELETE FROM `organizers` WHERE 1=1;
DELETE FROM `users` WHERE 1=1;
DELETE FROM `teams` WHERE 1=1;
INSERT INTO `teams` VALUES(1, 'FuRy', '$2b$12$3uvat8KCq5K0okD.lBIPROOYDOqT7J12p.hNFZs/E2lXNCfR/u/8m', 'Andrew is a god');
INSERT INTO `teams` VALUES(2, 'Artemis', '$2b$12$3uvat8KCq5K0okD.lBIPROOYDOqT7J12p.hNFZs/E2lXNCfR/u/8m', 'Not your average expieriance');
INSERT INTO `teams` VALUES(3, 'Faze', '$2b$12$3uvat8KCq5K0okD.lBIPROOYDOqT7J12p.hNFZs/E2lXNCfR/u/8m', 'Olof is a criminal');
INSERT INTO `teams` VALUES(4, 'Outer Heavan', '$2b$12$3uvat8KCq5K0okD.lBIPROOYDOqT7J12p.hNFZs/E2lXNCfR/u/8m', '... wtf');
INSERT INTO `users` (`id`, `username`, `password`, `team_id`, `is_owner_team`, `request_key`, `permission`, `description`, `role`) VALUES(1, 'Caleb', '$2b$12$3uvat8KCq5K0okD.lBIPROOYDOqT7J12p.hNFZs/E2lXNCfR/u/8m', 1, 1, '$2b$12$3uvat8KCq5K0okD.lBIPROOYDOqT7J12p.hNFZs/E2lXNCfR/u/8m', 2, 'Just your average player', 1);
INSERT INTO `users` (`id`, `username`, `password`, `team_id`, `request_key`, `permission`, `description`, `role`) VALUES(2, 'Bobby', '$2b$12$3uvat8KCq5K0okD.lBIPROOYDOqT7J12p.hNFZs/E2lXNCfR/u/8m', 3, '$2y$12$u45ZYckdk3X6HNr3/FdzxedTJ8o8CnWwyk8XWxLaKP3WuZ7DX/rn6', 1, 'pass me another cold one', 1);
INSERT INTO `users` (`id`, `username`, `password`, `team_id`, `description`, `role`) VALUES(3, 'Gucci', '$2b$12$3uvat8KCq5K0okD.lBIPROOYDOqT7J12p.hNFZs/E2lXNCfR/u/8m', 1, 'I like shaggy', 2);
INSERT INTO `organizers` VALUES(1, 'Ignis', 1, '$2b$12$3uvat8KCq5K0okD.lBIPROOYDOqT7J12p.hNFZs/E2lXNCfR/u/8m', 100, 'Best place to play!');
INSERT INTO `organizers` VALUES(2, 'VGL', 2, '$2b$12$3uvat8KCq5K0okD.lBIPROOYDOqT7J12p.hNFZs/E2lXNCfR/u/8m', 1000, 'Second Best place to play!');
INSERT INTO `tournaments` VALUES(1, 1, 'New Year', 2, 8, '2018-1-1 8:00:00', '2018-1-20', 100000, 'New year special');
INSERT INTO `tournaments` (`id`, `organizer_id`, `name`, `type`, `size`, `start_date`, `entry_fee`, `description`) VALUES(2, 1, 'Christmas', 1, 4, '2018-12-25 12:30:00', 500, 'Christmas special');
INSERT INTO `organizers_teams` VALUES(1, 1, 1, 0);
INSERT INTO `organizers_teams` VALUES(2, 1, 2, 0);
INSERT INTO `organizers_teams` VALUES(3, 1, 3, 0);
INSERT INTO `organizers_teams` VALUES(4, 1, 4, 0);
INSERT INTO `organizers_teams` VALUES(5, 2, 1, 0);
INSERT INTO `organizers_teams` VALUES(6, 2, 2, 1);
INSERT INTO `brackets` (`id`, `tournament_id`, `team_id`, `place`, `games_won`, `games_tied`, `games_lost`) VALUES(3, 1, 3, 1, 2, 0, 0);
INSERT INTO `brackets` (`id`, `tournament_id`, `team_id`, `place`, `games_won`, `games_tied`, `games_lost`) VALUES(1, 1, 1, 3, 1, 0, 1);
INSERT INTO `brackets` (`id`, `tournament_id`, `team_id`, `place`, `games_won`, `games_tied`, `games_lost`) VALUES(2, 1, 2, 2, 1, 0, 1);
INSERT INTO `brackets` (`id`, `tournament_id`, `team_id`, `place`, `games_won`, `games_tied`, `games_lost`) VALUES(4, 1, 4, 4, 0, 0, 2);
INSERT INTO `matches` (`id`, `tournament_id`, `home_id`, `away_id`, `home_score`, `away_score`, `start_date`, `end_date`) VALUES(1, 1, 3, 1, 16, 10, '2018-1-1 8:00:00', '2018-1-1 9:00:00');
INSERT INTO `matches` (`id`, `tournament_id`, `home_id`, `away_id`, `home_score`, `away_score`, `start_date`, `end_date`) VALUES(2, 1, 4, 3, 4, 16, '2018-3-1 8:00:00', '2018-3-1 9:00:00');
INSERT INTO `matches` (`id`, `tournament_id`, `home_id`, `away_id`, `home_score`, `away_score`, `start_date`, `end_date`) VALUES(3, 1, 2, 1, 15, 16, '2018-5-1 8:00:00', '2018-5-1 9:00:00');
INSERT INTO `matches` (`id`, `tournament_id`, `home_id`, `away_id`, `home_score`, `away_score`, `start_date`, `end_date`) VALUES(4, 1, 2, 4, 16, 2, '2018-8-1 10:00:00', '2018-8-1 11:00:00');
INSERT INTO `match_leaderboards` (`id`, `player_id`, `team_id`, `match_id`, `score`, `kills`, `assists`, `deaths`, `dpr`) VALUES(1, 1, 1, 1, 10, 10, 2, 8, 76);
INSERT INTO `match_leaderboards` (`id`, `player_id`, `team_id`, `match_id`, `score`, `kills`, `assists`, `deaths`, `dpr`) VALUES(2, 3, 1, 1, 20, 20, 0, 5, 170);
INSERT INTO `match_leaderboards` (`id`, `player_id`, `team_id`, `match_id`, `score`, `kills`, `assists`, `deaths`, `dpr`) VALUES(3, 2, 3, 1, 13, 15, 4, 7, 82);
INSERT INTO `match_leaderboards` (`id`, `player_id`, `team_id`, `match_id`, `score`, `kills`, `assists`, `deaths`, `dpr`) VALUES(4, 1, 1, 1, 10, 10, 2, 8, 76);
INSERT INTO `match_leaderboards` (`id`, `player_id`, `team_id`, `match_id`, `score`, `kills`, `assists`, `deaths`, `dpr`) VALUES(5, 1, 1, 1, 10, 10, 2, 2, 76);
INSERT INTO `match_leaderboards` (`id`, `player_id`, `team_id`, `match_id`, `score`, `kills`, `assists`, `deaths`, `dpr`) VALUES(6, 1, 1, 1, 10, 4, 2, 24, 76);
INSERT INTO `match_leaderboards` (`id`, `player_id`, `team_id`, `match_id`, `score`, `kills`, `assists`, `deaths`, `dpr`) VALUES(7, 1, 1, 1, 10, 10, 2, 5, 76);
INSERT INTO `match_leaderboards` (`id`, `player_id`, `team_id`, `match_id`, `score`, `kills`, `assists`, `deaths`, `dpr`) VALUES(8, 1, 1, 1, 10, 8, 2, 6, 76);
INSERT INTO `match_leaderboards` (`id`, `player_id`, `team_id`, `match_id`, `score`, `kills`, `assists`, `deaths`, `dpr`) VALUES(9, 1, 1, 1, 10, 12, 2, 3, 76);
INSERT INTO `match_leaderboards` (`id`, `player_id`, `team_id`, `match_id`, `score`, `kills`, `assists`, `deaths`, `dpr`) VALUES(10, 1, 1, 1, 10, 10, 2, 7, 76);
INSERT INTO `match_leaderboards` (`id`, `player_id`, `team_id`, `match_id`, `score`, `kills`, `assists`, `deaths`, `dpr`) VALUES(11, 1, 1, 1, 10, 5, 2, 0, 76);
INSERT INTO `match_leaderboards` (`id`, `player_id`, `team_id`, `match_id`, `score`, `kills`, `assists`, `deaths`, `dpr`) VALUES(12, 1, 1, 1, 10, 6, 2, 15, 76);