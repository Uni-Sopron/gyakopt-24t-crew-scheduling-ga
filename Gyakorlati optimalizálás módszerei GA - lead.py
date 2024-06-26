import json
import random
import numpy as np
import matplotlib.pyplot as plt

# Fájlok beolvasása
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def read_required_nurses_per_shift(file_path):
    data = read_json_file(file_path)
    return data["variations"]

def read_days_off_requested(file_path):
    data = read_json_file(file_path)
    return [ {int(k): v for k, v in variation.items()} for variation in data["variations"] ]

def read_algorithm_parameters(file_path):
    return read_json_file(file_path)

# Útvonalak
required_nurses_file_path       = 'required_nurses_per_shift.json'
days_off_file_path              = 'days_off_requested.json'
parameters_file_path            = 'parameters.json'

# Paraméterek beolvasása
required_nurses_variations      = read_required_nurses_per_shift(required_nurses_file_path)
days_off_variations             = read_days_off_requested(days_off_file_path)
algorithm_params                = read_algorithm_parameters(parameters_file_path)

# Paraméterek átadása
num_nurses                      = algorithm_params['num_nurses']
population_size                 = algorithm_params['population_size']
num_generations                 = algorithm_params['num_generations']
mutation_rate                   = algorithm_params['mutation_rate']
crossover_rate                  = algorithm_params['crossover_rate']

