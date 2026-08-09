import matplotlib.pyplot as plt
from chainconsumer import Truth, Chain
from chainconsumer.plotting import plot_contour, plot_truths
from chainconsumer.plotter import get_artists_from_chains
from chainconsumer.color_finder import colors
from hVmFigures.config import dpi, r, alpha_list, sigmas, dpi, fontsize
import numpy as np

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

    chain_plot_with_label(axes, chains_ALL, loc='upper right')
    axes.set_xlabel('$T_0$ [K]', fontsize=fontsize)
    axes.set_ylabel('γ', fontsize=fontsize)
    axes.set_ylim(1.49, 1.66)
    axes.set_xlim(7200, 14300)
    return fig, axes

def plot_covariance(mock_joint_sv, labels, positions):
    cov=np.cov(mock_joint_sv.T)/10
    corr=np.einsum('ij,i,j->ij',cov,1/np.sqrt(np.diag(cov)),1/np.sqrt(np.diag(cov)))

    fig = plt.figure(dpi=dpi, figsize=(10*r,8*r))
    plt.imshow(corr, vmin=-1, vmax=1, cmap='RdBu_r', origin='lower')
    plt.xticks([]) 
    plt.yticks([]) 

    plt.xticks(positions, labels, fontsize=fontsize)
    plt.yticks(positions, labels, fontsize=fontsize)
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False, 
        left=False,        # ticks along the bottom edge are off
        top=False) 
    plt.tick_params(
        axis='y',         
        which='both',     
        bottom=False,    
        left=False, 
        top=False) 

    cbar = plt.colorbar()
    cbar.ax.tick_params(labelsize=fontsize)
    return fig 

def area(chain): # Contour area size \sqrt{|C|}
    chain = Chain(samples = chain, name = 'summary')
    return np.sqrt(np.linalg.det(chain.get_covariance().matrix))

def FoM(chain): # Figure of Merit (FoM)
    return 1/area(chain)

def plot_FoM_bar(chains, chain_info):
    FoM_list = [FoM(chains[key]) for key, name in chain_info]
    list_name = [f'{i+1}: {name}' for i, (key, name) in enumerate(chain_info)]
    cmap = plt.colormaps['plasma']
    colors = cmap(np.linspace(0,0.8, len(list_name))[::-1])

    nrows = 1
    ncols = 1
    r = 1
    fig = plt.figure(dpi=dpi, figsize=(5.5*r,4*r))
    gs = fig.add_gridspec(nrows, ncols)
    axes = gs.subplots()

    gap = 0.5
    x = np.arange(len(list_name)) * (1 + gap)
    x_label = np.arange(len(list_name)) + 1
    axes.bar(x, FoM_list/FoM(chains['sansa']), label=list_name,  color=colors, width=1, alpha=0.8)
    axes.legend(fontsize=fontsize-3)
    axes.set_ylabel('FoM($S$) / FoM(LyαNNA)', fontsize=fontsize)
    axes.set_xlabel('Ranking', fontsize=fontsize)
    axes.set_xticks(x, x_label)
    axes.grid(True, linestyle=':', alpha=0.5)
    axes.set_ylim(0,0.3)

    return fig, axes