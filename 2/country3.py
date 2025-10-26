import pandas as pd

# === 1. Загрузка и очистка данных ===
df = pd.read_csv("countries.csv")

# Удалим пробелы
df["Country"] = df["Country"].str.strip()
df["Region"] = df["Region"].str.strip()

# Преобразуем столбцы с запятыми в числовые
cols_to_fix = [
    'Pop. Density (per sq. mi.)', 'Coastline (coast/area ratio)', 'Net migration',
    'Infant mortality (per 1000 births)', 'Literacy (%)', 'Phones (per 1000)',
    'Arable (%)', 'Crops (%)', 'Other (%)', 'Climate', 'Birthrate', 'Deathrate',
    'Agriculture', 'Industry', 'Service'
]
for col in cols_to_fix:
    df[col] = df[col].astype(str).str.replace(',', '.')
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Заполняем пропуски медианами
df = df.fillna(df.median(numeric_only=True))

print("=== Проверка 15 гипотез через группировку и фильтрацию ===\n")

# === Гипотеза 1 ===
by_region = df.groupby('Region')['GDP ($ per capita)'].mean().sort_values(ascending=False)
print("1️⃣ Средний ВВП по регионам (Европа vs Африка):")
print(by_region[['WESTERN EUROPE', 'SUB-SAHARAN AFRICA']])
if by_region['WESTERN EUROPE'] > by_region['SUB-SAHARAN AFRICA']:
    print("✅ Европа богаче Африки по среднему ВВП.\n")
else:
    print("❌ Гипотеза не подтверждается.\n")

# === Гипотеза 2 ===
sea = df[df['Coastline (coast/area ratio)'] > 0]['GDP ($ per capita)'].mean()
no_sea = df[df['Coastline (coast/area ratio)'] == 0]['GDP ($ per capita)'].mean()
print("2️⃣ Выход к морю и ВВП:")
print(f"   Средний ВВП с выходом к морю: {sea:.0f}")
print(f"   Средний ВВП без выхода к морю: {no_sea:.0f}")
if sea > no_sea:
    print("✅ Подтверждается: страны с выходом к морю богаче.\n")
else:
    print("❌ Не подтверждается.\n")

# === Гипотеза 3 ===
climate_gdp = df.groupby('Climate')['GDP ($ per capita)'].mean()
print("3️⃣ Климат и ВВП:")
print(climate_gdp)
print("✅ Если у климата 3 (умеренный) средний ВВП выше, гипотеза подтверждается.\n")

# === Гипотеза 4 ===
lit_reg = df.groupby('Region')['Literacy (%)'].mean()
print("4️⃣ Уровень грамотности по регионам (Европа vs Африка):")
print(lit_reg[['WESTERN EUROPE', 'SUB-SAHARAN AFRICA']])
if lit_reg['WESTERN EUROPE'] > lit_reg['SUB-SAHARAN AFRICA']:
    print("✅ Европа образованнее Африки.\n")
else:
    print("❌ Не подтверждается.\n")

# === Гипотеза 5 ===
mortality = df.groupby('Region')['Infant mortality (per 1000 births)'].mean().sort_values(ascending=False)
print("5️⃣ Средняя младенческая смертность по регионам:")
print(mortality.head())
print("✅ Если Африка на первом месте — гипотеза подтверждается.\n")

# === Гипотеза 6 ===
high_industry = df[df['Industry'] > 0.3]['GDP ($ per capita)'].mean()
low_industry = df[df['Industry'] <= 0.3]['GDP ($ per capita)'].mean()
print("6️⃣ Влияние индустрии на ВВП:")
print(f"   ВВП при Industry > 0.3: {high_industry:.0f}")
print(f"   ВВП при Industry <= 0.3: {low_industry:.0f}")
if high_industry > low_industry:
    print("✅ Подтверждается: индустриальные страны богаче.\n")
else:
    print("❌ Не подтверждается.\n")

# === Гипотеза 7 ===
agro = df[df['Agriculture'] > 0.3]['Literacy (%)'].mean()
other = df[df['Agriculture'] <= 0.3]['Literacy (%)'].mean()
print("7️⃣ Агроэкономики и грамотность:")
print(f"   Средняя грамотность при Agriculture > 0.3: {agro:.1f}")
print(f"   Средняя грамотность при Agriculture <= 0.3: {other:.1f}")
if agro < other:
    print("✅ Подтверждается: аграрные страны менее грамотны.\n")
else:
    print("❌ Не подтверждается.\n")

