SELECT
t1.play_id,
t1.home_team,
t1.away_team,
t1.game_date,
[desc],
t2.play_fileName
FROM TBL_NFLPLAYS_plays2 t1
LEFT JOIN TBL_NFLPLAYS_selectedPlays t2
ON t1.play_id = t2.play_id
AND t1.home_team = t2.home_team
AND t1.away_team = t2.away_team
AND t1.game_date = t2.game_date
WHERE t2.play_fileName IS NOT NULL


--SELECT * FROM TBL_NFLPLAYS_selectedPLays

UPDATE t1
SET t1.play_fileName = t2.play_fileName
FROM TBL_NFLPLAYS_plays2 t1
LEFT JOIN TBL_NFLPLAYS_selectedPlays t2
ON t1.play_id = t2.play_id
AND t1.home_team = t2.home_team
AND t1.away_team = t2.away_team
AND t1.game_date = t2.game_date

SELECT * FROM TBL_NFLPLAYS_plays2 WHERE play_fileName IS NOT NULL



