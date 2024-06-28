SELECT
    u.telegram_id,
    u.active_invite_code,
    COALESCE(qr_count.count, 0) AS count
FROM
    users u
LEFT JOIN (
    SELECT
        user,
        invite_code,
        COUNT(*) as count
    FROM
        qr_codes
    WHERE
        used = false
    GROUP BY
        user, invite_code
) qr_count ON u.telegram_id = qr_count.user AND u.active_invite_code = qr_count.invite_code
WHERE
    u.active_invite_code IS NOT NULL;