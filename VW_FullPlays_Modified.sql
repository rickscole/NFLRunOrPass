USE [NFL]
GO

/****** Object:  View [RP].[VW_FullPlays_Modified]    Script Date: 8/2/2020 1:04:08 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO







ALTER VIEW [RP].[VW_FullPlays_Modified] AS
WITH tMostMatches AS
(
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
	, tPlaysFull.[play_id]
	, tPlaysFull.[game_id]
	, tPlaysQuant.[PK_ID_Play]
	FROM [NFL].[RP].[TBL_Plays_Old] tPlaysFull
	INNER JOIN [NFL].[RP].[TBL_Play_Modified] tPlaysQuant
	ON tPlaysFull.[play_id] = tPlaysQuant.[id]
	AND tPlaysFull.[yardline_100] = tPlaysQuant.[q1]
	AND tPlaysFull.[quarter_seconds_remaining] = tPlaysQuant.[q2]
	AND tPlaysFull.[half_seconds_remaining] = tPlaysQuant.[q3]
	AND tPlaysFull.[game_seconds_remaining] = tPlaysQuant.[q4]
	AND tPlaysFull.[drive] = tPlaysQuant.[q5]
	AND tPlaysFull.[ydstogo] =tPlaysQuant.[q6]
	AND tPlaysFull.[posteam_score] = tPlaysQuant.[q9]
	AND tPlaysFull.[defteam_score] = tPlaysQuant.[q10]
	AND tPlaysFull.[score_differential] = tPlaysQuant.[q11]
	AND tPlaysFull.[play_type] = CASE WHEN tPlaysQuant.[type] = 1 THEN 'pass' ELSE 'run' END
),
tPKCounts AS
(
	SELECT
	[PK_ID_Play]
	, COUNT([PK_ID_Play]) AS [PK_ID_Play_COUNT]
	FROM tMostMatches
	GROUP BY [PK_ID_Play]
	--HAVING COUNT([PK_ID_Play]) = 1
),
tPKCounts_Repeats AS
(
	SELECT tMostMatches.*
	FROM tMostMatches
	INNER JOIN tPKCounts
	ON tMostMatches.[PK_ID_Play] = tPKCounts.[PK_ID_Play]
	WHERE tPKCounts.[PK_ID_Play_COUNT] > 1
),
tPKCounts_Good AS
(
	SELECT tMostMatches.*
	FROM tMostMatches
	INNER JOIN tPKCounts
	ON tMostMatches.[PK_ID_Play] = tPKCounts.[PK_ID_Play]
	WHERE tPKCounts.[PK_ID_Play_COUNT] = 1
),
tFinal AS
(
	SELECT tPKCounts_Repeats.*
	FROM tPKCounts_Repeats
	INNER JOIN tPKCounts_Good
	ON tPKCounts_Repeats.[PK_ID_Play] = tPKCounts_Good.[PK_ID_Play] - 1
	AND tPKCounts_Repeats.[away_team] = tPKCounts_Good.[away_team]
	AND tPKCounts_Repeats.[home_team] = tPKCounts_Good.[home_team]
	AND tPKCounts_Repeats.[game_date] = tPKCounts_Good.[game_date]

	UNION ALL 

	SELECT tPKCounts_Repeats.*
	FROM tPKCounts_Repeats
	INNER JOIN tPKCounts_Good
	ON tPKCounts_Repeats.[PK_ID_Play] = tPKCounts_Good.[PK_ID_Play] + 1 
	AND tPKCounts_Repeats.[away_team] = tPKCounts_Good.[away_team]
	AND tPKCounts_Repeats.[home_team] = tPKCounts_Good.[home_team]
	AND tPKCounts_Repeats.[game_date] = tPKCounts_Good.[game_date]

	UNION ALL

	SELECT * 
	FROM tPKCounts_Good
)
SELECT *
FROM tFinal

GO


