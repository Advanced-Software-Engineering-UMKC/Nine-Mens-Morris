# Nine-Mens-Morris

## Running the Project

**1. Create a Virtual Environment (Recommended but not necessary):**

A virtual environment isolates project dependencies from your system's Python environment, preventing conflicts.

**Steps:**

- **Open a terminal window.** I opened a terminal in my IDE
- **Navigate to the project directory.** 
- **Create a virtual environment named `venv`:**
```bash
   python -m venv venv
   ```

**2. Activate virtual Environment**
  - On windows
  ```bash
   venv/Scripts/activate
   ```
  - On Mac
  ```bash
   source venv/bin/activate
   ```
**3. Install dependencies**
  ```bash
   pip install -r requirements.txt
   ```
**4. Run the program**
  ```bash
   cd frontend
   python GameGUI.py
   ```