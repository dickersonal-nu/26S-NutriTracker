USE nutritracker;

-- =============================================================
-- ADDITIONAL MEAL_LOGS
-- Extends existing 25 logs. Athlete users: 2, 7, 10
-- Covers 2 full weeks of data across all meal periods.
-- =============================================================
INSERT INTO meal_logs (user_id, log_date, meal_period, logged_at) VALUES
  -- Jason Batum (user 2) — week of 3/17
  (2, '2025-03-17', 'breakfast', '2025-03-17 06:30:00'),
  (2, '2025-03-17', 'lunch',     '2025-03-17 11:30:00'),
  (2, '2025-03-17', 'dinner',    '2025-03-17 17:30:00'),
  (2, '2025-03-18', 'breakfast', '2025-03-18 06:45:00'),
  (2, '2025-03-18', 'lunch',     '2025-03-18 11:45:00'),
  (2, '2025-03-18', 'dinner',    '2025-03-18 17:45:00'),
  (2, '2025-03-19', 'breakfast', '2025-03-19 06:30:00'),
  (2, '2025-03-19', 'lunch',     '2025-03-19 11:30:00'),
  (2, '2025-03-19', 'dinner',    '2025-03-19 17:30:00'),
  (2, '2025-03-20', 'breakfast', '2025-03-20 06:30:00'),
  (2, '2025-03-20', 'lunch',     '2025-03-20 11:30:00'),
  (2, '2025-03-20', 'dinner',    '2025-03-20 17:30:00'),
  (2, '2025-03-21', 'breakfast', '2025-03-21 07:00:00'),
  (2, '2025-03-21', 'lunch',     '2025-03-21 12:00:00'),
  (2, '2025-03-21', 'dinner',    '2025-03-21 18:00:00'),
  (2, '2025-03-22', 'breakfast', '2025-03-22 07:15:00'),
  (2, '2025-03-22', 'lunch',     '2025-03-22 12:15:00'),
  (2, '2025-03-22', 'dinner',    '2025-03-22 18:15:00'),
  (2, '2025-03-23', 'breakfast', '2025-03-23 07:00:00'),
  (2, '2025-03-23', 'lunch',     '2025-03-23 12:00:00'),
  -- Jason Batum — week of 3/24
  (2, '2025-03-24', 'breakfast', '2025-03-24 06:30:00'),
  (2, '2025-03-24', 'lunch',     '2025-03-24 11:30:00'),
  (2, '2025-03-24', 'dinner',    '2025-03-24 17:30:00'),
  (2, '2025-03-25', 'breakfast', '2025-03-25 06:45:00'),
  (2, '2025-03-25', 'lunch',     '2025-03-25 11:45:00'),
  (2, '2025-03-25', 'dinner',    '2025-03-25 17:45:00'),
  (2, '2025-03-26', 'breakfast', '2025-03-26 06:30:00'),
  (2, '2025-03-26', 'lunch',     '2025-03-26 11:30:00'),
  (2, '2025-03-26', 'dinner',    '2025-03-26 17:30:00'),
  (2, '2025-03-27', 'breakfast', '2025-03-27 06:30:00'),
  (2, '2025-03-27', 'lunch',     '2025-03-27 11:30:00'),
  (2, '2025-03-27', 'dinner',    '2025-03-27 17:30:00'),
  (2, '2025-03-28', 'breakfast', '2025-03-28 06:45:00'),
  (2, '2025-03-28', 'lunch',     '2025-03-28 11:45:00'),
  (2, '2025-03-28', 'dinner',    '2025-03-28 17:45:00'),
  -- Diego Reyes (user 7) — week of 3/29
  (7, '2025-03-29', 'breakfast', '2025-03-29 07:00:00'),
  (7, '2025-03-29', 'lunch',     '2025-03-29 12:00:00'),
  (7, '2025-03-29', 'dinner',    '2025-03-29 18:00:00'),
  (7, '2025-03-30', 'breakfast', '2025-03-30 07:00:00'),
  (7, '2025-03-30', 'lunch',     '2025-03-30 12:00:00'),
  (7, '2025-03-30', 'dinner',    '2025-03-30 18:00:00'),
  (7, '2025-03-31', 'breakfast', '2025-03-31 07:15:00'),
  (7, '2025-03-31', 'lunch',     '2025-03-31 12:15:00'),
  (7, '2025-03-31', 'dinner',    '2025-03-31 18:15:00'),
  (7, '2025-04-01', 'breakfast', '2025-04-01 07:00:00'),
  (7, '2025-04-01', 'lunch',     '2025-04-01 12:00:00'),
  (7, '2025-04-01', 'dinner',    '2025-04-01 18:00:00'),
  (7, '2025-04-02', 'breakfast', '2025-04-02 07:00:00'),
  (7, '2025-04-02', 'lunch',     '2025-04-02 12:00:00'),
  (7, '2025-04-02', 'dinner',    '2025-04-02 18:00:00'),
  (7, '2025-04-03', 'breakfast', '2025-04-03 07:00:00'),
  (7, '2025-04-03', 'lunch',     '2025-04-03 12:00:00'),
  (7, '2025-04-03', 'dinner',    '2025-04-03 18:00:00'),
  -- Tyler Brooks (user 10) — week of 3/29
  (10,'2025-03-29', 'breakfast', '2025-03-29 07:15:00'),
  (10,'2025-03-29', 'lunch',     '2025-03-29 12:30:00'),
  (10,'2025-03-29', 'dinner',    '2025-03-29 18:30:00'),
  (10,'2025-03-30', 'breakfast', '2025-03-30 07:15:00'),
  (10,'2025-03-30', 'lunch',     '2025-03-30 12:30:00'),
  (10,'2025-03-30', 'dinner',    '2025-03-30 18:30:00'),
  (10,'2025-03-31', 'breakfast', '2025-03-31 07:15:00'),
  (10,'2025-03-31', 'lunch',     '2025-03-31 12:30:00'),
  (10,'2025-04-01', 'breakfast', '2025-04-01 07:15:00'),
  (10,'2025-04-01', 'lunch',     '2025-04-01 12:30:00'),
  (10,'2025-04-01', 'dinner',    '2025-04-01 18:30:00'),
  (10,'2025-04-02', 'breakfast', '2025-04-02 07:15:00'),
  (10,'2025-04-02', 'lunch',     '2025-04-02 12:30:00'),
  (10,'2025-04-03', 'breakfast', '2025-04-03 07:15:00'),
  (10,'2025-04-03', 'lunch',     '2025-04-03 12:30:00'),
  (10,'2025-04-03', 'dinner',    '2025-04-03 18:30:00');


