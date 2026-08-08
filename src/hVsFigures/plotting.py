import matplotlib.pyplot as plt
from chainconsumer import Truth, Chain
from chainconsumer.plotting import plot_contour, plot_truths
from chainconsumer.plotter import get_artists_from_chains
from chainconsumer.color_finder import colors
from hVsFigures.config import dpi, r, alpha_list, sigmas, dpi

def chain_plot_with_label(ax, chain_list, loc='lower left'):
    for i in range(len(chain_list)):
        truth = Truth(location={"$T_0$ [K]": 10090.90909091, "γ": 1.57636364}, line_width= 0.9, line_style= ':', alpha=0.2)
        plot_truths(ax, [truth], px="$T_0$ [K]", py="γ")
        plot_contour(ax, chain_list[i], px="$T_0$ [K]", py="γ")
    artists = get_artists_from_chains(chain_list)
    leg = ax.legend(handles=artists, loc=loc)
    for text, chain in zip(leg.get_texts(), chain_list):
        text.set_color(colors.format(chain.color))

def plot_posterior(chains, chain_info, color_list, alpha_list=alpha_list, sigmas=sigmas):
    chains_ALL = [
    Chain(
        samples=chains[key],
        name=name,
        color=color_list[i],
        shade_alpha=alpha_list[i],
        sigmas=sigmas,
    )
    for i, (key, name) in enumerate(chain_info)
]

    fig, axes = plt.subplots(dpi=dpi, figsize=(7*r,5*r), sharex=True, sharey=True)
    fig.subplots_adjust(wspace=0.02, hspace=0.02)

    fontsize = 12
    chain_plot_with_label(axes, chains_ALL, loc='upper right')
    axes.set_xlabel('$T_0$ [K]', fontsize=fontsize)
    axes.set_ylabel('γ', fontsize=fontsize)
    axes.set_ylim(1.49, 1.66)
    axes.set_xlim(7200, 14300)
    return fig, axes