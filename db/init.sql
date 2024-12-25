-- -- Create table for customers
-- CREATE TABLE IF NOT EXISTS customers (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     guid CHAR(36) UNIQUE,    -- UUID stored as a CHAR(36) string
--     name VARCHAR(255) NOT NULL
--     INDEX idx_guid (guid),
-- );

-- -- Create table for grocers
-- CREATE TABLE IF NOT EXISTS grocers (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     guid CHAR(36) UNIQUE,    -- UUID stored as a CHAR(36) string
--     name VARCHAR(255) NOT NULL
--     INDEX idx_guid (guid),
-- );

-- -- Create table for baskets
-- CREATE TABLE IF NOT EXISTS baskets (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     guid CHAR(36) UNIQUE,    -- UUID stored as a CHAR(36) string
--     customer_id CHAR(36) NOT NULL,    -- Foreign key to customers
--     INDEX idx_guid (guid),
--     FOREIGN KEY (customer_id) REFERENCES customers(id)
-- );

-- -- Create table for transactions
-- CREATE TABLE IF NOT EXISTS transactions (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     guid CHAR(36) UNIQUE,    -- UUID stored as a CHAR(36) string
--     customer_id CHAR(36) NOT NULL,  -- Foreign key to customers
--     grocer_id CHAR(36) NOT NULL,    -- Foreign key to grocers
--     amount DECIMAL(10, 2) NOT NULL,
--     status ENUM('NOT_YET_ORDERED', 'ORDERED', 'PENDING', 'PROCESSING', 'SUCCESS') DEFAULT 'NOT_YET_ORDERED',
--     INDEX idx_guid (guid),
--     FOREIGN KEY (customer_id) REFERENCES customers(id),
--     FOREIGN KEY (grocer_id) REFERENCES grocers(id)
-- );

-- -- Create table for orders
-- CREATE TABLE IF NOT EXISTS orders (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     guid CHAR(36) UNIQUE,    -- UUID stored as a CHAR(36) string
--     customer_id CHAR(36) NOT NULL,  -- Foreign key to customers
--     grocer_id CHAR(36) NOT NULL,    -- Foreign key to grocers
--     basket_id CHAR(36) NOT NULL,    -- Foreign key to baskets
--     total DECIMAL(10, 2) NOT NULL,
--     payment_id CHAR(36),    -- Foreign key to transactions
--     items JSON DEFAULT '[]',    -- Store items as a JSON array
--     INDEX idx_guid (guid),
--     FOREIGN KEY (customer_id) REFERENCES customers(id),
--     FOREIGN KEY (grocer_id) REFERENCES grocers(id),
--     FOREIGN KEY (basket_id) REFERENCES baskets(id),
--     FOREIGN KEY (payment_id) REFERENCES transactions(id)
-- );

-- -- Create table for the order queue
-- CREATE TABLE IF NOT EXISTS order_queues (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     guid CHAR(36) UNIQUE,    -- UUID stored as a CHAR(36) string
--     grocer_id CHAR(36) NOT NULL,    -- Foreign key to grocers
--     baskets JSON DEFAULT '[]',    -- Store baskets as a JSON array
--     INDEX idx_guid (guid),
--     FOREIGN KEY (grocer_id) REFERENCES grocers(id)
-- );

-- -- Create table for menus
-- CREATE TABLE IF NOT EXISTS menus (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     guid CHAR(36) UNIQUE,    -- UUID stored as a CHAR(36) string
--     grocer_id CHAR(36) NOT NULL,    -- Foreign key to grocers
--     INDEX idx_guid (guid),
--     FOREIGN KEY (grocer_id) REFERENCES grocers(id)
-- );

