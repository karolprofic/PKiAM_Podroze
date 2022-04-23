CREATE DATABASE travel_app

CREATE TABLE `travel_app`.`users` ( `id` INT NOT NULL AUTO_INCREMENT , `name` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL , `surname` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL , `city` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL , `currency` VARCHAR(3) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL , `avatar` VARCHAR(1024) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;

CREATE TABLE `travel_app`.`favorites` ( `id` INT NOT NULL AUTO_INCREMENT , `user_id` INT NOT NULL , `city` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;

INSERT INTO `users` (`id`, `name`, `surname`, `city`, `currency`, `avatar`) VALUES (NULL, 'Jan', 'Kowalski', 'Łódź', 'PLN', 'https://cdn.pixabay.com/photo/2018/08/28/12/41/avatar-3637425__340.png');

