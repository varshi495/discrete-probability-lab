from flask import Flask, render_template, request, jsonify
from distributions.binomial import binomial_stats, binomial_pmf, binomial_cdf

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/binomial")
def binomial():
    return render_template("binomial.html")

@app.get("/poisson")
def poisson():
    return render_template("placeholder.html", distribution="Poisson")

@app.get("/geometric")
def geometric():
    return render_template("placeholder.html", distribution="Geometric")

@app.post("/api/binomial")
def api_binomial():
    data = request.get_json(silent=True) or {}
    try:
        n_raw = data.get("n", 20)
        p_raw = data.get("p", 0.35)
        k_raw = data.get("k", 7)

        # Reject fractional trial counts instead of silently truncating them.
        n_float = float(n_raw)
        if not n_float.is_integer() or n_float < 1:
            raise ValueError("Number of trials n must be a positive integer.")
        n = int(n_float)

        p = float(p_raw)
        if not 0 <= p <= 1:
            raise ValueError("Probability p must be between 0 and 1.")

        k_float = float(k_raw)
        if not k_float.is_integer():
            raise ValueError("k must be an integer.")
        k = int(k_float)
        if not 0 <= k <= n:
            raise ValueError("k must be between 0 and n, inclusive.")

        stats = binomial_stats(n, p)
        return jsonify({
            "n": n,
            "p": p,
            "k": k,
            "stats": stats,
            "pmf": binomial_pmf(n, p, k),
            "cdf": binomial_cdf(n, p, k),
            "chart": [
                {"x": x, "probability": binomial_pmf(n, p, x)}
                for x in range(n + 1)
            ],
        })
    except (TypeError, ValueError, OverflowError) as exc:
        return jsonify({"error": str(exc) or "Please enter valid values."}), 400

if __name__ == "__main__":
    app.run(debug=True)
