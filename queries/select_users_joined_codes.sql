SELECT
    u1.telegram_id,
    u1.display_name,
    u1.created_at,
    invite_codes.code AS active_invite_code,
    u2.display_name AS active_code_created_by_display_name
FROM users u1
LEFT JOIN invite_codes ON u1.active_invite_code = invite_codes.code
LEFT JOIN users u2 ON invite_codes.created_by = u2.telegram_id;
