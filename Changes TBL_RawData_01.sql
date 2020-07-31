SELECT game_half,
COUNT(*)
FROM TBL_NFLPLAYS_plays2
GROUP BY game_half
ORDER BY COUNT(*) DESC

UPDATE TBL_NFLPLAYS_plays2
SET yardline_100 = NULL
WHERE yardline_100 = 'NA'

ALTER TABLE TBL_NFLPLAYS_plays2
ALTER COLUMN yardline_100 INT

UPDATE TBL_NFLPLAYS_plays2
SET quarter_seconds_remaining = NULL
WHERE quarter_seconds_remaining = 'NA'

ALTER TABLE TBL_NFLPLAYS_plays2
ALTER COLUMN quarter_seconds_remaining INT

UPDATE TBL_NFLPLAYS_plays2
SET half_seconds_remaining = NULL
WHERE half_seconds_remaining = 'NA'

UPDATE TBL_NFLPLAYS_plays2
SET half_seconds_remaining = '100'
WHERE half_seconds_remaining = '1.00E+03'

ALTER TABLE TBL_NFLPLAYS_plays2
ALTER COLUMN half_seconds_remaining INT

UPDATE TBL_NFLPLAYS_plays2
SET game_seconds_remaining = NULL
WHERE game_seconds_remaining = 'NA'

UPDATE TBL_NFLPLAYS_plays2
SET game_seconds_remaining = '100'
WHERE game_seconds_remaining = '1.00E+03'

UPDATE TBL_NFLPLAYS_plays2
SET game_seconds_remaining = '200'
WHERE game_seconds_remaining = '2.00E+03'

UPDATE TBL_NFLPLAYS_plays2
SET game_seconds_remaining = '300'
WHERE game_seconds_remaining = '3.00E+03'

ALTER TABLE TBL_NFLPLAYS_plays2
ALTER COLUMN game_seconds_remaining INT

ALTER TABLE TBL_NFLPLAYS_plays2
ALTER COLUMN drive INT

UPDATE TBL_NFLPLAYS_plays2
SET down = NULL
WHERE down = 'NA'

ALTER TABLE TBL_NFLPLAYS_plays2
ALTER COLUMN ydstogo INT

UPDATE TBL_NFLPLAYS_plays2
SET posteam_timeouts_remaining = NULL
WHERE posteam_timeouts_remaining = 'NA'

UPDATE TBL_NFLPLAYS_plays2
SET defteam_timeouts_remaining = NULL
WHERE defteam_timeouts_remaining = 'NA'

UPDATE TBL_NFLPLAYS_plays2
SET posteam_score = NULL
WHERE posteam_score = 'NA'

ALTER TABLE TBL_NFLPLAYS_plays2
ALTER COLUMN posteam_score INT

UPDATE TBL_NFLPLAYS_plays2
SET defteam_score = NULL
WHERE defteam_score = 'NA'

ALTER TABLE TBL_NFLPLAYS_plays2
ALTER COLUMN defteam_score INT

UPDATE TBL_NFLPLAYS_plays2
SET score_differential = NULL
WHERE score_differential = 'NA'

ALTER TABLE TBL_NFLPLAYS_plays2
ALTER COLUMN score_differential INT

UPDATE TBL_NFLPLAYS_plays2
SET wp = NULL
WHERE wp = 'NA'

ALTER TABLE TBL_NFLPLAYS_plays2
ALTER COLUMN wp FLOAT

UPDATE TBL_NFLPLAYS_plays2
SET away_wp = NULL
WHERE away_wp = 'NA'

ALTER TABLE TBL_NFLPLAYS_plays2
ALTER COLUMN away_wp FLOAT

UPDATE TBL_NFLPLAYS_plays2
SET wpa = NULL
WHERE wpa = 'NA'

ALTER TABLE TBL_NFLPLAYS_plays2
ALTER COLUMN wpa FLOAT