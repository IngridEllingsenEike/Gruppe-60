# Importer nødvendige biblioteker
import pandas as pd  # Pandas for håndtering av data i tabellformat (CSV-filer)
import matplotlib.pyplot as plt  # Matplotlib for plotting av data
import numpy as np  # NumPy for numeriske operasjoner, bl.a. å håndtere manglende verdier

# Deloppgave d: Les inn data fra filene
# Les CSV-filer som inneholder temperatur- og trykkdata fra to kilder: en lokal værstasjon og MET-instituttet
df1 = pd.read_csv('temperatur_trykk_met_samme_rune_time_datasett.csv.txt', sep=';', encoding='utf-8')
df2 = pd.read_csv('Cleaned_Pressure_and_Temperature_Data.csv', sep=';', encoding='utf-8')

# Sjekk og splitt kolonnene manuelt om nødvendig
# Deloppgave e: Håndtering av datoer og tidspunkter som er i ulike formater
# Hvis det bare finnes én kolonne (dårlig formatert), splitt den på semikolon
if len(df1.columns) == 1:
    df1 = df1.iloc[:, 0].str.split(';', expand=True)
    df1.columns = ['Navn', 'Stasjon', 'Tid(norsk normaltid)', 'Lufttemperatur', 'Lufttrykk i havnivå']
if len(df2.columns) == 1:
    df2 = df2.iloc[:, 0].str.split(';', expand=True)
    df2.columns = ['Dato og tid', 'Tid siden start (sek)', 'Trykk - barometer (bar)', 'Trykk - absolutt trykk maaler (bar)', 'Temperatur (gr Celsius)']

#Rens dataene og konverter typer for df1 (den lokale værstasjonen)
df1['Lufttemperatur'] = df1['Lufttemperatur'].replace('', np.nan)  # Erstatt tomme strenger med NaN
df1['Lufttrykk i havnivå'] = df1['Lufttrykk i havnivå'].replace('', np.nan)  # Samme for trykk
# Konverterer tall med komma til punktum for å støtte float-konvertering
df1['Lufttemperatur'] = df1['Lufttemperatur'].str.replace(',', '.').astype(float)
df1['Lufttrykk i havnivå'] = df1['Lufttrykk i havnivå'].str.replace(',', '.').astype(float)
# Konverterer tid til datetime-format for enkel håndtering og plotting
df1['Tid(norsk normaltid)'] = pd.to_datetime(df1['Tid(norsk normaltid)'], format='%d.%m.%Y %H:%M')

# Rens dataene og konverter typer for df2 (MET data)
df2['Temperatur (gr Celsius)'] = df2['Temperatur (gr Celsius)'].replace('', np.nan)
df2['Trykk - barometer (bar)'] = df2['Trykk - barometer (bar)'].replace('', np.nan)
df2['Trykk - absolutt trykk maaler (bar)'] = df2['Trykk - absolutt trykk maaler (bar)'].replace('', np.nan)
df2['Temperatur (gr Celsius)'] = df2['Temperatur (gr Celsius)'].str.replace(',', '.').astype(float)
df2['Trykk - barometer (bar)'] = df2['Trykk - barometer (bar)'].str.replace(',', '.').astype(float)
df2['Trykk - absolutt trykk maaler (bar)'] = df2['Trykk - absolutt trykk maaler (bar)'].str.replace(',', '.').astype(float)
df2['Dato og tid'] = pd.to_datetime(df2['Dato og tid'], errors='coerce')

# Deloppgave i: Konverter trykk fra bar til hPa (hektopascal for riktig skala)
df2['Trykk - barometer (hPa)'] = df2['Trykk - barometer (bar)'] * 10
df2['Trykk - absolutt trykk maaler (hPa)'] = df2['Trykk - absolutt trykk maaler (bar)'] * 10

# Filtrer bort rader med ugyldige tidsverdier
df1.dropna(subset=['Tid(norsk normaltid)'], inplace=True)
df2.dropna(subset=['Dato og tid'], inplace=True)

# Deloppgave g: Interpoler manglende verdier for trykk - barometer (hPa)
df2['Trykk - barometer (hPa)'] = df2['Trykk - barometer (hPa)'].interpolate(method='linear')

