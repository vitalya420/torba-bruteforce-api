INSERT INTO qr_codes (text, invite_code, user, created_at, extra_json)
VALUES (:text, :code, :telegram_id, :created_at, :extra_json);