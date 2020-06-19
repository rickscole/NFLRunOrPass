USE [NFL]
GO
/****** Object:  StoredProcedure [RP].[SP_InsertIntoTable_ForecastIteration]    Script Date: 1/28/2020 12:00:48 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		rsc
-- Create date: 2019-08-21
-- Description:	insert into forecast iteration table; for use in Python
-- =============================================
ALTER PROCEDURE [RP].[SP_InsertIntoTable_ForecastIteration] 
	-- Add the parameters for the stored procedure here

AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

	/*
	INSERT INTO TBL_ML_forecastIteration (tempoTimbri_forecastIteration,distanceMetric,weightMethods,powerParameter,algorithms,evalMetric,numberOfNeighbors,modelName,numberOfClasses)
	SELECT SYSDATETIME(),distanceMetric,weightMethods,powerParameter,algorithms,evalMetric, numberOfNeighbors,modelName,numberOfClasses 
	FROM TBL_ML_forecastIteration_temp
	*/

	INSERT INTO RP.TBL_ForecastIteration (tempoTimbri_forecastIteration,modelName,numberOfClasses,forecastType)
	SELECT SYSDATETIME(), modelName,numberOfClasses,forecastType 
	FROM RP.TBL_ForecastIteration_Temp

	DELETE FROM RP.TBL_ForecastIteration_Temp
END


