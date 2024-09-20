import pandas as pd



import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# For Models
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.model_selection import GridSearchCV

# For Evaluation 
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score

newdf = pd.read_csv("./crawler/data_cleaning/cleaned_data_dropna.csv", sep=',')
model_name = newdf['model_name']
newdf = newdf.drop('model_name', axis=1)
newdf.round(0).astype(int)



plt.figure(figsize=(10, 6))
sns.histplot(newdf['price'], bins=30, kde=True, color='blue')
plt.title('Distribution of Phone Prices')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()



import matplotlib.pyplot as plt
import seaborn as sns

f,ax = plt.subplots(figsize=(35,35))
sns.heatmap(newdf.corr(),annot=True,fmt='.1f',ax=ax)
plt.show()


from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


y = newdf['price'].values
X = newdf.drop(columns = ['price'])

# Scaling all the variables to a range of 0 to 1
from sklearn.preprocessing import MinMaxScaler
features = X.columns.values
scaler = MinMaxScaler(feature_range = (0,1))

scaler.fit(X)
X = pd.DataFrame(scaler.transform(X))
X.columns = features



from sklearn.ensemble import ExtraTreesRegressor
import matplotlib.pyplot as plt
model = ExtraTreesRegressor()
model.fit(X,y)

feat_importances = pd.Series(model.feature_importances_, index=X.columns)
feat_importances.nlargest(5).plot(kind='barh')




from sklearn.model_selection import train_test_split


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)




from sklearn.linear_model import LinearRegression

logreg = LinearRegression()
logreg.fit(X_train, y_train)

# Make predictions on the test data
y_pred = logreg.predict(X_test)



from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
print('MAE:', mean_absolute_error(y_test, y_pred))
print('MSE:', mean_squared_error(y_test, y_pred))
print('r2_score:', r2_score(y_test,y_pred))



print("Testing Accuracy:",logreg.score(X_test,y_test))


#plt.figure(figsize=(10, 6))
#sns.scatterplot(x=y_test, y=y_pred, alpha=0.6)
#sns.lineplot(x=[y_test.min(), y_test.max()], y=[y_test.min(), y_test.max()], color='red', linestyle='--')
#plt.xlabel("Actual Values")
#plt.ylabel("Predicted Values")
#plt.title("Actual vs Predicted Values with Line of Best Fit")
#plt.show()


plt.figure(figsize=(12, 10))
plt.xlim(0,50000)


ax1 = sns.distplot(y_test, hist=False, color="r", label="Actual Value")

sns.distplot(y_pred, hist=False, color="b", label="Fitted Values" , ax=ax1)


plt.title('Actual vs Fitted Values for Price')
plt.xlabel('Price (in dollars)')
plt.ylabel('Proportion of Smartphones')

plt.show()
plt.close()

# Update predicted price in phones dataset


realDataset = pd.read_csv("./crawler/data_preparation/phones.csv", sep=',')



pred_price_all = logreg.predict(X)

X['model_name'] = model_name
X['pred_price'] = pred_price_all

X

realDataset['recommended_price'] = pd.Series(dtype='float')
realDataset['able_to_predict'] = pd.Series(dtype='bool')



for index, row in realDataset.iterrows():
    #row['recommended_price'] = X.loc[X['model_name'] == row['model_name']]['pred_price']
    try:
        if X.loc[X['model_name'] == row['model_name']]['pred_price'] > 0:
            realDataset.at[index,'recommended_price'] = X.loc[X['model_name'] == row['model_name']]['pred_price']
            realDataset.at[index,'able_to_predict'] = True
        else:
            realDataset.at[index,'recommended_price'] = row['best_price']
            realDataset.at[index,'able_to_predict'] = False
    except:
        realDataset.at[index,'recommended_price'] = row['best_price']
        realDataset.at[index,'able_to_predict'] = False

realDataset.to_csv("./crawler/data_preparation/final_phones.csv", sep=',')
