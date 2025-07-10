DROP TABLE IF EXISTS `comments`;

CREATE TABLE `comments` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    comment_uuid VARCHAR(255) NOT NULL UNIQUE,
    post_uuid VARCHAR(255) NOT NULL,
    timestamp BIGINT NOT NULL,
    content TEXT NOT NULL,
    INDEX idx_comment_uuid (comment_uuid),
    INDEX idx_post_uuid (post_uuid)
);

DROP TABLE IF EXISTS `posts`;

CREATE TABLE `posts` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_uuid VARCHAR(255) NOT NULL UNIQUE,
    user_uuid VARCHAR(255) NOT NULL,
    timestamp BIGINT NOT NULL,
    content TEXT NOT NULL,
    INDEX idx_post_uuid (post_uuid),
    INDEX idx_user_uuid (user_uuid)
);

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_uuid VARCHAR(255) NOT NULL UNIQUE,
    nickname VARCHAR(255) NOT NULL,
    birthday DATE NOT NULL,
    INDEX idx_user_uuid (user_uuid)
);
