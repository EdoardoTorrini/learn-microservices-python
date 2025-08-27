DROP TABLE IF EXISTS `inventory`;

CREATE TABLE `inventory` (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    quantity INT NOT NULL,
    INDEX idx_product_id (product_id)
);

DROP TABLE IF EXISTS `orders`;

CREATE TABLE `orders` (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(36) NOT NULL UNIQUE,
    product_ids VARCHAR(255) NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    credit_card_number VARCHAR(20),
    status ENUM('PENDING', 'APPROVED', 'REJECTED') DEFAULT 'PENDING'
);