# Sjekker hvor mange gyldige data vi har for hver kolonne
print("Antall gyldige datapunkter for hver kolonne i df1:")
print(df1.count())
print("\nAntall gyldige datapunkter for hver kolonne i df2:")
print(df2.count())

# Deloppgave f: Plott temperaturdata fra begge filene
plt.figure(figsize=(15, 12))

# Temperaturplot
plt.subplot(2, 1, 1)
plt.plot(df1['Tid(norsk normaltid)'], df1['Lufttemperatur'], label='Temperatur (Sola)', linestyle='-', color='orange')
plt.plot(df2['Dato og tid'], df2['Temperatur (gr Celsius)'], label='Temperatur MET', linestyle='--', color='blue')

# Deloppgave h: Beregn og plott temperaturfall for Sola
start_tidspunkt = pd.Timestamp('2021-06-11 17:31:00')
slutt_tidspunkt = pd.Timestamp('2021-06-12 03:05:00')
# Filtrer dataene for å vise temperaturfall
tempfall_df1 = df1[(df1['Tid(norsk normaltid)'] >= start_tidspunkt) & (df1['Tid(norsk normaltid)'] <= slutt_tidspunkt)]
tempfall_df2 = df2[(df2['Dato og tid'] >= start_tidspunkt) & (df2['Dato og tid'] <= slutt_tidspunkt)]
plt.plot(tempfall_df1['Tid(norsk normaltid)'], tempfall_df1['Lufttemperatur'], label='Temperaturfall (Sola)', color='red')
plt.plot(tempfall_df2['Dato og tid'], tempfall_df2['Temperatur (gr Celsius)'], label='Temperaturfall (MET)', color='purple')

plt.ylabel('Temperatur (°C)')
plt.xlabel('Tid')
plt.title('Temperaturdata fra begge stasjoner')
plt.legend()

# Deloppgave i: Plott trykkdata fra begge stasjonene
plt.subplot(2, 1, 2)
plt.plot(df1['Tid(norsk normaltid)'], df1['Lufttrykk i havnivå'], label='Lufttrykk i havnivå (Sola)', linestyle='--', color='green')
plt.plot(df2['Dato og tid'], df2['Trykk - barometer (hPa)'], label='Barometrisk trykk (MET)', linestyle='-', color='blue', linewidth=2)
plt.plot(df2['Dato og tid'], df2['Trykk - absolutt trykk maaler (hPa)'], label='Absolutt trykk (MET)', linestyle=':', color='orange')

# Juster y-aksen for trykk for bedre visualisering
plt.ylim(1000, 1022.5)

plt.ylabel('Trykk (hPa)')
plt.xlabel('Tid')
plt.title('Trykkdata fra begge stasjoner')
plt.legend()

plt.tight_layout()
plt.show()

# Ekstra debugging-plott: Kun Barometrisk trykk (MET)
plt.figure(figsize=(10, 6))
plt.plot(df2['Dato og tid'], df2['Trykk - barometer (hPa)'], label='Barometrisk trykk (MET)', linestyle='-', color='blue', linewidth=2)
plt.ylabel('Trykk (hPa)')
plt.xlabel('Tid')
plt.title('Barometrisk trykk (MET) - Debugging')
plt.legend()
plt.show()

# Kombinert plott for trykk for bedre synlighet
plt.figure(figsize=(15, 6))
plt.plot(df1['Tid(norsk normaltid)'], df1['Lufttrykk i havnivå'], label='Lufttrykk i havnivå (Sola)', linestyle='--', color='green')
plt.plot(df2['Dato og tid'], df2['Trykk - barometer (hPa)'], label='Barometrisk trykk (MET)', linestyle='-', color='blue', linewidth=3)
plt.plot(df2['Dato og tid'], df2['Trykk - absolutt trykk maaler (hPa)'], label='Absolutt trykk (MET)', linestyle=':', color='orange', linewidth=2)

plt.ylabel('Trykk (hPa)')
plt.xlabel('Tid')
plt.title('Kombinert Trykkdata - Bedre Synlighet')
plt.legend()
plt.show()
