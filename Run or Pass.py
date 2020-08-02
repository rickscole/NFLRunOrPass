
# import libraries
import time
import pyodbc
import pandas
from sklearn import model_selection
import datetime
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler 
from sklearn.decomposition import PCA 
from sklearn.ensemble import RandomForestClassifier
from pandas import DataFrame 
import numpy
from urllib.parse import quote_plus
from sqlalchemy import create_engine, event
import itertools

# start stopwatch
pyts_startTime = time.time()
pyobj_Connection = pyodbc.connect('Driver={SQL Server};''Server=LAPTOP-NTC9E1A0\SQLEXPRESS;''Database=NFL;''Trusted_Connection=yes;');
pyobj_Cursor = pyobj_Connection.cursor()

class pyclass_Predictions_All(object):
    
    # NOTES
    #202007200829:
    # this method of using range to create a list that defines the indices for the X attributes is needed because we need to grab the Primary Key ID value for the observations
    # ultimately this value is stripped out of the actual train/test setup, but we need it to go through the cross validation bit so that a list of train and test indeces can be ...
    # ... properly identified and reattached to the dataframe when we make actual predictions on the dataset at the very end
    
    # define functions
    def __call__():
        pass
    def pyfx_GetAdjacentArrayTitle(pyparam_Array,pyparam_ArrayName,pyparam_ArrayElementOrdinality):
        '''
        used to help get cross-joined dataframe
        '''
        pyparam_Array = ['None' if pyndx_Array == None else pyndx_Array for pyndx_Array in pyparam_Array]
        pyarr_AdjacentArrayNameLength = len(pyparam_Array)
        pyarr_AdjacentArrayName = [pyparam_ArrayName] * pyarr_AdjacentArrayNameLength
        pyarr_AdjacentArrayName = [str(pyndx_Item) for pyndx_Item in pyarr_AdjacentArrayName]
        pyarr_ArrayElementOrdinality = [pyparam_ArrayElementOrdinality] * pyarr_AdjacentArrayNameLength
        pyarr_ArrayElementOrdinality = [str(pyndx_Item) for pyndx_Item in pyarr_ArrayElementOrdinality]
        pyobj_Dataframe_ModelParameters = DataFrame({'ModelParameter':pyarr_AdjacentArrayName,'ModelParameterValue':pyparam_Array,'ID_ModelParameterValue':pyarr_ArrayElementOrdinality})
        return pyobj_Dataframe_ModelParameters  
    def pyfx_GetLearnerArguments(self,pyparam_ModelName,pyparam_Connection):
        '''
        get list of arguments for learner
        '''
        pyvar_SQL = "SELECT * FROM NFL.RP.TBL_LearnerArgument WHERE learnerName = '" + pyparam_ModelName + "'";
        pyparam_Connection.commit();
        pydf_LearnerArguments = pandas.read_sql_query(pyvar_SQL, pyparam_Connection);
        return pydf_LearnerArguments
    def pyfx_GetNumberOfIterations(self,pyparam_LearnerArguments):
        '''
        get number of iterations for a given forecast iteration
        '''
        pyvar_DynamicString = ''.join(["len(pyarr_Select_" + pyndx_Arguments + ")*" for pyndx_Arguments in pyparam_LearnerArguments])[:-1] 
        return pyvar_DynamicString
    def pyfx_CompileModelConfigs(self, pyparam_LearnerArguments):
        '''
        get optimal configuration for a given iteration
        '''
        pyvar_DynamicString = "[(" + ''.join(["pyndx_Select_" + pyndx_Arguments + "," for pyndx_Arguments in pyparam_LearnerArguments])[:-1] + ")"
        pyvar_DynamicString = pyvar_DynamicString + ''.join([" for pyndx_Select_" + pyndx_Arguments + " in pyarr_Select_" + pyndx_Arguments for pyndx_Arguments in pyparam_LearnerArguments]) + "]"
        return pyvar_DynamicString
    def pyfx_PreprocessData(self, pyfxparam_XAttributes_Train, pyfxparam_XAttributes_Validation,pyfxparam_YAttributes, pyfxparam_ValidationSize, pyfxparam_Seed, pfxparam_StandardizeData_Optimal, pyfxparam_UsesPCA_Optimal, pyfxparam_NumberOfComponents_Optimal):
        '''
        standard preprocessing of data in model creation
        '''
        if pfxparam_StandardizeData_Optimal == True:
            pyobj_MinMaxScaler = preprocessing.MinMaxScaler()
            pyarr_XAttributes_Train = pyobj_MinMaxScaler.fit_transform(pyfxparam_XAttributes_Train)
            pyarr_XAttributes_Train = pandas.DataFrame(pyarr_XAttributes_Train)
            pyobj_MinMaxScaler = preprocessing.MinMaxScaler()
            pyarr_XAttributes_Validation = pyobj_MinMaxScaler.fit_transform(pyfxparam_XAttributes_Validation)
            pyarr_XAttributes_Validation = pandas.DataFrame(pyarr_XAttributes_Validation)
        if pyfxparam_UsesPCA_Optimal == True:
            pyobj_Scaler = StandardScaler();
            pyarr_XAttributes_Train = pyobj_Scaler.fit_transform(pyarr_XAttributes_Train);
            pyarr_XAttributes_Validation = pyobj_Scaler.fit_transform(pyarr_XAttributes_Validation);
            pyobj_PCA = PCA(n_components = pyfxparam_NumberOfComponents_Optimal);
            pyarr_XAttributes_Train_PostNormalization = pyobj_PCA.fit_transform(pyarr_XAttributes_Train);
            pyarr_XAttributes_Validation_PostNormalization = pyobj_PCA.transform(pyarr_XAttributes_Validation); 
            #pyarr_ExplainedVariance = pyobj_PCA.explained_variance_ratio_;
        else:
            pyarr_XAttributes_Train_PostNormalization = pyarr_XAttributes_Train;
            pyarr_XAttributes_Validation_PostNormalization = pyarr_XAttributes_Validation;
        pylist_ReturnList = [pyarr_XAttributes_Train_PostNormalization,pyarr_XAttributes_Validation_PostNormalization]
        return pylist_ReturnList
    def pyfx_GetCVResults(self, pyfxparam_NumberOfSplits, pyfxparam_Seed, pyfxparam_Model, pyfxparam_XAttributes_Train_PostNormalization, pyfxparam_YAttributes_Train_PostNormalization, pyfxparam_EvalMetric):
        '''
        get cross validated results for a given learner
        '''
        pyobj_KFold = model_selection.KFold(n_splits = pyfxparam_NumberOfSplits, random_state = pyfxparam_Seed)
        pyobj_CVResults = model_selection.cross_val_score(pyfxparam_Model, pyfxparam_XAttributes_Train_PostNormalization, pyfxparam_YAttributes_Train_PostNormalization, cv = pyobj_KFold, scoring = pyfxparam_EvalMetric)
        #pyobj_Model.fit(pyarr_XAttributes_Train_PostNormalization, pyarr_YAttributes_Train_PostNormalization)
        #pyobj_Predictions = pyobj_Model.predict(pyarr_XAttributes_Validation_PostNormalization)
        #pyobj_ModelResults_Accuracy_Validation = pyobj_Model.predict(pyarr_XAttributes_Validation_PostNormalization)
        return pyobj_CVResults
    def pyfx_ForecastIteration(self, pyfxparam_ModelName, pyfxparam_NumberOfClasses, pyfxparam_ForecastType):
        '''
        inserts into forecast iteration table
        also returns forecast iteration ID
        '''
        print("Inserting into forecast iteration table")
        pydf_ForecastIteration = DataFrame({'modelName':[pyfxparam_ModelName],'numberOfClasses':pyfxparam_NumberOfClasses,'forecastType':pyfxparam_ForecastType})
        for pyndx_Index, pyndx_Row in pydf_ForecastIteration.iterrows():
            pyobj_Cursor.execute("INSERT INTO NFL.RP.TBL_ForecastIteration([modelName],[numberOfClasses],[forecastType]) values (?,?,?)",pyndx_Row['modelName'],pyndx_Row['numberOfClasses'],pyndx_Row['forecastType'])
            pyobj_Connection.commit()
        pyvar_SQL = "{call [NFL].[RP].[SP_InsertIntoTable_ForecastIteration]}"
        pyobj_Cursor.execute(pyvar_SQL)
        pyobj_Connection.commit()
        # return forecast ID
        pyvar_SQL = "SELECT MAX(PK_ID_forecastIteration) AS PK_ID_forecastIteration FROM [NFL].[RP].[TBL_ForecastIteration]"
        pyobj_Cursor.execute(pyvar_SQL)
        pyvar_PK_ID_ForecastIteration = pyobj_Cursor.fetchval()
        return pyvar_PK_ID_ForecastIteration
    def pyfx_ForecastParameter_Create(self, pyfxparam_LearnerArguments, pyfxparam_Learner):
        '''
        create forecast parameters dataframe
        '''
        print("Inserting into forecast parameters table")
        pyvar_DynamicString = "DataFrame({" + ''.join( "'" + pyndx_LearnerArguments + "': [str(pyarr_Select_" + pyndx_LearnerArguments + ").strip('[]')],"  for pyndx_LearnerArguments in pyfxparam_LearnerArguments)[:-1] + "})"
        #pyvar_DynamicString = "pyvar_cursor.execute('INSERT INTO dbo.TBL_ML_" + pyfxparam_Learner + "forecastParameters_temp(" + ''.join("[" + pyndx_Arguments +  "]," for pyndx_Arguments in pyfxparam_LearnerArguments)[:-1] + ") values (" + (len(pyfxparam_LearnerArguments) * '?,')[:-1] + ")', " + ''.join("pyndx_row['" + pyndx_Arguments + "'],"  for pyndx_Arguments in pyfxparam_LearnerArguments)[:-1] + ")"
        return pyvar_DynamicString
    def pyfx_ForecastParameter_Upload(self, pyfxparam_Dataframe, pyfxparam_LearnerArguments, pyfxparam_Learner):
        '''
        upload forecast parameters dataframe to db
        '''
        for pyndx_index, pyndx_Row in pyfxparam_Dataframe.iterrows():
            pyvar_DynamicString = "pyobj_Cursor.execute('INSERT INTO NFL.RP.TBL_ForecastParameters_" + pyfxparam_Learner + "_Temp(" + ''.join("[" + pyndx_Arguments +  "]," for pyndx_Arguments in pyfxparam_LearnerArguments)[:-1] + ") values (" + (len(pyfxparam_LearnerArguments) * '?,')[:-1] + ")', " + ''.join("pyndx_Row['" + pyndx_Arguments + "'],"  for pyndx_Arguments in pyfxparam_LearnerArguments)[:-1] + ")"
            exec(pyvar_DynamicString)
            #print(pyvar_DynamicString)
        pyvar_SQL = "{call [NFL].[RP].[SP_InsertIntoTable_ForecastParameters_" + pyfxparam_Learner + "]}"
        pyobj_Cursor.execute(pyvar_SQL)
        pyobj_Connection.commit()
    def pyfx_AggregatedResults(self,pyfxparam_Accuracy_Mean, pyfxparam_Accuracy_Stdev):
        '''
        get previous agg results ID
        insert into agg results table
        '''
        print("Inserting into aggregate results table")
        pyvar_SQL = "SELECT MAX(PK_ID_AggregatedResults) AS MaxValue FROM NFL.RP.TBL_AggregatedResults"
        pyobj_ExecutedCursor = pyobj_Cursor.execute(pyvar_SQL)
        pyobj_ExecutedCursor_FetchaAll = pyobj_ExecutedCursor.fetchall()
        for pyndx_Row in pyobj_ExecutedCursor_FetchaAll:
            pyvar_Previous_ID_AggregatedResults =  pyndx_Row[0]
        pydf_Accuracy = DataFrame({'meanAccuracy': pyfxparam_Accuracy_Mean, 'stdevAccuracy':pyfxparam_Accuracy_Stdev})
        for pyndx_index, pyndx_Row in pydf_Accuracy.iterrows():
            pyobj_Cursor.execute("INSERT INTO NFL.RP.TBL_AggregatedResults_Temp([meanAccuracy],[stdevAccuracy]) values (?,?)",pyndx_Row['meanAccuracy'],pyndx_Row['stdevAccuracy'])
            pyobj_Connection.commit()  
        pyvar_SQL = "{call [NFL].[RP].[SP_InsertIntoTable_AggregatedResults]}"
        pyobj_Cursor.execute(pyvar_SQL)
        pyobj_Connection.commit()
        return(pyvar_Previous_ID_AggregatedResults)
    def pyfx_Results(self,pyfxparam_Accuracy):
        '''
        get previous results ID
        insert into results table
        '''
        print("Inserting into results table")
        pyvar_SQL = "SELECT MAX(PK_ID_Results) AS MaxValue FROM NFL.RP.TBL_Results"
        pyobj_ExecutedCursor = pyobj_Cursor.execute(pyvar_SQL)
        pyobj_ExecutedCursor_FetchaAll = pyobj_ExecutedCursor.fetchall()
        for pyndx_Row in pyobj_ExecutedCursor_FetchaAll:
            pyvar_Previous_ID_Results =  pyndx_Row[0]
        pydf_Accuracy = DataFrame({'Accuracy': pyfxparam_Accuracy})
        for pyndx_index, pyndx_Row in pydf_Accuracy.iterrows():
            pyobj_Cursor.execute("INSERT INTO NFL.RP.TBL_Results_Temp([Accuracy]) values (?)",pyndx_Row['Accuracy'])
            pyobj_Connection.commit()  
        pyvar_SQL = "{call [NFL].[RP].[SP_InsertIntoTable_Results]}"
        pyobj_Cursor.execute(pyvar_SQL)
        pyobj_Connection.commit()
        return(pyvar_Previous_ID_Results)
    def pyfx_UploadPredictions(self, pyfxparam_Train_Index, pyfxparam_Validation_Index, pyfx_ModelResults_Train, pyarr_ModelResults_Validation):
        pydf_ModelResults = DataFrame({'ID_Observation':pyfxparam_Train_Index,'Prediction':pyfx_ModelResults_Train, 'CVType':['train']*len(pyfxparam_Train_Index)})
        pydf_ModelResults = pydf_ModelResults.append(DataFrame({'ID_Observation':pyfxparam_Validation_Index,'Prediction':pyarr_ModelResults_Validation, 'CVType':['validation']*len(pyfxparam_Validation_Index)}))
        for pyndx_Index, pyndx_Row in pydf_ModelResults.iterrows():
            pyobj_Cursor.execute("INSERT INTO NFL.RP.TBL_Predictions_Categorical_Temp([FK_ID_Observation],[Prediction],[CVType]) values (?,?,?)",pyndx_Row['ID_Observation'],pyndx_Row['Prediction'],pyndx_Row['CVType'])
            pyobj_Connection.commit()
        pyvar_SQL = "{call [NFL].[RP].[SP_InsertIntoTable_Predictions_Categorical]}"
        pyobj_Cursor.execute(pyvar_SQL)
        pyobj_Connection.commit()
    def pyfx_IntTryParse(self,value):
        '''
        try and parse out an integer
        '''
        try:
            return int(value), True
        except ValueError:
            return value, False
    def pyfx_FloatTryParse(self,value):
        '''
        try and parse out a float
        '''
        try:
            return float(value), True
        except ValueError:
            return value, False
    def pyfx_TryParse(self,pyparam_Value):
        '''
        multi-purpose data type parser
        '''
        if pyparam_Value == "None":
            pyvar_ReturnValue = None
        elif self.pyfx_IntTryParse(pyparam_Value)[1] == True:
            pyvar_ReturnValue = self.pyfx_IntTryParse(pyparam_Value)[0]
        elif self.pyfx_FloatTryParse(pyparam_Value)[1] == True:
            pyvar_ReturnValue = self.pyfx_FloatTryParse(pyparam_Value)[0]
        elif pyparam_Value == "True":
            pyvar_ReturnValue = True
        elif pyparam_Value == "False":
            pyvar_ReturnValue = False
        else:
            pyvar_ReturnValue = pyparam_Value
        return pyvar_ReturnValue
    
    # load dataset
    pyvar_SQL = "SELECT TOP 16000 * FROM [NFL].[RP].[TBL_Play_Modified] ORDER BY [PK_ID_Play] ASC";
    pyobj_Connection.commit();
    pyobj_Dataset = pandas.read_sql_query(pyvar_SQL, pyobj_Connection);
    
    # initial split-out validation dataset
    pyvar_ValidationSize = .3
    pyvar_Seed = 7
    pyarr_Dataset_WithAttributes = pyobj_Dataset.values;
    pyarr_XAttributes_Range = [0] #202007200829
    pyarr_XAttributes_Range.extend([*range(2,27)])
    pyarr_XAttributes = pyarr_Dataset_WithAttributes[:,pyarr_XAttributes_Range]
    pyarr_YAttributes = pyarr_Dataset_WithAttributes[:,1]
    pyarr_XAttributes_Train, pyarr_XAttributes_Validation, pyarr_YAttributes_Train, pyarr_YAttributes_Validation = model_selection.train_test_split(pyarr_XAttributes, pyarr_YAttributes, test_size = pyvar_ValidationSize, random_state=pyvar_Seed)
    global pyarr_Train_Index #202007200829
    pyarr_Train_Index = pyarr_XAttributes_Train[:,0] 
    global pyarr_Validation_Index #202007200829
    pyarr_Validation_Index = pyarr_XAttributes_Validation[:,0] 
    pyarr_XAttributes_Train = pyarr_XAttributes_Train[:,1:25] 
    pyarr_XAttributes_Validation = pyarr_XAttributes_Validation[:,1:25]
    
    # static parameters / shortcut variables
    pyvar_ForecastType = ('exploratory') 
    pyvar_NumberOfRecords = len(pyarr_Dataset_WithAttributes[:,25])
    pyvar_XAttributes_Train_Length = len(pyarr_XAttributes_Train)
    pyvar_XAttributes_Test_Length = len(pyarr_XAttributes_Validation)
    pyvar_NumberOfClasses = 2
    pyts_TempoTimbri = datetime.datetime.now()
    
    # available argument inputs
    pyarr_Avail_UsesPCA = [True,False]
    pyarr_Avail_NumberOfComponents = [] #N202001231139
    pyarr_Avail_StandardizeData = [True,False]
    pyarr_Avail_NumberOfSplits = [] #N202001231139
    pyarr_Avail_EvalMetric = ['accuracy','balanced_accuracy','average_precision','brier_score_loss','f1','f1_micro','f1_macro','f1_weighted','f1_samples','neg_log_loss','precision','recall','jaccard','roc_auc','explained_variance','max_error',
                             'neg_mean_absolute_error','neg_mean_squared_error','neg_mean_squared_log_error','neg_median_absolute_error','r2']
    
    # model results arrays
    pyarr_ModelResults = []
    pyarr_ModelResults_Accuracy_Mean = []
    pyarr_ModelResults_Accuracy_Stdev = []
    pyarr_ObservationNumber = []

