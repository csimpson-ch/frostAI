import os
from module_processing import *

# read the raw csv file
file_path = os.path.join(os.path.join(os.getcwd(), "data"), "Waipara_AWS_2023.csv")
df = read_csv_waipara_aws(file_path)

# set hours to store as features for each observation
df2 = create_feature_target_df(df, hour_diff_to_store=range(1, 97, 1))

# save processed df as csv, for quicker access later
df2.to_csv(os.path.join(os.path.join(os.getcwd(), "data"), "Waipara_AWS_2023_featured.csv"))
