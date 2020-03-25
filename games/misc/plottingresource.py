def plot(self, game):
    """ matplotlib plot representation of the resource game """
    # Create figure and axes
    fig, ax = plt.subplots()
    pc = self.player_cover(strategies)
    colors = mcolors.cnames.keys()
    for i in range(self.r_m):
        width = 10
        height = len(pc[i])*10 + 4
        x, y = (15*i, 0)
        rect = patches.Rectangle((x, y), width, height, facecolor='none')
        for j in range(len(pc[i])):
            r = 4
            color = colors[pc[i][j]]
            circ = patches.Circle((x+5, 3 + r + (r+1)*2*j), r, color=color, ec=color)
            ax.add_patch(circ)
        ax.add_patch(rect)
    axwidth = 15*self.r_m + 5
    ax.set_xlim((-5, axwidth))
    ax.set_ylim((-5, max(10*self.n + 4, axwidth*.7)))
    plt.show()