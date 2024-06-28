INSERT INTO user_invite_codes_history (user, invite_code, created_at)
SELECT :user, :code, :created_at
WHERE NOT EXISTS (
    SELECT 1
    FROM user_invite_codes_history
    WHERE user = :user AND invite_code = :code
);