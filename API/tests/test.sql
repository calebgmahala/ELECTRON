USE test;
DELETE FROM `organizers` WHERE 1=1;
DELETE FROM `users` WHERE 1=1;
DELETE FROM `teams` WHERE 1=1;
INSERT INTO `users` VALUES(1);
INSERT INTO `users` VALUES(2);
INSERT INTO `organizers` VALUES(1, 'Ignis', 1, 100, 'Best place to play!');
INSERT INTO `organizers` VALUES(2, 'VGL', 2, 1000, 'Second Best place to play!');
INSERT INTO `teams` VALUES(1, 'FuRy', 1, 'Andrew is a god');
INSERT INTO `teams` VALUES(2, 'Artemis', 2, 'Not your average expieriance');
INSERT INTO `teams` VALUES(3, 'Faze', 2, 'Olof is a criminal');
INSERT INTO `teams` VALUES(4, 'Outer Heavan', 1, '... wtf');

