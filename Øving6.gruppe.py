import pandas as pd
import matplotlib.pyplot as plt

# Deloppgave d: Les inn data fra de to filene
df1 = pd.read_csv('temperatur_trykk_met_samme_rune_time_datasett.csv.txt', sep=';', encoding='utf-8')
df2 = pd.read_csv('trykk_og_temperaturlogg_rune_time.csv.txt', sep=';', encoding='utf-8')

# Deloppgave e: Rens dataene og konverter dem til riktig format
df1['Lufttemperatur'] = df1['Lufttemperatur'].replace('', pd.NA).str.replace(',', '.').astype(float)
df1['Lufttrykk i havnivå'] = df1['Lufttrykk i havnivå'].replace('', pd.NA).str.replace(',', '.').astype(float)
df1['Tid(norsk normaltid)'] = pd.to_datetime(df1['Tid(norsk normaltid)'], format='%d.%m.%Y %H:%M')

df2['Temperatur (gr Celsius)'] = df2['Temperatur (gr Celsius)'].replace('', pd.NA).str.replace(',', '.').astype(float)
df2['Trykk - barometer (bar)'] = df2['Trykk - barometer (bar)'].replace('', pd.NA).str.replace(',', '.').astype(float)
df2['Dato og tid'] = pd.to_datetime(df2['Dato og tid'], errors='coerce')

# Deloppgave f: Plotting av temperatur fra begge stasjoner
fig, ax1 = plt.subplots(1, 1, figsize=(12, 6))

# Temperatur for begge stasjoner
ax1.plot(df1['Tid(norsk normaltid)'], df1['Lufttemperatur'], label='Temperatur Sola', color='orange')
ax1.plot(df2['Dato og tid'], df2['Temperatur (gr Celsius)'], label='Temperatur MET', color='blue')

# Deloppgave g: Beregne glidende gjennomsnitt for temperaturen
df1['Gjennomsnittstemperatur'] = df1['Lufttemperatur'].rolling(window=30, min_periods=1).mean()
# Legg til gjennomsnittstemperatur i plottet
ax1.plot(df1['Tid(norsk normaltid)'], df1['Gjennomsnittstemperatur'], label='Gjennomsnittstemperatur', linestyle='--', color='green')

# Deloppgave h: Temperaturfall fra 11. juni 17:31 til 12. juni 03:05
start_tid = pd.Timestamp('2021-06-11 17:31:00')
slutt_tid = pd.Timestamp('2021-06-12 03:05:00')

df1_fall = df1[(df1['Tid(norsk normaltid)'] >= start_tid) & (df1['Tid(norsk normaltid)'] <= slutt_tid)]
# Plott temperaturfallet
ax1.plot(df1_fall['Tid(norsk normaltid)'], df1_fall['Lufttemperatur'], label='Temperaturfall 11.-12. juni', color='red', linestyle=':')

# Legge til temperaturfall mellom solnedgang og soloppgang
solnedgang_tid = pd.Timestamp('2021-06-11 23:30:00')
soloppgang_tid = pd.Timestamp('2021-06-12 04:00:00')

df1_solnedgang_soloppgang = df1[(df1['Tid(norsk normaltid)'] >= solnedgang_tid) & (df1['Tid(norsk normaltid)'] <= soloppgang_tid)]
# Plott temperaturfall mellom solnedgang og soloppgang
ax1.plot(df1_solnedgang_soloppgang['Tid(norsk normaltid)'], df1_solnedgang_soloppgang['Lufttemperatur'], label='Temperaturfall solnedgang til soloppgang', color='purple', linestyle='-.')

# Deloppgave i: Plotting av trykkdata fra begge stasjoner (for fullstendighet, trykket er ikke fokus her)
df2['Trykk - barometer (hPa)'] = df2['Trykk - barometer (bar)'] * 1000

# Plotting av trykk
fig, ax2 = plt.subplots(1, 1, figsize=(12, 6))
ax2.plot(df1['Tid(norsk normaltid)'], df1['Lufttrykk i havnivå'], label='Barometrisk trykk (Sola)', color='green')
ax2.plot(df2['Dato og tid'], df2['Trykk - barometer (hPa)'], label='Barometrisk trykk (MET)', color='blue')

# Legg til etiketter og tittel
ax1.set_title('Temperaturdata fra begge stasjoner med temperaturfall')
ax1.set_ylabel('Temperatur (°C)')
ax1.legend()

ax2.set_title('Trykkdata fra begge stasjoner')
ax2.set_ylabel('Trykk (hPa)')
ax2.legend()

# Vise plottet
plt.tight_layout()
plt.show()
