
import pandas as pd 
 
df = pd.read_csv("titanic.csv") 
 
df.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis = 1, inplace = True) 
 
df['Embarked'].fillna('S', inplace = True) 
 
age1 = df[df['Pclass'] == 1]['Age'].median() 
age2 = df[df['Pclass'] == 2]['Age'].median() 
age3 = df[df['Pclass'] == 3]['Age'].median() 
 
def set_age(row): 
    if pd.isnull(row['Age']): 
        if row['Pclass'] == 1: 
            return age1 
        elif row['Pclass'] == 2: 
            return age2 
        elif row['Pclass'] == 3: 
            return age3 
    return row['Age'] 
 
df['Age'] = df.apply(set_age, axis = 1) 
 
def set_sex(sex): 
    if sex == 'male': 
        return 1 
    elif sex == 'female': 
        return 0 
 
df['Sex'] = df['Sex'].apply(set_sex) 
 
df[list(pd.get_dummies(df['Embarked']).columns)] = pd.get_dummies(df['Embarked']) 
 
df.drop('Embarked', axis = 1, inplace = True) 
 
df.info() 
 
#------------------------ 
 
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler 
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.metrics import confusion_matrix, accuracy_score 
 
#1. Розділення набору даних на 2 частини: 
X = df.drop("Survived", axis=1) 
y = df["Survived"] 
 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25) 
 
sc = StandardScaler() 
 
#2. Виконання стандартизації показників в обох наборах даних 
X_train = sc.fit_transform(X_train) 
X_test = sc.transform(X_test) 
 
#3. Створення об'єкту класифікатора KNN. Налаштування параметра моделі 
classifier = KNeighborsClassifier(n_neighbors=3) 
 
#4. Навчання моделі на тренінговому наборі даних 
classifier.fit(X_train, y_train) 
 
#5. Розраховування прогнозу значень цільової змінної для тестового набору даних 
y_pred = classifier.predict(X_test) 
 
print(y_pred) 
 
for p, t in zip(y_pred, y_test): 
    print(f"p={p}; t={t}") 
 
#6. Оцінення точності прогнозу 
percent = accuracy_score(y_test, y_pred)*100 
print(percent) 
 
print(confusion_matrix(y_test, y_pred))