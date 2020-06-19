USE [NFL]
GO

/****** Object:  Table [RP].[TBL_forecastIteration]    Script Date: 1/28/2020 2:25:48 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [RP].[TBL_ForecastIteration](
	[PK_ID_forecastIteration] [int] IDENTITY(1,1) NOT NULL,
	[tempoTimbri_forecastIteration] [datetime2](7) NULL,
	[modelName] [nvarchar](1024) NULL,
	[numberOfClasses] [int] NULL,
	[forecastType] [nvarchar](16) NULL,
PRIMARY KEY CLUSTERED 
(
	[PK_ID_forecastIteration] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