# === Гипотеза 8 ===
high_phone = df[df['Phones (per 1000)'] > 300]['Literacy (%)'].mean()
low_phone = df[df['Phones (per 1000)'] <= 300]['Literacy (%)'].mean()
print("8️⃣ Телефонизация и грамотность:")
print(f"   Грамотность при >300 телефонов: {high_phone:.1f}")
print(f"   Грамотность при <=300 телефонов: {low_phone:.1f}")
if high_phone > low_phone:
    print("✅ Подтверждается: больше телефонов — выше грамотность.\n")
else:
    print("❌ Не подтверждается.\n")

# === Гипотеза 9 ===
high_birth = df[df['Birthrate'] > 25]['GDP ($ per capita)'].mean()
low_birth = df[df['Birthrate'] <= 25]['GDP ($ per capita)'].mean()
print("9️⃣ Рождаемость и ВВП:")
print(f"   ВВП при высокой рождаемости: {high_birth:.0f}")
print(f"   ВВП при низкой рождаемости: {low_birth:.0f}")
if high_birth < low_birth:
    print("✅ Подтверждается: высокая рождаемость характерна для бедных стран.\n")
else:
    print("❌ Не подтверждается.\n")

# === Гипотеза 10 ===
high_ind = df[df['Industry'] > 0.3]['Deathrate'].mean()
low_ind = df[df['Industry'] <= 0.3]['Deathrate'].mean()
print("🔟 Индустриализация и смертность:")
print(f"   Средняя смертность при Industry > 0.3: {high_ind:.2f}")
print(f"   Средняя смертность при Industry <= 0.3: {low_ind:.2f}")
if high_ind < low_ind:
    print("✅ Подтверждается: индустриальные страны имеют ниже смертность.\n")
else:
    print("❌ Не подтверждается.\n")

# === Гипотеза 11 ===
df['Density_group'] = pd.cut(df['Pop. Density (per sq. mi.)'],
                             bins=[0, 50, 200, 1000, 10000],
                             labels=['низкая','средняя','высокая','очень высокая'])
density_phone = df.groupby('Density_group')['Phones (per 1000)'].mean()
print("11️⃣ Плотность населения и телефонизация:")
print(density_phone)
print("✅ Если телефонизация растёт с плотностью — гипотеза подтверждается.\n")

# === Гипотеза 12 ===
urban = df[df['Pop. Density (per sq. mi.)'] > 200]['Agriculture'].mean()
rural = df[df['Pop. Density (per sq. mi.)'] <= 200]['Agriculture'].mean()
print("12️⃣ Урбанизация и сельское хозяйство:")
print(f"   Agriculture при плотности >200: {urban:.2f}")
print(f"   Agriculture при плотности <=200: {rural:.2f}")
if urban < rural:
    print("✅ Подтверждается: города меньше зависят от сельского хозяйства.\n")
else:
    print("❌ Не подтверждается.\n")

# === Гипотеза 13 ===
service_high = df[df['Service'] > 0.5]['GDP ($ per capita)'].mean()
service_low = df[df['Service'] <= 0.5]['GDP ($ per capita)'].mean()
print("13️⃣ Сфера услуг и ВВП:")
print(f"   ВВП при Service > 0.5: {service_high:.0f}")
print(f"   ВВП при Service <= 0.5: {service_low:.0f}")
if service_high > service_low:
    print("✅ Подтверждается: страны с развитой сферой услуг богаче.\n")
else:
    print("❌ Не подтверждается.\n")

# === Гипотеза 14 ===
positive = df[df['Net migration'] > 0]['GDP ($ per capita)'].mean()
negative = df[df['Net migration'] <= 0]['GDP ($ per capita)'].mean()
print("14️⃣ Миграция и ВВП:")
print(f"   ВВП при положительной миграции: {positive:.0f}")
print(f"   ВВП при отрицательной миграции: {negative:.0f}")
if positive > negative:
    print("✅ Подтверждается: страны, куда едут люди, богаче.\n")
else:
    print("❌ Не подтверждается.\n")

# === Гипотеза 15 ===
large = df[df['Area (sq. mi.)'] > df['Area (sq. mi.)'].median()]['GDP ($ per capita)'].mean()
small = df[df['Area (sq. mi.)'] <= df['Area (sq. mi.)'].median()]['GDP ($ per capita)'].mean()
print("15️⃣ Размер страны и ВВП:")
print(f"   ВВП у больших стран: {large:.0f}")
print(f"   ВВП у малых стран: {small:.0f}")
if large < small:
    print("✅ Подтверждается: большие страны не всегда богаче.\n")
else:
    print("❌ Не подтверждается.\n")

print("✅ Проверка всех 15 гипотез завершена.")
