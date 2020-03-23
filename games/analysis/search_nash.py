def find_eq(payoffs):

    tolerance = 10**-8  # numerical tolerance for comparing floats
    # candidate pure nash equilibria
    cpnes = list(np.argwhere(payoffs[0] > np.amax(payoffs[0], 0) - tolerance))
    cpnes = [tuple(cpne) for cpne in cpnes]
    for i in range(1, self.N):
        pm = payoffs[i]
        for cpne in cpnes[:]:
            ind = cpne[:i] + (slice(None),) + cpne[i+1:]
            if pm[cpne] < np.max(pm[ind]) - tolerance:
                cpnes.pop(cpnes.index(cpne))
    return cpnes