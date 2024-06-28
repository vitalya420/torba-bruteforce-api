PRAGMA foreign_keys = ON;

CREATE TABLE "invite_codes" (
	"code"	TEXT UNIQUE,
	"created_by"	INTEGER,
	"created_at"	INTEGER,
	PRIMARY KEY("code"),
	FOREIGN KEY("created_by") REFERENCES "users"
);

CREATE TABLE "qr_codes" (
	"id"	INTEGER,
	"text"	TEXT,
	"invite_code"	TEXT,
	"user"	INTEGER,
	"used"	INTEGER DEFAULT 0,
	"created_at"	INTEGER,
	"used_at"	INTEGER,
	"extra_json"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("invite_code") REFERENCES "invite_codes"("code") ON DELETE SET NULL,
	FOREIGN KEY("user") REFERENCES "users"("telegram_id") ON DELETE SET NULL
);

CREATE TABLE "user_invite_codes_history" (
	"id"	INTEGER,
	"user"	INTEGER,
	"invite_code"	INTEGER,
	"created_at"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user") REFERENCES "users"("telegram_id"),
	FOREIGN KEY("invite_code") REFERENCES "invite_codes"("code")
);

CREATE TABLE "users" (
	"telegram_id"	INTEGER,
	"active_invite_code"	INTEGER,
	"display_name"	TEXT,
	"created_at"	INTEGER,
	PRIMARY KEY("telegram_id")
);

CREATE UNIQUE INDEX idx_invite_code ON invite_codes (code);
