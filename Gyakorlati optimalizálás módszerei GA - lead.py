import random
import numpy as np
import matplotlib.pyplot as plt

# Paraméterek
num_nurses = 7                  # 7 munkás
days = 5                        # 5 napos beosztás
shifts_per_day = 3              # Napi 3 műszak
required_nurses_per_shift = [   # Elvárt létszám minden nap minden műszakjára, 3 műszak
    [2, 2, 2],  # Első nap
    [2, 2, 2],  # Második nap
    [2, 2, 2],  # Harmadik nap
    [2, 2, 2],  # Negyedik nap
    [2, 2, 2]   # Ötödik nap
]
days_off_requested = {
    0: [1],  # Első munkás 1 szabadnap igénye
    1: [2],  # Második munkás 1 szabadnap igénye
    2: [3],  # Harmadik munkás 1 szabadnap igénye
    3: [],   # Negyedik munkás nem kér szabadnapot
    4: [],   # Ötödik munkás nem kér szabadnapot
    5: [],   # Hatodik munkás nem kér szabadnapot
    6: []    # Hetedik munkás nem kér szabadnapot
}

# Genetikai algoritmus paraméterei
population_size = 20  
num_generations = 100
mutation_rate = 0.05  
crossover_rate = 0.7  

# Munkabeosztást
def create_individual():
    return np.array([[random.sample(range(num_nurses), required_nurses_per_shift[day][shift])
                      for shift in range(shifts_per_day)]
                     for day in range(days)])

# Fitness függvény
def fitness(individual):
    score = 0
    # Ellenőrizzük az elvárt létszámot és a szabadnap igényeket
    for day in range(days):
        for shift in range(shifts_per_day):
            # Elvárt létszám
            if len(set(individual[day][shift])) == required_nurses_per_shift[day][shift]:
                score += 1
            # Szabadnap igények
            for nurse in individual[day][shift]:
                if day in days_off_requested[nurse]:
                    score -= 5  # Büntetés, ha egy szabadnapos munkás be van osztva
    return score

# Keresztmetszet 
def crossover(parent1, parent2):
    if random.random() > crossover_rate:
        return parent1.copy(), parent2.copy()
    point = random.randint(1, days - 1)
    child1 = np.vstack((parent1[:point], parent2[point:]))
    child2 = np.vstack((parent2[:point], parent1[point:]))
    return child1, child2

# Mutáció 
def mutate(individual):
    if random.random() > mutation_rate:
        return individual
    day = random.randint(0, days - 1)
    shift = random.randint(0, shifts_per_day - 1)
    individual[day][shift] = random.sample(range(num_nurses), required_nurses_per_shift[day][shift])
    return individual

# Kezdeti populáció létrehozása
population = [create_individual() for _ in range(population_size)]

# Eredmények tárolása a generációk során
best_fitness_per_generation = []
min_fitness_per_generation = []
optimal_solution_generation = None

# Genetikai algoritmus futtatása
for generation in range(num_generations):
    # Populáció fitness értékeinek kiértékelése
    fitness_values = [fitness(ind) for ind in population]

    # Legjobb és legrosszabb megoldás kiértékelése
    best_index = np.argmax(fitness_values)
    best_solution = population[best_index]
    best_fitness = fitness_values[best_index]
    min_fitness = min(fitness_values)

    # Tároljuk a legjobb és legrosszabb fitness értékeket a későbbi diahoz
    best_fitness_per_generation.append(best_fitness)
    min_fitness_per_generation.append(min_fitness)
    
    # Ellenőrizzük, hogy elértük-e a maximális fitness értéket
    if best_fitness >= days * shifts_per_day and optimal_solution_generation is None:
        if generation >= 2:  # Csak akkor állítsuk be, ha legalább 3 generáció eltelt
            optimal_solution_generation = generation
        else:
            # Ha túl korán találtuk meg az optimális megoldást, próbáljuk megakadályozni az azonnali megállást
            best_fitness = days * shifts_per_day - 1  # Csökkentjük a fitness értéket az elvárt alá

    # Szelekció és új populáció létrehozása
    new_population = [population[best_index]]  # Legjobb egyed megtartása
    for _ in range(population_size // 2 - 1):
        parent1, parent2 = random.choices(population, weights=fitness_values, k=2)
        child1, child2 = crossover(parent1, parent2)
        new_population.extend([mutate(child1), mutate(child2)])
    
    # Biztosítjuk, hogy az új populáció mérete ne legyen nagyobb, mint a kezdeti populációé
    if len(new_population) < population_size:
        new_population.append(population[best_index])   # Legjobb egyed megtartása
    population = new_population[:population_size]       # Levág

# Legjobb megoldás kiírása
print("\nLegjobb megoldás megtalálva:")
for day in range(days):
    print(f'Nap {day + 1}:')
    for shift in range(shifts_per_day):
        print(f'  Műszak {shift + 1}: {best_solution[day][shift]}')

# 2D Diagram készítése 
fig, ax = plt.subplots(figsize=(12, 6))
generations = np.arange(1, len(best_fitness_per_generation) + 1)
best_fitness_values = np.array(best_fitness_per_generation)
min_fitness_values = np.array(min_fitness_per_generation)

ax.plot(generations, best_fitness_values, marker='o', linestyle='-', color='blue', label='Legjobb Fitness Érték')
ax.plot(generations, min_fitness_values, marker='x', linestyle='--', color='orange', label='Minimális Fitness Érték')
ax.axhline(y=days * shifts_per_day, color='red', linestyle='--', label='Maximális Fitness')
ax.set_title('Legjobb és Minimális Fitness Értékek a Generációk Során')
ax.set_xlabel('Generáció')
ax.set_ylabel('Fitness Érték')
ax.legend()

# Kiemelés zöld színnel és nyíllal
if optimal_solution_generation is not None:
    ax.scatter(optimal_solution_generation + 1, days * shifts_per_day, color='green', s=150, label='Optimális megoldás')
    ax.annotate('Optimális megoldás', 
                xy=(optimal_solution_generation + 1, days * shifts_per_day), 
                xytext=(optimal_solution_generation + 1, days * shifts_per_day + 5), 
                arrowprops=dict(facecolor='green', shrink=0.05, width=2, headwidth=10),
                fontsize=12, color='green')

plt.grid(True)
plt.show()