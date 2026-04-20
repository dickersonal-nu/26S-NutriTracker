
"""Admin Blueprint
REST API Routes:
  4.1  PUT    /admin/users/<user_id>/role
  4.2  GET    /admin/metrics
  4.3  GET    /admin/audit-logs
  4.4  PUT    /admin/menu-updates
  4.5  GET    /admin/reports
  4.6  GET    /admin/alerts
         DELETE /admin/alerts/<alert_id>
         DELETE /admin/users/<user_id>"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from backend.db_connection import get_db
from mysql.connector import Error

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# write a row to the AuditLog table
def _write_audit_log(cursor, action, target_type, target_id, detail):
    cursor.execute(
        """
        INSERT INTO AuditLog (action, target_type, target_id, detail, timestamp)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (action, target_type, target_id, detail, datetime.utcnow()),
    )


# 4.1  PUT /admin/users/<user_id>/role
@admin_bp.route("/users/<int:user_id>/role", methods=["PUT"])
def update_user_role(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        if not data or "role" not in data:
            return jsonify({"error": "Missing 'role' in request body"}), 400

        valid_roles = {"student", "staff", "admin", "nutrition_manager", "guest"}
        new_role = data["role"]
        if new_role not in valid_roles:
            return jsonify({"error": f"Invalid role. Must be one of: {valid_roles}"}), 422

        cursor.execute("SELECT user_id, role FROM Users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"error": f"User {user_id} not found"}), 404

        old_role = user["role"]

        cursor.execute(
            "UPDATE Users SET role = %s WHERE user_id = %s",
            (new_role, user_id),
        )

        _write_audit_log(
            cursor,
            action="update_role",
            target_type="user",
            target_id=user_id,
            detail=f"Role changed from '{old_role}' to '{new_role}'",
        )

        get_db().commit()
        current_app.logger.info(f"User {user_id} role updated: {old_role} -> {new_role}")

        return jsonify({
            "message":  f"User {user_id} role updated to '{new_role}'",
            "user_id":  user_id,
            "old_role": old_role,
            "new_role": new_role,
        }), 200

    except Error as e:
        current_app.logger.error(f"DB error in update_user_role: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# 4.2  GET /admin/metrics
@admin_bp.route("/metrics", methods=["GET"])
def get_system_metrics():
    cursor = get_db().cursor(dictionary=True)
    try:
        since = request.args.get("since")

        if since:
            try:
                datetime.strptime(since, "%Y-%m-%d")   # validate format
            except ValueError:
                return jsonify({"error": "Invalid 'since' format. Use YYYY-MM-DD"}), 400

            cursor.execute(
                "SELECT * FROM SystemMetrics WHERE recorded_at >= %s ORDER BY recorded_at DESC",
                (since,),
            )
        else:
            cursor.execute("SELECT * FROM SystemMetrics ORDER BY recorded_at DESC")

        metrics = cursor.fetchall()
        return jsonify({"count": len(metrics), "metrics": metrics}), 200

    except Error as e:
        current_app.logger.error(f"DB error in get_system_metrics: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# 4.3  GET /admin/audit-logs
@admin_bp.route("/audit-logs", methods=["GET"])
def get_audit_logs():
    cursor = get_db().cursor(dictionary=True)
    try:
        action = request.args.get("action")
        limit  = request.args.get("limit", 50, type=int)

        if action:
            cursor.execute(
                "SELECT * FROM AuditLog WHERE action = %s ORDER BY timestamp DESC LIMIT %s",
                (action, limit),
            )
        else:
            cursor.execute(
                "SELECT * FROM AuditLog ORDER BY timestamp DESC LIMIT %s",
                (limit,),
            )

        logs = cursor.fetchall()
        return jsonify({"count": len(logs), "logs": logs}), 200

    except Error as e:
        current_app.logger.error(f"DB error in get_audit_logs: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# 4.4  PUT /admin/menu-updates
@admin_bp.route("/menu-updates", methods=["PUT"])
def push_menu_updates():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body required"}), 400

        required = {"dining_hall_id", "items", "effective_date"}
        missing  = required - data.keys()
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400

        dining_hall_id = data["dining_hall_id"]
        items          = data["items"]
        effective_date = data["effective_date"]

        for item in items:
            cursor.execute(
                """
                UPDATE MenuItems
                SET item_name   = %s,
                    calories    = %s,
                    effective_date = %s
                WHERE dining_hall_id = %s AND item_id = %s
                """,
                (
                    item.get("item_name"),
                    item.get("calories"),
                    effective_date,
                    dining_hall_id,
                    item.get("item_id"),
                ),
            )

        _write_audit_log(
            cursor,
            action="push_menu_update",
            target_type="dining_hall",
            target_id=dining_hall_id,
            detail=f"Menu updated for {effective_date} — {len(items)} items",
        )

        get_db().commit()
        return jsonify({
            "message":        "Menu update applied",
            "dining_hall_id": dining_hall_id,
            "items_updated":  len(items),
            "effective_date": effective_date,
        }), 200

    except Error as e:
        current_app.logger.error(f"DB error in push_menu_updates: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# 4.5  GET /admin/reports
@admin_bp.route("/reports", methods=["GET"])
def get_reports():
    cursor = get_db().cursor(dictionary=True)
    try:
        report_type = request.args.get("type")
        limit       = request.args.get("limit", 20, type=int)

        if report_type:
            cursor.execute(
                "SELECT * FROM Reports WHERE report_type = %s ORDER BY created_at DESC LIMIT %s",
                (report_type, limit),
            )
        else:
            cursor.execute(
                "SELECT * FROM Reports ORDER BY created_at DESC LIMIT %s",
                (limit,),
            )

        reports = cursor.fetchall()
        return jsonify({"count": len(reports), "reports": reports}), 200

    except Error as e:
        current_app.logger.error(f"DB error in get_reports: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# 4.6  GET /admin/alerts
@admin_bp.route("/alerts", methods=["GET"])
def get_alerts():
    cursor = get_db().cursor(dictionary=True)
    try:
        severity = request.args.get("severity")
        resolved = request.args.get("resolved", "false").lower() == "true"
        resolved_int = 1 if resolved else 0

        if severity:
            cursor.execute(
                """
                SELECT * FROM Alerts
                WHERE resolved = %s AND severity = %s
                ORDER BY created_at DESC
                """,
                (resolved_int, severity),
            )
        else:
            cursor.execute(
                "SELECT * FROM Alerts WHERE resolved = %s ORDER BY created_at DESC",
                (resolved_int,),
            )

        alerts = cursor.fetchall()
        return jsonify({"count": len(alerts), "alerts": alerts}), 200

    except Error as e:
        current_app.logger.error(f"DB error in get_alerts: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# DELETE /admin/alerts/<alert_id> (resolved alerts)
@admin_bp.route("/alerts/<int:alert_id>", methods=["DELETE"])
def dismiss_alert(alert_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT alert_id FROM Alerts WHERE alert_id = %s", (alert_id,))
        if not cursor.fetchone():
            return jsonify({"error": f"Alert {alert_id} not found"}), 404

        cursor.execute(
            "UPDATE Alerts SET resolved = 1, resolved_at = %s WHERE alert_id = %s",
            (datetime.utcnow(), alert_id),
        )
        get_db().commit()

        return jsonify({"message": f"Alert {alert_id} dismissed", "alert_id": alert_id}), 200

    except Error as e:
        current_app.logger.error(f"DB error in dismiss_alert: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# DELETE /admin/users/<user_id>  (deactivates user)
@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
def deactivate_user(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id, username FROM Users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"error": f"User {user_id} not found"}), 404

        cursor.execute(
            "UPDATE Users SET is_active = 0, deactivated_at = %s WHERE user_id = %s",
            (datetime.utcnow(), user_id),
        )

        _write_audit_log(
            cursor,
            action="deactivate_user",
            target_type="user",
            target_id=user_id,
            detail=f"User '{user['username']}' deactivated",
        )

        get_db().commit()
        current_app.logger.info(f"User {user_id} deactivated")

        return jsonify({"message": f"User {user_id} deactivated", "user_id": user_id}), 200

    except Error as e:
        current_app.logger.error(f"DB error in deactivate_user: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()