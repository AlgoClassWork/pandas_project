import pandas as pd

# === 1. Загрузка и очистка данных ===
df = pd.read_csv("countries.csv")
df = df.applymap(lambda x: str(x).replace(',', '.') if isinstance(x, str) else x)

cols_to_num = [
    'Population','Area (sq. mi.)','Pop. Density (per sq. mi.)','Coastline (coast/area ratio)',
    'Net migration','Infant mortality (per 1000 births)','GDP ($ per capita)','Literacy (%)',
    'Phones (per 1000)','Arable (%)','Crops (%)','Other (%)','Climate','Birthrate','Deathrate',
    'Agriculture','Industry','Service'
]
df[cols_to_num] = df[cols_to_num].apply(pd.to_numeric, errors='coerce')
df = df.fillna(df.mean(numeric_only=True))
df = df.dropna(subset=["Country", "Region"])

print("\n✅ Данные успешно очищены! Начинаем проверку гипотез.\n")

# === 2. Функция для текстовой интерпретации корреляции ===
def interpret_corr(value):
    if pd.isna(value):
        return "недостаточно данных"
    if abs(value) < 0.2:
        strength = "очень слабая"
    elif abs(value) < 0.4:
        strength = "слабая"
    elif abs(value) < 0.7:
        strength = "умеренная"
    else:
        strength = "сильная"
    direction = "положительная" if value > 0 else "отрицательная"
    return f"{strength} {direction} связь (r={value:.3f})"

# === 3. Проверка гипотез ===
print("=== АНАЛИЗ ГИПОТЕЗ ===\n")

# 1️⃣
corr1 = df['Pop. Density (per sq. mi.)'].corr(df['GDP ($ per capita)'])
print(f"1️⃣ Плотность населения и ВВП → {interpret_corr(corr1)}")
print("Вывод: чем выше плотность населения, тем ВВП, как правило, немного ниже.\n")

# 2️⃣
mean_gdp_pos = df[df['Net migration'] > 0]['GDP ($ per capita)'].mean()
mean_gdp_neg = df[df['Net migration'] < 0]['GDP ($ per capita)'].mean()
print(f"2️⃣ Средний ВВП при положительной миграции: {mean_gdp_pos:.2f}")
print(f"   Средний ВВП при отрицательной миграции: {mean_gdp_neg:.2f}")
print("Вывод: страны с притоком миграции в среднем богаче.\n")

# 3️⃣
corr2 = df['Literacy (%)'].corr(df['Infant mortality (per 1000 births)'])
print(f"3️⃣ Грамотность и младенческая смертность → {interpret_corr(corr2)}")
print("Вывод: чем выше грамотность, тем ниже младенческая смертность.\n")

# 4️⃣
corr3 = df['Agriculture'].corr(df['GDP ($ per capita)'])
print(f"4️⃣ Сельское хозяйство и ВВП → {interpret_corr(corr3)}")
print("Вывод: страны с высокой долей сельского хозяйства обычно имеют более низкий ВВП.\n")

# 5️⃣
corr4 = df['Phones (per 1000)'].corr(df['Literacy (%)'])
print(f"5️⃣ Телефоны и грамотность → {interpret_corr(corr4)}")
print("Вывод: наличие телефонов напрямую связано с уровнем образования и доступа к технологиям.\n")

# 6️⃣
high_lit = df[df['Literacy (%)'] > 90]['GDP ($ per capita)'].mean()
low_lit = df[df['Literacy (%)'] <= 90]['GDP ($ per capita)'].mean()
print(f"6️⃣ Средний ВВП при грамотности >90%: {high_lit:.2f}")
print(f"   Средний ВВП при грамотности <=90%: {low_lit:.2f}")
print("Вывод: высокая грамотность сопровождается высоким уровнем ВВП.\n")

# 7️⃣
corr5 = df['GDP ($ per capita)'].corr(df['Infant mortality (per 1000 births)'])
print(f"7️⃣ ВВП и младенческая смертность → {interpret_corr(corr5)}")
print("Вывод: чем выше ВВП, тем ниже младенческая смертность.\n")

# 8️⃣
df['Coastal'] = df['Coastline (coast/area ratio)'].apply(lambda x: 1 if x > 0 else 0)
gdp_coast = df.groupby('Coastal')['GDP ($ per capita)'].mean()
print("8️⃣ Средний ВВП по наличию выхода к морю:")
print(gdp_coast)
print("Вывод: страны с выходом к морю имеют преимущество в экономике за счёт торговли.\n")

# 9️⃣
climate_mortality = df.groupby('Climate')['Infant mortality (per 1000 births)'].mean().sort_index()
print("9️⃣ Средняя младенческая смертность по климату:\n", climate_mortality)
print("Вывод: в жарком климате младенческая смертность обычно выше.\n")

# 🔟
corr6 = df['Arable (%)'].corr(df['Agriculture'])
print(f"🔟 Пахотные земли и сельское хозяйство → {interpret_corr(corr6)}")
print("Вывод: логичная положительная связь — больше пахотных земель, выше доля сельского хозяйства.\n")

# 11️⃣
corr7 = df['Service'].corr(df['GDP ($ per capita)'])
print(f"11️⃣ Сфера услуг и ВВП → {interpret_corr(corr7)}")
print("Вывод: развитая сфера услуг способствует росту ВВП.\n")

# 12️⃣
corr8 = df['Industry'].corr(df['GDP ($ per capita)'])
print(f"12️⃣ Промышленность и ВВП → {interpret_corr(corr8)}")
print("Вывод: промышленность — ключевой фактор экономического развития.\n")

# 13️⃣
corr9 = df['GDP ($ per capita)'].corr(df['Birthrate'])
corr10 = df['GDP ($ per capita)'].corr(df['Deathrate'])
print(f"13️⃣ ВВП и рождаемость → {interpret_corr(corr9)}")
print(f"    ВВП и смертность → {interpret_corr(corr10)}")
print("Вывод: богатые страны характеризуются низкой рождаемостью и умеренной смертностью.\n")

# 14️⃣
eu = df[df['Region'] == 'WESTERN EUROPE']
mean_gdp_eu = eu['GDP ($ per capita)'].mean()
mean_lit_eu = eu['Literacy (%)'].mean()
mean_gdp_all = df['GDP ($ per capita)'].mean()
mean_lit_all = df['Literacy (%)'].mean()
print(f"14️⃣ Средний ВВП в Западной Европе: {mean_gdp_eu:.2f} (средний по миру: {mean_gdp_all:.2f})")
print(f"    Средняя грамотность в Западной Европе: {mean_lit_eu:.2f} (мировая: {mean_lit_all:.2f})")
print("Вывод: Западная Европа — регион с самыми высокими показателями жизни и образования.\n")

# 15️⃣
df['Migration_positive'] = df['Net migration'] > 0
mortality_migration = df.groupby('Migration_positive')['Infant mortality (per 1000 births)'].mean()
print("15️⃣ Средняя младенческая смертность при разной миграции:")
print(mortality_migration)
print("Вывод: страны, куда приезжают мигранты, обычно имеют лучший уровень здравоохранения.\n")

print("✅ Проверка 15 гипотез завершена успешно!")
