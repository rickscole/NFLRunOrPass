use nfl
--select top 100 * FROM [NFL].[RP].[TBL_Plays_Old] tPlaysFull 

--select play_id,
--game_id,
--count(*)
--from [NFL].[RP].[TBL_Plays_Old] tPlaysFull 
--group by play_id,
--game_id
--having count(*) > 2

--select * from [NFL].[RP].[TBL_Plays_Old] tPlaysFull  
--where play_id = 1835 and game_id = 2011120406

--select * from rp.VW_FullPlays_Modified vPlays

;WITH tPlaysFull_ID AS
(
	SELECT *
	, ROW_NUMBER() OVER(ORDER BY [play_id], [game_id]) + 100000 AS [PK_ID_Play_Adjusted]
	, ROW_NUMBER() OVER(PARTITION BY [play_id], [game_id] ORDER BY RAND()) AS [ID_Repeats]
	FROM [NFL].[RP].[TBL_Plays_Old] tPlaysFull
),
tv_FullPlaysModified_Repeats AS
(
	SELECT *
	, ROW_NUMBER() OVER (PARTITION BY [PK_ID_Play] ORDER BY RAND()) AS [ID_Repeats]
	FROM [NFL].[RP].VW_FullPlays_Modified vPlays 
)
, tv_FullPlaysModified_UnqPK AS
(
	SELECT * 
	FROM tv_FullPlaysModified_Repeats
	WHERE [ID_Repeats] = 1
),
tConsolidated AS
(
	SELECT tPlaysFull_ID.*
	, tv_FullPlaysModified_UnqPK.[PK_ID_Play]
	FROM tPlaysFull_ID
	LEFT JOIN tv_FullPlaysModified_UnqPK
	ON tPlaysFull_ID.[play_id] = tv_FullPlaysModified_UnqPK.[play_id]
	AND tPlaysFull_ID.[game_id] = tv_FullPlaysModified_UnqPK.[game_id]
	WHERE tPlaysFull_ID.[ID_Repeats] = 1
	AND tv_FullPlaysModified_UnqPK.[PK_ID_Play] IS NOT NULL

	UNION ALL 

	SELECT tPlaysFull_ID.*
	, tPlaysFull_ID.[PK_ID_Play_Adjusted] AS [PK_ID_Play]
	FROM tPlaysFull_ID
	LEFT JOIN tv_FullPlaysModified_UnqPK
	ON tPlaysFull_ID.[play_id] = tv_FullPlaysModified_UnqPK.[play_id]
	AND tPlaysFull_ID.[game_id] = tv_FullPlaysModified_UnqPK.[game_id]
	WHERE tPlaysFull_ID.[ID_Repeats] = 1
	AND tv_FullPlaysModified_UnqPK.[PK_ID_Play] IS NULL 
)
SELECT *
INTO [NFL].[RP].[TBL_Play]
FROM tConsolidated


--SELECT [game_id]
--, [play_id]
--, COUNT(*)
--FROM tPlaysFull_ID
--WHERE [ID_Repeats] = 1
--GROUP BY 
--[game_id]
--, [play_id]


--select top 10 * from [NFL].[RP].VW_FullPlays_Modified vPlays 


--SELECT tPlaysFull_ID.*
--FROM tPlaysFull_ID
--LEFT JOIN 


--SELECT PK_ID_Play,
--COUNT(*) FROM [NFL].[RP].VW_FullPlays_Modified vPlays 
--group by PK_ID_Play
--having count(*) > 1

--select * from [NFL].[RP].VW_FullPlays_Modified vPlays  where PK_ID_Play = 30079