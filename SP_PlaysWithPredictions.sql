USE [NFL]
GO

/****** Object:  StoredProcedure [RP].[SP_PlaysWithPredictions]    Script Date: 8/2/2020 1:12:44 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO






-- =============================================
-- Author:		rsc
-- Create date: 2020-07-22_1835
-- Description:	insert into categorical predictions table; for use in PBI
-- =============================================
ALTER PROCEDURE [RP].[SP_PlaysWithPredictions] 
AS
BEGIN
	SET NOCOUNT ON;

	DECLARE @sqlvar_ID_ForecastIteration INT
	SET @sqlvar_ID_ForecastIteration = (SELECT MAX([PK_ID_ForecastIteration]) FROM [NFL].[RP].[TBL_ForecastIteration])

	DECLARE @sqlvar_ID_ForecastParameter_RF INT
	SET @sqlvar_ID_ForecastParameter_RF = (SELECT MAX([PK_ID_ForecastParameter_RF]) FROM [NFL].[RP].[TBL_ForecastParameters_RF])

	DECLARE @sqlvar_ID_AggregatedResults INT
	SET @sqlvar_ID_AggregatedResults = (SELECT MAX([PK_ID_AggregatedResults]) FROM [NFL].[RP].[TBL_AggregatedResults] WHERE [FK_ID_ForecastIteration] = @sqlvar_ID_ForecastIteration)

	--SELECT * 
	--FROM [NFL].[RP].[TBL_Results] 
	--WHERE [FK_ID_AggregatedResults] = @sqlvar_ID_AggregatedResults
 
	SELECT
	tPredix.[FK_ID_ForecastIteration]
	, tPredix.[Prediction]
	, tPredix.[CVType]
	, tPlay.[home_team]
	, tPlay.[away_team]
	, tPlay.[posteam]
	, tPlay.[defteam]
	, tPlay.[yardline_100]
	, tPlay.[game_date]
	, tPlay.[quarter_seconds_remaining]
	, tPlay.[half_seconds_remaining]
	, tPlay.[game_seconds_remaining]
	, tPlay.[game_half]
	, tPlay.[drive]
	, tPlay.[sp]
	, tPlay.[qtr]
	, tPlay.[down]
	, tPlay.[ydstogo]
	, tPlay.[ydsnet]
	, tPlay.[play_type]
	, tPlay.[yards_gained]
	, tPlay.[shotgun]
	, tPlay.[no_huddle]
	, tPlay.[qb_kneel]
	, tPlay.[qb_spike]
	, tPlay.[qb_scramble]
	, tPlay.[pass_location]
	, tPlay.[air_yards]
	, tPlay.[yards_after_catch]
	, tPlay.[run_location]
	, tPlay.[run_gap]
	, tPlay.[home_timeouts_remaining]
	, tPlay.[away_timeouts_remaining]
	, tPlay.[posteam_timeouts_remaining]
	, tPlay.[defteam_timeouts_remaining]
	, tPlay.[total_home_score]
	, tPlay.[total_away_score]
	, tPlay.[posteam_score]
	, tPlay.[defteam_score]
	, tPlay.[score_differential]
	, ABS(tPlay.[score_differential]) AS [score_differential_ABS]
	, tPlay.[penalty]
	, tPlay.[replay_or_challenge]
	, tPlay.[play_id]
	, tPlay.[game_id]
	, tPlay.[PK_ID_Play]
	, CASE WHEN tPredix.[Prediction] = -1 AND tPlay.[play_type] = 'run' THEN 1 ELSE 0 END AS [Run]
	, CASE WHEN tPredix.[Prediction] = -1 AND tPlay.[play_type] = 'pass' THEN 1 ELSE 0 END AS [Play Action Error]
	, CASE WHEN tPredix.[Prediction] = 1 AND tPlay.[play_type] = 'run' THEN  1 ELSE 0 END AS [Draw Error]
	, CASE WHEN tPredix.[Prediction] = 1 AND tPlay.[play_type] = 'pass' THEN 1 ELSE 0 END AS [Pass]
	, CASE WHEN tPredix.[Prediction] = -1 AND tPlay.[play_type] = 'run' THEN 'Run' 
		WHEN tPredix.[Prediction] = -1 AND tPlay.[play_type] = 'pass' THEN 'Play Action Error'
		WHEN tPredix.[Prediction] = 1 AND tPlay.[play_type] = 'run' THEN 'Draw Error'
		WHEN tPredix.[Prediction] = 1 AND tPlay.[play_type] = 'pass' THEN 'Pass' END
	AS [PredictionType]
	FROM [NFL].[RP].[TBL_Predictions_Categorical] tPredix
	INNER JOIN [NFL].[RP].[TBL_Play] tPlay
	ON tPredix.[FK_ID_Observation] = tPlay.[PK_ID_Play]
	--INNER JOIN [NFL].[RP].[VW_FullPlays_Modified] vFullPlays
	--ON tPlay.[PK_ID_Play] = vFullPlays.[PK_ID_Play]
	WHERE [FK_ID_AggregatedResults] = @sqlvar_ID_AggregatedResults
	ORDER BY tPlay.[PK_ID_Play] ASC
END
GO


