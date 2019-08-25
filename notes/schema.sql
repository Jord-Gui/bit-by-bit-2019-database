DROP TABLE IF EXISTS note;
CREATE TABLE note
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    filename    TEXT UNIQUE NOT NULL,
    content     TEXT
);

DROP TABLE IF EXISTS activity;
CREATE TABLE activity
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    words       INTEGER NOT NULL,
    int_time    INTEGER NOT NULL
);