-- =============================================================
-- Admin seed data — INSERTs into existing DDL tables
-- Run AFTER 01_nutritracker_ddl.sql
-- =============================================================

USE nutritracker;


-- ----- demographics (IDs 1–10) -----
INSERT INTO demographics (student_type, major, college_year, athletic_team, dietary_label) VALUES
 ('undergraduate', 'Music Technology', 'junior', NULL, 'none'),
 ('undergraduate', 'Sports Science', 'freshman', 'Men\'s Basketball', 'none'),
 ('staff', 'Data Science', NULL, NULL, 'none'),
 ('staff', 'Computer Science', NULL, NULL, 'none'),
 ('undergraduate', 'Biology', 'sophomore', NULL, 'vegetarian'),
 ('undergraduate', 'Computer Science', 'senior', NULL, 'vegan'),
 ('undergraduate', 'Mechanical Engineering', 'junior', 'Men\'s Soccer', 'none'),
 ('graduate', 'Public Health', NULL, NULL, 'gluten-free'),
 ('undergraduate', 'Nursing', 'freshman', NULL, 'none'),
 ('undergraduate', 'Business Administration', 'senior', 'Women\'s Tennis', 'none');


-- ----- users (IDs 1–10, Laura = user_id 4, role_id 4 = administrator) -----
INSERT INTO users (role_id, demographic_id, first_name, last_name, email, password_hash, is_active, last_login) VALUES
 (1, 1,  'Jordan',    'Carter',    'j.carter@northeastern.edu',    '$2b$12$KIXxHDdSrPHPHPHP1234560uQwErTyUiOpAsDfGhJkLzXcVbNm12', TRUE, '2025-04-04 08:32:00'),
 (2, 2,  'Jason',     'Batum',     'j.batum@northeastern.edu',     '$2b$12$KIXxHDdSrPHPHPHP1234561uQwErTyUiOpAsDfGhJkLzXcVbNm12', TRUE, '2025-04-04 07:15:00'),
 (3, 3,  'Immanuel',  'Hoffborne', 'i.hoffborne@northeastern.edu', '$2b$12$KIXxHDdSrPHPHPHP1234562uQwErTyUiOpAsDfGhJkLzXcVbNm12', TRUE, '2025-04-03 14:00:00'),
 (4, 4,  'Laura',     'Smith',     'l.smith@northeastern.edu',     '$2b$12$KIXxHDdSrPHPHPHP1234563uQwErTyUiOpAsDfGhJkLzXcVbNm12', TRUE, '2025-04-04 09:00:00'),
 (1, 5,  'Priya',     'Nair',      'p.nair@northeastern.edu',      '$2b$12$KIXxHDdSrPHPHPHP1234564uQwErTyUiOpAsDfGhJkLzXcVbNm12', TRUE, '2025-04-04 11:20:00'),
 (1, 6,  'Marcus',    'Webb',      'm.webb@northeastern.edu',      '$2b$12$KIXxHDdSrPHPHPHP1234565uQwErTyUiOpAsDfGhJkLzXcVbNm12', TRUE, '2025-04-03 20:45:00'),
 (2, 7,  'Diego',     'Reyes',     'd.reyes@northeastern.edu',     '$2b$12$KIXxHDdSrPHPHPHP1234566uQwErTyUiOpAsDfGhJkLzXcVbNm12', TRUE, '2025-04-04 06:50:00'),
 (3, 8,  'Anika',     'Patel',     'a.patel@northeastern.edu',     '$2b$12$KIXxHDdSrPHPHPHP1234567uQwErTyUiOpAsDfGhJkLzXcVbNm12', TRUE, '2025-04-02 16:30:00'),
 (1, 9,  'Sofia',     'Moran',     's.moran@northeastern.edu',     '$2b$12$KIXxHDdSrPHPHPHP1234568uQwErTyUiOpAsDfGhJkLzXcVbNm12', TRUE, '2025-04-04 12:10:00'),
 (2, 10, 'Tyler',     'Brooks',    't.brooks@northeastern.edu',    '$2b$12$KIXxHDdSrPHPHPHP1234569uQwErTyUiOpAsDfGhJkLzXcVbNm12', TRUE, '2025-04-04 07:00:00');


