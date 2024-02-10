import pandas as pd
import numpy as np
import mord
from scipy import stats
from enum import Enum
from typing import Union, Tuple
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from measures import discret_prediction_rate
from transforms import round_rating

Measuretype = Enum('MeasureType', 'PVALUE AIC BIC NOTCH0')

def make_binary_variables(dependent_variable_name: str, input_frame: pd.DataFrame ) -> Tuple[pd.DataFrame, list]:
    '''
    Naive Bayes classifier for Gaussian models. 
    '''

    class_names = set(input_frame[dependent_variable_name])
    print(f'Number of variables to make is {len(class_names)}.')
    input_frame['binary'] = input_frame[dependent_variable_name]
    input_frame = pd.get_deummies(input_frame, prefix = 'binary', columns = ['binary'])
    binary_column_names = [f'binary{class_names}' for class_name in class_names]
    return input_frame, binary_column_names


def backward_elimination(indepndent: pd.DataFrame, dependent: pd.Series, model: callable, measure_type: Measuretype = Measuretype.PVALUE, alpha: float or int =0,
                         significance_level: float = 0.05, train_size: float or int = 1, need_summary: bool = True) -> Union[list, Tuple[list, pd.DataFrame]]:

                        features = indepndent.columns.tolist()
                        if measure_type == Measuretype.NOTCH0:
                            summary = pd.Dataframe(index = (['None'] + features))
                        else:
                            if train_size != 1:
                                raise ValueError('When the measure tpe is not NOTCH0 the train size variable must be the default, 1')
                            else: 
                                summary = pd.DataFrame(index=(['notch0', 'None'] + features))

                        if train_size == 1:
                            independent_train, independent_test, dependent_train, depedendent_test = independent, independent, dependent, dependent
                        else: 
                            independent_train, independent_test, dependent_train, depedendent_test = train_test_split(independent, dependent, train_size = train_size, stratify = dependent)
                        step_num = 0
                        while len(features) > 1:
                            step_num += 1
                            current_independent_train = independent_train[features]
                            current_independent_test = independent_test[features]
                            current_model = model(current_independent_train, dependent_train, alpha)
                            measures = pd.Sries(index=['None']+features, dtype='float64')
                            predictions = current_model.predict(current_independent_test)
                            if isinstance(predictions, np.ndarray):
                                predictions = pd.Series(predictions, dtype = 'float64')
                            predictions.index = depedendent_test.index
                            predictions = round_rating(predictions)
                            notch0 = discreet_prediction_rate(depedendent_test, predictions)

                            if measure_type ==  Measur_Type.NOTCH0:
                                measures.at['None'] = notch0
                            else:
                                summary.loc['notch0', f'step_{step_num}'] = notch0

                            if measure_type == Measuretype.PVALUE:
                                measures = current_model.pvalues
                                max_value = measures.max()
                                feauture_to_drop = 'None'
                                if max_value >= significance_level:
                                    feauture_to_drop = measures.idmax()
                            
                            elif measure_type == Measuretype.AIC:
                                measures.at['None'] = current_model.aic
                                for column in features:
                                    current_independent = independent[features].drop(columns = [column])
                                    current_model = model(current_independent, dependent, alpha = alpha)
                                    measures.at[column] = current_model.aic
                                feauture_to_drop = measures.idxmin()

                            elif measure_type == Measuretype.BIC:
                                measures.at['None'] = current_model.bic
                                for column in features:
                                    current_independent = independent[features].drop(columns = [column])
                                    current_model = model(current_independent, dependent, alpha = alpha)
                                    measures.at[column] = current_model.bic
                                feauture_to_drop = measures.idxmin()
                            
                            elif measure_type == Measuretype.NOTCH0:
                                for column in features:
                                    current_independent_train = independent_train[features].drop(columns = [column])
                                    current_independent_test = independent_test[features].drop(columns = [column])
                                    current_model = model(current_independent_train, dependent_train, alpha)
                                    predictions =current_model.predict(current_independent_test)
                                    if isinstance(predictions, np.ndarray):
                                        predictions = pd.Seris(predictions, dtype = 'float64')
                                    predictions.index = depedendent_test.index
                                    predictions = round_rating(predictions)
                                    notch0 = discreet_prediction_rate(depedendent_test, predictions)
                                    measures.at[column] = notch0
                                feauture_to_drop = measures.idxmax()

                            else: 
                                raise ValueError(f'Invalid measure_type value: {measure_type}')
                            
                            summary.loc[['None'] + features, f'step_{step_num}'] = measures

                            if feauture_to_drop != 'None':
                                features.remove(feauture_to_drop)
                            else:
                                break
                        
                        if need_summary:
                            summary = summary.round(4)
                            return features, summary

                        else:
                            return features
                            

class OLM(mord.LogisticAT):

    def __init__(self, alpha = 0):
        super(OLS, self).__init__(alpha=alpha)

    def fit(self, x, y):
        super(OLM, self).fit(x,y)
        n, k = x.shape
        y_predicted = self.predict(x)
        self.theta_ = pd.Series(self.theta_, index = self.classes_[:-1], name='Upper limit of classes', dtype='float64')
        self.coef_ = pd.Series(self.coef_, index=x.columns, name='coefficients', dtype= 'float64')
        self.params = self.coef_

        #Sample variance and degrees of freedom

        sse = np.sum((y_predicted - y)**2, axis=0)
        df = float(n-k-1)
        self.sse = sse / df

        #Sample variance for x
        variance_x = x.T.dot(x)
        self.se = np.sqrt(np.diagonal(self.sse*np.linalg.piv(variance_x.values)))

        #T statistic for each beta
        self.tvalues = self.coef_ / self.se

        # P-value for each beta. This is a two sided t-test, since the betas can be positive or negative.
        pvalues = 1 - stats.t.cdf(abs(self.tvalues), df)
        self.pvalues = pd.Series(data = pvalues, index=x.columns, dtype = 'float64')

        self.loglikelihood = np.sum(np.log(self.predict_proba(x).max(axis=1)))
        #AIC
        self.aic = 2*(len(self.coef_) + len(self.theta_)) -2*self.loglikelihood
        #BIC
        self.bic = np.log(n) * (len(self.coef_) + len(sel.theta_)) - 2*self.loglikelihood

def ordered_logt_model(independent_variable_df: pd.DataFrame, dependent_variable_ser: pd.Series, alpha: float or int = 0) -> OLM:
    if len(dependent_variable_ser) > dependent_variable_ser.notna().sum():
        raise ValueError('Dependent variable series contains Nan.')
    olm = OLM(alpha=alpha)
    olm.fit(independent_variable_df, dependent_variable_ser)
    return olm

def estimate_naively(dependent_variable_ser: pd.Series, independent_variable_df: pd.DataFrame) -> object:
    model = GaussianNB()
    model = model.fit(independent_variable_df, dependent_variable_ser)
    return model
    