"""
Admin Blueprint — Laura Smith
REST API Routes:
  4.1  PUT    /admin/users/<user_id>/role
  4.2  GET    /admin/metrics
  4.3  GET    /admin/audit-logs
  4.4  PUT    /admin/menu-updates
  4.5  GET    /admin/reports
  4.6  GET    /admin/alerts
       DELETE /admin/alerts/<alert_id>
       DELETE /admin/users/<user_id>
"""

from flask import Blueprint, request, jsonify, current_app
from backend.db_connection import get_db
from mysql.connector import Error
import json

admin_bp = Blueprint('admin', __name__)


# helper: write a row to audit_logs
def _write_audit(cursor, user_id, table_name, action, old_vals, new_vals):
    cursor.execute(
        """
        INSERT INTO audit_logs (user_id, table_name, action, old_values, new_values)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (user_id, table_name, action,
         json.dumps(old_vals) if old_vals else None,
         json.dumps(new_vals) if new_vals else None),
    )


# ---------- 4.1  PUT /admin/users/<user_id>/role ----------
@admin_bp.route('/users/<int:user_id>/role', methods=['PUT'])
def update_user_role(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        if not data or 'role_id' not in data:
            return jsonify({'error': "Missing 'role_id' in request body"}), 400

        new_role_id = data['role_id']

        # verify user exists
        cursor.execute('SELECT user_id, role_id FROM users WHERE user_id = %s', (user_id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': f'User {user_id} not found'}), 404

        old_role_id = user['role_id']

        # verify target role exists
        cursor.execute('SELECT role_id, role_name FROM roles WHERE role_id = %s', (new_role_id,))
        role = cursor.fetchone()
        if not role:
            return jsonify({'error': f'Role {new_role_id} not found'}), 422

        cursor.execute('UPDATE users SET role_id = %s WHERE user_id = %s',
                       (new_role_id, user_id))

        _write_audit(cursor, user_id, 'users', 'UPDATE',
                     {'role_id': old_role_id},
                     {'role_id': new_role_id})

        get_db().commit()
        return jsonify({
            'message':      f'User {user_id} role updated',
            'user_id':      user_id,
            'old_role_id':  old_role_id,
            'new_role_id':  new_role_id,
            'new_role_name': role['role_name'],
        }), 200

    except Error as e:
        current_app.logger.error(f'update_user_role error: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# ---------- 4.2  GET /admin/metrics ----------
@admin_bp.route('/metrics', methods=['GET'])
def get_system_metrics():
    cursor = get_db().cursor(dictionary=True)
    try:
        since = request.args.get('since')
        query = 'SELECT metric_id, metric_type, value, unit, recorded_at FROM system_metrics'
        params = []

        if since:
            query += ' WHERE recorded_at >= %s'
            params.append(since)

        query += ' ORDER BY recorded_at DESC LIMIT 200'
        cursor.execute(query, params)
        rows = cursor.fetchall()

        for r in rows:
            r['value'] = float(r['value'])
            r['recorded_at'] = str(r['recorded_at'])

        return jsonify({'count': len(rows), 'metrics': rows}), 200

    except Error as e:
        current_app.logger.error(f'get_system_metrics error: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# ---------- 4.3  GET /admin/audit-logs ----------
@admin_bp.route('/audit-logs', methods=['GET'])
def get_audit_logs():
    cursor = get_db().cursor(dictionary=True)
    try:
        action = request.args.get('action')      # INSERT, UPDATE, or DELETE
        limit  = request.args.get('limit', 50, type=int)

        query  = ('SELECT audit_id, user_id, table_name, action, '
                  'old_values, new_values, performed_at FROM audit_logs')
        params = []

        if action:
            query += ' WHERE action = %s'
            params.append(action)

        query += ' ORDER BY performed_at DESC LIMIT %s'
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        for r in rows:
            r['performed_at'] = str(r['performed_at'])
            # old_values / new_values may already be parsed by mysql.connector
            if isinstance(r['old_values'], str):
                r['old_values'] = json.loads(r['old_values'])
            if isinstance(r['new_values'], str):
                r['new_values'] = json.loads(r['new_values'])

        return jsonify({'count': len(rows), 'logs': rows}), 200

    except Error as e:
        current_app.logger.error(f'get_audit_logs error: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# ---------- 4.4  PUT /admin/menu-updates ----------
@admin_bp.route('/menu-updates', methods=['PUT'])
def push_menu_updates():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body required'}), 400

        required = {'hall_id', 'items', 'effective_date'}
        missing  = required - data.keys()
        if missing:
            return jsonify({'error': f'Missing fields: {missing}'}), 400

        hall_id        = data['hall_id']
        items          = data['items']
        effective_date = data['effective_date']

        updated = 0
        for item in items:
            cursor.execute(
                '''UPDATE menu_items
                   SET name = %s, available_date = %s
                   WHERE item_id = %s AND hall_id = %s''',
                (item.get('name'), effective_date, item['item_id'], hall_id))
            updated += cursor.rowcount

        _write_audit(cursor, None, 'menu_items', 'UPDATE', None,
                     {'hall_id': hall_id, 'items_updated': updated,
                      'effective_date': effective_date})

        get_db().commit()
        return jsonify({
            'message':        'Menu update applied',
            'hall_id':        hall_id,
            'items_updated':  updated,
            'effective_date': effective_date,
        }), 200

    except Error as e:
        current_app.logger.error(f'push_menu_updates error: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# ---------- 4.5  GET /admin/reports ----------
@admin_bp.route('/reports', methods=['GET'])
def get_reports():
    cursor = get_db().cursor(dictionary=True)
    try:
        report_type = request.args.get('type')
        limit       = request.args.get('limit', 20, type=int)

        query  = ('SELECT report_id, created_by, title, report_type, '
                  'status, generated_at, file_path FROM reports')
        params = []

        if report_type:
            query += ' WHERE report_type = %s'
            params.append(report_type)

        query += ' ORDER BY generated_at DESC LIMIT %s'
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        for r in rows:
            if r['generated_at']:
                r['generated_at'] = str(r['generated_at'])

        return jsonify({'count': len(rows), 'reports': rows}), 200

    except Error as e:
        current_app.logger.error(f'get_reports error: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# ---------- 4.6  GET /admin/alerts ----------
@admin_bp.route('/alerts', methods=['GET'])
def get_alerts():
    cursor = get_db().cursor(dictionary=True)
    try:
        alert_type = request.args.get('alert_type')
        is_read    = request.args.get('is_read', 'false').lower() == 'true'

        query  = ('SELECT alert_id, user_id, goal_id, alert_type, '
                  'message, is_read, triggered_at FROM alerts WHERE is_read = %s')
        params = [is_read]

        if alert_type:
            query += ' AND alert_type = %s'
            params.append(alert_type)

        query += ' ORDER BY triggered_at DESC'
        cursor.execute(query, params)
        rows = cursor.fetchall()

        for r in rows:
            r['triggered_at'] = str(r['triggered_at'])
            r['is_read'] = bool(r['is_read'])

        return jsonify({'count': len(rows), 'alerts': rows}), 200

    except Error as e:
        current_app.logger.error(f'get_alerts error: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# ---------- DELETE /admin/alerts/<alert_id> ----------
@admin_bp.route('/alerts/<int:alert_id>', methods=['DELETE'])
def dismiss_alert(alert_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('SELECT alert_id FROM alerts WHERE alert_id = %s', (alert_id,))
        if not cursor.fetchone():
            return jsonify({'error': f'Alert {alert_id} not found'}), 404

        cursor.execute('UPDATE alerts SET is_read = TRUE WHERE alert_id = %s', (alert_id,))
        get_db().commit()

        return jsonify({'message': f'Alert {alert_id} dismissed', 'alert_id': alert_id}), 200

    except Error as e:
        current_app.logger.error(f'dismiss_alert error: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# ---------- DELETE /admin/users/<user_id> ----------
@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
def deactivate_user(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            'SELECT user_id, first_name, last_name FROM users WHERE user_id = %s',
            (user_id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': f'User {user_id} not found'}), 404

        cursor.execute('UPDATE users SET is_active = FALSE WHERE user_id = %s', (user_id,))

        _write_audit(cursor, user_id, 'users', 'UPDATE',
                     {'is_active': True},
                     {'is_active': False})

        get_db().commit()
        return jsonify({
            'message': f"User {user['first_name']} {user['last_name']} deactivated",
            'user_id': user_id,
        }), 200

    except Error as e:
        current_app.logger.error(f'deactivate_user error: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
