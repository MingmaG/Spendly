"""Pure data-query helpers for the profile page. No Flask imports here."""
from datetime import datetime

from database.db import get_db


def get_recent_transactions(user_id, limit=10):
    """Return the user's most recent expenses, newest first.

    Each item: {"date": "Jun 18, 2026", "description": ..., "category": ..., "amount": float}
    Owner: subagent 1 (transaction history).
    """
    db = get_db()
    rows = db.execute(
        "SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC, id DESC LIMIT ?",
        (user_id, limit),
    ).fetchall()
    db.close()

    return [
        {
            "date": datetime.strptime(row["date"], "%Y-%m-%d").strftime("%b %d, %Y"),
            "description": row["description"] or "",
            "category": row["category"],
            "amount": float(row["amount"]),
        }
        for row in rows
    ]


def get_summary_stats(user_id):
    """Return {"total_spent": float, "transaction_count": int, "top_category": str}.

    Owner: subagent 2 (summary stats).
    """
    db = get_db()
    rows = db.execute(
        "SELECT category, amount FROM expenses WHERE user_id = ?", (user_id,)
    ).fetchall()
    db.close()

    if not rows:
        return {"total_spent": 0, "transaction_count": 0, "top_category": "—"}

    totals_by_category = {}
    total_spent = 0.0
    for row in rows:
        total_spent += row["amount"]
        totals_by_category[row["category"]] = (
            totals_by_category.get(row["category"], 0) + row["amount"]
        )

    top_category = max(totals_by_category, key=totals_by_category.get)

    return {
        "total_spent": total_spent,
        "transaction_count": len(rows),
        "top_category": top_category,
    }


def get_category_breakdown(user_id):
    """Return [{"name": str, "amount": float, "percent": int}, ...] for categories with spend.

    Owner: subagent 3 (category breakdown).
    """
    db = get_db()
    rows = db.execute(
        "SELECT category, amount FROM expenses WHERE user_id = ?", (user_id,)
    ).fetchall()
    db.close()

    if not rows:
        return []

    totals_by_category = {}
    for row in rows:
        category = row["category"]
        totals_by_category[category] = totals_by_category.get(category, 0) + row["amount"]

    total_spent = sum(totals_by_category.values())

    breakdown = []
    for category, total in totals_by_category.items():
        raw_percent = (total / total_spent) * 100 if total_spent else 0
        percent = round(raw_percent / 10) * 10
        if percent == 0 and total > 0:
            percent = 10
        breakdown.append({"name": category, "amount": float(total), "percent": percent})

    breakdown.sort(key=lambda item: item["amount"], reverse=True)
    return breakdown
