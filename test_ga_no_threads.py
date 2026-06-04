# In test_ga_no_threads.py
import population
import simulation 
import genome 
import creature 
import numpy as np
import pybullet as p
import os
import csv

# Create a folder for elite CSV files if it doesn't exist
elite_folder = "g100_pop20"
os.makedirs(elite_folder, exist_ok=True)

# Create a summary CSV file for all generations
summary_filename = os.path.join(elite_folder, "g100_pop20_summary.csv")
with open(summary_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["generation", "best_fitness", "mean_fitness", "mean_links", "max_links", "dist_to_center"])

pop = population.Population(pop_size=20, gene_count=3)
sim = simulation.Simulation()

all_generation_stats = []

for iteration in range(100):
    for cr in pop.creatures:
        cr.clear_position_data()  # Reset position history for consistency calculation
        try:
            sim.run_creature(cr, 2400)
        except (RuntimeError, p.error) as e:
            print(f"Simulation failed: {e}")
            cr.crash_fitness = -1e6
        
    # Calculate score_for_fitness for each creature
    fits = []
    for cr in pop.creatures:
        if hasattr(cr, 'crash_fitness'):
            fits.append(cr.crash_fitness)
        else:
            fits.append(cr.attain_fitness_score())

    for cr in pop.creatures:
        if hasattr(cr, 'crash_fitness'):
            del cr.crash_fitness

    #min_fit = np.min(fits)
    #if min_fit <= 0:
       # fits = [f + abs(min_fit) + 1 for f in fits]

    # Replace with clipping negative fitness to zero:
    fits = [max(0, f) for f in fits]

    fit_map = population.Population.get_fitness_map(fits)

    links = [len(cr.get_expanded_links()) for cr in pop.creatures]
    dist = [cr.attain_current_proximity_to_origin() for cr in pop.creatures if cr.locations]  # No need to pass position
    print(iteration, "fittest:", np.round(np.max(fits), 3),
          "mean:", np.round(np.mean(fits), 3), "mean links", np.round(np.mean(links)),
          "max links", np.round(np.max(links)), "dist to centre", np.round(np.min(dist), 3))

    # new stats accumulation:
    with open(summary_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            iteration,
            np.round(np.max(fits), 3),
            np.round(np.mean(fits), 3),
            np.round(np.mean(links), 3),
            np.round(np.max(links), 3),
            np.round(np.min(dist), 3)
        ])

    # Create score_for_fitness map for parent selection
    fit_map = population.Population.get_fitness_map(fits)
    new_creatures = []
    for i in range(len(pop.creatures)):
        p1_ind = population.Population.select_parent(fit_map)
        p2_ind = population.Population.select_parent(fit_map)
        p1 = pop.creatures[p1_ind]
        p2 = pop.creatures[p2_ind]
        # now we have the parents!
        dna = genome.Genome.crossover(p1.dna, p2.dna)
        dna = genome.Genome.point_mutate(dna, rate=0.1, amount=0.25)
        dna = genome.Genome.shrink_mutate(dna, rate=0.25)
        dna = genome.Genome.grow_mutate(dna, rate=0.1)
        cr = creature.Creature(1)
        cr.update_dna(dna)
        new_creatures.append(cr)

    # Elitism: Keep the best creature from the previous generation
    max_fit = np.max(fits)
    elite_indices = [i for i, f in enumerate(fits) if f == max_fit]

    if elite_indices:
        elite_index = elite_indices[0]
        elite_cr = pop.creatures[elite_index]
        new_cr = creature.Creature(1)
        new_cr.update_dna(elite_cr.dna)
        new_creatures[0] = new_cr
        filename = os.path.join(elite_folder, f"elite_pop20_g{iteration}.csv")
        
        genome.Genome.to_csv(elite_cr.dna, filename)
        print(f"Saved elite of generation {iteration} with fitness {max_fit} to {filename}")
    else:
        print(f"Warning: No elite found for generation {iteration} (this should not happen!)")


    
    pop.creatures = new_creatures
