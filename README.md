# Discrete Probability Distributions Lab

A simple Flask web application for an undergraduate AIML laboratory, with interactive Binomial, Poisson, and Geometric distribution modules.

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
- Poisson inputs (rate λ and event count k), with defaults 4 and 4
- Geometric inputs (success probability p and trial of first success k), with defaults 0.35 and 3
- Mean, variance, standard deviation, second moment, and skewness
- PMF and CDF calculators for Binomial, Poisson, and Geometric distributions
- Small probabilities use scientific notation, and near-one CDFs retain their small complementary tail in the display
- Download distribution results and PMF charts as named PDFs (`binomial.pdf`, `poisson.pdf`, or `geometric.pdf`)
- Dynamic PMF bar charts with probability tooltips and a dashed mean reference line
- Input validation and edge-case handling

## Notes
- No database is required.
- For `p = 0` or `p = 1`, the variance is zero and skewness is displayed as not defined.
- For Geometric, `p` must be greater than 0; at `p = 1` the first success is certain on the first trial and skewness is not defined.
- Poisson rate values are limited to 0 through 1000 so the distribution chart remains practical to render.
- Geometric trials count from 1; its success probability must be greater than 0 and at most 1.
- The Geometric chart shows at most 1,000 trials and aims to include all but 1e-6 of the distribution's probability mass.

## Experiment results

I followed the quality-control steps and used the batch counts shown in the lab image: `1, 0, 2, 1, 3, 0, 1, 2, 1, 0`. There were 10 batches with 20 products in each batch, so 200 products were inspected. I counted 11 defects altogether, giving an observed defect rate of **5.5%** and an average of **1.1 defects per batch**.

### Binomial: 20 products, defect probability 0.05

For `n = 20` and `p = 0.05`, the mean is **1 defect**, the variance is **0.95**, and the probability of exactly 2 defects is **0.1887** (about 18.87%).

| Defects in a batch | Binomial probability | Expected batches out of 10 | Observed batches |
|---:|---:|---:|---:|
| 0 | 0.3585 | 3.58 | 3 |
| 1 | 0.3774 | 3.77 | 4 |
| 2 | 0.1887 | 1.89 | 2 |
| 3 | 0.0596 | 0.60 | 1 |

When I changed the defect probability to `0.10`, the mean increased to **2 defects** and the variance to **1.8**. The chance of exactly 2 defects became **0.2852**. The probablity graph moved toward larger defect counts, becuase defects are more likely on each product.

### Poisson: 100 products, rate λ = 5

For 100 inspected products and a 5% defect rate, the expected number of defects is `100 × 0.05 = 5`, so I used `λ = 5`. The table compares that Poisson model with the matching Binomial model, `Binomial(100, 0.05)`.

| Defects | Binomial probability | Poisson probability |
|---:|---:|---:|
| 0 | 0.0059 | 0.0067 |
| 1 | 0.0312 | 0.0337 |
| 2 | 0.0812 | 0.0842 |
| 3 | 0.1396 | 0.1404 |
| 4 | 0.1781 | 0.1755 |
| 5 | 0.1800 | 0.1755 |

The probabilities are quite close, especially around 3 to 5 defects. The Binomial graph has its highest point around 5, while the Poisson graph is highest at 4 and 5. They are not exactly the same, but the Poisson model is a good approximation here.

### Geometric: first defect with p = 0.05

The Geometric model gives the chance that the first defect appears on a particular inspection attempt. For example, the probability is **0.0500** on attempt 1, **0.0475** on attempt 2, and **0.0407** on attempt 5. The chance of seeing a defect by attempt 5 is **0.2262** (22.62%); by attempt 20 it is **0.6415**. The average wait is **20 inspections**. The graph decreases as the attempt number grows, since fewer products remain with no defect found yet.

### Overall result and testing

In my 10 batches, the number of defects was mostly between 0 and 2, and the obeserved average of 1.1 was near the Binomial model's expected average of 1. The measured defect rate of 5.5% is a little above the assumed 5%, but this is only 200 products, so more batches should be checked before deciding if the process has a real quality problem. The graphs helped me see how a higher defect probability shifts the Binomial outcomes and how the Poisson model can estimate counts for a larger group.

I ran the automated tests: **23 passed**. I also checked the PDF export in the browser; it produced a valid PDF with the distribution name as the file name.

## web application screenshot

<img width="1919" height="950" alt="image" src="https://github.com/user-attachments/assets/68cc5c74-436e-47cc-a649-ede66862d9b5" />
<img width="1169" height="489" alt="image" src="https://github.com/user-attachments/assets/176f6bc2-d743-40b3-83c2-1d1d916ca4fe" />

![alt text](image.png)
![alt text](image-1.png)
