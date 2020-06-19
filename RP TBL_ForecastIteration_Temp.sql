USE [NFL]
GO

/****** Object:  Table [RP].[TBL_ForecastIteration_Temp]    Script Date: 1/28/2020 2:26:41 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [RP].[TBL_ForecastIteration_Temp](
	[modelName] [nvarchar](1024) NULL,
	[numberOfClasses] [int] NULL,
	[forecastType] [nvarchar](16) NULL
) ON [PRIMARY]
GO