-- ----- dining_halls (IDs 1–5) -----
INSERT INTO dining_halls (name, location, building_code, latitude, longitude, operating_hours, is_active) VALUES
 ('Stetson East', 'Willis Avenue, Boston MA', 'STE', 42.339200, -71.087800,
  '{"mon-fri": {"open": "07:00", "close": "22:00"}, "sat-sun": {"open": "09:00", "close": "21:00"}}', TRUE),
 ('Stetson West', 'Leon Street, Boston MA', 'STW', 42.338900, -71.088500,
  '{"mon-fri": {"open": "07:00", "close": "21:00"}, "sat-sun": {"open": "09:00", "close": "20:00"}}', TRUE),
 ('International Village', 'Davenport Street, Boston MA', 'IV', 42.336700, -71.086200,
  '{"mon-fri": {"open": "07:00", "close": "23:00"}, "sat-sun": {"open": "10:00", "close": "22:00"}}', TRUE),
 ('Levine Marketplace', 'Forsyth Street, Boston MA', 'LM', 42.340100, -71.089300,
  '{"mon-fri": {"open": "08:00", "close": "20:00"}, "sat-sun": {"open": "10:00", "close": "18:00"}}', TRUE),
 ('Outtakes Express', 'Curry Student Center, Boston MA', 'OE', 42.338500, -71.090100,
  '{"mon-fri": {"open": "10:00", "close": "20:00"}, "sat": {"open": "11:00", "close": "17:00"}, "sun": "closed"}', TRUE);


-- ----- system_metrics -----
INSERT INTO system_metrics (metric_type, value, unit, recorded_at) VALUES
 ('active_users',        142.0000, 'count',   '2025-04-01 08:00:00'),
 ('api_requests_per_min', 38.5000, 'count',   '2025-04-01 08:00:00'),
 ('db_query_avg_ms',      12.3000, 'ms',      '2025-04-10 09:00:00'),
 ('active_users',        158.0000, 'count',   '2025-04-15 08:00:00'),
 ('api_requests_per_min', 41.0000, 'count',   '2025-04-15 08:00:00'),
 ('error_rate',            2.1000, 'percent', '2025-04-15 08:00:00'),
 ('response_time_ms',    87.0000,  'ms',      '2025-04-17 10:00:00');


-- ----- reports -----
INSERT INTO reports (created_by, title, report_type, status, generated_at) VALUES
 (3, 'April Nutrition Summary',    'nutrition_summary', 'complete', '2025-04-15 12:00:00'),
 (3, 'Weekly Active Users Report', 'trend_analysis',    'complete', '2025-04-14 09:00:00'),
 (4, 'Q1 Budget Overview',         'nutrition_summary', 'complete', '2025-04-01 10:00:00'),
 (NULL, 'System Health Weekly',    'trend_analysis',    'pending',  NULL);


-- ----- alerts -----
INSERT INTO alerts (user_id, goal_id, alert_type, message, is_read) VALUES
 (2, 1,    'exceeded_max', 'Sodium intake exceeded daily maximum (2300 mg).', FALSE),
 (7, NULL, 'system',       'Scheduled maintenance window tonight 2-4 AM.',    FALSE),
 (1, NULL, 'below_min',    'Protein intake below daily minimum (50 g).',      FALSE),
 (5, NULL, 'system',       'New menu items added to Stetson East.',           TRUE);


-- ----- audit_logs -----
INSERT INTO audit_logs (user_id, table_name, action, old_values, new_values) VALUES
 (4, 'users',      'UPDATE', '{"role_id": 1}', '{"role_id": 2}'),
 (4, 'menu_items', 'UPDATE', NULL, '{"hall_id": 1, "items_updated": 3, "effective_date": "2025-04-20"}'),
 (4, 'users',      'UPDATE', '{"is_active": true}', '{"is_active": false}');
