from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

nutrition = Blueprint('nutrition', __name__)


@nutrition.route('/daily/<int:user_id>', methods=['GET'])
def get_daily_nutrition(user_id):
    log_date = request.args.get('date', '2025-04-04')
    cursor = get_db().cursor(dictionary=True)
    try:
        query = '''
            SELECT n.name AS nutrient, n.unit,
                   ROUND(SUM(min_t.amount * mli.servings), 2) AS total_intake,
                   ng.min_value, ng.max_value
            FROM meal_logs ml
            JOIN meal_log_items mli        ON ml.log_id         = mli.log_id
            JOIN menu_item_nutrients min_t ON mli.item_id       = min_t.item_id
            JOIN nutrients n               ON min_t.nutrient_id = n.nutrient_id
            LEFT JOIN nutrition_goals ng   ON ng.user_id        = ml.user_id
              AND ng.nutrient_id = n.nutrient_id
              AND ml.log_date BETWEEN ng.effective_from
                  AND COALESCE(ng.effective_to, '9999-12-31')
            WHERE ml.user_id  = %s
              AND ml.log_date = %s
            GROUP BY n.nutrient_id, n.name, n.unit, ng.min_value, ng.max_value
        '''
        cursor.execute(query, (user_id, log_date))
        results = cursor.fetchall()
        return jsonify(results), 200
    except Error as e:
        current_app.logger.error(f'GET /nutrition/daily/{user_id} error: {e}')
        return jsonify({'error': str(e)}), 500


@nutrition.route('/menu', methods=['GET'])
def get_menu_nutrition():
    available_date = request.args.get('date', '2025-04-04')
    cursor = get_db().cursor(dictionary=True)
    try:
        query = '''
            SELECT mi.name AS menu_item, mi.description, dh.name AS dining_hall,
                   n.name AS nutrient, n.unit, min_t.amount
            FROM menu_items mi
            JOIN dining_halls dh           ON mi.hall_id        = dh.hall_id
            JOIN menu_item_nutrients min_t ON mi.item_id        = min_t.item_id
            JOIN nutrients n               ON min_t.nutrient_id = n.nutrient_id
            WHERE mi.available_date = %s
              AND mi.is_active = TRUE
            ORDER BY dh.name, mi.name, n.name
        '''
        cursor.execute(query, (available_date,))
        results = cursor.fetchall()
        return jsonify(results), 200
    except Error as e:
        current_app.logger.error(f'GET /nutrition/menu error: {e}')
        return jsonify({'error': str(e)}), 500


@nutrition.route('/log', methods=['POST'])
def log_meal():
    cursor = get_db().cursor(dictionary=True)
    try:
        data        = request.get_json()
        user_id     = data.get('user_id')
        log_date    = data.get('log_date')
        meal_period = data.get('meal_period')
        items       = data.get('items', [])

        if not all([user_id, log_date, meal_period]):
            return jsonify({'error': 'user_id, log_date, and meal_period are required'}), 400

        cursor.execute(
            'INSERT INTO meal_logs (user_id, log_date, meal_period) VALUES (%s, %s, %s)',
            (user_id, log_date, meal_period)
        )
        new_log_id = cursor.lastrowid
        for item in items:
            cursor.execute(
                'INSERT INTO meal_log_items (log_id, item_id, servings) VALUES (%s, %s, %s)',
                (new_log_id, item['item_id'], item['servings'])
            )
        get_db().commit()
        return jsonify({'message': 'Meal logged successfully', 'log_id': new_log_id}), 201
    except Error as e:
        current_app.logger.error(f'POST /nutrition/log error: {e}')
        return jsonify({'error': str(e)}), 500


@nutrition.route('/history/<int:user_id>', methods=['GET'])
def get_weekly_history(user_id):
    start  = request.args.get('start', '2025-03-29')
    end    = request.args.get('end',   '2025-04-04')
    cursor = get_db().cursor(dictionary=True)
    try:
        query = '''
            SELECT ml.log_date, ml.meal_period,
                   n.name AS nutrient, n.unit,
                   ROUND(SUM(min_t.amount * mli.servings), 2) AS total
            FROM meal_logs ml
            JOIN meal_log_items mli        ON ml.log_id         = mli.log_id
            JOIN menu_item_nutrients min_t ON mli.item_id       = min_t.item_id
            JOIN nutrients n               ON min_t.nutrient_id = n.nutrient_id
            WHERE ml.user_id  = %s
              AND ml.log_date BETWEEN %s AND %s
            GROUP BY ml.log_date, ml.meal_period, n.name, n.unit
            ORDER BY ml.log_date, ml.meal_period
        '''
        cursor.execute(query, (user_id, start, end))
        results = cursor.fetchall()
        return jsonify(results), 200
    except Error as e:
        current_app.logger.error(f'GET /nutrition/history/{user_id} error: {e}')
        return jsonify({'error': str(e)}), 500


