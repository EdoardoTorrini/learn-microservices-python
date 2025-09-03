CREATE DATABASE IF NOT EXISTS db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE db;

DROP TABLE IF EXISTS `orders`;

CREATE TABLE `orders` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    orderId CHAR(36) NOT NULL UNIQUE,
    productIds VARCHAR(1024) NOT NULL,
    customerId VARCHAR(255) NOT NULL,
    creditCardNumber VARCHAR(64) NOT NULL,
    status ENUM('PENDING', 'APPROVED', 'REJECTED') NOT NULL DEFAULT 'PENDING'
    -- INDEX idx_order_id (order_id), 
    -- INDEX idx_product_ids (product_ids)
);

