BEGIN TRANSACTION;

INSERT INTO invite_codes (code, created_by, created_at)
VALUES (:code, :created_by, :telegram_id)
ON CONFLICT(code) DO NOTHING;

UPDATE users
SET active_invite_code = :code
WHERE telegram_id = :telegram_id;

