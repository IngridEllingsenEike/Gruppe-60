import csv
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
# Initialiser lister for å lagre data fra den første filen
times = []
temps = []
pressures = []
# Les data fra 'temperatur_trykk_met_samme_rune_time_datasett.csv'
with open('/Users/ingridellingsen/Library/Mobile Documents/com~apple~CloudDocs/EKSAMNER /DAT120/Gruppeoppgave del 1/temperatur_trykk_met_samme_rune_time_datasett.csv.txt', mode='r') as file:
    reader = csv.reader(file, delimiter=';')
    header = next(reader)  # Hopp over header-linjen
    for row in reader:
        try:
            # Konverter tid til datetime-objekt
            time = datetime.strptime(row[2], '%d.%m.%Y %H:%M')
            # Konverter temperatur og trykk til flyttall
            temp = float(row[3].replace(',', '.'))
            pressure = float(row[4].replace(',', '.'))
            # Legg verdiene til i listene
            times.append(time)
            temps.append(temp)
            pressures.append(pressure)
        except ValueError:
            # Hopp over rader med feil data
            continue
# Initialiser lister for å lagre data fra den andre filen
times_1 = []
barometric_pressures = []
absolute_pressures = []
temps_1 = []
# Les data fra 'trykk_og_temperaturlogg_rune_time.csv'
with open('/Users/ingridellingsen/Library/Mobile Documents/com~apple~CloudDocs/EKSAMNER /DAT120/Gruppeoppgave del 1/trykk_og_temperaturlogg_rune_time.csv.txt', mode='r') as file:
    reader = csv.reader(file, delimiter=';')
    header = next(reader)  # Hopp over header-linjen
    for row in reader:
        # Prøv å lese og konvertere hver verdi; hvis ikke mulig, sett til None
        try:
            time = datetime.strptime(row[0], '%m.%d.%Y %H:%M') if row[0] else None
        except ValueError:
            time = None
        try:
            barometric_pressure = float(row[2].replace(',', '.')) * 10 if row[2] else None
        except ValueError:
            barometric_pressure = None
        try:
            absolute_pressure = float(row[3].replace(',', '.')) * 10 if row[3] else None
        except ValueError:
            absolute_pressure = None
        try:
            temp = float(row[4].replace(',', '.')) if row[4] else None
        except ValueError:
            temp = None
        # Legg verdiene til i listene
        times_1.append(time)
        barometric_pressures.append(barometric_pressure)
        absolute_pressures.append(absolute_pressure)
        temps_1.append(temp)
# Fyll inn manglende tidsverdier ved å anta 10 sekunders intervaller
for i in range(1, len(times_1)):
    if times_1[i] is None and times_1[i - 1] is not None:
        times_1[i] = times_1[i - 1] + timedelta(seconds=10)
# Fortsett å fylle inn eventuelle resterende manglende tidsverdier
for i in range(len(times_1)):
    if times_1[i] is None:
        times_1[i] = times_1[i - 1] + timedelta(seconds=10)
# Definer funksjon for å fylle inn manglende verdier ved bruk av glidende gjennomsnitt
def fill_missing_with_moving_average(values, n=5):
    filled_values = values[:]
    for i in range(len(values)):
        if values[i] is None:
            # Finn de n forrige og n neste verdiene som ikke er None
            prev_values = [values[j] for j in range(max(0, i - n), i) if values[j] is not None]
            next_values = [values[j] for j in range(i + 1, min(len(values), i + n + 1)) if values[j] is not None]
            combined_values = prev_values + next_values
            if combined_values:
                # Beregn gjennomsnittet av de gyldige naboverdiene
                filled_values[i] = sum(combined_values) / len(combined_values)
            else:
                # Hvis ingen gyldige naboer, sett verdien til NaN
                filled_values[i] = np.nan
    return filled_values
