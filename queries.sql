SELECT * FROM builds;
SELECT * FROM users;

SELECT * FROM builds
JOIN users
ON builds.user_id = users.id;

SELECT * FROM builds WHERE user_id = 1;

INSERT INTO builds (race, class, background, class_description, bg_description, user_id) VALUES ("elf", "barbarian", "acolyte", "lorem ipsum", "loremBG", 1);