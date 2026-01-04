
# NOTE: the two csv files do not have all the same country names; of the 236 countries, 162 are common between files
# OUTPUT: one graph for each trait; graphs have dots which represent a country; dot coordinates are temp. and trait score

import csv
import matplotlib.pyplot as plt
import numpy as np

scores_csv_lines = list()           # ["country", agreeable_score, extraversion_score, openness_score, conscientiousness_score, neuroticism_score]
total_scores_per_country = dict()   # {"country": [total_agreeable, total_extraversion, total_openness, total_conscientiousness, total_neuroticism]}
total_temp_per_country = dict()     # {"country": total_temp}
score_entries_per_country = dict()  # {"country": count}
mean_scores_per_country = dict()    # {"country": [mean_agreeable, mean_extraversion, mean_openness, mean_conscientiousness, mean_neuroticism]}

mean_agreeableness = list()
mean_extraversion = list()
mean_openness = list()
mean_conscientiousness = list()
mean_neuroticism = list()
mean_temp = list()

def list_mean(a):
    return round(sum(a) / len(a), 4)

# read traits csv to list l1
with open('big_five_scores.csv', 'r', newline = '') as f:
    reader = csv.reader(f)
    next(reader)  # skip first line with titles
    for i, line in enumerate(reader):
        scores_csv_lines.append([line[1]] + [float(line[i]) for i in range(4, 9)])

# count total scores and no. of entries per country
for line in scores_csv_lines:
    country = line[0]
    if country in total_scores_per_country:
        score_entries_per_country[country] += 1
        current_scores = total_scores_per_country[country]
        scores_to_add = [line[i] for i in range(1, 6)]
        total_scores_per_country[country] = [x + y for x, y in zip(current_scores, scores_to_add)]
    else:
        score_entries_per_country[country] = 1
        total_scores_per_country[country] = [line[i] for i in range(1, 6)]

# calculate mean scores
for country, total_scores in total_scores_per_country.items():
    country_entries = score_entries_per_country[country]
    mean_scores_per_country[country] = [total_scores[i] / country_entries for i in range(5)]

# read temperature csv
with open('combined_temperature.csv', 'r', newline = '') as f:
    reader = csv.reader(f)
    next(reader)  # skip first line with titles
    for i, line in enumerate(reader):
        country = line[0]
        if country in total_temp_per_country:
            total_temp_per_country[country] += float(line[2])
        else:
            total_temp_per_country[country] = float(line[2])

# separate mean scores to lists for plotting
for country, total_temp in total_temp_per_country.items():
    if country not in mean_scores_per_country: continue
    mean_scores = mean_scores_per_country[country]
    mean_agreeableness.append(mean_scores[0])
    mean_extraversion.append(mean_scores[1])
    mean_openness.append(mean_scores[2])
    mean_conscientiousness.append(mean_scores[3])
    mean_neuroticism.append(mean_scores[4])
    mean_temp.append(total_temp_per_country[country] / 122)  # temp is taken from 1901 to 2022 (122 yrs)

print(f'\n{'TRAIT':<22} {'MEAN SCORE'}')
print(f'--------------------------------------------')
print(f'{'Neuroticism':<22} {list_mean(mean_neuroticism)}')
print(f'{'Extraversion':<22} {list_mean(mean_extraversion)}')
print(f'{'Agreeableness':<22} {list_mean(mean_agreeableness):<6}')
print(f'{'Conscientiousness':<22} {list_mean(mean_conscientiousness)}')
print(f'{'Openness':<22} {list_mean(mean_openness)}')

plt.title('Temperature to Psychological Trait Score\n(162 countries)')
plt.xlabel('Trait Score')
plt.ylabel('Mean Annual Temperature [°C]')
y = np.array(mean_temp)

x = np.array(mean_agreeableness)
plt.scatter(x, y, label = 'agreeableness')

x = np.array(mean_extraversion)
plt.scatter(x, y, label = 'extraversion')

x = np.array(mean_openness)
plt.scatter(x, y, label = 'openness')

x = np.array(mean_conscientiousness)
plt.scatter(x, y, label = 'conscientiousness')

x = np.array(mean_neuroticism)
plt.scatter(x, y, label = 'neuroticism')

plt.legend(loc = "upper center", ncol = 5)
plt.show()
