from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

analytics = Blueprint('analytics', __name__)


# Immanuel story 3.1: filter nutrition data by hall, date range, student type
@analytics.route('/filter', methods=['GET'])
def filter_nutrition_data():
    # read query params — hall and student_type are optional
    hall_name = request.args.get('hall')
    start_date = request.args.get('start', '2025-03-29')
    end_date = request.args.get('end', '2025-04-04')
    student_type = request.args.get('student_type')

    cursor = get_db().cursor(dictionary=True)
    try:
        # base query: total nutrient consumption per day in a date range
        query = '''
            SELECT dh.name AS dining_hall, d.student_type, d.college_year,
                   n.name AS nutrient, n.unit,
                   ROUND(AVG(min_t.amount * mli.servings), 2) AS avg_intake,
                   COUNT(DISTINCT ml.user_id) AS num_users
            FROM meal_logs ml
            JOIN meal_log_items mli ON ml.log_id = mli.log_id
            JOIN menu_items mi ON mli.item_id = mi.item_id
            JOIN dining_halls dh ON mi.hall_id = dh.hall_id
            JOIN menu_item_nutrients min_t ON mi.item_id = min_t.item_id
            JOIN nutrients n ON min_t.nutrient_id = n.nutrient_id
            JOIN users u ON ml.user_id = u.user_id
            JOIN demographics d ON u.demographic_id = d.demographic_id
            WHERE ml.log_date BETWEEN %s AND %s
        '''
        params = [start_date, end_date]

        # add on optional filters only if user passed them
        if hall_name:
            query += ' AND dh.name = %s'
            params.append(hall_name)
        if student_type:
            query += ' AND d.student_type = %s'
            params.append(student_type)

        query += '''
            GROUP BY dh.name, d.student_type, d.college_year, n.name, n.unit
            ORDER BY n.name, d.college_year
        '''

        cursor.execute(query, params)
        return jsonify(cursor.fetchall()), 200

    except Error as e:
        # logs for debugging, return 500 so frontend sees it - stole from jasmine
        current_app.logger.error(f'/analytics/filter failed: {e}')
        return jsonify({'error': str(e)}), 500
    
# Immanuel story 3.3: nutrient totals per day over a date range
@analytics.route('/trends', methods=['GET'])
def trends():
    # read query params — hall and student_type are optional
    start_date = request.args.get('start', '2025-03-29')
    end_date = request.args.get('end', '2025-04-04')
    nutrient = request.args.get('nutrient')  # None means "all nutrients"

    cursor = get_db().cursor(dictionary=True)
    try:
        # base query: average intake per nutrient and then grouped by hall + demographic
        query = '''
            SELECT ml.log_date, n.name as nutrient, n.unit,
                round(sum(min_t.amount * mli.servings), 2) as total_consumed,
                count(distinct ml.user_id) as users_tracked
            FROM meal_logs ml
            JOIN meal_log_items mli on ml.log_id = mli.log_id
            JOIN menu_items mi on mli.item_id = mi.item_id
            JOIN menu_item_nutrients min_t on mi.item_id = min_t.item_id
            JOIN nutrients n on min_t.nutrient_id = n.nutrient_id
            WHERE ml.log_date BETWEEN %s AND %s
        '''
        params = [start_date, end_date]

        # add on optional filters only if user passed them
        if nutrient:
            query += ' AND n.name = %s'
            params.append(nutrient)

        query += '''
            GROUP BY ml.log_date, n.name, n.unit
            ORDER BY ml.log_date, n.name
        '''

        cursor.execute(query, params)
        return jsonify(cursor.fetchall()), 200

    except Error as e:
        # logs for debugging, return 500 so frontend sees it - stole from jasmine
        current_app.logger.error(f'/analytics/trends failed: {e}')
        return jsonify({'error': str(e)}), 500