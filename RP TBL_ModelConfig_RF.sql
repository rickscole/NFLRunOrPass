USE [NFL]
GO

/****** Object:  Table [RP].[TBL_ModelConfig_RF]    Script Date: 1/31/2020 5:11:36 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [RP].[TBL_ModelConfig_RF](
	[PK_ID_modelConfig] [int] IDENTITY(1,1) NOT NULL,
	[FK_ID_forecastIteration] [int] NULL,
	[estimators] [int] NULL,
	[splitCriterion] [nvarchar](64) NULL,
	[maxDepth] [nvarchar](8) NULL,
	[minSampleSplit] [int] NULL,
	[minSampleLeaf] [int] NULL,
	[maxFeatures] [nvarchar](8) NULL,
	[maxLeafNodes] [nvarchar](8) NULL,
	[minImpurityDecrease] [float] NULL,
	[bootstrap] [nvarchar](5) NULL,
	[OOBScore] [nvarchar](16) NULL,
	[usesPCA] [nvarchar](5) NULL,
	[numberOfComponents] [int] NULL,
	[standardizeData] [nvarchar](5) NULL,
	[numberOfSplits] [int] NULL,
	[evalMetric] [nvarchar](64) NULL,
	[CCPAlpha] [float] NULL,
	[SplitMethod] [nvarchar] (64) NULL
) ON [PRIMARY]
GO
