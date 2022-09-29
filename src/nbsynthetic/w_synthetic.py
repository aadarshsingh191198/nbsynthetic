# Copyright 2022 Softpoint Consultores SL. All Rights Reserved.
#
# Licensed under MIT License (the "License");
# you may not use this file except in compliance with the License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import warnings
import numpy as np
import pandas as pd
from pandas.core.dtypes.dtypes import CategoricalDtype
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_selector as selector
from sklearn.preprocessing import MinMaxScaler, \
    QuantileTransformer, KBinsDiscretizer

warnings.filterwarnings('ignore', '.*do not.*', )
pd.options.mode.chained_assignment = None


def columns_type(df: pd.DataFrame):
    """
    Args:
        df(pd.DataFrame):
            input data
    
    Returns:
        two lists with numerical and 
        categorical column names.
    """
    numerical_columns_selector = selector(
        dtype_exclude=CategoricalDtype
        )
    categorical_columns_selector = selector(
        dtype_include=CategoricalDtype
        )
    numerical_columns = numerical_columns_selector(df)
    categorical_columns = categorical_columns_selector(df)
    return numerical_columns, categorical_columns


def data_transformation(
    df: pd.DataFrame, 
    numerical_columns, 
    categorical_columns,
    ):
    """
    Args:
        df(pd.DataFrame):
            input data
        numerical_columns:
            list with numerical columns names 
        categorical_columns:
            list with categorical columns name
    
    Returns:
        prepared dataframe for input"""

    n_quantiles = int(len(df)*0.7)
    categorical_scaler = make_pipeline(
        MinMaxScaler(
            feature_range=(-1, 1),
            clip=True
            )
        )
    numerical_scaler = make_pipeline(
    # A quantile transform will map a variable’s 
    # probability distribution to another probability 
    # distribution.By performing a rank 
    # transformation, a quantile transform smooths out 
    # unusual distributions and is less influenced by 
    # outliers than scaling methods.
    # https://scikit-learn.org/stable/modules/preprocessing.html#preprocessing-transformer
        QuantileTransformer(
            n_quantiles=n_quantiles, 
            output_distribution='uniform',
            ),
        MinMaxScaler(
            feature_range=(-1, 1),
            clip=True
            )
        )
    scaled_X = df.copy()
    for cat_c in categorical_columns:
      scaled_X[cat_c] = categorical_scaler.fit_transform(
          np.array(df[cat_c]).reshape(-1, 1)
          ).flatten()
    
    for num_c in numerical_columns:
      scaled_X[num_c] = numerical_scaler.fit_transform(
          np.array(df[num_c]).reshape(-1, 1)
          ).flatten()

    return np.array(scaled_X),\
                    categorical_scaler, numerical_scaler


def generate_data(
    df: pd.DataFrame,  
    x_synthetic, 
    categorical_columns, 
    numerical_columns, 
    categorical_scaler, 
    numerical_scaler
    ): 
    """
    Args:
        df(pd.DataFrame):
            input data
        x_synthetic:
            data generated by GAN network  
        categorical_columns:
            list with categorical columns name  
        numerical_columns:
                list with numerical columns names     
        categorical_scaler: 
                scikit learn transfomed used for
                input data preparation for categorical
                features
        numerical_scaler: 
                scikit learn transfomed used for
                input data preparation for numerical
                features
    Returns:
        Synthetic dataframe (pd.DataFrame)"""

    newdf = pd.DataFrame(
        x_synthetic, 
        columns=df.columns
        )
    for cat_c in categorical_columns:
      if np.unique(df[cat_c]).shape[0] > 1:
        newdf[cat_c] = categorical_scaler.inverse_transform(
            np.array(
                newdf[cat_c]).reshape(-1,1)
                )
        kbins = KBinsDiscretizer(
              n_bins=np.unique(df[cat_c]).shape[0], 
              encode='ordinal', 
              strategy='uniform'
              )
        newdf[cat_c] = kbins.fit_transform(
            np.array(newdf[cat_c]).reshape(-1,1)
            ).astype(int)
        newdf[cat_c]= newdf[cat_c].astype('category')
      else:
        pass
    
    for num_c in numerical_columns:
      newdf[num_c] = numerical_scaler.inverse_transform(
          np.array(
              newdf[num_c]).reshape(-1,1)
              ).flatten().astype('float64')
    
    for cat_c in categorical_columns:
      if np.unique(df[cat_c]).shape[0] == 2:
        newdf[cat_c].replace(
            [np.unique(newdf[cat_c])[0],
            np.unique(newdf[cat_c])[1]],
            [np.unique(df[cat_c])[0],
            np.unique(df[cat_c])[1]],
            inplace=True
            )
      else:
        pass
    
    return newdf


def synthetic_data(
    df: pd.DataFrame, 
    WGAN, 
    samples: int,
    n_features,
    initial_lr,
    dropout,
    epochs
    ):
    """Args:

          df (pd.DataFrame): 
            input data frame
          gan (Keras models): 
            keras GAN models
          samples (int):
            number of instances for the
            synthetic dataset
          number of features (int):
              number of input features
          initial_lr:
              initial learning rate for NN
          droput:
              apply Dropout to input 
                
      Returns:

          Synthetic dataframe (pd.DataFrame)
          """

    if len(df) > 48:
      batch_size = 48
    else:
      batch_size = (int(len(df) / 8) - 1) * 8

    numerical_columns,\
    categorical_columns = columns_type(df)
    scaled_X,\
    categorical_scaler,\
    numerical_scaler = data_transformation(
        df, 
        numerical_columns, 
        categorical_columns
        )
    

    def train_gan(
        scaled_X,
        n_features,
        initial_lr,
        dropout
        ): 
      gan = WGAN(
        number_of_features=n_features, 
        learning_rate=initial_lr, 
        dropout=dropout, 
        )    
      G_loss,\
      D_loss = gan.train(
          scaled_data=scaled_X, 
          epochs=epochs, 
          batch_size=batch_size,
          )
      return G_loss, D_loss, gan

    G_loss,\
    D_loss,\
    gan = train_gan(
        scaled_X, 
        n_features,
        initial_lr,
        dropout
        )
    """
    if G_loss > 1:
      G_loss,\
      D_loss,\
      gan = train_gan(
          scaled_X, 
          n_features, 
          initial_lr/10, 
          dropout
          )
    else:
      pass
      if G_loss > 1:
          G_loss,\
          D_loss,\
          gan = train_gan(
              scaled_X, 
              n_features, 
              initial_lr/100, 
              dropout
              )
      else:
        pass"""
  
    x_synthetic,\
    y_synthetic = gan.create_fake_samples(
        batch_size=samples
        )
    newdf = generate_data(
        df, 
        x_synthetic, 
        categorical_columns, 
        numerical_columns, 
        categorical_scaler, 
        numerical_scaler
        ) 
    for c in numerical_columns:
      scaler = MinMaxScaler(
                feature_range=(
                    df[c].min(), 
                    df[c].max()
                    ),
                clip=True
                )
      newdf[c] = scaler.fit_transform(
              np.array(
                  newdf[c]).reshape(-1, 1)
                  ).flatten()

    
    return newdf
