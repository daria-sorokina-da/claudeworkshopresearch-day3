-- Royal Stables — seed data
--
-- Contains DELIBERATE integrity violations. Five classes of problem are planted.
-- They are listed in EXERCISE.md, but do not read that list before you have gone
-- looking — finding them is the exercise.
--
-- Everything here is invented. There is no real data in this repository.

INSERT INTO stables (stable_id, name, county) VALUES
    (1, 'Northgate',   'Norfolk'),
    (2, 'Willowmere',  'Suffolk'),
    (3, 'Ashcombe',    'Norfolk'),
    (4, 'Fairwater',   'Cambridgeshire');

INSERT INTO horses (horse_id, name, registration_no, foaled_on, retired_on, stable_id) VALUES
    (1,  'Copperfield',   'RS-1001', '2018-04-20', NULL,         1),
    (2,  'Bramble',       'RS-1002', '2019-03-11', NULL,         1),
    (3,  'Silvermane',    'RS-1003', '2017-05-02', '2025-09-30', 2),
    (4,  'Dobbin',        'RS-1004', '2020-06-15', NULL,         2),
    (5,  'Marigold',      'RS-1005', '2019-08-08', NULL,         3),
    (6,  'Thistledown',   'RS-1006', '2018-02-28', NULL,         3),
    (7,  'Pennywhistle',  'RS-1007', '2021-04-01', NULL,         4),
    (8,  'Greyling',      'RS-1008', '2016-07-19', '2024-11-15', 4),
    (9,  'Hazelnut',      'RS-1009', '2020-09-23', NULL,         1),
    (10, 'Quickthorn',    'RS-1010', '2019-01-30', NULL,         2),
    -- Duplicate registration number: RS-1003 already belongs to Silvermane.
    (11, 'Mistletoe',     'RS-1003', '2021-02-14', NULL,         3),
    -- Retired before it was born.
    (12, 'Barleycorn',    'RS-1012', '2022-05-01', '2021-08-14', 1),
    -- stable_id 99 does not exist.
    (13, 'Nutmeg',        'RS-1013', '2020-11-11', NULL,         99),
    -- Second duplicate registration, different pair.
    (14, 'Sorrel',        'RS-1007', '2021-06-30', NULL,         2),
    -- No registration number at all.
    (15, 'Willowherb',    NULL,      '2022-03-19', NULL,         3);

INSERT INTO riders (rider_id, name, licence_no, stable_id) VALUES
    (1, 'A. Fenwick',  'LIC-201', 1),
    (2, 'B. Marlowe',  'LIC-202', 2),
    (3, 'C. Ainsley',  'LIC-203', 3),
    (4, 'D. Rooke',    'LIC-204', 4),
    (5, 'E. Sparrow',  'LIC-205', 1);

INSERT INTO races (race_id, name, run_on, distance_f, going) VALUES
    (1, 'Northgate Spring Plate',   '2026-03-02', 8,  'good'),
    (2, 'Willowmere Handicap',      '2026-03-09', 12, 'soft'),
    (3, 'Ashcombe Novice Stakes',   '2026-03-16', 6,  'firm'),
    (4, 'Fairwater Cup',            '2026-03-23', 10, 'good'),
    (5, 'Midsummer Dash',           '2026-06-15', 5,  'firm'),
    (6, 'Harvest Long Distance',    '2026-09-07', 16, 'heavy'),
    (7, 'Michaelmas Trial',         '2026-09-28', 10, 'soft'),
    -- Two Sunday fixtures. Nothing wrong with these rows; they matter because a
    -- Sunday is the last day of an ISO week, and something in the reporting code
    -- has an opinion about the last day of a range.
    (8, 'Sunday Selling Plate',     '2026-03-08', 7,  'good'),
    (9, 'Easter Sunday Sprint',     '2026-04-05', 5,  'firm');

INSERT INTO race_entries (entry_id, race_id, horse_id, rider_id, finish_position, placed) VALUES
    (1,  1, 1,  1, 1, 1),
    (2,  1, 2,  2, 4, 0),
    (3,  1, 5,  3, 2, 1),
    (4,  1, 9,  5, 7, 0),
    (5,  2, 3,  2, 1, 1),
    (6,  2, 4,  2, 3, 1),
    (7,  2, 6,  3, 5, 0),
    (8,  2, 10, 1, 2, 1),
    (9,  3, 7,  4, 1, 1),
    (10, 3, 5,  3, 6, 0),
    (11, 3, 9,  5, 3, 1),
    (12, 4, 1,  1, 2, 1),
    (13, 4, 4,  2, 1, 1),
    (14, 4, 6,  3, 8, 0),
    (15, 4, 10, 1, 4, 0),
    (16, 5, 7,  4, 2, 1),
    (17, 5, 2,  1, 1, 1),
    (18, 5, 9,  5, 5, 0),
    (19, 6, 3,  2, 3, 1),
    (20, 6, 6,  3, 1, 1),
    (21, 7, 1,  1, 4, 0),
    (22, 7, 4,  2, 2, 1),
    (23, 7, 10, 1, 1, 1),
    -- Orphan: horse_id 777 does not exist.
    (24, 7, 777, 3, 6, 0),
    -- Orphan: race_id 999 does not exist.
    (25, 999, 5, 3, 2, 1),
    -- Orphan rider.
    (26, 6, 2, 888, 5, 0),
    -- Silvermane (id 3) retired 2025-09-30 but is entered in a 2026 race.
    (27, 5, 3, 2, 4, 0),
    -- placed flag contradicts finish_position: 1st but not placed.
    (28, 3, 10, 1, 1, 0),
    -- placed flag contradicts finish_position: 9th but placed.
    (29, 4, 9, 5, 9, 1),
    -- Entries for the two Sunday fixtures.
    (30, 8, 2,  1, 1, 1),
    (31, 8, 5,  3, 2, 1),
    (32, 8, 9,  5, 4, 0),
    (33, 9, 7,  4, 1, 1),
    (34, 9, 2,  1, 3, 1);

INSERT INTO vet_visits (visit_id, horse_id, visited_on, reason, lame) VALUES
    (1,  1,  '2026-02-10', 'routine dental',        0),
    (2,  2,  '2026-02-14', 'lameness near fore',    1),
    (3,  4,  '2026-03-01', 'routine vaccination',   0),
    (4,  5,  '2026-03-05', 'lameness off hind',     1),
    (5,  6,  '2026-01-22', 'routine dental',        0),
    (6,  7,  '2026-06-01', 'lameness near hind',    1),
    (7,  9,  '2026-02-28', 'routine vaccination',   0),
    (8,  10, '2026-03-12', 'colic - resolved',      0),
    -- Visit predates the horse's foaling date (Pennywhistle foaled 2021-04-01).
    (9,  7,  '2019-05-14', 'routine dental',        0),
    -- Orphan horse.
    (10, 555, '2026-03-18', 'routine dental',       0),
    -- Visit after retirement (Greyling retired 2024-11-15).
    (11, 8,  '2026-01-09', 'routine dental',        0);
