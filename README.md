# Casetta Smart Building RL Environment

Welcome to the **Casetta** modular reinforcement learning environment, designed to simulate energy flows in a smart building. This architecture allows you to flexibly create, test, and extend building and energy system scenarios.

---

## 📦 Project Structure

```
casetta/
│
├── config/                            # Configuration files (e.g., scenarios, parameters)
│
├── modules/                           # All simulation modules and managers
│   ├── building/                      # Building-level assets
│   ├── core/                          # Abstract base classes and core interfaces
│   ├── electricity/                   # Electrical system components
│   ├── exchange/                      # Resource exchange managers
│   ├── thermal/                       # Thermal system components
│
├── utils/                             # Utilities and shared logic
│
├── casetta.py                         # Main Gym Environment class
├── main.py                            # Example runner or entry point
├── environment.yml                    # Conda environment setup
├── .gitignore
└── README.md
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

* **core/**
  Abstract base classes for all producers and consumers (energy, thermal, hot water) and exchange managers.

* **building/**
  Includes the `Building` class and HVAC control logic.

* **electricity/**
  Electrical components such as grid interface, batteries, and photovoltaic systems.

* **thermal/**
  Thermal infrastructure including hot water tanks, heat pumps, and thermal storage.

* **exchange/**
  Exchange managers to route energy, hot water, and thermal resources between modules.

* **utils/**
  Common utilities, dynamic module instantiation, and typed definitions.

---

## 🛠️ Adding a New Module

1. **Create** your module class in the relevant folder, inheriting from a base class in `core/`.
2. **Implement** required methods: `reset()`, `step()`, `get_state()`, and optionally `consume()` / `produce()`.
3. **Register** your module in `modules_factory.py`.
4. **Update** the `config.json` file as needed.

---

## 🤝 Contributing

- Please document all core classes and methods.
- Follow the organizational conventions shown above!
---

## License

MIT License – see `LICENSE` file for details.