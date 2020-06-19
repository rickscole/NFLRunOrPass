USE [NFL]
GO

/****** Object:  Table [RP].[TBL_AggregatedResults]    Script Date: 11/5/2019 11:26:40 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [RP].[TBL_AggregatedResults](
	[PK_ID_AggregatedResults] [int] IDENTITY(1,1) NOT NULL,
	[tempoTimbri_aggregatedResults] [datetime2](7) NULL,
	[FK_ID_forecastIteration] [int] NULL,
	[meanAccuracy] [float] NULL,
	[stdevAccuracy] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[PK_ID_AggregatedResults] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