-- -- Create table for single items (non-weighted items)
-- CREATE TABLE IF NOT EXISTS single_items (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     guid CHAR(36) UNIQUE,    -- UUID stored as a CHAR(36) string
--     name VARCHAR(255) NOT NULL,
--     menu_id CHAR(36) NOT NULL,    -- Foreign key to menus
--     grocer_id CHAR(36) NOT NULL,    -- Foreign key to grocers
--     price DECIMAL(10, 2) NOT NULL,
--     INDEX idx_guid (guid),
--     FOREIGN KEY (menu_id) REFERENCES menus(id),
--     FOREIGN KEY (grocer_id) REFERENCES grocers(id)
-- );

-- -- Create table for weighted items
-- CREATE TABLE IF NOT EXISTS single_weighted_items (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     guid CHAR(36) UNIQUE,    -- UUID stored as a CHAR(36) string
--     name VARCHAR(255) NOT NULL,
--     menu_id CHAR(36) NOT NULL,    -- Foreign key to menus
--     grocer_id CHAR(36) NOT NULL,    -- Foreign key to grocers
--     price DECIMAL(10, 2) NOT NULL,
--     weight DECIMAL(10, 2) NOT NULL,    -- Weight of the item
--     INDEX idx_guid (guid),
--     FOREIGN KEY (menu_id) REFERENCES menus(id),
--     FOREIGN KEY (grocer_id) REFERENCES grocers(id)
-- );

-- -- Create table for basket items
-- CREATE TABLE IF NOT EXISTS basket_items (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     guid CHAR(36) UNIQUE,    -- UUID stored as a CHAR(36) string
--     item_id CHAR(36) NOT NULL,    -- Foreign key to single_items or single_weighted_items
--     basket_id CHAR(36) NOT NULL,    -- Foreign key to baskets
--     customer_id CHAR(36) NOT NULL,    -- Foreign key to customers
--     total DECIMAL(10, 2) NOT NULL,
--     amount DECIMAL(10, 2) NOT NULL,    -- Quantity or weight
--     INDEX idx_guid (guid),
--     FOREIGN KEY (item_id) REFERENCES single_items(id),
--     FOREIGN KEY (basket_id) REFERENCES baskets(id),
--     FOREIGN KEY (customer_id) REFERENCES customers(id)
-- );

-- Create table for customers
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guid CHAR(36) UNIQUE,    -- UUID stored as a CHAR(36) string
    name VARCHAR(255) NOT NULL,
    INDEX idx_guid (guid)   -- Correctly placed INDEX
);

-- Create table for grocers
CREATE TABLE IF NOT EXISTS grocers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guid CHAR(36) UNIQUE,    -- UUID stored as a CHAR(36) string
    name VARCHAR(255) NOT NULL,
    INDEX idx_guid (guid)   -- Correctly placed INDEX
);

-- Create table for baskets
CREATE TABLE IF NOT EXISTS baskets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guid CHAR(36) UNIQUE,    -- UUID stored as a CHAR(36) string
    customer_id CHAR(36) NOT NULL,    -- Foreign key to customers
    INDEX idx_guid (guid),   -- Correctly placed INDEX
    FOREIGN KEY (customer_id) REFERENCES customers(guid)
);

-- Create table for transactions
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guid CHAR(36) UNIQUE,    -- UUID stored as a CHAR(36) string
    customer_id CHAR(36) NOT NULL,  -- Foreign key to customers
    grocer_id CHAR(36) NOT NULL,    -- Foreign key to grocers
    amount DECIMAL(10, 2) NOT NULL,
    status ENUM('NOT_YET_ORDERED', 'ORDERED', 'PENDING', 'PROCESSING', 'SUCCESS') DEFAULT 'NOT_YET_ORDERED',
    INDEX idx_guid (guid),   -- Correctly placed INDEX
    FOREIGN KEY (customer_id) REFERENCES customers(guid),
    FOREIGN KEY (grocer_id) REFERENCES grocers(guid)
);

