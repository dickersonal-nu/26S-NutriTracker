DROP TABLE IF EXISTS AuditLog;
DROP TABLE IF EXISTS Alerts;
DROP TABLE IF EXISTS Reports;
DROP TABLE IF EXISTS SystemMetrics;
DROP TABLE IF EXISTS MenuItems;
DROP TABLE IF EXISTS Users;


CREATE TABLE Users (
    user_id        INT          AUTO_INCREMENT PRIMARY KEY,
    username       VARCHAR(64)  NOT NULL UNIQUE,
    email          VARCHAR(128) NOT NULL UNIQUE,
    role           VARCHAR(32)  NOT NULL DEFAULT 'student',
                                -- valid: student | staff | admin | nutrition_manager | guest
    is_active      TINYINT(1)   NOT NULL DEFAULT 1,
    deactivated_at DATETIME     DEFAULT NULL,
    created_at     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE AuditLog (
    log_id      INT           AUTO_INCREMENT PRIMARY KEY,
    action      VARCHAR(64)   NOT NULL,   -- e.g. 'update_role', 'push_menu_update', 'deactivate_user'
    target_type VARCHAR(64)   NOT NULL,   -- e.g. 'user', 'dining_hall'
    target_id   INT           NOT NULL,
    detail      VARCHAR(512)  DEFAULT NULL,
    timestamp   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE SystemMetrics (
    metric_id   INT           AUTO_INCREMENT PRIMARY KEY,
    metric_name VARCHAR(128)  NOT NULL,
    metric_value DECIMAL(12,4) NOT NULL,
    recorded_at DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE Reports (
    report_id   INT          AUTO_INCREMENT PRIMARY KEY,
    report_type VARCHAR(64)  NOT NULL,   -- e.g. 'nutrition', 'usage', 'financial'
    title       VARCHAR(256) NOT NULL,
    content     TEXT         DEFAULT NULL,
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE Alerts (
    alert_id    INT          AUTO_INCREMENT PRIMARY KEY,
    title       VARCHAR(256) NOT NULL,
    detail      TEXT         DEFAULT NULL,
    severity    VARCHAR(32)  NOT NULL DEFAULT 'info',
                             -- suggested values: info | warning | critical
    resolved    TINYINT(1)   NOT NULL DEFAULT 0,
    resolved_at DATETIME     DEFAULT NULL,
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE MenuItems (
    item_id        INT           AUTO_INCREMENT PRIMARY KEY,
    dining_hall_id INT           NOT NULL,
    item_name      VARCHAR(256)  NOT NULL,
    calories       INT           DEFAULT NULL,
    effective_date DATE          DEFAULT NULL
);


INSERT INTO Users (username, email, role) VALUES
    ('alice_admin',   'alice@nutritracker.com',   'admin'),
    ('bob_staff',     'bob@nutritracker.com',      'staff'),
    ('carol_student', 'carol@nutritracker.com',    'student'),
    ('dan_nutrition', 'dan@nutritracker.com',      'nutrition_manager'),
    ('eve_guest',     'eve@nutritracker.com',      'guest');

INSERT INTO SystemMetrics (metric_name, metric_value, recorded_at) VALUES
    ('active_users',        142,    '2025-04-01 08:00:00'),
    ('api_requests_per_min', 38.5,  '2025-04-01 08:00:00'),
    ('db_query_avg_ms',      12.3,  '2025-04-10 09:00:00'),
    ('active_users',        158,    '2025-04-15 08:00:00'),
    ('api_requests_per_min', 41.0,  '2025-04-15 08:00:00');

INSERT INTO Reports (report_type, title, content) VALUES
    ('nutrition', 'April Nutrition Summary',   'Average daily caloric intake across dining halls for April 2025.'),
    ('usage',     'Weekly Active Users Report','User login activity for the week of April 14–20 2025.'),
    ('financial', 'Q1 Budget Overview',        'Dining services expenditure breakdown for Q1 2025.');

INSERT INTO Alerts (title, detail, severity, resolved) VALUES
    ('High API Error Rate',    'Error rate exceeded 5% threshold at 2:00 AM.',   'critical', 0),
    ('Low Dining Hall Stock',  'North Hall running low on protein options.',      'warning',  0),
    ('Scheduled Maintenance',  'DB backup scheduled for Sunday 3:00 AM.',        'info',     0),
    ('Resolved: Login Spike',  'Unusual login volume resolved after 10 minutes.','warning',  1);

INSERT INTO MenuItems (dining_hall_id, item_name, calories, effective_date) VALUES
    (1, 'Grilled Chicken',   350, '2025-04-21'),
    (1, 'Caesar Salad',      220, '2025-04-21'),
    (1, 'Pasta Marinara',    480, '2025-04-21'),
    (2, 'Turkey Sandwich',   410, '2025-04-21'),
    (2, 'Vegetable Stir Fry',300, '2025-04-21');

INSERT INTO AuditLog (action, target_type, target_id, detail) VALUES
    ('update_role',    'user',        2, 'Role changed from ''guest'' to ''staff'''),
    ('push_menu_update','dining_hall', 1, 'Menu updated for 2025-04-20 — 3 items'),
    ('deactivate_user','user',        5, 'User ''eve_guest'' deactivated');