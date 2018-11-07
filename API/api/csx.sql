DROP DATABASE IF EXISTS `csx`;
CREATE DATABASE `csx`;
DROP DATABASE IF EXISTS `test`;
CREATE DATABASE `test`;
USE csx;
DROP TABLE IF EXISTS `organizers_teams`;
DROP TABLE IF EXISTS `tournaments`;
DROP TABLE IF EXISTS `organizers`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `teams`;
CREATE TABLE `teams` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(45) NOT NULL,
    `description` text,
    PRIMARY KEY (`id`)
);
CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(45) NOT NULL,
    `password` varchar(45) NOT NULL,
    `team_id` int(11) NOT NULL,
    `is_owner_team` boolean NOT NULL DEFAULT false,
    `description` text,
    `role` int(2),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`team_id`) REFERENCES `teams`(`id`)
);
CREATE TABLE `organizers` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(45) NOT NULL,
    `owner_id` int(11) NOT NULL,
    `entry_fee` int(10), -- money value in cents --
    `description` text,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`owner_id`) REFERENCES `users`(`id`)
);
CREATE TABLE `tournaments` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`organizer_id` int(11) NOT NULL,
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
USE test;
DROP TABLE IF EXISTS `organizers_teams`;
DROP TABLE IF EXISTS `tournaments`;
DROP TABLE IF EXISTS `organizers`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `teams`;
CREATE TABLE `teams` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(45) NOT NULL,
    `description` text,
    PRIMARY KEY (`id`)
);
CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(45) NOT NULL,
    `password` varchar(45) NOT NULL,
    `team_id` int(11) NOT NULL,
    `is_owner_team` boolean NOT NULL DEFAULT false,
    `description` text,
    `role` int(11),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`team_id`) REFERENCES `teams`(`id`)
);
CREATE TABLE `organizers` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(45) NOT NULL,
    `owner_id` int(11) NOT NULL,
    `entry_fee` int(10), -- money value in cents --
    `description` text,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`owner_id`) REFERENCES `users`(`id`)
);
CREATE TABLE `tournaments` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`organizer_id` int(11) NOT NULL,
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