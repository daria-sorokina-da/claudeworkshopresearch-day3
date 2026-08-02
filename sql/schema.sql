-- Royal Stables — schema
--
-- Deliberately under-constrained. Several things that SHOULD be enforced by the
-- database are not, which is the point of the SQL data-quality exercise.
--
-- Do not "fix" this file until you have found the problems by querying for them.

DROP TABLE IF EXISTS race_entries;
DROP TABLE IF EXISTS vet_visits;
DROP TABLE IF EXISTS races;
DROP TABLE IF EXISTS riders;
DROP TABLE IF EXISTS horses;
DROP TABLE IF EXISTS stables;

CREATE TABLE stables (
    stable_id   INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    county      TEXT
);

CREATE TABLE horses (
    horse_id            INTEGER PRIMARY KEY,
    name                TEXT NOT NULL,
    -- No UNIQUE constraint. There should be one.
    registration_no     TEXT,
    foaled_on           DATE,
    retired_on          DATE,
    -- No REFERENCES clause. There should be one.
    stable_id           INTEGER
);

CREATE TABLE riders (
    rider_id    INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    licence_no  TEXT,
    stable_id   INTEGER
);

CREATE TABLE races (
    race_id     INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    run_on      DATE NOT NULL,
    distance_f  INTEGER,
    going       TEXT
);

CREATE TABLE race_entries (
    entry_id        INTEGER PRIMARY KEY,
    race_id         INTEGER,
    horse_id        INTEGER,
    rider_id        INTEGER,
    finish_position INTEGER,
    placed          INTEGER
);

CREATE TABLE vet_visits (
    visit_id    INTEGER PRIMARY KEY,
    horse_id    INTEGER,
    visited_on  DATE NOT NULL,
    reason      TEXT,
    lame        INTEGER DEFAULT 0
);

CREATE INDEX idx_entries_race ON race_entries(race_id);
CREATE INDEX idx_visits_horse ON vet_visits(horse_id);
