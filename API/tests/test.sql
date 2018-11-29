USE test;
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