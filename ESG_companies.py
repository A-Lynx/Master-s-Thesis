import pandas as pd
import yfinance as yf
from tqdm import tqdm  # индикатор прогресса

# --- 1. Загружаем тикеры MSCI ACWI ---
acwi = pd.read_csv("ACWI_holdings.csv", header=7)  # 8-я строка содержит заголовки
tickers = acwi['Ticker'].tolist()

# --- 2. Функция для получения ESG данных ---
def get_esg_data(ticker):
    try:
        company = yf.Ticker(ticker)
        esg_df = company.sustainability  # получаем ESG данные
        if esg_df is None or esg_df.empty:
            return None
        esg_df = pd.DataFrame.transpose(esg_df)
        return {
            'Ticker': ticker,
            'Total_ESG': esg_df.loc['esgScores', 'totalEsg'],
            'Environmental': esg_df.loc['esgScores', 'environmentScore'],
            'Social': esg_df.loc['esgScores', 'socialScore'],
            'Governance': esg_df.loc['esgScores', 'governanceScore']
        }
    except Exception as e:
        return {
            'Ticker': ticker,
            'Total_ESG': None,
            'Environmental': None,
            'Social': None,
            'Governance': None,
            'Error': str(e)
        }

# --- 3. Сбор ESG данных для всех тикеров ---
results = []
for t in tqdm(tickers):
    data = get_esg_data(t)
    if data is not None:
        results.append(data)

# --- 4. Создаём DataFrame и фильтруем только с ESG ---
df_esg = pd.DataFrame(results)
df_esg_filtered = df_esg[df_esg['Total_ESG'].notnull()]

# --- 5. Сохраняем ---
df_esg_filtered.to_csv('ACWI_ESG_Data.csv', index=False)
df_esg_filtered.to_excel('ACWI_ESG_Data.xlsx', index=False)

print(f"✅ Данные собраны. Всего компаний с ESG: {len(df_esg_filtered)}")