-- Create table for orders
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guid CHAR(36) UNIQUE,    -- UUID stored as a CHAR(36) string
    customer_id CHAR(36) NOT NULL,  -- Foreign key to customers
    grocer_id CHAR(36) NOT NULL,    -- Foreign key to grocers
    basket_id CHAR(36) NOT NULL,    -- Foreign key to baskets
    total DECIMAL(10, 2) NOT NULL,
    payment_id CHAR(36),    -- Foreign key to transactions
    items JSON DEFAULT '[]',    -- Store items as a JSON array
    INDEX idx_guid (guid),   -- Correctly placed INDEX
    FOREIGN KEY (customer_id) REFERENCES customers(guid),
    FOREIGN KEY (grocer_id) REFERENCES grocers(guid),
    FOREIGN KEY (basket_id) REFERENCES baskets(guid),
    FOREIGN KEY (payment_id) REFERENCES transactions(guid)
);

-- Create table for the order queue
CREATE TABLE IF NOT EXISTS order_queues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guid CHAR(36) UNIQUE,    -- UUID stored as a CHAR(36) string
    grocer_id CHAR(36) NOT NULL,    -- Foreign key to grocers
    baskets JSON DEFAULT '[]',    -- Store baskets as a JSON array
    INDEX idx_guid (guid),   -- Correctly placed INDEX
    FOREIGN KEY (grocer_id) REFERENCES grocers(guid)
);

-- Create table for menus
CREATE TABLE IF NOT EXISTS menus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guid CHAR(36) UNIQUE,    -- UUID stored as a CHAR(36) string
    grocer_id CHAR(36) NOT NULL,    -- Foreign key to grocers
    INDEX idx_guid (guid),   -- Correctly placed INDEX
    FOREIGN KEY (grocer_id) REFERENCES grocers(guid)
);

-- Create table for single items (non-weighted items)
CREATE TABLE IF NOT EXISTS single_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guid CHAR(36) UNIQUE,    -- UUID stored as a CHAR(36) string
    name VARCHAR(255) NOT NULL,
    menu_id CHAR(36) NOT NULL,    -- Foreign key to menus
    grocer_id CHAR(36) NOT NULL,    -- Foreign key to grocers
    price DECIMAL(10, 2) NOT NULL,
    INDEX idx_guid (guid),   -- Correctly placed INDEX
    FOREIGN KEY (menu_id) REFERENCES menus(guid),
    FOREIGN KEY (grocer_id) REFERENCES grocers(guid)
);

-- Create table for weighted items
CREATE TABLE IF NOT EXISTS single_weighted_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guid CHAR(36) UNIQUE,    -- UUID stored as a CHAR(36) string
    name VARCHAR(255) NOT NULL,
    menu_id CHAR(36) NOT NULL,    -- Foreign key to menus
    grocer_id CHAR(36) NOT NULL,    -- Foreign key to grocers
    price DECIMAL(10, 2) NOT NULL,
    weight DECIMAL(10, 2) NOT NULL,    -- Weight of the item
    INDEX idx_guid (guid),   -- Correctly placed INDEX
    FOREIGN KEY (menu_id) REFERENCES menus(guid),
    FOREIGN KEY (grocer_id) REFERENCES grocers(guid)
);

-- Create table for basket items
CREATE TABLE IF NOT EXISTS basket_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guid CHAR(36) UNIQUE,    -- UUID stored as a CHAR(36) string
    item_id CHAR(36) NOT NULL,    -- Foreign key to single_items or single_weighted_items
    basket_id CHAR(36) NOT NULL,    -- Foreign key to baskets
    customer_id CHAR(36) NOT NULL,    -- Foreign key to customers
    total DECIMAL(10, 2) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,    -- Quantity or weight
    INDEX idx_guid (guid),   -- Correctly placed INDEX
    FOREIGN KEY (item_id) REFERENCES single_items(guid),
    FOREIGN KEY (basket_id) REFERENCES baskets(guid),
    FOREIGN KEY (customer_id) REFERENCES customers(guid)
);

-- Add some dummy customers
INSERT INTO customers (guid, name) VALUES
    (UUID(), 'Adolf Johnson'),
    (UUID(), 'Michelle Hitler');

-- Add some dummy grocers
INSERT INTO grocers (guid, name) VALUES
    (UUID(), 'Shuk Givatayim'),
    (UUID(), 'Market Ramat Gan');

