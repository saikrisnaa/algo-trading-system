from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def prepare_features(df):
    print("Initial DataFrame columns:", df.columns)
    print(f"Initial rows for ML: {df.shape}")
    df['RSI'] = compute_rsi(df['Close'], period=7)  # Use period=7 for less NA
    df['ShortMA'] = df['Close'].rolling(window=5).mean()
    df['LongMA'] = df['Close'].rolling(window=10).mean()
    print("Rows after feature add (before dropna):", df.shape)
    print("NAs per column:\n", df.isna().sum())
    df = df.dropna()
    print(f"Rows after dropna and features: {df.shape}")
    if df.shape[0] < 10:
        print("WARNING: Too few rows for ML.")
    df = df.copy()
    df.loc[:, 'Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
    feature_cols = ['RSI', 'ShortMA', 'LongMA', 'Volume']
    X = df[feature_cols]
    y = df['Target']
    print(f"Final ML feature set rows: {X.shape}")
    return X.dropna(), y.dropna()

def ml_decision_tree(df):
    X, y = prepare_features(df)
    if X.empty or y.empty:
        print("no ml data for this ticker")
        return 0, None  # No data to train on
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    return acc, clf


