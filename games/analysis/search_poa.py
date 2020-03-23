def set_poas(self):
    """ calculate price of anarchy and price of stability
    from all pure nash and social optimum

    Note:
        setter method for self.poa & self.pos

    Raises:
        ValueError: if self.welfare or self.pnes is None
    """
    if self.welfare is None:
        raise ValueError('must set value of self.welfare')

    if self.pnes is None:
        raise ValueError('must set value of self.pnes')

    pne_welfare = np.array([self.welfare[pne] for pne in self.pnes], dtype='float')
    price_ratios = list(pne_welfare/self.welfare[self.opt])
    self.poa, pos = min(price_ratios), max(price_ratios)

def set_opt(self):
    """ find action that maximizes welfare

    Note:
        setter method for self.opt

    Raises:
        ValueError: if self.welfare is None
    """
    if self.welfare is None:
        raise ValueError('must set value of self.welfare')

    self.opt = np.unravel_index(np.argmax(self.welfare), self.welfare.shape)

def player_cover(self, strategies):
    """ returns list of which players are covering the resource """
    return [[j for j in range(self.n) if i in strategies[j]] for i in range(self.r_m)]

def set_s_payoff(self):
    """ set social payoff matrix """
    self.set_dependency(['st_dict'])
    sp_dict = {}
    for k, v in self.st_dict.items():
        p_cover = self.player_cover(v)
        value = sum([self.w_r(i, p_cover[i]) for i in range(self.r_m)])
        sp_dict.update({k: value})
    self.s_payoff = np.array(dict_nlist(sp_dict))