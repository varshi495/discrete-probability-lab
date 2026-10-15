# Discrete Probability Distributions Lab

A simple Flask web application for an undergraduate AIML laboratory. The Binomial module is functional; Poisson and Geometric pages are placeholders for future development.

## Requirements
- Python 3.10 or newer
- Internet connection to load Chart.js from its CDN in the browser

## Run on Windows (PowerShell)
1. Extract the ZIP file.
2. Open PowerShell in the extracted `discrete-probability-lab` folder.
3. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

5. Start the application:

   ```powershell
   python app.py
   ```

6. Open http://127.0.0.1:5000 in your browser.

## Included
- Home page and navigation for Home, Binomial, Poisson, and Geometric
- Binomial inputs (n and p), with defaults 20 and 0.35
- Mean, variance, standard deviation, second moment, and skewness
- PMF and CDF calculators
- Dynamic PMF bar chart with probability tooltips and a dashed mean reference line
- Input validation and edge-case handling

## Notes
- No database is required.
- For `p = 0` or `p = 1`, the variance is zero and skewness is displayed as not defined.
- Poisson and Geometric modules are placeholders in this version.



<img width="1919" height="950" alt="image" src="https://github.com/user-attachments/assets/68cc5c74-436e-47cc-a649-ede66862d9b5" />
<img width="1169" height="489" alt="image" src="https://github.com/user-attachments/assets/176f6bc2-d743-40b3-83c2-1d1d916ca4fe" />