-- =============================================================
-- ADDITIONAL MEAL_LOG_ITEMS
-- log_ids 26-91 correspond to the logs inserted above.
-- item_ids 1-35 are all valid from 02_nutritracker_data.sql
-- =============================================================
INSERT INTO meal_log_items (log_id, item_id, servings) VALUES
  -- Log 26: Jason breakfast 3/17
  (26, 1, 2.0), (26, 4, 1.0), (26, 26, 1.0),
  -- Log 27: Jason lunch 3/17
  (27, 6, 2.0), (27, 7, 2.0), (27, 13, 1.0),
  -- Log 28: Jason dinner 3/17
  (28, 11, 1.5), (28, 12, 1.0), (28, 13, 1.0), (28, 26, 1.0),
  -- Log 29: Jason breakfast 3/18
  (29, 3, 1.0), (29, 4, 1.0), (29, 5, 2.0),
  -- Log 30: Jason lunch 3/18
  (30, 6, 2.0), (30, 7, 1.5), (30, 9, 1.0),
  -- Log 31: Jason dinner 3/18
  (31, 21, 1.5), (31, 22, 2.0), (31, 24, 1.0),
  -- Log 32: Jason breakfast 3/19
  (32, 1, 2.0), (32, 26, 1.0), (32, 30, 1.0),
  -- Log 33: Jason lunch 3/19
  (33, 29, 1.0), (33, 7, 1.5), (33, 13, 1.0),
  -- Log 34: Jason dinner 3/19
  (34, 14, 1.0), (34, 12, 1.0), (34, 13, 2.0),
  -- Log 35: Jason breakfast 3/20
  (35, 27, 1.0), (35, 26, 1.0), (35, 5, 1.0),
  -- Log 36: Jason lunch 3/20
  (36, 6, 2.0), (36, 7, 2.0), (36, 18, 1.0),
  -- Log 37: Jason dinner 3/20
  (37, 11, 1.0), (37, 22, 2.0), (37, 13, 1.0), (37, 26, 1.0),
  -- Log 38: Jason breakfast 3/21
  (38, 4, 1.0), (38, 1, 2.0), (38, 5, 1.0),
  -- Log 39: Jason lunch 3/21
  (39, 16, 1.0), (39, 7, 1.5), (39, 18, 1.0),
  -- Log 40: Jason dinner 3/21
  (40, 21, 1.0), (40, 22, 1.5), (40, 13, 1.0),
  -- Log 41: Jason breakfast 3/22
  (41, 28, 1.0), (41, 26, 1.0), (41, 30, 1.0),
  -- Log 42: Jason lunch 3/22
  (42, 6, 2.0), (42, 9, 1.0), (42, 7, 1.5),
  -- Log 43: Jason dinner 3/22
  (43, 11, 1.5), (43, 12, 1.0), (43, 24, 1.0), (43, 26, 1.0),
  -- Log 44: Jason breakfast 3/23
  (44, 1, 2.0), (44, 4, 1.0), (44, 5, 2.0),
  -- Log 45: Jason lunch 3/23
  (45, 29, 1.0), (45, 13, 1.0), (45, 33, 1.0),
  -- Log 46: Jason breakfast 3/24
  (46, 27, 1.0), (46, 26, 1.0), (46, 30, 1.0),
  -- Log 47: Jason lunch 3/24
  (47, 6, 2.0), (47, 7, 2.0), (47, 13, 1.0),
  -- Log 48: Jason dinner 3/24
  (48, 11, 1.0), (48, 12, 1.5), (48, 13, 1.0), (48, 26, 1.0),
  -- Log 49: Jason breakfast 3/25
  (49, 1, 2.0), (49, 4, 1.0), (49, 5, 1.0),
  -- Log 50: Jason lunch 3/25
  (50, 6, 2.0), (50, 7, 1.5), (50, 18, 1.0),
  -- Log 51: Jason dinner 3/25
  (51, 21, 1.5), (51, 22, 2.0), (51, 13, 1.0),
  -- Log 52: Jason breakfast 3/26
  (52, 28, 1.0), (52, 26, 1.0), (52, 5, 1.0),
  -- Log 53: Jason lunch 3/26
  (53, 6, 2.0), (53, 9, 1.0), (53, 7, 1.5),
  -- Log 54: Jason dinner 3/26
  (54, 11, 1.5), (54, 12, 1.0), (54, 24, 1.0), (54, 26, 1.0),
  -- Log 55: Jason breakfast 3/27
  (55, 4, 1.0), (55, 1, 2.0), (55, 30, 1.0),
  -- Log 56: Jason lunch 3/27
  (56, 29, 1.0), (56, 7, 1.5), (56, 13, 1.0),
  -- Log 57: Jason dinner 3/27
  (57, 14, 1.0), (57, 15, 1.0), (57, 13, 1.0),
  -- Log 58: Jason breakfast 3/28
  (58, 27, 1.0), (58, 26, 1.0), (58, 5, 2.0),
  -- Log 59: Jason lunch 3/28
  (59, 6, 2.0), (59, 7, 2.0), (59, 9, 1.0),
  -- Log 60: Jason dinner 3/28
  (60, 11, 1.0), (60, 22, 2.0), (60, 13, 2.0), (60, 26, 1.0),
  -- Log 61: Diego breakfast 3/29
  (61, 4, 1.0), (61, 26, 1.0), (61, 5, 1.0),
  -- Log 62: Diego lunch 3/29
  (62, 6, 2.0), (62, 7, 1.5), (62, 18, 1.0),
  -- Log 63: Diego dinner 3/29
  (63, 14, 1.0), (63, 15, 1.0), (63, 13, 1.0),
  -- Log 64: Diego breakfast 3/30
  (64, 1, 1.0), (64, 4, 1.0), (64, 5, 1.0),
  -- Log 65: Diego lunch 3/30
  (65, 6, 2.0), (65, 7, 1.5), (65, 9, 1.0),
  -- Log 66: Diego dinner 3/30
  (66, 11, 1.0), (66, 12, 1.0), (66, 13, 1.0),
  -- Log 67: Diego breakfast 3/31
  (67, 28, 1.0), (67, 26, 1.0), (67, 5, 1.0),
  -- Log 68: Diego lunch 3/31
  (68, 29, 1.0), (68, 18, 1.0), (68, 20, 1.0),
  -- Log 69: Diego dinner 3/31
  (69, 21, 1.0), (69, 22, 1.5), (69, 24, 1.0),
  -- Log 70: Diego breakfast 4/1
  (70, 4, 1.0), (70, 5, 2.0), (70, 30, 1.0),
  -- Log 71: Diego lunch 4/1
  (71, 6, 2.0), (71, 7, 2.0), (71, 13, 1.0),
  -- Log 72: Diego dinner 4/1
  (72, 14, 1.0), (72, 12, 1.0), (72, 33, 1.0),
  -- Log 73: Diego breakfast 4/2
  (73, 27, 1.0), (73, 26, 1.0), (73, 5, 1.0),
  -- Log 74: Diego lunch 4/2
  (74, 6, 1.5), (74, 7, 1.5), (74, 18, 1.0),
  -- Log 75: Diego dinner 4/2
  (75, 11, 1.0), (75, 22, 1.0), (75, 13, 1.0),
  -- Log 76: Diego breakfast 4/3
  (76, 1, 1.0), (76, 4, 1.0), (76, 5, 1.0),
  -- Log 77: Diego lunch 4/3
  (77, 16, 1.0), (77, 18, 1.0), (77, 20, 1.0),
  -- Log 78: Diego dinner 4/3
  (78, 21, 1.0), (78, 22, 1.5), (78, 13, 1.0),
  -- Log 79: Tyler breakfast 3/29
  (79, 28, 1.0), (79, 3, 1.0), (79, 5, 1.0),
  -- Log 80: Tyler lunch 3/29
  (80, 29, 1.0), (80, 18, 1.0), (80, 35, 1.0),
  -- Log 81: Tyler dinner 3/29
  (81, 11, 1.0), (81, 12, 1.0), (81, 13, 1.0),
  -- Log 82: Tyler breakfast 3/30
  (82, 3, 1.0), (82, 5, 1.0), (82, 30, 1.0),
  -- Log 83: Tyler lunch 3/30
  (83, 6, 1.0), (83, 7, 1.0), (83, 18, 1.0),
  -- Log 84: Tyler dinner 3/30
  (84, 21, 1.0), (84, 22, 1.0), (84, 13, 1.0),
  -- Log 85: Tyler breakfast 3/31
  (85, 28, 1.0), (85, 26, 1.0), (85, 5, 1.0),
  -- Log 86: Tyler lunch 3/31
  (86, 29, 1.0), (86, 18, 1.0), (86, 20, 1.0),
  -- Log 87: Tyler breakfast 4/1
  (87, 4, 1.0), (87, 5, 1.0), (87, 30, 1.0),
  -- Log 88: Tyler lunch 4/1
  (88, 6, 1.0), (88, 7, 1.0), (88, 13, 1.0),
  -- Log 89: Tyler dinner 4/1
  (89, 11, 1.0), (89, 12, 1.0), (89, 33, 1.0),
  -- Log 90: Tyler breakfast 4/2
  (90, 3, 1.0), (90, 5, 1.0), (90, 30, 1.0),
  -- Log 91: Tyler lunch 4/3
  (91, 29, 1.0), (91, 18, 1.0), (91, 35, 1.0);