# Fyll inn manglende barometriske trykkverdier
barometric_pressures = fill_missing_with_moving_average(barometric_pressures)
# Filtrer ut data med None-verdier for tid og temperatur
filtered_data = [
    (t, bp, ap, temp) for t, bp, ap, temp in zip(times_1, barometric_pressures, absolute_pressures, temps_1)
    if t is not None and temp is not None
]
times_1_filtered, barometric_pressures_filtered, absolute_pressures_filtered, temps_1_filtered = zip(*filtered_data)
# Sorter dataene fra begge datasettene basert på tid
times, temps, pressures = zip(*sorted(zip(times, temps, pressures)))
times_1_filtered, barometric_pressures_filtered, absolute_pressures_filtered, temps_1_filtered = zip(
    *sorted(zip(times_1_filtered, barometric_pressures_filtered, absolute_pressures_filtered, temps_1_filtered))
)
# Definer funksjon for å beregne glidende gjennomsnitt
def moving_average(times, values, n):
    avg_times = []
    avg_values = []
    for i in range(n, len(values) - n):
        # Legg til det midterste tidspunktet i vinduet
        avg_times.append(times[i])
        # Beregn gjennomsnittet over vinduet
        window = values[i - n:i + n + 1]
        avg_values.append(sum(window) / len(window))
    return avg_times, avg_values
# Beregn glidende gjennomsnitt for temperatur med n=30
n = 30
avg_times, avg_temps = moving_average(times, temps, n)
# Beregn glidende gjennomsnitt for temperatur med 30 minutters intervaller (n=180)
n_30min = 180
avg_times_1, avg_temps_1 = moving_average(times_1_filtered, temps_1_filtered, n_30min)
# Lag en figur for temperatur fra begge filene med glidende gjennomsnitt
fig1, ax1 = plt.subplots(figsize=(10, 5))
# Plott rå temperaturdata
ax1.plot(times, temps, color='tab:red', linestyle='-', label='Temperatur (MET - time)')
ax1.plot(times_1_filtered, temps_1_filtered, color='tab:orange', linestyle='-', label='Temperatur')
ax1.set_xlabel('Tid')
ax1.set_ylabel('Temperatur (°C)', color='tab:red')
ax1.tick_params(axis='y', labelcolor='tab:red')
ax1.legend(loc='upper left')
# Plott glidende gjennomsnitt av temperatur
ax1.plot(avg_times_1, avg_temps_1, color='tab:blue', linestyle='-', linewidth=2, label='Gjennomsnitt Temperatur')
ax1.legend(loc='upper right')
plt.xticks(rotation=45)  # Roter x-akse etikettene for bedre lesbarhet
plt.grid(True)
plt.tight_layout()  # Juster layout for å unngå overlapping
# Lag en figur for trykk fra begge filene
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(times, pressures, color='tab:blue', linestyle='-', label='Absolutt Trykk MET')
ax2.plot(times_1_filtered, barometric_pressures_filtered, color='tab:cyan', linestyle='-', label='Barometrisk Trykk')
ax2.plot(times_1_filtered, absolute_pressures_filtered, color='tab:green', linestyle='-', label='Absolutt Trykk MET')
ax2.set_xlabel('Tid')
ax2.set_ylabel('Trykk (hPa)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
# Definer tidsintervallet for temperaturfallet
start_time = datetime(2021, 6, 11, 17, 31)
end_time = datetime(2021, 6, 12, 3, 5)
# Finn indekser for tidspunkter innenfor det spesifikke intervallet
interval_indices = [i for i, t in enumerate(times) if start_time <= t <= end_time]
interval_times = [times[i] for i in interval_indices]
interval_temps = [temps[i] for i in interval_indices]
# Lag en figur for temperaturfallet i den spesifikke tidsperioden
fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.plot(interval_times, interval_temps, color='tab:red', linestyle='-', label='Temperaturfall i Tidsperiode')
ax3.set_xlabel('Tid')
ax3.set_ylabel('Temperatur (°C)', color='tab:red')
ax3.tick_params(axis='y', labelcolor='tab:red')
plt.title('Temperaturfall fra 11. juni 2021 kl 17:31 til 12. juni 2021 kl 03:05')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
# Vis alle plottene
plt.show()