def run_task(task_id, required_nurses_per_shift, days_off_requested):
    days = len(required_nurses_per_shift)
    shifts_per_day = len(required_nurses_per_shift[0])

    # Munkabeosztás létrehozása
    def create_individual():
        return [[random.sample(range(num_nurses), required_nurses_per_shift[day][shift])
                 for shift in range(shifts_per_day)]
                for day in range(days)]

    # Fitness függvény
    def fitness(individual):
        score = 0
        nurse_workdays = {nurse: 0 for nurse in range(num_nurses)}
        
        for day in range(days):
            for shift in range(shifts_per_day):
                # Elvárt létszám
                if len(set(individual[day][shift])) == required_nurses_per_shift[day][shift]:
                    score += 1
                else:
                    score -= 1
                
                # Szabadnap igények
                for nurse in individual[day][shift]:
                    nurse_workdays[nurse] += 1
                    if nurse in days_off_requested and day in days_off_requested[nurse]:
                        score -= 1
                    
        # Két egymást követő műszak ellenőrzése
        for day in range(days):
            for shift in range(shifts_per_day - 1):
                for nurse in individual[day][shift]:
                    if nurse in individual[day][shift + 1]:
                        score -= 1

        # Egymást követő napok/műszak ellenőrzése
        for day in range(days - 1):
            for shift in range(shifts_per_day):
                for nurse in individual[day][shift]:
                    if nurse in individual[day + 1][shift]:
                        score -= 1

        # Maximális munkanapok számának ellenőrzése
        for nurse, workdays in nurse_workdays.items():
            if workdays > days:
                score -= 1
        
        return score

    # Keresztmetszet
    def crossover(parent1, parent2):
        if random.random() > crossover_rate:
            return parent1.copy(), parent2.copy()
        point = random.randint(1, days - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
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
    max_fitness_value = days * shifts_per_day  # A maximális elérhető fitness érték

    # Genetikai algoritmus futtatása
    for generation in range(num_generations):
        # Populáció fitness értékeinek kiértékelése
        fitness_values = [fitness(ind) for ind in population]
        
        # Normalizáljuk a fitness értékeket
        min_fitness_value = min(fitness_values)
        if min_fitness_value < 0:
            fitness_values = [f - min_fitness_value + 1 for f in fitness_values]  # +1, hogy biztosan pozitív legyen minden érték

        # Legjobb és legrosszabb megoldás kiértékelése
        best_index = np.argmax(fitness_values)
        best_solution = population[best_index]
        best_fitness = fitness_values[best_index]
        min_fitness = min(fitness_values)

        # Tároljuk a legjobb és legrosszabb fitness értékeket a diahoz
        best_fitness_per_generation.append(best_fitness)
        min_fitness_per_generation.append(min_fitness)

        # Ellenőrzése annak, hogy elértük-e a maximális fitness értéket
        if best_fitness >= max_fitness_value and optimal_solution_generation is None:
            if generation >= 2:  # Csak akkor állítsuk be, ha legalább 3 generáció eltelt
                optimal_solution_generation = generation
            else:
                # Ha túl korán találtuk meg az optimális megoldást, próbáljuk megakadályozni az azonnali megállást
                best_fitness = max_fitness_value - 1  # Csökkentjük a fitness értéket az elvárt alá

        # Szelekció és új populáció létrehozása
        new_population = [population[best_index]]  # Legjobb egyed megtartása
        for _ in range(population_size // 2 - 1):
            if sum(fitness_values) == 0:
                parent1, parent2 = random.choices(population, k=2)
            else:
                parent1, parent2 = random.choices(population, weights=fitness_values, k=2)
            child1, child2 = crossover(parent1, parent2, days)
            new_population.extend([mutate(child1, required_nurses_per_shift), mutate(child2, required_nurses_per_shift)])

        # Biztosítani, hogy az új populáció mérete ne legyen nagyobb, mint a kezdeti populációé
        if len(new_population) < population_size:
            new_population.append(population[best_index])   # Legjobb egyed megtartása
        population = new_population[:population_size]       # Levág

    return best_solution, best_fitness_per_generation, min_fitness_per_generation, optimal_solution_generation, max_fitness_value

# Futtatás 
def run_single_task():
    required_nurses_per_shift = required_nurses_variations[0]
    days_off_requested = days_off_variations[0]

    best_solution, best_fitness_per_generation, min_fitness_per_generation, optimal_solution_generation, max_fitness_value = genetic_algorithm(required_nurses_per_shift, days_off_requested)

    # Legjobb megoldás kiírása
    if optimal_solution_generation is None:
        print("Nincs optimális megoldás.")
    else:
        print("\nLegjobb megoldás megtalálva:")
        for day in range(len(required_nurses_per_shift)):
            print(f'Nap {day + 1}:')
            for shift in range(len(required_nurses_per_shift[0])):
                print(f'  Műszak {shift + 1}: {best_solution[day][shift]}')

    # 2D Diagram készítése 
    fig, ax = plt.subplots(figsize=(12, 6))
    generations = np.arange(1, len(best_fitness_per_generation) + 1)
    best_fitness_values = np.array(best_fitness_per_generation)
    min_fitness_values = np.array(min_fitness_per_generation)

    ax.plot(generations, best_fitness_values, marker='o', linestyle='-', color='blue', label='Legjobb Fitness Érték')
    ax.plot(generations, min_fitness_values, marker='x', linestyle='--', color='orange', label='Minimális Fitness Érték')
    ax.axhline(y=max_fitness_value, color='red', linestyle='--', label='Maximális Fitness')
    ax.set_title('Legjobb és Minimális Fitness Értékek a Generációk Során')
    ax.set_xlabel('Generáció')
    ax.set_ylabel('Fitness Érték')
    ax.legend()

    # Kiemelés
    if optimal_solution_generation is not None and best_fitness_values[optimal_solution_generation] >= max_fitness_value:
        ax.scatter(optimal_solution_generation + 1, max_fitness_value, color='green', s=150, label='Optimális megoldás')
        ax.annotate('Optimális megoldás', 
                    xy=(optimal_solution_generation + 1, max_fitness_value), 
                    xytext=(optimal_solution_generation + 1, max_fitness_value + 1), 
                    arrowprops=dict(facecolor='green', shrink=0.05, width=2, headwidth=10, headlength=20),
                    fontsize=12, color='green')

    plt.grid(True)
    plt.show()

# Futtatás
run_single_task()