-- =============================================================
-- ADDITIONAL NUTRITION_GOALS
-- Expanding to ~50 total rows across all athlete users.
-- =============================================================
INSERT INTO nutrition_goals (user_id, nutrient_id, min_value, max_value, period, effective_from, effective_to) VALUES
  -- Jason Batum — additional nutrients
  (2, 9,   NULL,  50.0, 'daily', '2025-01-15', NULL),
  (2, 3,   NULL,  20.0, 'daily', '2025-01-15', NULL),
  (2, 12, 1000.0, NULL, 'daily', '2025-01-15', NULL),
  (2, 14, 3500.0, NULL, 'daily', '2025-01-15', NULL),
  (2, 16,   90.0, NULL, 'daily', '2025-01-15', NULL),
  -- Diego Reyes — additional nutrients
  (7, 2,   NULL,  70.0, 'daily', '2025-01-20', NULL),
  (7, 6,   NULL, 2300.0,'daily', '2025-01-20', NULL),
  (7, 8,   25.0,  NULL, 'daily', '2025-01-20', NULL),
  (7, 9,   NULL,  60.0, 'daily', '2025-01-20', NULL),
  (7, 12, 1000.0, NULL, 'daily', '2025-01-20', NULL),
  -- Tyler Brooks — additional nutrients
  (10, 2,  NULL,  65.0, 'daily', '2025-02-10', NULL),
  (10, 7, 280.0, 380.0, 'daily', '2025-02-10', NULL),
  (10, 8,  25.0,  NULL, 'daily', '2025-02-10', NULL),
  (10, 9,  NULL,  55.0, 'daily', '2025-02-10', NULL),
  (10, 12,1000.0, NULL, 'daily', '2025-02-10', NULL),
  -- Jason — weekly goals
  (2, 1,  21000.0, 24500.0, 'weekly', '2025-01-15', NULL),
  (2, 10,  1400.0,  1750.0, 'weekly', '2025-01-15', NULL),
  -- Diego — weekly goals
  (7, 1,  19600.0, 22400.0, 'weekly', '2025-01-20', NULL),
  (7, 10,  1260.0,  1540.0, 'weekly', '2025-01-20', NULL),
  -- Tyler — weekly goals
  (10, 1, 17500.0, 21000.0, 'weekly', '2025-02-10', NULL),
  (10, 10, 1120.0,  1400.0, 'weekly', '2025-02-10', NULL),
  -- Previous season goals for Jason (expired)
  (2, 1,  2800.0, 3200.0, 'daily', '2024-09-01', '2025-01-14'),
  (2, 10,  180.0,  220.0, 'daily', '2024-09-01', '2025-01-14'),
  (7, 1,  2600.0, 3000.0, 'daily', '2024-09-01', '2025-01-19'),
  (7, 10,  160.0,  200.0, 'daily', '2024-09-01', '2025-01-19'),
  (10, 1, 2300.0, 2800.0, 'daily', '2024-09-01', '2025-02-09'),
  (10, 10, 140.0,  180.0, 'daily', '2024-09-01', '2025-02-09'),
  -- Jordan Carter — additional nutrients
  (1, 7,  200.0,  275.0, 'daily', '2025-01-01', NULL),
  (1, 8,   25.0,   NULL, 'daily', '2025-01-01', NULL),
  (1, 9,   NULL,   50.0, 'daily', '2025-01-01', NULL);


