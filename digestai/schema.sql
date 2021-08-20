DROP TABLE IF EXISTS upload;

CREATE TABLE upload (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME,
    filepath TEXT NOT NULL,
    filename TEXT NOT NULL,
    upload_type TEXT,
    processed BOOLEAN DEFAULT FALSE
);

CREATE TABLE imageupload (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME,
    filepath TEXT NOT NULL,
    filename TEXT NOT NULL,
    upload_type TEXT,
    processed BOOLEAN DEFAULT FALSE
);