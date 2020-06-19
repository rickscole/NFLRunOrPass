USE [NFL]
GO
/****** Object:  StoredProcedure [RP].[SP_ML_insertIntoTable_RFforecastParameters]    Script Date: 1/31/2020 5:08:23 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		rsc
-- Create date: 2020-01-31_0955
-- Description:	insert into RF forecast parameters table; for use in Python
-- =============================================
ALTER PROCEDURE [RP].[SP_InsertIntoTable_ForecastParameters_RF] 
	-- Add the parameters for the stored procedure here

AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

	DECLARE @sqlparam_FK_ID_forecastIteration INT
	SET @sqlparam_FK_ID_forecastIteration = (SELECT MAX(PK_ID_forecastIteration) FROM RP.TBL_ForecastIteration)

	INSERT INTO  RP.TBL_ForecastParameters_RF ([FK_ID_forecastIteration],[tempoTimbri_SVMforecastParameter],[estimators],[splitCriterion],[maxDepth],[minSampleSplit],[minSampleLeaf],[maxFeatures],[maxLeafNodes],[minImpurityDecrease],[bootstrap],[OOBScore],[usesPCA],[numberOfComponents],[standardizeData],[numberOfSplits],[evalMetric])
	SELECT  @sqlparam_FK_ID_forecastIteration,SYSDATETIME(),[estimators],[splitCriterion],[maxDepth],[minSampleSplit],[minSampleLeaf],[maxFeatures],[maxLeafNodes],[minImpurityDecrease],[bootstrap],[OOBScore],[usesPCA],[numberOfComponents],[standardizeData],[numberOfSplits],[evalMetric]
	FROM TBL_ForecastParameters_RF_Temp

	DELETE FROM RP.TBL_ForecastParameters_RF_Temp
END

