import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import logging
import math
import numpy as np
import pandas as pd
import seaborn as sns
import scipy.cluster.hierarchy
from sklearn import manifold
import drep
from drep.d_analyze_dendy2 import plot_secondary_dendrograms_from_wd, _make_special_dendrogram, get_highest_self, circular_dendrogram
import pickle
import shutil
import radialtree as rt
import csv
from matplotlib import cm

# Replace 'your_path' with the actual paths to your data files
nbd_path = 'data_tables/Ndb.csv'
cdb_path = 'data_tables/updated_Cdb.csv'
wdb_path = 'data_tables/Wdb.csv'

Ndb = pd.read_csv(nbd_path)
Cdb = pd.read_csv(cdb_path)
Wdb = pd.read_csv(wdb_path)

## updated it to Create WorkDirectory
wd = drep.WorkDirectory.WorkDirectory('drep')
# Store dataframes in WorkDirectory
wd.store_db(Ndb, 'Ndb')
wd.store_db(Cdb, 'Cdb')
wd.store_db(Wdb, 'Wdb')

pickle_file_path = '/Users/michellehauer/Documents/Beinart_Lab_old_comp/Phage/drep_outputs/NEW_sequencesExtracted/2009_16/metagenome/species_from_all/exact_drep_output_files/metagenome_species_all/data/Clustering_files/secondary_linkage_cluster_0.pickle'

with open(pickle_file_path, 'rb') as file:
    # Load the linkage matrix (first value)
    linkage_matrix = pickle.load(file)

    # Load the db (second value)
    db = pickle.load(file)

    # Load the dictionary of arguments (third value)
    arguments = pickle.load(file)

target_dir = wd.location + '/data/Clustering_files/'
shutil.copy(pickle_file_path, target_dir)
wd.load_cached()

# Replace 'your_plot_dir' with the desired plot directory path
plot_dir = 'figures'

##################
# Define your custom colors for each label
custom_colors = {
    "Niu South": "#009999",
    "Abe": "#99ccff",
    "Tahi Moana": "#336699",
    "Tow Cam": "#d98cb3",
    "Kilo Moana": "#666699",
    "Tu'i Malila": "#e6ac00"
}

# Create a custom colormap with your defined colors
num_labels = len(custom_colors)
custom_cmap = cm.colors.ListedColormap([custom_colors[label] for label in custom_colors])


