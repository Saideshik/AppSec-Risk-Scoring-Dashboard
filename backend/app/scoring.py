from datetime import datetime, timezone

SEV_WEIGHT = {
    "critical": 10,
    "high": 7,
    "medium": 4,
    "low": 1,
    "info": 0,
}

SENS_WEIGHT = {
    "low": 0,
    "medium": 6,
    "high": 12,
}

def clamp(n: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, n))

def risk_label(score: int) -> str:
    if score >= 85:
        return "Critical"
    if score >= 70:
        return "High"
    if score >= 40:
        return "Medium"
    return "Low"

def aging_points(detected_at: datetime) -> float:
    now = datetime.now(timezone.utc)
    if detected_at.tzinfo is None:
        detected_at = detected_at.replace(tzinfo=timezone.utc)
    days = (now - detected_at).days

    if days <= 7:
        return 0
    if days <= 30:
        return 6 * (days - 7) / (30 - 7)
    if days <= 90:
        return 6 + 6 * (days - 30) / (90 - 30)
    return 18

def compute_app_risk(app, open_findings: list) -> dict:
    base = 0.0
    open_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}

    for f in open_findings:
        sev = (f.severity or "info").lower()
        sev_w = SEV_WEIGHT.get(sev, 0)
        if sev in open_counts:
            open_counts[sev] += 1

        cvss = f.cvss if f.cvss is not None else (
            9.8 if sev == "critical" else
            7.5 if sev == "high" else
            5.0 if sev == "medium" else
            2.0
        )
        cvss_component = clamp(cvss, 0, 10)

        exploit = 1.0 if f.exploit_available else 0.0
        exposure = 1.0 if (f.internet_exposed or app.internet_exposed) else 0.0

        base += (sev_w * 2.2) + (cvss_component * 1.5) + (exploit * 8.0) + (exposure * 6.0) + aging_points(f.detected_at)

    sens = SENS_WEIGHT.get((app.data_sensitivity or "low").lower(), 0)
    critical_count_bonus = clamp(open_counts["critical"] * 6.0, 0, 24)

    raw = base + sens + critical_count_bonus
    score = int(round(clamp((raw / 180.0) * 100.0, 0, 100)))

    return {
        "score": score,
        "label": risk_label(score),
        "open_counts": open_counts,
    }

def compute_mttr_days(fixed_findings: list):
    diffs = []
    for f in fixed_findings:
        if f.fixed_at and f.detected_at:
            diffs.append((f.fixed_at - f.detected_at).total_seconds() / 86400.0)
    if not diffs:
        return None
    return sum(diffs) / len(diffs)
