# Central place to tweak policy decisions
# For MVP, we keep it simple: 24 days annual leave, inclusive date calculation,
# weekends and holidays are counted (can be improved later).
# Add accruals/proration/blackout dates here if needed.
POLICY = {
    "annual_leave_days": 24,
    "count_weekends": True,
    "inclusive_dates": True,
}
