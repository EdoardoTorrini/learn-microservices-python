CREATE DATABASE IF NOT EXISTS db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE db;

DROP TABLE IF EXISTS `orders`;

CREATE TABLE `orders` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id CHAR(36) NOT NULL UNIQUE,
    product_ids VARCHAR(1024) NOT NULL,
    customer_id VARCHAR(255) NOT NULL,
    credit_card_number VARCHAR(64) NOT NULL,
    status ENUM('PENDING', 'APPROVED', 'REJECTED') NOT NULL DEFAULT 'PENDING'
    -- INDEX idx_order_id (order_id), 
    -- INDEX idx_product_ids (product_ids)
);

