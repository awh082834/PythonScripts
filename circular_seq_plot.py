from pycirclize import Circos
from pycirclize.parser import Gff
from pycirclize.utils import load_prokaryote_example_file
import argparse

parser = argparse.ArgumentParser(description="Create Circularized Plot of Input Sequence")

parser.add_argument('input', metavar='input', type=str,help='Input file in the form of a GFF')
parser.add_argument('sample', metavar='sample', type=str, help='Name of the sample, will be used as the plot title')
parser.add_argument('output', metavar='output', type=str, help='Output filename')

args = parser.parse_args()


# Load GFF file
gff = Gff(args.input)

circos = Circos(sectors={gff.name: gff.range_size})
circos.text(args.sample, size=15)

sector = circos.sectors[0]
cds_track = sector.add_track((90, 100))
cds_track.axis(fc="#EEEEEE", ec="none")

# Plot forward CDS
cds_track.genomic_features(
    gff.extract_features("CDS", target_strand=1),
    plotstyle="arrow",
    r_lim=(95, 100),
    fc="salmon",
)

# Plot reverse CDS
cds_track.genomic_features(
    gff.extract_features("CDS", target_strand=-1),
    plotstyle="arrow",
    r_lim=(90, 95),
    fc="skyblue",
)
# Extract CDS product labels
pos_list, labels = [], []
for feat in gff.extract_features("CDS"):
    start, end = int(str(feat.location.end)), int(str(feat.location.start))
    pos = (start + end) / 2
    label = feat.qualifiers.get("product", [""])[0]
    if label == "" or label.startswith("hypothetical"):
        continue
    if len(label) > 20:
        label = label[:20] + "..."
    pos_list.append(pos)
    labels.append(label)

# Plot CDS product labels on outer position
cds_track.xticks(
    pos_list,
    labels,
    label_orientation="vertical",
    show_bottom_line=True,
    label_size=6,
    line_kws=dict(ec="grey"),
)
# Plot xticks & intervals on inner position
cds_track.xticks_by_interval(
    interval=5000,
    outer=False,
    show_bottom_line=True,
    label_formatter=lambda v: f"{v/ 1000:.1f} Kb",
    label_orientation="vertical",
    line_kws=dict(ec="grey"),
)

fig = circos.plotfig()
fig.savefig(args.output,dpi=300,pad_inches=0.5)