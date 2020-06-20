USE [NFL]
GO

/****** Object:  Table [RP].[TBL_ModelParameter]    Script Date: 11/5/2019 2:54:12 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [RP].[TBL_ModelParameter](
	[modelParameter] [nvarchar](128) NULL,
	[modelParameterValue] [nvarchar](128) NULL,
	[ID_modelParameterValue] [int] NULL
) ON [PRIMARY]
GO
