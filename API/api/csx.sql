DROP DATABASE IF EXISTS `csx`;
CREATE DATABASE `csx`;
DROP DATABASE IF EXISTS `test`;
CREATE DATABASE `test`;
USE csx;
DROP TABLE IF EXISTS `match_leaderboards`;
DROP TABLE IF EXISTS `matches`;
DROP TABLE IF EXISTS `organizers_teams`;
DROP TABLE IF EXISTS `tournaments`;
DROP TABLE IF EXISTS `organizers`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `teams`;
CREATE TABLE `teams` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(45) NOT NULL,
    `team_key` varchar(64) NOT NULL,
    `description` text,
    PRIMARY KEY (`id`)
);
CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(45) NOT NULL,
    `password` varchar(64) NOT NULL,
    `request_key` varchar(64),
    `permission` int(1) NOT NULL DEFAULT 0,
    `team_id` int(11),
    `is_owner_team` int(1) NOT NULL DEFAULT 0,
    `description` text,
    `role` int(11),
    UNIQUE (`username`),
    UNIQUE (`request_key`),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`team_id`) REFERENCES `teams`(`id`)
);
CREATE TABLE `organizers` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(45) NOT NULL,
    `owner_id` int(11) NOT NULL,
    `organizer_key` varchar(64) NOT NULL,
    `entry_fee` int(10), -- money value in cents --
    `description` text,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`owner_id`) REFERENCES `users`(`id`)
);
CREATE TABLE `tournaments` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `organizer_id` int(11),
    `name` varchar(45),
    `type` int(1) NOT NULL,
    `size` int(3) NOT NULL,
    `start_date` datetime,
    `end_date` date,
    `entry_fee` int(10), -- money value in cents --
    `description` text,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`organizer_id`) REFERENCES `organizers`(`id`)
);
CREATE TABLE `organizers_teams` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `organizer_id` int(11) NOT NULL,
    `team_id` int(11) NOT NULL,
    `request` int(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`organizer_id`) REFERENCES `organizers`(`id`),
    FOREIGN KEY (`team_id`) REFERENCES `teams`(`id`)
);
CREATE TABLE `brackets` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `tournament_id` int(11),
    `team_id` int(11),
    `user_id` int(11),
    `place` int(4) NOT NULL,
    `games_won` int(4) NOT NULL DEFAULT 0,
    `games_tied` int(4) NOT NULL DEFAULT 0,
    `games_lost` int(4) NOT NULL DEFAULT 0,
    `score` int(4),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`tournament_id`) REFERENCES `tournaments`(`id`),
    FOREIGN KEY (`team_id`) REFERENCES `teams`(`id`)
);
CREATE TABLE `matches` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `tournament_id` int(11),
    `home_id` int(11),
    `away_id` int(11),
    `home_score` int(11),
    `away_score` int(11),
    `start_date` datetime,
    `end_date` datetime,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`tournament_id`) REFERENCES `tournaments`(`id`),
    FOREIGN KEY (`home_id`) REFERENCES `teams`(`id`),
    FOREIGN KEY (`away_id`) REFERENCES `teams`(`id`)
);
CREATE TABLE `match_leaderboards` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `player_id` int(11),
    `team_id` int(11),
    `match_id` int(11) NOT NULL,
    `score` int(4),
    `kills` int(4),
    `assists` int(4),
    `deaths` int(4),
    `dpr` int(4),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`player_id`) REFERENCES `users`(`id`),
    FOREIGN KEY (`team_id`) REFERENCES `teams`(`id`),
    FOREIGN KEY (`match_id`) REFERENCES `matches`(`id`)
);
USE test;
DROP TABLE IF EXISTS `match_leaderboards`;
DROP TABLE IF EXISTS `matches`;
DROP TABLE IF EXISTS `organizers_teams`;
DROP TABLE IF EXISTS `tournaments`;
DROP TABLE IF EXISTS `organizers`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `teams`;
CREATE TABLE `teams` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(45) NOT NULL,
    `team_key` varchar(64) NOT NULL,
    `description` text,
    PRIMARY KEY (`id`)
);
CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(45) NOT NULL,
    `password` varchar(64) NOT NULL,
    `request_key` varchar(64),
    `permission` int(1) NOT NULL DEFAULT 0,
    `team_id` int(11),
    `is_owner_team` int(1) NOT NULL DEFAULT 0,
    `description` text,
    `role` int(11),
    UNIQUE (`username`),
    UNIQUE (`request_key`),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`team_id`) REFERENCES `teams`(`id`)
);
CREATE TABLE `organizers` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(45) NOT NULL,
    `owner_id` int(11) NOT NULL,
    `organizer_key` varchar(64) NOT NULL,
    `entry_fee` int(10), -- money value in cents --
    `description` text,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`owner_id`) REFERENCES `users`(`id`)
);
CREATE TABLE `tournaments` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`organizer_id` int(11),
	`name` varchar(45),
	`type` int(1) NOT NULL,
    `size` int(3) NOT NULL,
	`start_date` datetime,
	`end_date` date,
    `entry_fee` int(10), -- money value in cents --
    `description` text,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`organizer_id`) REFERENCES `organizers`(`id`)
);
CREATE TABLE `organizers_teams` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
    `organizer_id` int(11) NOT NULL,
    `team_id` int(11) NOT NULL,
    `request` int(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`organizer_id`) REFERENCES `organizers`(`id`),
    FOREIGN KEY (`team_id`) REFERENCES `teams`(`id`)
);
CREATE TABLE `brackets` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `tournament_id` int(11),
    `team_id` int(11),
    `user_id` int(11),
    `place` int(4) NOT NULL,
    `games_won` int(4) NOT NULL DEFAULT 0,
    `games_tied` int(4) NOT NULL DEFAULT 0,
    `games_lost` int(4) NOT NULL DEFAULT 0,
    `score` int(4),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`tournament_id`) REFERENCES `tournaments`(`id`),
    FOREIGN KEY (`team_id`) REFERENCES `teams`(`id`)
);
CREATE TABLE `matches` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `tournament_id` int(11),
    `home_id` int(11),
    `away_id` int(11),
    `home_score` int(11),
    `away_score` int(11),
    `start_date` datetime,
    `end_date` datetime,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`tournament_id`) REFERENCES `tournaments`(`id`),
    FOREIGN KEY (`home_id`) REFERENCES `teams`(`id`),
    FOREIGN KEY (`away_id`) REFERENCES `teams`(`id`)
);
CREATE TABLE `match_leaderboards` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `player_id` int(11),
    `team_id` int(11),
    `match_id` int(11) NOT NULL,
    `score` int(4),
    `kills` int(4),
    `assists` int(4),
    `deaths` int(4),
    `dpr` int(4),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`player_id`) REFERENCES `users`(`id`),
    FOREIGN KEY (`team_id`) REFERENCES `teams`(`id`),
    FOREIGN KEY (`match_id`) REFERENCES `matches`(`id`)
);