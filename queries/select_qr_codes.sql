SELECT *
FROM qr_codes
WHERE qr_codes.user = :telegram_id
  AND used = FALSE
  AND invite_code = (
      SELECT active_invite_code
      FROM users
      WHERE telegram_id = :telegram_id
  );