class pyclass_Predictions_RF:
    
    # static parameters / shortcut variables
    pyvar_ModelName = ('RF')
    
    # available argument inputs
    pyarr_Avail_Estimators = [] #N202001231117
    pyarr_Avail_SplitCriterion = ['gini','entropy']
    pyarr_Avail_MaxDepth = [None] #N202001231137
    pyarr_Avail_MinSampleSplit = [] #N202001231139
    pyarr_Avail_MinSampleLeaf = [] #N202001231139
    pyarr_Avail_MaxFeatures = [None,'auto','sqrt','log2']
    pyarr_Avail_MaxLeafNodes = [None] #N202001231137
    pyarr_Avail_MinImpurityDecrease = [] #N202001231130
    pyarr_Avail_SplitMethod = ['best','random']
    pyarr_Avail_Bootstrap = [True,False]
    pyarr_Avail_OOBScore = [True,False] #N202001231130
    pyarr_Avail_CCPAlpha = [] #N202001240848
    
    # selected argument inputs
    pyarr_Select_Estimators = [10,100]
    pyarr_Select_SplitCriterion = ['gini']
    pyarr_Select_MaxDepth = [12]
    pyarr_Select_MinSampleSplit = [2]
    pyarr_Select_MinSampleLeaf = [1]
    pyarr_Select_MaxFeatures = ['auto']
    pyarr_Select_MaxLeafNodes = [50]
    pyarr_Select_MinImpurityDecrease = [0]
    pyarr_Select_SplitMethod = ['best']
    pyarr_Select_Bootstrap = [True]
    pyarr_Select_OOBScore = [False]
    pyarr_Select_CCPAlpha = [0]
    pyarr_Select_UsesPCA = [False]
    pyarr_Select_NumberOfComponents = [12]
    pyarr_Select_StandardizeData = [True]
    pyarr_Select_NumberOfSplits = [10]
    pyarr_Select_EvalMetric = ['accuracy']

    # invoke members of collective class
    pyobj_Predictions_All = pyclass_Predictions_All()
    pyobj_Dataset = pyobj_Predictions_All.pyobj_Dataset
    pyvar_ValidationSize = pyobj_Predictions_All.pyvar_ValidationSize
    pyvar_Seed = pyobj_Predictions_All.pyvar_Seed
    pyarr_Dataset_WithAttributes = pyobj_Predictions_All.pyarr_Dataset_WithAttributes
    pyarr_XAttributes = pyobj_Predictions_All.pyarr_XAttributes
    pyarr_YAttributes = pyobj_Predictions_All.pyarr_YAttributes
    pyarr_XAttributes_Train = pyobj_Predictions_All.pyarr_XAttributes_Train
    pyarr_XAttributes_Validation = pyobj_Predictions_All.pyarr_XAttributes_Validation
    pyarr_YAttributes_Train =  pyobj_Predictions_All.pyarr_YAttributes_Train
    pyarr_YAttributes_Validation = pyobj_Predictions_All.pyarr_YAttributes_Validation
    pyvar_ForecastType = pyobj_Predictions_All.pyvar_ForecastType
    pyvar_NumberOfRecords = pyobj_Predictions_All.pyvar_NumberOfRecords
    pyvar_XAttributes_Train_Length = pyobj_Predictions_All.pyvar_XAttributes_Train_Length
    pyvar_XAttributes_Test_Length = pyobj_Predictions_All.pyvar_XAttributes_Test_Length
    pyvar_NumberOfClasses = pyobj_Predictions_All.pyvar_NumberOfClasses
    pyts_TempoTimbri = pyobj_Predictions_All.pyts_TempoTimbri
    pyarr_Avail_UsesPCA = pyobj_Predictions_All.pyarr_Avail_UsesPCA
    pyarr_Avail_NumberOfComponents = pyobj_Predictions_All.pyarr_Avail_NumberOfComponents
    pyarr_Avail_StandardizeData = pyobj_Predictions_All.pyarr_Avail_StandardizeData
    pyarr_Avail_NumberOfSplits = pyobj_Predictions_All.pyarr_Avail_NumberOfSplits
    pyarr_Avail_EvalMetric = pyobj_Predictions_All.pyarr_Avail_EvalMetric
    pyarr_ModelResults = pyobj_Predictions_All.pyarr_ModelResults
    pyarr_ModelResults_Accuracy_Mean = pyobj_Predictions_All.pyarr_ModelResults_Accuracy_Mean
    pyarr_ModelResults_Accuracy_Stdev = pyobj_Predictions_All.pyarr_ModelResults_Accuracy_Stdev
    pyarr_ObservationNumber = pyobj_Predictions_All.pyarr_ObservationNumber
    pydf_LearnerArguments = pyobj_Predictions_All.pyfx_GetLearnerArguments(pyvar_ModelName,pyobj_Connection)
    pylist_LearnerArguments = list(pydf_LearnerArguments.loc[: , "argumentInput"])
    pyobj_Predictions_All.pyfx_ForecastIteration(pyvar_ModelName, 2, 'exploratory')
    pyvar_DynamicString = "pyvar_NumberOfIterations = " + pyobj_Predictions_All.pyfx_GetNumberOfIterations(pylist_LearnerArguments)
    exec(pyvar_DynamicString)
    
    # upload all model configurations to db
    #pyvar_DynamicString = "pyarr_ModelConfigs = " + pyobj_Predictions_All.pyfx_CompileModelConfigs(pylist_LearnerArguments)
    #pyarr_ModelConfigs = [(pyndx_Select_Estimators,pyndx_Select_MaxDepth,pyndx_Select_MinSampleSplit,pyndx_Select_MinSampleLeaf,pyndx_Select_MaxFeatures,pyndx_Select_MinImpurityDecrease,pyndx_Select_SplitMethod,pyndx_Select_Bootstrap,pyndx_Select_OOBScore,pyndx_Select_CCPAlpha,pyndx_Select_UsesPCA,pyndx_Select_NumberOfComponents,pyndx_Select_StandardizeData,pyndx_Select_NumberOfSplits,pyndx_Select_EvalMetric) for pyndx_Select_Estimators in pyarr_Select_Estimators for pyndx_Select_MaxDepth in pyarr_Select_MaxDepth for pyndx_Select_MinSampleSplit in pyarr_Select_MinSampleSplit for pyndx_Select_MinSampleLeaf in pyarr_Select_MinSampleLeaf for pyndx_Select_MaxFeatures in pyarr_Select_MaxFeatures for pyndx_Select_MinImpurityDecrease in pyarr_Select_MinImpurityDecrease for pyndx_Select_SplitMethod in pyarr_Select_SplitMethod for pyndx_Select_Bootstrap in pyarr_Select_Bootstrap for pyndx_Select_OOBScore in pyarr_Select_OOBScore for pyndx_Select_CCPAlpha in pyarr_Select_CCPAlpha for pyndx_Select_UsesPCA in pyarr_Select_UsesPCA for pyndx_Select_NumberOfComponents in pyarr_Select_NumberOfComponents for pyndx_Select_StandardizeData in pyarr_Select_StandardizeData for pyndx_Select_NumberOfSplits in pyarr_Select_NumberOfSplits for pyndx_Select_EvalMetric in pyarr_Select_EvalMetric]
    #exec(pyvar_DynamicString)
    
    #pyvar_DynamicString = "pydf_ModelParameters = DataFrame({'ModelParameter': [], 'ModelParameterValue':[],'ID_ModelParameterValue':[]})"
    #pyvar_DynamicString = ''.join(" pydf_ModelParameters_Sub = pyfx_GetAdjacentArrayTitle(pyarr_Select_" + pyndx_LearnerArgument + ",'" + pyndx_LearnerArgument + "'," + str(pyndx_LearnerArgument_Index) + "); pydf_ModelParameters = pydf_ModelParameters.append(pydf_ModelParameters_Sub);" for pyndx_LearnerArgument_Index, pyndx_LearnerArgument in enumerate(pylist_LearnerArguments, start = 1))
    #pyvar_DynamicString = "pydf_ModelParameters = DataFrame({'ModelParameter': [], 'ModelParameterValue':[],'ID_ModelParameterValue':[]}); " + pyvar_DynamicString
    #exec(pyvar_DynamicString)
    #for pyndx_index, pyndx_row in pydf_ModelParameters.iterrows():
    #    pyobj_Cursor.execute("INSERT INTO NFL.RP.TBL_ModelParameter([ModelParameter],[ModelParameterValue],[ID_ModelParameterValue]) values (?,?,?)",pyndx_row['ModelParameter'],pyndx_row['ModelParameterValue'],pyndx_row['ID_ModelParameterValue'])
    #    pyobj_Connection.commit()
        
    pyvar_DynamicString = "pydf_ForecastParameters = " + pyobj_Predictions_All.pyfx_ForecastParameter_Create(pylist_LearnerArguments,pyvar_ModelName)
    exec(pyvar_DynamicString)
    pyobj_Predictions_All.pyfx_ForecastParameter_Upload(pydf_ForecastParameters,pylist_LearnerArguments,pyvar_ModelName)
    
    #pyvar_SQL = "{call NFL.[RP].[SP_CrossJoinArrays_" + pyvar_ModelName + "]}";
    #pyobj_Cursor.execute(pyvar_SQL)
    #pyobj_Connection.commit()
    
    pylist_ModelConfig = []
    pyvar_DynamicString = "itertools.product("
    pyvar_DynamicString = pyvar_DynamicString + ''.join("pyarr_Select_" + pyndx_Arguments + "," for pyndx_Arguments in pylist_LearnerArguments) [:-1] + ")"
    pyvar_DynamicString = "for pyndx_Element in " + pyvar_DynamicString + ": pylist_ModelConfig.append(pyndx_Element)"
    exec(pyvar_DynamicString)
    
    # run models and gather data
    print(pyvar_NumberOfIterations, "scheduled to run")
    pyndx_Iteration = 1
    for pyndx_Estimators in pyarr_Select_Estimators:
        for pyndx_SplitCriterion in pyarr_Select_SplitCriterion:
            for pyndx_MaxDepth in pyarr_Select_MaxDepth:
                for pyndx_MinSampleSplit in pyarr_Select_MinSampleSplit:
                    for pyndx_MinSampleLeaf in pyarr_Select_MinSampleLeaf:
                        for pyndx_MaxFeatures in pyarr_Select_MaxFeatures:
                            for pyndx_MaxLeafNodes in pyarr_Select_MaxLeafNodes:
                                for pyndx_MinImpurityDecrease in pyarr_Select_MinImpurityDecrease:
                                    for pyndx_Bootstrap in pyarr_Select_Bootstrap:
                                        for pyndx_OOBScore in pyarr_Select_OOBScore:
                                            for pyndx_CCPAlpha in pyarr_Select_CCPAlpha:
                                                for pyndx_UsesPCA in pyarr_Select_UsesPCA:
                                                    for pyndx_NumberOfComponents in pyarr_Select_NumberOfComponents:
                                                        for pyndx_StandardizeData in pyarr_Select_StandardizeData:
                                                            for pyndx_NumberOfSplits in pyarr_Select_NumberOfSplits:
                                                                for pyndx_EvalMetric in pyarr_Select_EvalMetric:
                                                                
                                                                    # normalize as needed
                                                                    pylist_PreprocessData = pyobj_Predictions_All.pyfx_PreprocessData(pyarr_XAttributes_Train, pyarr_XAttributes_Validation, pyarr_YAttributes_Train, pyvar_ValidationSize, pyvar_Seed, pyndx_StandardizeData, pyndx_UsesPCA, pyndx_NumberOfComponents)
                                                                    pyarr_XAttributes_Train_PostNormalization, pyarr_YAttributes_Train_PostNormalization, pyarr_XAttributes_Validation_PostNormalization, pyarr_YAttributes_Validation_PostNormalization = pylist_PreprocessData[0],pyarr_YAttributes_Train, pylist_PreprocessData[1], pyarr_YAttributes_Validation
                                                                                                                                        
                                                                    # create model
                                                                    try:
                                                                        pyobj_Model = RandomForestClassifier(n_estimators = pyndx_Estimators,
                                                                                                             criterion= pyndx_SplitCriterion, 
                                                                                                             max_depth = pyndx_MaxDepth, 
                                                                                                             min_samples_split = pyndx_MinSampleSplit, 
                                                                                                             min_samples_leaf = pyndx_MinSampleLeaf, 
                                                                                                             max_features = pyndx_MaxFeatures, 
                                                                                                             max_leaf_nodes = pyndx_MaxLeafNodes, 
                                                                                                             min_impurity_decrease = pyndx_MinImpurityDecrease,
                                                                                                             bootstrap = pyndx_Bootstrap,
                                                                                                             oob_score = pyndx_OOBScore)                                                                             
                                                                        pyobj_CVResults = pyobj_Predictions_All.pyfx_GetCVResults(pyndx_NumberOfSplits, pyvar_Seed, pyobj_Model, pyarr_XAttributes_Train_PostNormalization, pyarr_YAttributes_Train_PostNormalization, pyndx_EvalMetric)
                                                                        pybin_SuccessfulModel = True
                                                                    except:
                                                                        pyobj_Model = None
                                                                        pyobj_CVResults = [None] * pyndx_NumberOfSplits
                                                                        pybin_SuccessfulModel = False
                                                                        
                                                                    if pybin_SuccessfulModel == True:
                                                                        pyarr_ModelResults.extend(pyobj_CVResults)
                                                                        pyarr_ModelResults_Accuracy_Mean.append(pyobj_CVResults.mean())
                                                                        pyarr_ModelResults_Accuracy_Stdev.append(pyobj_CVResults.std())
                                                                    else:
                                                                        pyarr_ModelResults.extend(pyobj_CVResults)
                                                                        pyarr_ModelResults_Accuracy_Mean.append(None)
                                                                        pyarr_ModelResults_Accuracy_Stdev.append(None)
                                                                    
                                                                    pyarr_ObservationNumber.extend([pyndx_Iteration] * len(pyobj_CVResults))
                                                                    pyndx_Iteration = pyndx_Iteration + 1
                                                                    print(pyndx_Iteration)
                                                                    
    
    # find optimal configuration
    print("Finding optimal configuration")
    global pyndx_TopModel
    pyndx_TopModel = pyarr_ModelResults_Accuracy_Mean.index(max(pyarr_ModelResults_Accuracy_Mean))
    pyvar_DynamicString = ''.join(["pyvar_" + pyndx_Arguments + "_Optimal,"  for pyndx_Arguments in pylist_LearnerArguments])[:-1]
    pyvar_DynamicString = pyvar_DynamicString + " = " + ''.join(["pylist_ModelConfig[" + str(pyndx_TopModel) + "][" + str(pyndx_Arguments_Index) + "]," for  pyndx_Arguments_Index,pyndx_Arguments in enumerate(pylist_LearnerArguments, start = 0)])[:-1]
    exec(pyvar_DynamicString)
    
    # run optimal configuration
    print("Running optimal configuration")
    pylist_PreprocessData = pyobj_Predictions_All.pyfx_PreprocessData(pyarr_XAttributes_Train, pyarr_XAttributes_Validation, pyarr_YAttributes_Train, pyvar_ValidationSize, pyvar_Seed, pyvar_StandardizeData_Optimal, pyvar_UsesPCA_Optimal, pyvar_NumberOfComponents_Optimal)
    pyarr_XAttributes_Train_PostNormalization, pyarr_YAttributes_Train_PostNormalization, pyarr_XAttributes_Validation_PostNormalization, pyarr_YAttributes_Validation_PostNormalization = pyarr_XAttributes_Train_PostNormalization, pyarr_YAttributes_Train_PostNormalization, pyarr_XAttributes_Validation_PostNormalization, pyarr_YAttributes_Validation_PostNormalization = pylist_PreprocessData[0],pyarr_YAttributes_Train, pylist_PreprocessData[1], pyarr_YAttributes_Validation
    pyobj_Model = RandomForestClassifier(n_estimators = pyobj_Predictions_All.pyfx_TryParse(pyvar_Estimators_Optimal),
                                     criterion= pyobj_Predictions_All.pyfx_TryParse(pyvar_SplitCriterion_Optimal), 
                                     max_depth = pyobj_Predictions_All.pyfx_TryParse(pyvar_MaxDepth_Optimal), 
                                     min_samples_split = pyobj_Predictions_All.pyfx_TryParse(pyvar_MinSampleSplit_Optimal), 
                                     min_samples_leaf = pyobj_Predictions_All.pyfx_TryParse(pyvar_MinSampleLeaf_Optimal), 
                                     max_features = pyobj_Predictions_All.pyfx_TryParse(pyvar_MaxFeatures_Optimal), 
                                     max_leaf_nodes = pyobj_Predictions_All.pyfx_TryParse(pyvar_MaxLeafNodes_Optimal), 
                                     min_impurity_decrease = pyobj_Predictions_All.pyfx_TryParse(pyvar_MinImpurityDecrease_Optimal),
                                     bootstrap = pyobj_Predictions_All.pyfx_TryParse(pyvar_Bootstrap_Optimal),
                                     oob_score = pyobj_Predictions_All.pyfx_TryParse(pyvar_OOBScore_Optimal))                                                                             
    pyobj_CVResults = pyobj_Predictions_All.pyfx_GetCVResults(pyvar_NumberOfSplits_Optimal, pyvar_Seed, pyobj_Model, pyarr_XAttributes_Train_PostNormalization, pyarr_YAttributes_Train_PostNormalization, pyvar_EvalMetric_Optimal)
    pyobj_Model.fit(pyarr_XAttributes_Train_PostNormalization, pyarr_YAttributes_Train_PostNormalization)
    pyarr_ModelResults_Train = pyobj_Model.predict(pyarr_XAttributes_Train_PostNormalization)
    pyarr_ModelResults_Validation = pyobj_Model.predict(pyarr_XAttributes_Validation_PostNormalization)
    
    pyarr_ModelResults_Accuracy_Mean = [pyobj_CVResults.mean()] 
    pyarr_ModelResults_Accuracy_Stdev = [pyobj_CVResults.std()]
    pyvar_Previous_ID_AggregatedResults = pyobj_Predictions_All.pyfx_AggregatedResults(pyarr_ModelResults_Accuracy_Mean, pyarr_ModelResults_Accuracy_Stdev)
    pyvar_Previous_ID_Results = pyobj_Predictions_All.pyfx_Results(pyobj_CVResults)
    
    print("Inserting into predictions table")
    pyobj_Predictions_All.pyfx_UploadPredictions(pyarr_Train_Index, pyarr_Validation_Index, pyarr_ModelResults_Train, pyarr_ModelResults_Validation)
    
    
    
    #print(pyobj_Model.fit(pyarr_XAttributes_Train_PostNormalization, pyarr_YAttributes_Train_PostNormalization))
    
    
    

a = pyclass_Predictions_RF()

pyobj_Cursor.close();
pyobj_Connection.close();

# pyndx_TopModel = pyparam_ModelResults_Accuracy_Mean.index(max(pyparam_ModelResults_Accuracy_Mean))