# Step 2: Read the data file
data_file = 'data_tables/updated_Cdb.csv'  # Replace with your file path
labels_metadata = {}
with open(data_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        labels_metadata[row['genome']] = row['Vent']

#####################


# Call the function to generate the dendrogram
g, Z2, names = plot_secondary_dendrograms_from_wd(wd, plot_dir)

# Initialize an empty list to store the indices
indices = []

# Iterate over elements in array1
for i, label1 in enumerate(Z2["ivl"]):
    # Iterate over elements in array2
    for j, label2 in enumerate(Cdb["genome"]):
        # Check if labels match
        if label1 == label2:
            # If labels match, append the index of label2 to indices
            indices.append(j)

# Assuming you have numleaf as the number of leaves
numleaf = len(Z2["leaves"])  # Example value, replace with your actual value







vent_sorted = Cdb.loc[indices,"Vent"]
df = vent_sorted.reset_index()


def lookup_data(label):
    return custom_colors.get(label, None)

# Apply the function to the DataFrame column to generate a new column with corresponding data
df['colorz'] = df["Vent"].apply(lookup_data)


#custom_cmap = cm.colors.ListedColormap([vent_sorted["colorz"] for label in vent_sorted])

# Assign the colors to the specific labels
# colors_dict = {label: custom_cmap([i % num_labels]) for i, label in enumerate(custom_colors.keys())}
#colors_dict = {"Vent Field":custom_cmap(df["vent"])}

#colors_dict = {}
#for index, row in df.iterrows():
#    try:
#        rgb_color = plt.cm.colors.to_rgb(row['colorz'])
#        colors_dict[row['index']] = rgb_color
#    except ValueError:
#        print(f"Invalid color name '{row['colorz']}' at index {index}. Skipping...")
color_dict = {}
for i in range(num_labels):
    rgb_color = custom_cmap(i / (num_labels - 1))  # Get RGB color from the colormap
    color_dict[i] = rgb_color

colcolors = {
    "Niu South": color_dict[0],
    "Abe": color_dict[1],
    "Tahi Moana": color_dict[2],
    "Tow Cam": color_dict[3],
    "Kilo Moana": color_dict[4],
    "Tu'i Malila": color_dict[5]
}

def lookup_data2(label):
    return colcolors.get(label, None)

df['crgb'] = df["Vent"].apply(lookup_data2)







# Repeat for species as well

spec = Cdb["Host"][indices]
species = spec.reset_index()

custom_colors2 = {
    "A. kojimai": "darksalmon",##336699",
    "A. strummeri": "peachpuff",#"#cc6666",
    "A. boucheti": "lightsteelblue",#"#ffb366",
    "I. nautilei": "#BC8F8F",#darkseagreen#"#669999",
    "B. septemdierum": "slategrey",#"#666699"
}
# Create a custom colormap with your defined colors
num_labels2 = len(custom_colors2)
custom_cmap2 = cm.colors.ListedColormap([custom_colors2[label] for label in custom_colors2])


def lookup_data3(label):
    return custom_colors2.get(label, None)
    
species['colorz'] = species["Host"].apply(lookup_data3)

color_dict_spec = {}
for i in range(num_labels2):
    rgb_color = custom_cmap2(i / (num_labels2 - 1))  # Get RGB color from the colormap
    color_dict_spec[i] = rgb_color

colcolors2 = {
    "A. kojimai": color_dict_spec[0],
    "A. strummeri": color_dict_spec[1],
    "A. boucheti": color_dict_spec[2],
    "I. nautilei": color_dict_spec[3],
    "B. septemdierum": color_dict_spec[4]
}

def lookup_data4(label):
    return colcolors2.get(label, None)

species['crgb'] = species["Host"].apply(lookup_data4)









# Repeat for CYCLE as well

cyc = Cdb["Infection"][indices]
cycle = cyc.reset_index()

custom_colors3 = {
    "lytic": "lemonchiffon", #lemonchiffon, lightsteelblue, powderblue
    "lytic_TS": "khaki", #khaki , slategrey, cadetblue
    "lysogenic": "sandybrown", #sandybrown  , mocassin, peachpuff
    "lysogenic_TS": "peru", #peru , sandybrown, darksalmon
}

# Create a custom colormap with your defined colors
num_labels3 = len(custom_colors3)
custom_cmap3 = cm.colors.ListedColormap([custom_colors3[label] for label in custom_colors3])


def lookup_data5(label):
    return custom_colors3.get(label, None)
    
cycle['colorz'] = cycle["Infection"].apply(lookup_data5)

color_dict_cyc = {}
for i in range(num_labels3):
    rgb_color = custom_cmap3(i / (num_labels3 - 1))  # Get RGB color from the colormap
    color_dict_cyc[i] = rgb_color

colcolors3 = {
    "lytic": color_dict_cyc[0],
    "lytic_TS": color_dict_cyc[1],
    "lysogenic": color_dict_cyc[2],
    "lysogenic_TS": color_dict_cyc[3],
}

def lookup_data6(label):
    return colcolors3.get(label, None)

cycle['crgb'] = cycle["Infection"].apply(lookup_data6)





# Repeat for CRISPR as well

cris = Cdb["CRISPR_match"][indices]
cris = cris.reset_index()

custom_colors4 = {
    "Yes": "powderblue", #lemonchiffon, lightsteelblue, powderblue
    "No": "cadetblue", #khaki , slategrey , cadetblue
}

# Create a custom colormap with your defined colors
num_labels4 = len(custom_colors4)
custom_cmap4 = cm.colors.ListedColormap([custom_colors4[label] for label in custom_colors4])


def lookup_data7(label):
    return custom_colors4.get(label, None)
    
cris['colorz'] = cris["CRISPR_match"].apply(lookup_data5)

color_dict_cris = {}
for i in range(num_labels4):
    rgb_color = custom_cmap4(i / (num_labels4 - 1))  # Get RGB color from the colormap
    color_dict_cris[i] = rgb_color

colcolors4 = {
    "Yes": color_dict_cris[0],
    "No": color_dict_cris[1],
}

def lookup_data8(label):
    return colcolors4.get(label, None)

cris['crgb'] = cris["CRISPR_match"].apply(lookup_data6)





Ve = Cdb["Vent"]
V = Ve.reset_index()
V['color'] = V["Vent"].apply(lookup_data)
V['crgb'] = V["Vent"].apply(lookup_data2)



Sp = Cdb["Host"]
S = Sp.reset_index()
S['color'] = S["Host"].apply(lookup_data3)
S['crgb'] = S["Host"].apply(lookup_data4)



Cy = Cdb["Infection"]
C = Cy.reset_index()
C['color'] = C["Infection"].apply(lookup_data5)
C['crgb'] = C["Infection"].apply(lookup_data6)
         
                        
Cri = Cdb["CRISPR_match"]
Cr = Cri.reset_index()
Cr['color'] = Cr["CRISPR_match"].apply(lookup_data7)
Cr['crgb'] = Cr["CRISPR_match"].apply(lookup_data8)
                                 


#colors_legends = {"Vent Field": {"colors": colors, "labels": labels}}
# Initialize an empty list to store the indices
indices = []

# Iterate over elements in array1
for i, label1 in enumerate(names):
    # Iterate over elements in array2
    for j, label2 in enumerate(Cdb["genome"]):
        # Check if labels match
        if label1 == label2:
            # If labels match, append the index of label2 to indices
            indices.append(j)



#S_col = S.loc[indices,"crgb"]
S_col = S["crgb"][indices]
S_color = S_col.reset_index()
#S_color['crgb'] = S["Host"].apply(lookup_data4)

V_col = V["crgb"][indices]
V_color = V_col.reset_index()


C_col = C["crgb"][indices]
C_color = C_col.reset_index()

Cris_col = Cr["crgb"][indices]
Cris_color = Cris_col.reset_index()

#V_color['crgb'] = V_color['crgb'][::-1]


colors_dict = {"CRISPR_match": Cris_color["crgb"], "Infection": C_color["crgb"], "Vent Field": V_color["crgb"], "Species": S_color["crgb"]}

#Johann

#Z2["ivl"] = []

    # Initialize a .pdf
if plot_dir != False:
    pp = PdfPages(plot_dir + '4COL.pdf')
    save = True
else:
    save = False
plt.figure(figsize=(5,5))
rt.plot2(Z2, colorlabels=colors_dict)

# Create the circular dendrogram
#fig, ax = circular_dendrogram(linkage_matrix, plot_dir)
        # Save the file
fig = plt.gcf()

if save == True:
    pp.savefig(fig, bbox_inches='tight')
plt.show()
plt.close(fig)

pp.close()
plt.close('all')