-- =============================================================
-- ADDITIONAL ALERTS
-- Expanding to ~60 total rows.
-- =============================================================
INSERT INTO alerts (user_id, goal_id, alert_type, message, is_read, triggered_at) VALUES
  -- Jason — various nutrient alerts across dates
  (2, 4,  'below_min',    'You are below your minimum calorie goal of 3000 kcal.', TRUE,  '2025-03-17 15:00:00'),
  (2, 5,  'below_min',    'Your protein intake is below your daily minimum of 200g.', TRUE,  '2025-03-17 15:00:00'),
  (2, 8,  'exceeded_max', 'Your sodium intake has exceeded your daily maximum of 2500mg.', TRUE,  '2025-03-18 18:30:00'),
  (2, 4,  'below_min',    'You are below your minimum calorie goal of 3000 kcal.', TRUE,  '2025-03-19 14:00:00'),
  (2, 5,  'below_min',    'Your protein intake is below your daily minimum of 200g.', TRUE,  '2025-03-20 14:00:00'),
  (2, 6,  'below_min',    'Your carbohydrate intake is below your daily minimum of 350g.', TRUE,  '2025-03-21 14:00:00'),
  (2, 8,  'exceeded_max', 'Your sodium intake has exceeded your daily maximum of 2500mg.', TRUE,  '2025-03-22 18:30:00'),
  (2, 4,  'below_min',    'You are below your minimum calorie goal of 3000 kcal.', TRUE,  '2025-03-23 14:00:00'),
  (2, 5,  'below_min',    'Your protein intake is below your daily minimum of 200g.', TRUE,  '2025-03-24 14:00:00'),
  (2, 4,  'below_min',    'You are below your minimum calorie goal of 3000 kcal.', TRUE,  '2025-03-25 14:00:00'),
  (2, 8,  'exceeded_max', 'Your sodium intake has exceeded your daily maximum of 2500mg.', TRUE,  '2025-03-26 18:30:00'),
  (2, 5,  'below_min',    'Your protein intake is below your daily minimum of 200g.', TRUE,  '2025-03-27 14:00:00'),
  (2, 6,  'below_min',    'Your carbohydrate intake is below your daily minimum of 350g.', TRUE,  '2025-03-28 14:00:00'),
  (2, 4,  'below_min',    'You are below your minimum calorie goal of 3000 kcal.', FALSE, '2025-04-01 14:00:00'),
  (2, 5,  'below_min',    'Your protein intake is below your daily minimum of 200g.', FALSE, '2025-04-02 14:00:00'),
  (2, 8,  'exceeded_max', 'Your sodium intake has exceeded your daily maximum of 2500mg.', FALSE, '2025-04-03 18:30:00'),
  -- Diego Reyes alerts
  (7, 13, 'below_min',    'You are below your minimum calorie goal of 2800 kcal.', TRUE,  '2025-03-29 15:00:00'),
  (7, 14, 'below_min',    'Your protein intake is below your daily minimum of 180g.', TRUE,  '2025-03-29 15:00:00'),
  (7, 16, 'exceeded_max', 'Your sodium intake has exceeded your daily maximum of 2300mg.', TRUE,  '2025-03-30 18:00:00'),
  (7, 13, 'below_min',    'You are below your minimum calorie goal of 2800 kcal.', TRUE,  '2025-03-31 15:00:00'),
  (7, 14, 'below_min',    'Your protein intake is below your daily minimum of 180g.', TRUE,  '2025-04-01 15:00:00'),
  (7, 13, 'below_min',    'You are below your minimum calorie goal of 2800 kcal.', TRUE,  '2025-04-02 15:00:00'),
  (7, 16, 'exceeded_max', 'Your sodium intake has exceeded your daily maximum of 2300mg.', FALSE, '2025-04-03 18:00:00'),
  (7, 13, 'below_min',    'You are below your minimum calorie goal of 2800 kcal.', FALSE, '2025-04-04 15:00:00'),
  -- Tyler Brooks alerts
  (10, 16,'below_min',    'You are below your minimum calorie goal of 2500 kcal.', TRUE,  '2025-03-29 15:00:00'),
  (10, 17,'exceeded_max', 'Your sodium intake is approaching your daily maximum of 2000mg.', TRUE,  '2025-03-30 18:00:00'),
  (10, 16,'below_min',    'You are below your minimum calorie goal of 2500 kcal.', TRUE,  '2025-03-31 15:00:00'),
  (10, 16,'below_min',    'You are below your minimum calorie goal of 2500 kcal.', TRUE,  '2025-04-01 15:00:00'),
  (10, 17,'exceeded_max', 'Your sodium intake is approaching your daily maximum of 2000mg.', TRUE,  '2025-04-02 18:00:00'),
  (10, 16,'below_min',    'You are below your minimum calorie goal of 2500 kcal.', FALSE, '2025-04-03 15:00:00'),
  -- Jordan Carter alerts
  (1, 2,  'below_min',    'Your protein intake is below your daily minimum of 120g.', TRUE,  '2025-03-30 20:00:00'),
  (1, 1,  'exceeded_max', 'Your calorie intake has exceeded your daily maximum of 2200 kcal.', TRUE,  '2025-03-31 20:00:00'),
  (1, 2,  'below_min',    'Your protein intake is below your daily minimum of 120g.', FALSE, '2025-04-04 20:00:00'),
  -- System alerts
  (4, NULL,'system',      'Database backup completed successfully.', TRUE,  '2025-03-30 03:00:00'),
  (4, NULL,'system',      'Scheduled nightly data sync completed successfully.', TRUE,  '2025-03-31 02:00:00'),
  (4, NULL,'system',      'High server load detected — 95% CPU usage for 10 minutes.', TRUE,  '2025-04-01 14:30:00'),
  (4, NULL,'system',      'Database backup completed successfully.', TRUE,  '2025-04-02 03:00:00'),
  (4, NULL,'system',      'Scheduled nightly data sync completed successfully.', TRUE,  '2025-04-03 02:00:00'),
  (4, NULL,'system',      'Scheduled nightly data sync completed successfully.', FALSE, '2025-04-04 02:00:00'),
  (4, NULL,'system',      'SSL certificate expiring in 30 days — renewal required.', FALSE, '2025-04-04 08:00:00');
