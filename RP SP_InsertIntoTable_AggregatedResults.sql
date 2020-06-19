USE [NFL]
GO
/****** Object:  StoredProcedure [RP].[SP_InsertIntoTable_AggregatedResults]    Script Date: 1/28/2020 11:58:01 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		rsc
-- Create date: 2019-08-06
-- Description:	insert into aggregated results into table; for use in Python
-- =============================================
ALTER PROCEDURE [RP].[SP_InsertIntoTable_AggregatedResults] 
	-- Add the parameters for the stored procedure here
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

	DECLARE @sqlparam_FK_ID_ForecastIteration INT
	SET @sqlparam_FK_ID_ForecastIteration = (SELECT MAX(PK_ID_forecastIteration) FROM RP.TBL_ForecastIteration)

	INSERT INTO RP.TBL_AggregatedResults ([tempoTimbri_aggregatedResults],[FK_ID_forecastIteration],[meanAccuracy],[stdevAccuracy])
	SELECT SYSDATETIME(), @sqlparam_FK_ID_ForecastIteration, meanAccuracy, stdevAccuracy FROM RP.TBL_AggregatedResults_Temp

	DELETE FROM RP.TBL_AggregatedResults_Temp
END