-- Add some baskets for the customers
INSERT INTO baskets (guid, customer_id) VALUES
    (UUID(), (SELECT guid FROM customers WHERE name = 'Adolf Johnson' LIMIT 1)),
    (UUID(), (SELECT guid FROM customers WHERE name = 'Michelle Hitler' LIMIT 1));

-- Add some menus
INSERT INTO menus (guid, grocer_id) VALUES
    (UUID(), (SELECT guid FROM grocers WHERE name = 'Shuk Givatayim' LIMIT 1)),
    (UUID(), (SELECT guid FROM grocers WHERE name = 'Market Ramat Gan' LIMIT 1));

-- Add some single items (non-weighted items)
INSERT INTO single_items (guid, name, menu_id, grocer_id, price) VALUES
    (UUID(), '1L Milk', (SELECT guid FROM menus WHERE grocer_id = (SELECT guid FROM grocers WHERE name = 'Shuk Givatayim' LIMIT 1) LIMIT 1), (SELECT guid FROM grocers WHERE name = 'Shuk Givatayim' LIMIT 1), 10.90),
    (UUID(), 'Egg Carton (12)', (SELECT guid FROM menus WHERE grocer_id = (SELECT guid FROM grocers WHERE name = 'Shuk Givatayim' LIMIT 1) LIMIT 1), (SELECT guid FROM grocers WHERE name = 'Shuk Givatayim' LIMIT 1), 18.90),
    (UUID(), 'Honey (250ml)', (SELECT guid FROM menus WHERE grocer_id = (SELECT guid FROM grocers WHERE name = 'Market Ramat Gan' LIMIT 1) LIMIT 1), (SELECT guid FROM grocers WHERE name = 'Market Ramat Gan' LIMIT 1), 13.60);

-- Add some single weighted items
INSERT INTO single_weighted_items (guid, name, menu_id, grocer_id, price, weight) VALUES
    (UUID(), 'Apples (per kg)', (SELECT guid FROM menus WHERE grocer_id = (SELECT guid FROM grocers WHERE name = 'Shuk Givatayim' LIMIT 1) LIMIT 1), (SELECT guid FROM grocers WHERE name = 'Shuk Givatayim' LIMIT 1), 8.90, 1.0),
    (UUID(), 'Chicken Breast (per kg)', (SELECT guid FROM menus WHERE grocer_id = (SELECT guid FROM grocers WHERE name = 'Market Ramat Gan' LIMIT 1) LIMIT 1), (SELECT guid FROM grocers WHERE name = 'Market Ramat Gan' LIMIT 1), 29.90, 1.5);

-- Add some basket items (non-weighted items)
INSERT INTO basket_items (guid, item_id, basket_id, customer_id, total, amount) VALUES
    (UUID(), (SELECT guid FROM single_items WHERE name = '1L Milk' LIMIT 1), (SELECT guid FROM baskets WHERE customer_id = (SELECT guid FROM customers WHERE name = 'Adolf Johnson' LIMIT 1) LIMIT 1), (SELECT guid FROM customers WHERE name = 'Adolf Johnson' LIMIT 1), 10.90, 1),
    (UUID(), (SELECT guid FROM single_items WHERE name = 'Egg Carton (12)' LIMIT 1), (SELECT guid FROM baskets WHERE customer_id = (SELECT guid FROM customers WHERE name = 'Michelle Hitler' LIMIT 1) LIMIT 1), (SELECT guid FROM customers WHERE name = 'Michelle Hitler' LIMIT 1), 18.90, 1);
    -- (UUID(), (SELECT guid FROM single_weighted_items WHERE name = 'Apples (per kg)' LIMIT 1), (SELECT guid FROM baskets WHERE customer_id = (SELECT guid FROM customers WHERE name = 'Adolf Johnson' LIMIT 1) LIMIT 1), (SELECT id FROM customers WHERE name = 'Adolf Johnson' LIMIT 1), 21.90, 1);
