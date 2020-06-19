USE [NFL]
GO

/****** Object:  Table [RP].[TBL_ForecastParameters_RF_Temp]  Script Date: 1/31/2020 5:11:04 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [RP].[TBL_ForecastParameters_RF_Temp](
	[FK_ID_forecastIteration] [int] NULL,
	[estimators] [nvarchar](1024) NULL,
	[splitCriterion] [nvarchar](1024) NULL,
	[maxDepth] [nvarchar](1024) NULL,
	[minSampleSplit] [nvarchar](1024) NULL,
	[minSampleLeaf] [nvarchar](1024) NULL,
	[maxFeatures] [nvarchar](1024) NULL,
	[maxLeafNodes] [nvarchar](1024) NULL,
	[minImpurityDecrease] [nvarchar](1024) NULL,
	[bootstrap] [nvarchar](1024) NULL,
	[OOBScore] [nvarchar](1024) NULL,
	[usesPCA] [nvarchar](1024) NULL,
	[numberOfComponents] [nvarchar](1024) NULL,
	[standardizeData] [nvarchar](1024) NULL,
	[numberOfSplits] [nvarchar](1024) NULL,
	[evalMetric] [nvarchar](1024) NULL
) ON [PRIMARY]
GO
