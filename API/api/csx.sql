DROP DATABASE IF EXISTS `csx`;
CREATE DATABASE `csx`;
DROP DATABASE IF EXISTS `test`;
CREATE DATABASE `test`;
USE csx;
DROP TABLE IF EXISTS `organizers`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `teams`;
CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (`id`)
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
CREATE TABLE `teams` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(45) NOT NULL,
    `owner_id` int(11) NOT NULL,
    `description` text,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`owner_id`) REFERENCES `users`(`id`)
);
USE test;
DROP TABLE IF EXISTS `organizers`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `teams`;
CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
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
CREATE TABLE `teams` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(45) NOT NULL,
    `owner_id` int(11) NOT NULL,
    `description` text,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`owner_id`) REFERENCES `users`(`id`)
);

