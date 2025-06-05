CALCULATING_STATS = "📊 Statistiken werden berechnet..."


def returnStatsInfoMessage(stats: dict) -> str:
    return (
        "<b>PromoBot-Statistik</b>\n\n"
        f"<b>Verkäufer: {stats.get('total_sellers')}</b>\n\n"
        f"📇 registriert: {stats.get('registered_sellers')}\n"
        f"✅ aktiv: {stats.get('active_sellers')}\n"
        f"🙅 gesperrt: {stats.get('inactive_sellers')}\n\n"
        f"<b>Promos: {stats.get('total_promos')}</b>\n\n"
        f"✅ aktiv: {stats.get('active_promos')}\n"
        f"🚫 inaktiv: {stats.get('inactive_promos')}\n"
        f"🗑 gelöscht: {stats.get('deleted_promos')}"
    )
