CREATE DATABASE travel_app

CREATE TABLE `travel_app`.`users` (
    `id` INT NOT NULL AUTO_INCREMENT ,
    `name` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL ,
    `surname` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL ,
    `city` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL ,
    `currency` VARCHAR(3) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL ,
    `avatar` VARCHAR(1024) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL ,
    `username` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL UNIQUE,
    `password` VARCHAR(1024) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL ,
    PRIMARY KEY (`id`)) ENGINE = InnoDB;

CREATE TABLE `travel_app`.`favorites` (
    `id` INT NOT NULL AUTO_INCREMENT ,
    `user_id` INT NOT NULL ,
    `city` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL ,
    PRIMARY KEY (`id`)) ENGINE = InnoDB;

INSERT INTO `users` (`id`, `name`, `surname`, `city`, `currency`, `avatar`, `username`, `password`)
VALUES (NULL, 'Jan', 'Kowalski', 'Łódź', 'PLN', 'https://cdn.pixabay.com/photo/2018/08/28/12/41/avatar-3637425__340.png', 'jan123', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');
INSERT INTO `users` (`id`, `name`, `surname`, `city`, `currency`, `avatar`, `username`, `password`)
VALUES (NULL, 'Anna', 'Nowak', 'Warszawa', 'PLN', 'https://cdn.pixabay.com/photo/2018/08/28/12/41/avatar-3637425__340.png', 'anna123', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');

INSERT INTO `favorites` (`id`, `user_id`, `city`)
VALUES (NULL, '1', 'Praga');
INSERT INTO `favorites` (`id`, `user_id`, `city`)
VALUES (NULL, '1', 'Berlin');
INSERT INTO `favorites` (`id`, `user_id`, `city`)
VALUES (NULL, '2', 'Ateny');