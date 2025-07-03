# Casetta Smart Building RL Environment

Welcome to the **Casetta** modular reinforcement learning environment, designed to simulate energy flows in a smart building. This architecture allows you to flexibly create, test, and extend building and energy system scenarios.

---

## 📦 Project Structure

```
casetta/
│
├── config/                  # Configuration files (e.g., scenarios, parameters)
│   └── config.json
│
├── modules/                 # All simulation modules and managers
│   ├── building/            # Building-level assets
│   │   ├── building.py
│   │   └── hvac.py
│   ├── core/                # Abstract base classes and interfaces
│   │   ├── base_module.py
│   │   ├── energy_consumer.py
│   │   └── energy_producer.py
│   ├── electricity/         # Electrical system components
│   │   ├── electric_battery.py
│   │   ├── grid.py
│   │   └── photovoltaic.py
│   ├── exchange/            # Resource exchange managers
│   │   ├── energy_exchange_manager.py
│   │   └── thermal_exchange_manager.py
│   ├── thermal/             # Thermal system components
│   │   ├── domestic_hot_water_tank.py
│   │   ├── heat_pump.py
│   │   └── thermal_energy_storage.py
│   └── __init__.py
│
├── utils/                   # Utilities and shared logic
│   ├── common.py
│   ├── modules_factory.py
│   └── types.py
│
├── casetta.py               # Main Gym Environment class
├── main.py                  # Example runner or entry point
└── environment.yml          # Conda environment setup
```

---

## 🚀 Getting Started

### **Set up your environment**
1. Clone the repository:
   ```sh
   git clone https://github.com/your-org/casetta.git
   cd casetta
   ```
2. Install dependencies (using Conda/miniconda):
   ```sh
   conda env create -f environment.yml
   conda activate casetta
   ```
3. Run the environment:
   ```sh
   python main.py
   ```

---

## 🧩 Module Organization

- **core/**  
  Abstract interfaces for all modules (`BaseModule`, `EnergyConsumer`, `EnergyProducer`).

- **building/**  
  Building-level assets (e.g., `Building`, `HVAC` controllers).

- **electricity/**  
  Electrical system components: grid, battery storage, PV, etc.

- **thermal/**  
  Thermal system components: hot water tank, heat pump, thermal storage.

- **exchange/**  
  Managers for coordinating energy and thermal flows between modules.

- **utils/**  
  Helpers, module factory for instantiation, and typed dataclasses.

---

## 🛠️ Adding a New Module

1. **Create** your module class in the relevant folder, inheriting from the appropriate base in `core/`.
2. **Implement** required methods: `reset()`, `step()`, `get_state()`, and where needed, `consume()` or `produce()`.
3. **Register** your module in the `modules_factory.py`.
4. **Update** config files as necessary.

---

## 🤝 Contributing

- Please document all core classes and methods.
- Follow the organizational conventions shown above!
---

## License

MIT License – see `LICENSE` file for details.