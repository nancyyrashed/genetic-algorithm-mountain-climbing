import pandas as pd
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv("point_0.2_summary.csv")

# Set a common style
plt.style.use("ggplot")

# Plot Best Fitness
plt.figure(figsize=(10,6))
plt.plot(df["Generation"], df["BestFitness"], label="Best Fitness", color="blue")
plt.xlabel("Generation")
plt.ylabel("Best Fitness")
plt.title("Best Fitness over Generations")
plt.legend()
plt.tight_layout()
plt.savefig("plot_best_fitness.png")
plt.show()

# Plot Mean Fitness
plt.figure(figsize=(10,6))
plt.plot(df["Generation"], df["MeanFitness"], label="Mean Fitness", color="green")
plt.xlabel("Generation")
plt.ylabel("Mean Fitness")
plt.title("Mean Fitness over Generations")
plt.legend()
plt.tight_layout()
plt.savefig("plot_mean_fitness.png")
plt.show()

# Plot Mean Links
plt.figure(figsize=(10,6))
plt.plot(df["Generation"], df["MeanLinks"], label="Mean Links", color="purple")
plt.xlabel("Generation")
plt.ylabel("Mean Links")
plt.title("Mean Number of Links over Generations")
plt.legend()
plt.tight_layout()
plt.savefig("plot_mean_links.png")
plt.show()

# Plot Max Links
plt.figure(figsize=(10,6))
plt.plot(df["Generation"], df["MaxLinks"], label="Max Links", color="orange")
plt.xlabel("Generation")
plt.ylabel("Max Links")
plt.title("Maximum Number of Links over Generations")
plt.legend()
plt.tight_layout()
plt.savefig("plot_max_links.png")
plt.show()

print("Plots saved as PNGs: plot_best_fitness.png, plot_mean_fitness.png, etc.")
