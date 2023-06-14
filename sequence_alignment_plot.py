from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from pygenomeviz import GenomeViz, Genbank
from pygenomeviz.align import AlignCoord, MMseqs
import argparse

#
#TODO: Add in command line arguments for the list of gbk files
#

parser = argparse.ArgumentParser(description="Create a comparative genomics plot for a number of input sequences.")
parser.add_argument('input',metavar="input",type=str,nargs='+', help="List of inputs in the form of GBK files")
parser.add_argument('--outdir', dest="output_dir", type=str,help="Name of output directory to be created")
parser.add_argument('--t',dest="threads",type=int,nargs="?",help="Amount of threads used by MMseqs for alignment")
parser.add_argument('--plot_width', dest='plot_width',type=int,nargs="?",help="Final size of output file, default 20")
parser.add_argument('--label_size',dest='label_size',type=int,nargs="?",help="Size of the annotation labels, default 10")
parser.add_argument('--colors',dest="colors", type=str,nargs='+',help="List of colors for plot in order: feature color, normal link, inverted link")

args = parser.parse_args()
color_list = args.colors

gv = GenomeViz(
    fig_width=args.plot_width,
    fig_track_height=0.5,
    feature_track_ratio=0.5,
    tick_track_ratio=0.5,
    align_type="center",
    tick_style="bar",
    tick_labelsize=args.label_size,
)

files_list = args.input

#Runs mmseq modules in GenomeViz and creates the link file
mmseqs = MMseqs(files_list, args.output_dir, 0, 1e-3, args.threads)
align_coords = mmseqs.run()
AlignCoord.write(align_coords, args.output_dir + "/aligned_coords.tsv")
links = AlignCoord.filter(align_coords, 0, 0)

#Runs through the GBK files and creates the feature track and adds in the features
for idx, gbk_file in enumerate(files_list):
    gbk = Genbank(gbk_file)
    track = gv.add_feature_track(gbk.name, gbk.range_size, labelsize=10)
    track.add_genbank_features(
        gbk,
        label_type="product" if idx == 0 else None,  # Labeling only top track
        label_handle_func=lambda s : "" if s.startswith("hypothetical") else s,  # Ignore 'hypothetical ~~~' label
        labelsize=8,
        labelvpos="top",
        facecolor=color_list[0],
        linewidth=0.5,
        labelrotation=45,
    )

normal_color, inverted_color, alpha = color_list[1], color_list[2], 0.5
min_identity = int(min(link.identity for link in links))

#Creates the link between all of the features from the links file output by mmseq module
for link in links:
    link_data1 = (link.ref_name, link.ref_start, link.ref_end)
    link_data2 = (link.query_name, link.query_start, link.query_end)
    gv.add_link(link_data1, link_data2, normal_color, inverted_color, alpha, v=link.identity, vmin=min_identity, curve=True)

fig = gv.plotfig()

# Add Legends (Maybe there is a better way)
handles = [
    Line2D([], [], marker=">", color=color_list[0], label="CDS", ms=10, ls="none"),
    Patch(color=normal_color, label="Normal Link"),
    Patch(color=inverted_color, label="Inverted Link"),
]
fig.legend(handles=handles, bbox_to_anchor=(1, 1))

# Set colorbar for link
gv.set_colorbar(fig, bar_colors=[normal_color, inverted_color], alpha=alpha, vmin=min_identity, bar_height=0.25, bar_label="Identity", bar_labelsize=10)

fig.savefig(args.output_dir + "/alignment_plot.png",dpi=300,pad_inches=1)