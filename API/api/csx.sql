DROP DATABASE IF EXISTS `csx`;
CREATE DATABASE `csx`;
DROP DATABASE IF EXISTS `testing`;
CREATE DATABASE `testing`;
USE csx;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `organizers`;
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
INSERT INTO `users` VALUES(1);
INSERT INTO `users` VALUES(2);
INSERT INTO `organizers` VALUES(1, 'Ignis', 1, 100, 'Best place to play!');
INSERT INTO `organizers` VALUES(2, 'VGL', 2, 1000, 'Second Best place to play!');
USE testing;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `organizers`;
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
INSERT INTO `users` VALUES(1);
INSERT INTO `users` VALUES(2);
INSERT INTO `organizers` VALUES(1, 'Ignis', 1, 100, 'Best place to play!');
INSERT INTO `organizers` VALUES(2, 'VGL', 2, 1000, 'Second Best place to play!');
