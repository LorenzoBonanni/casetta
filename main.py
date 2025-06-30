import numpy as np

hours = range(24)
external_temperature_profile = [15 + 5 * np.sin(np.pi * (h - 6) / 12) for h in hours]
import matplotlib.pyplot as plt

plt.plot(external_temperature_profile)
plt.title('External Temperature Profile')
plt.xlabel('Hour')
plt.ylabel('Temperature (°C)')
plt.show()
