	SELECT 
	--COUNT(*)
	tPlaysFull.[home_team]
	, tPlaysFull.[away_team]
	, tPlaysFull.[posteam]
	, tPlaysFull.[defteam]
	, tPlaysFull.[yardline_100]
	, tPlaysFull.[game_date]
	, tPlaysFull.[quarter_seconds_remaining]
	, tPlaysFull.[half_seconds_remaining]
	, tPlaysFull.[game_seconds_remaining]
	, tPlaysFull.[game_half]
	, tPlaysFull.[drive]
	, tPlaysFull.[sp]
	, tPlaysFull.[qtr]
	, tPlaysFull.[down]
	, tPlaysFull.[ydstogo]
	, tPlaysFull.[ydsnet]
	, tPlaysFull.[play_type]
	, tPlaysFull.[yards_gained]
	, tPlaysFull.[shotgun]
	, tPlaysFull.[no_huddle]
	, tPlaysFull.[qb_kneel]
	, tPlaysFull.[qb_spike]
	, tPlaysFull.[qb_scramble]
	, tPlaysFull.[pass_location]
	, tPlaysFull.[air_yards]
	, tPlaysFull.[yards_after_catch]
	, tPlaysFull.[run_location]
	, tPlaysFull.[run_gap]
	, tPlaysFull.[home_timeouts_remaining]
	, tPlaysFull.[away_timeouts_remaining]
	, tPlaysFull.[posteam_timeouts_remaining]
	, tPlaysFull.[defteam_timeouts_remaining]
	, tPlaysFull.[total_home_score]
	, tPlaysFull.[total_away_score]
	, tPlaysFull.[posteam_score]
	, tPlaysFull.[defteam_score]
	, tPlaysFull.[score_differential]
	, tPlaysFull.[penalty]
	, tPlaysFull.[replay_or_challenge]
	FROM [practice].[dbo].[TBL_NFLPLAYS_plays2] tPlaysFull
	INNER JOIN [practice].[dbo].[TBL_ML_RP] tPlaysQuant
	ON tPlaysFull.[play_id] = tPlaysQuant.[id]
	AND tPlaysFull.[yardline_100] = tPlaysQuant.[q1]
	AND tPlaysFull.[quarter_seconds_remaining] = tPlaysQuant.[q2]
	AND tPlaysFull.[half_seconds_remaining] = tPlaysQuant.[q3]
	AND tPlaysFull.[game_seconds_remaining] = tPlaysQuant.[q4]
	AND tPlaysFull.[drive] = tPlaysQuant.[q5]
	AND tPlaysFull.[ydstogo] =tPlaysQuant.[q6]
	AND tPlaysFull.[posteam_timeouts_remaining] =tPlaysQuant.[q7]
	AND tPlaysFull.[defteam_timeouts_remaining] =tPlaysQuant.[q8]
	AND tPlaysFull.[posteam_score] = tPlaysQuant.[q9]
	AND tPlaysFull.[defteam_score] = tPlaysQuant.[q10]
	AND tPlaysFull.[score_differential] = tPlaysQuant.[q11]
	AND tPlaysFull.[play_type] = CASE WHEN tPlaysQuant.[type] = 1 THEN 'pass' ELSE 'run' END
	AND CASE WHEN tPlaysFull.[down] = 1 THEN 1 ELSE 0 END = tPlaysQuant.[b3_1]
	AND CASE WHEN tPlaysFull.[down] = 2 THEN 1 ELSE 0 END = tPlaysQuant.[b3_2]
	AND CASE WHEN tPlaysFull.[down] = 3 THEN 1 ELSE 0 END = tPlaysQuant.[b3_3]
	AND CASE WHEN tPlaysFull.[down] = 4 THEN 1 ELSE 0 END = tPlaysQuant.[b3_4]