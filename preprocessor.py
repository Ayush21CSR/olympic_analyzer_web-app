#
# import pandas as pd
#
#
# def preprocess(df,region_df):
#     # filtering for summer olympics
#     df = df[df['Season'] == 'Summer']
#     # merge with region_df
#     df = df.merge(region_df, on='NOC', how='left')
#     # dropping duplicates
#     df.drop_duplicates(inplace=True)
#     # one hot encoding medals
#     df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
#     return df


import pandas as pd


def preprocess(df: pd.DataFrame, region_df: pd.DataFrame) -> pd.DataFrame:
    # Merge the athlete and region dataframes
    df = df.merge(region_df, on='NOC', how='left')

    # Drop duplicate entries for medals
    df.drop_duplicates(inplace=True)

    # One hot encoding for the 'Medal' column
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df

