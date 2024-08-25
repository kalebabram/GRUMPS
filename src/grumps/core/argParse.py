from argparse import ArgumentParser
from grumps.__about__ import __version__
from grumps.__about__ import __author__
from grumps.__about__ import __date__

def argParseFunc():
    description = """Genomic distance based Rapid Uncovering of Microbial Population\
               Structures. grumps reads a normalized distance matrix  and returns a \
               filtered result.   It can be run in 'summary', 'regular', \
               'strict', 'sigma', 'target', 'clique', and 'small' modes. \
               For more information please see the white \
               paper: https://doi.org/10.1101/2022.12.19.521123"""

    epilog = """grumps is designed to assist and speed up the construction \
               of species level population structures using Mash distances as \
               an input. ANI values can be used as well if the ANI values are \
               converted to a decimal difference value {i.e. (100 - ANIvalue)\
               /100}. Additional helper scripts are provided if you do not \
               have a correctly formated distance matrix to input."""
    usage = """grumps [-h] [-v] [-m MODE] [-c CUTOFF] [-s SIGMA] [-M MEDOID] \
    [-p HEATMAP] [-C CLUSTERMETHOD] [-f FIGFORMAT] [-t TARGETFP] \
    [-r REMOVEFP] filepath"""
                          
                      
    parser = ArgumentParser(description=description, epilog = epilog, usage = usage)
    parser.add_argument("-v", "--version", action="version", version="grumps\
                        v{} ({}) By: {}\
                        ".format(__version__, __date__, __author__))    
            
    parser.add_argument("filepath", metavar="filepath",
                        help="The filepath to a mash distance matrix \
                        with genome ID (any unique string can be used as \
                        a genome ID) as both column and index. \
                        ", type=str)
    parser.add_argument("-m", "--mode", dest="mode", metavar = "MODE",
                        help="Specify the mode GRUMPS runs in. \
                        Available modes are: 'summary', 'regular', 'strict', \
                        'sigma', 'clique', 'target', 'remover', and 'small'. \
                        Please refer to the white paper or GitHub for more \
                        information concerning the usage for each mode.\
                        [default: 'regular']", choices=['summary', 'regular', 
                        'strict','sigma', 'clique', 'target', 
                        'remover','small'] ,\
                        default='regular',type=str)
    parser.add_argument("-c", "--cutoff", dest="cutoff", metavar = 'CUTOFF',
                        help="The maximun distance threshold to \
                        which species membership will be determined. \
                        [default: 0.05]", default = 0.05, type=float)
    parser.add_argument("-s", "--sigma", dest="sigma", metavar = 'SIGMA',
                        help="Perform sigma cleaning step after 'regular' \
                        or 'strict' cleaning modes. [default: yes]\
                        ", choices = ['yes', 'no'], default = 'yes', type=str)
    parser.add_argument("-M", "--medoid", dest="medoid",metavar="MEDOID",
                        help="Genomes with a distance to the medoid that is \
                        higher than the specified cutoff are removed. \
                        [default: yes]", choices=['yes','no'], default='yes',
                        type=str)
    parser.add_argument("-p","--heatmap", dest="heatMap", metavar = 'HEATMAP',
                        help = "If heatmap\
                        should be made at the end of program. Valid only for \
                        'regular', 'strict', 'sigma', 'target', \
                        'remover', and 'small' modes. [default: 'yes']\
                        ", choices = ['yes', 'no'], default = 'yes', 
                        type = str)
    parser.add_argument("-C", "--clustermethod", dest = "clustermethod",
                        metavar = 'CLUSTERMETHOD',
                        help = "The type of method to use in \
                        scipy.cluster.hierarchy.linkage(). Options \
                        include: 'single', 'complete', 'average', 'weighted'\
                        , 'centroid', 'median', or 'ward'.\
                        [default: 'ward']", default = 'ward', \
                        choices = ['single', 'complete', 'average', 
                        'weighted''centroid', 'median','ward'], type=str)
    parser.add_argument("-f", "--figformat", dest="figformat", 
                        metavar = 'FIGFORMAT',
                        help="The format of any images generated by the \
                        script. Options are: 'png', 'svg', and 'pdf'. \
                        Note: 'svg' \
                        and 'pdf' modes are not recommended for heatmaps made \
                        with 'regular' or 'strict' modes. For publication \
                        quality heatmaps use the R script. [default: 'png']\
                        ", choices = ['png', 'svg', 'pdf'], 
                        default = 'png', type=str)
    parser.add_argument("-t", "--target", dest="targetFP",
                        help="If one or more genomes is required to be in the \
                         final dataset, you can specify the genome ID. This is \
                         a useful option where a species has significant \
                         contamination but a genome \
                         should be included in the cleaned species. The genome\
                          ID must be identical to the genome ID in the \
                          distance matrix.", type=str)
    parser.add_argument('-r', '--remove', dest='removeFP',
                        help="If one or more genomes to be removed from the \
                         final dataset, you can specify the genome ID(s). This \
                         is a useful option where a species has genomes \
                         that should not \
                         be included in the cleaned species. The genome\
                         ID(s) must be identical to the genome ID in the \
                         distance matrix.", type=str)
    args = parser.parse_args()
    if not hasattr(args, 'filepath'):
        parser.print_help()
        
    return args
    
