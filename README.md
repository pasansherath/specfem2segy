# specfem2segy

specfem2segy.py is a Python3 code that can be used to SEGY format common shot gathers from ascii format seismograms output into the OUTPUT_FILES folder by SPECFEM2D. 

This code requires the following Python libraries to be already installed in your system.
    • Numpy
    • Pandas
    • Obspy
    • Matplotlib

For convenience, parameters required for generating the common shot gather in SEGY format can be parsed through the command line. 


usage: specfem2segy.py [-h] [--df data folder] --stype seismograph type
                       --scomp seismograph component
                       [--stbeg first station number] --stend last station
                       number --offbeg first station offset --offend last
                       station offset --offsp station offset spacing
                       [--resamp resample rate] [--plotpdf plot pdf?]
                       --outname segy file name

Create SEGY common shot gathers from ascii format SPECFEM2D synthetic
seismogram files. Channel number and offset are the only SEGY trace headers
assgined. Byte ordering is big endian.

optional arguments:
  -h, --help            show this help message and exit
  --df data folder      Folder where the output ascii seismograms from
                        SPECFEM2D are saved. Defaults to 'OUTPUT_FILES/'. Note
                        that you have to include the trailing '/' after the
                        name of the folder.
  --stype seismograph type
                        Seimograph type. 'd' for displacement, 'v' for
                        velocity.
  --scomp seismograph component
                        Seimograph component. 'Z' for vertical, 'X' for
                        radial.
  --stbeg first station number
                        Identification number for the first station in the
                        ascii seismogram files. Defaults to 1.
  --stend last station number
                        Identification number for the last station in the
                        ascii seismogram files. You can use a number less than
                        the number of seismogram files for smaller gathers
  --offbeg first station offset
                        Source-receiver offset (in km) for first station. Use
                        negative values for stations to the west of the
                        source.
  --offend last station offset
                        Source-receiver offset (in km) for last station. Use
                        positive values for stations to the west of the
                        source.
  --offsp station offset spacing
                        Spacing between adjacent stations (in km).
  --resamp resample rate
                        Resample rate for the output SEGY file. Defaults to
                        200 Hz.
  --plotpdf plot pdf?   Whether to plot a pdf file of the gather for checking.
                        Use True for plotting.
  --outname segy file name
                        Name for the output segy file. The same name will be
                        used for the output pdf file if --plotpdf True.