@nutrition.route('/goals/<int:user_id>', methods=['GET'])
def get_goal_status(user_id):
    log_date = request.args.get('date', '2025-04-04')
    cursor   = get_db().cursor(dictionary=True)
    try:
        query = '''
            SELECT n.name AS nutrient, n.unit,
                   ROUND(SUM(min_t.amount * mli.servings), 2) AS daily_total,
                   ng.min_value AS goal_min, ng.max_value AS goal_max,
                   CASE
                     WHEN SUM(min_t.amount * mli.servings) < ng.min_value THEN 'BELOW'
                     WHEN ng.max_value IS NOT NULL
                          AND SUM(min_t.amount * mli.servings) > ng.max_value THEN 'ABOVE'
                     ELSE 'ON TRACK'
                   END AS status
            FROM meal_logs ml
            JOIN meal_log_items mli        ON ml.log_id         = mli.log_id
            JOIN menu_item_nutrients min_t ON mli.item_id       = min_t.item_id
            JOIN nutrients n               ON min_t.nutrient_id = n.nutrient_id
            JOIN nutrition_goals ng        ON ng.user_id        = ml.user_id
              AND ng.nutrient_id = n.nutrient_id
              AND ml.log_date BETWEEN ng.effective_from
                  AND COALESCE(ng.effective_to, '9999-12-31')
            WHERE ml.user_id  = %s
              AND ml.log_date = %s
            GROUP BY n.nutrient_id, n.name, n.unit, ng.min_value, ng.max_value
        '''
        cursor.execute(query, (user_id, log_date))
        results = cursor.fetchall()
        return jsonify(results), 200
    except Error as e:
        current_app.logger.error(f'GET /nutrition/goals/{user_id} error: {e}')
        return jsonify({'error': str(e)}), 500


@nutrition.route('/alerts/<int:user_id>', methods=['GET'])
def get_alerts(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = '''
            SELECT alert_id, alert_type, message, triggered_at, is_read
            FROM alerts
            WHERE user_id = %s
              AND is_read = FALSE
            ORDER BY triggered_at DESC
        '''
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()
        return jsonify(results), 200
    except Error as e:
        current_app.logger.error(f'GET /nutrition/alerts/{user_id} error: {e}')
        return jsonify({'error': str(e)}), 500


@nutrition.route('/log/<int:log_id>', methods=['PUT'])
def update_meal_log(log_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data        = request.get_json()
        meal_period = data.get('meal_period')
        log_date    = data.get('log_date')

        if not meal_period and not log_date:
            return jsonify({'error': 'Provide at least meal_period or log_date to update'}), 400

        if meal_period and log_date:
            cursor.execute(
                'UPDATE meal_logs SET meal_period=%s, log_date=%s WHERE log_id=%s',
                (meal_period, log_date, log_id)
            )
        elif meal_period:
            cursor.execute(
                'UPDATE meal_logs SET meal_period=%s WHERE log_id=%s',
                (meal_period, log_id)
            )
        else:
            cursor.execute(
                'UPDATE meal_logs SET log_date=%s WHERE log_id=%s',
                (log_date, log_id)
            )
        get_db().commit()
        return jsonify({'message': f'Meal log {log_id} updated'}), 200
    except Error as e:
        current_app.logger.error(f'PUT /nutrition/log/{log_id} error: {e}')
        return jsonify({'error': str(e)}), 500


@nutrition.route('/goal/<int:goal_id>', methods=['PUT'])
def update_nutrition_goal(goal_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data      = request.get_json()
        min_value = data.get('min_value')
        max_value = data.get('max_value')
        cursor.execute(
            'UPDATE nutrition_goals SET min_value=%s, max_value=%s WHERE goal_id=%s',
            (min_value, max_value, goal_id)
        )
        get_db().commit()
        return jsonify({'message': f'Goal {goal_id} updated'}), 200
    except Error as e:
        current_app.logger.error(f'PUT /nutrition/goal/{goal_id} error: {e}')
        return jsonify({'error': str(e)}), 500


@nutrition.route('/log/<int:log_id>', methods=['DELETE'])
def delete_meal_log(log_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('DELETE FROM meal_logs WHERE log_id = %s', (log_id,))
        get_db().commit()
        return jsonify({'message': f'Meal log {log_id} deleted'}), 200
    except Error as e:
        current_app.logger.error(f'DELETE /nutrition/log/{log_id} error: {e}')
        return jsonify({'error': str(e)}), 500
