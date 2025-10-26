import pandas as pd

# === 1. Загрузка и очистка данных ===

df = pd.read_csv("countries.csv")

# Удалим лишние пробелы
df["Country"] = df["Country"].str.strip()
df["Region"] = df["Region"].str.strip()

# Список столбцов, где числа записаны с запятыми
cols_to_fix = [
    'Pop. Density (per sq. mi.)', 'Coastline (coast/area ratio)', 'Net migration',
    'Infant mortality (per 1000 births)', 'Literacy (%)', 'Phones (per 1000)',
    'Arable (%)', 'Crops (%)', 'Other (%)', 'Climate', 'Birthrate', 'Deathrate',
    'Agriculture', 'Industry', 'Service'
]

# Приводим данные к числовому типу
for col in cols_to_fix:
    df[col] = df[col].astype(str).str.replace(',', '.')
    df[col] = df[col].apply(lambda x: pd.to_numeric(x, errors='coerce'))

# Заполняем пропуски медианами
df = df.fillna(df.median(numeric_only=True))

# === 2. Проверка гипотез ===

print("Проверка гипотез о факторах, влияющих на качество жизни населения:\n")

# --- Гипотеза 1 ---
corr1 = df['GDP ($ per capita)'].corr(df['Literacy (%)'])
print("1️⃣ Гипотеза: ВВП зависит от уровня грамотности населения.")
print(f"   Корреляция: {corr1:.2f}")
if corr1 > 0.5:
    print("   ✅ Подтверждается: высокий уровень грамотности связан с высоким ВВП.\n")
else:
    print("   ❌ Не подтверждается.\n")

# --- Гипотеза 2 ---
corr2 = df['GDP ($ per capita)'].corr(df['Infant mortality (per 1000 births)'])
print("2️⃣ Гипотеза: чем выше ВВП, тем ниже младенческая смертность.")
print(f"   Корреляция: {corr2:.2f}")
if corr2 < -0.5:
    print("   ✅ Подтверждается: высокий ВВП связан с низкой смертностью младенцев.\n")
else:
    print("   ❌ Не подтверждается.\n")

# --- Гипотеза 3 ---
corr3 = df['GDP ($ per capita)'].corr(df['Phones (per 1000)'])
print("3️⃣ Гипотеза: чем выше ВВП, тем больше телефонов на 1000 человек.")
print(f"   Корреляция: {corr3:.2f}")
if corr3 > 0.5:
    print("   ✅ Подтверждается: высокий ВВП связан с высоким уровнем телефонизации.\n")
else:
    print("   ❌ Не подтверждается.\n")

# --- Гипотеза 4 ---
corr4 = df['GDP ($ per capita)'].corr(df['Agriculture'])
print("4️⃣ Гипотеза: чем больше доля сельского хозяйства, тем ниже ВВП.")
print(f"   Корреляция: {corr4:.2f}")
if corr4 < -0.5:
    print("   ✅ Подтверждается: аграрные экономики имеют ниже ВВП.\n")
else:
    print("   ❌ Не подтверждается.\n")

# --- Гипотеза 5 ---
coast = df[df['Coastline (coast/area ratio)'] > 0]['GDP ($ per capita)'].mean()
no_coast = df[df['Coastline (coast/area ratio)'] == 0]['GDP ($ per capita)'].mean()
print("5️⃣ Гипотеза: страны, имеющие выход к морю, богаче.")
print(f"   Средний ВВП при выходе к морю: {coast:.0f}")
print(f"   Средний ВВП без выхода к морю: {no_coast:.0f}")
if coast > no_coast:
    print("   ✅ Подтверждается: страны с выходом к морю имеют выше средний ВВП.\n")
else:
    print("   ❌ Не подтверждается.\n")

# --- Гипотеза 6 ---
corr6 = df['Literacy (%)'].corr(df['Infant mortality (per 1000 births)'])
print("6️⃣ Гипотеза: чем выше уровень грамотности, тем ниже младенческая смертность.")
print(f"   Корреляция: {corr6:.2f}")
if corr6 < -0.5:
    print("   ✅ Подтверждается: грамотность снижает детскую смертность.\n")
else:
    print("   ❌ Не подтверждается.\n")

# --- Гипотеза 7 ---
by_region = df.groupby('Region')['GDP ($ per capita)'].mean().sort_values(ascending=False)
print("7️⃣ Гипотеза: средний ВВП в Европе выше, чем в Африке.")
print(by_region[['WESTERN EUROPE', 'NORTHERN AFRICA', 'SUB-SAHARAN AFRICA']])
if by_region['WESTERN EUROPE'] > by_region['SUB-SAHARAN AFRICA']:
    print("   ✅ Подтверждается: Европа богаче Африки по среднему ВВП.\n")
else:
    print("   ❌ Не подтверждается.\n")

# --- Гипотеза 8 ---
corr8 = df['Birthrate'].corr(df['GDP ($ per capita)'])
print("8️⃣ Гипотеза: чем выше рождаемость, тем ниже ВВП.")
print(f"   Корреляция: {corr8:.2f}")
if corr8 < -0.5:
    print("   ✅ Подтверждается: высокая рождаемость характерна для бедных стран.\n")
else:
    print("   ❌ Не подтверждается.\n")

# --- Гипотеза 9 ---
corr9 = df['Deathrate'].corr(df['GDP ($ per capita)'])
print("9️⃣ Гипотеза: чем выше смертность, тем ниже ВВП.")
print(f"   Корреляция: {corr9:.2f}")
if corr9 < -0.5:
    print("   ✅ Подтверждается: в странах с высокой смертностью ниже ВВП.\n")
else:
    print("   ❌ Не подтверждается.\n")

# --- Гипотеза 10 ---
corr10 = df['Service'].corr(df['Literacy (%)'])
print("🔟 Гипотеза: чем выше доля сферы услуг, тем выше уровень грамотности.")
print(f"   Корреляция: {corr10:.2f}")
if corr10 > 0.5:
    print("   ✅ Подтверждается: развитая сфера услуг связана с образованным населением.\n")
else:
    print("   ❌ Не подтверждается.\n")

print("✅ Проверка 10 гипотез завершена.")
