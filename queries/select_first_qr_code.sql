SELECT
    qr_codes.*
FROM
    users
JOIN
    qr_codes
ON
    users.active_invite_code = qr_codes.invite_code
WHERE
    users.telegram_id = :telegram_id
    AND qr_codes.used = 0
ORDER BY
    qr_codes.created_at
LIMIT 1;