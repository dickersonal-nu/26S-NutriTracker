"""
Laura Smith — Admin Blueprint
REST API Routes:
  4.1  PUT  /admin/users/<user_id>/role
  4.2  GET  /admin/metrics
  4.3  GET  /admin/audit-logs
  4.4  PUT  /admin/menu-updates
  4.5  GET  /admin/reports
  4.6  GET  /admin/alerts
       DELETE /admin/alerts/<alert_id>
       DELETE /admin/users/<user_id>
"""

from flask import Blueprint, request, jsonify
from datetime import datetime

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

from models import db, User, AuditLog, Alert, Report, SystemMetric   # your actual models


# PUT /admin/users/<user_id>/role
@admin_bp.route("/users/<int:user_id>/role", methods=["PUT"])
def update_user_role(user_id):
    data = request.get_json()
    if not data or "role" not in data:
        return jsonify({"error": "Missing 'role' in request body"}), 400

    valid_roles = {"student", "staff", "admin", "nutrition_manager", "guest"}
    new_role = data["role"]
    if new_role not in valid_roles:
        return jsonify({"error": f"Invalid role. Must be one of: {valid_roles}"}), 422

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": f"User {user_id} not found"}), 404

    old_role = user.role
    user.role = new_role
    db.session.commit()

    # Write to audit log
    log = AuditLog(
        action      = "update_role",
        target_type = "user",
        target_id   = user_id,
        detail      = f"Role changed from '{old_role}' to '{new_role}'",
        timestamp   = datetime.utcnow(),
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({
        "message":  f"User {user_id} role updated to '{new_role}'",
        "user_id":  user_id,
        "old_role": old_role,
        "new_role": new_role,
    }), 200


# GET /admin/metrics
@admin_bp.route("/metrics", methods=["GET"])
def get_system_metrics():
    since = request.args.get("since")
    query = SystemMetric.query
    if since:
        try:
            since_dt = datetime.strptime(since, "%Y-%m-%d")
            query = query.filter(SystemMetric.recorded_at >= since_dt)
        except ValueError:
            return jsonify({"error": "Invalid 'since' format. Use YYYY-MM-DD"}), 400

    metrics = query.order_by(SystemMetric.recorded_at.desc()).all()
    return jsonify({
        "count":   len(metrics),
        "metrics": [m.to_dict() for m in metrics],
    }), 200



# GET /admin/audit-logs
@admin_bp.route("/audit-logs", methods=["GET"])
def get_audit_logs():
    action = request.args.get("action")
    limit  = request.args.get("limit", 50, type=int)

    query = AuditLog.query
    if action:
        query = query.filter(AuditLog.action == action)

    logs = query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
    return jsonify({
        "count": len(logs),
        "logs":  [l.to_dict() for l in logs],
    }), 200


# PUT /admin/menu-updates

@admin_bp.route("/menu-updates", methods=["PUT"])
def push_menu_updates():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    required = {"dining_hall_id", "items", "effective_date"}
    missing  = required - data.keys()
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    # TODO: update menu items in DB for given dining_hall_id

    log = AuditLog(
        action      = "push_menu_update",
        target_type = "dining_hall",
        target_id   = data["dining_hall_id"],
        detail      = f"Menu updated for {data['effective_date']} — {len(data['items'])} items",
        timestamp   = datetime.utcnow(),
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({
        "message":        "Menu update applied",
        "dining_hall_id": data["dining_hall_id"],
        "items_updated":  len(data["items"]),
        "effective_date": data["effective_date"],
    }), 200



#GET /admin/reports
@admin_bp.route("/reports", methods=["GET"])
def get_reports():
    report_type = request.args.get("type")
    limit       = request.args.get("limit", 20, type=int)

    query = Report.query
    if report_type:
        query = query.filter(Report.report_type == report_type)

    reports = query.order_by(Report.created_at.desc()).limit(limit).all()
    return jsonify({
        "count":   len(reports),
        "reports": [r.to_dict() for r in reports],
    }), 200


#GET /admin/alerts
@admin_bp.route("/alerts", methods=["GET"])
def get_alerts():
    severity = request.args.get("severity")
    resolved = request.args.get("resolved", "false").lower() == "true"

    query = Alert.query.filter(Alert.resolved == resolved)
    if severity:
        query = query.filter(Alert.severity == severity)

    alerts = query.order_by(Alert.created_at.desc()).all()
    return jsonify({
        "count":  len(alerts),
        "alerts": [a.to_dict() for a in alerts],
    }), 200


# DELETE /admin/alerts/<alert_id> 
@admin_bp.route("/alerts/<int:alert_id>", methods=["DELETE"])
def dismiss_alert(alert_id):
    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({"error": f"Alert {alert_id} not found"}), 404

    alert.resolved    = True
    alert.resolved_at = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "message":  f"Alert {alert_id} dismissed",
        "alert_id": alert_id,
    }), 200


# DELETE /admin/users/<user_id> 
@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
def deactivate_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": f"User {user_id} not found"}), 404

    user.is_active    = False
    user.deactivated_at = datetime.utcnow()
    db.session.commit()

    log = AuditLog(
        action      = "deactivate_user",
        target_type = "user",
        target_id   = user_id,
        detail      = f"User '{user.username}' deactivated",
        timestamp   = datetime.utcnow(),
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({
        "message": f"User {user_id} deactivated",
        "user_id": user_id,
    }), 200
