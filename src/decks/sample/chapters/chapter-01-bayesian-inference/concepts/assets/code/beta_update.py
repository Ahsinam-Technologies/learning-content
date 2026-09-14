prior_alpha, prior_beta = 2, 2
successes, failures = 8, 3

posterior_alpha = prior_alpha + successes
posterior_beta = prior_beta + failures
posterior_mean = posterior_alpha / (posterior_alpha + posterior_beta)
decision = "review" if posterior_mean > 0.70 else "defer"
