from Learning.prog.finance.pricing.simulated import vasicek_irb


def calc_error(params, loan_data):
    a, b, sigma = params
    default_probs = []
    for index, row in loan_data.iterrows():
        r = row["Interest Rate"]
        t = row["Loan Term"]
        r_sim = vasicek_irb(r, a, b, sigma, t)
        default_prob = np.mean(r_sim[-1] < r)
        default_probs.append(default_prob)
    error = np.mean((default_probs - loan_data["Default Rate"])**2)
    return error