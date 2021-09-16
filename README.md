# specfem2segy

specfem2segy.py is a Python3 code for generating SEGY format common shot gathers from ascii format seismograms output into the OUTPUT_FILES folder by SPECFEM2D. 

*Channel number and offset are the only SEGY trace headers assgined. Byte ordering is big endian.


This code requires the following Python libraries to be already installed in your system.

* Numpy
* Pandas
* Obspy
* Matplotlib

For convenience, parameters required for generating the common shot gather in SEGY format can be parsed through the command line. 

## Usage: 
<addr> python3 specfem2segy.py [arguments] 
    
## Arguments:
    
Argument | Required | Description
-------|------|------ 
-h, --help | | show help
--df | No |Folder where the output ascii seismograms from SPECFEM2D are saved. Defaults to 'OUTPUT_FILES/'. Note that you have to include the trailing '/' after the name of the folder.
--stype | Yes | Seimograph type. 'd' for displacement, 'v' for velocity.
--scomp | Yes | Seimograph component. 'Z' for vertical, 'X' for radial.
--stbeg | No  | Identification number for the first station in the ascii seismogram files. Defaults to 1.
--stend | Yes |Identification number for the last station in the ascii seismogram files. You can use a number less than the number of seismogram files for smaller gathers
--offbeg | Yes | Source-receiver offset (in km) for first station. Use negative values for stations to the west of the source.
--offend | Yes |Source-receiver offset (in km) for last station. Use positive values for stations to the west of the source.
--offsp | Yes | Spacing between adjacent stations (in km).
--resamp | No | Resample rate for the output SEGY file. Defaults to 200 Hz.
--plotpdf | No |Whether to plot a pdf file of the gather for checking. Use True for plotting. Defaults to False (pdf not plotted).
--outname | Yes | Name for the output segy file. The same name will be used for the output pdf file if --plotpdf True.
