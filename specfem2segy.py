import pandas as pd
import numpy as np
from obspy.core import Trace, Stream
import matplotlib.pyplot as plt
from obspy.core.utcdatetime import UTCDateTime
import argparse

def write_to_segy(filename, stream, INLINE, delta=0.005):
    """
    Function to write ObsPy streams into SEGY files.
    """
    from obspy.io.segy.segy import SEGYTraceHeader
    
    ##+++++ trace headers +++++##
    for i, trace in enumerate(stream):
        trace.data = trace.data.astype('float32')
        trace.stats.delta = delta
        if not hasattr(trace.stats, 'segy.trace_header'):
            trace.stats.segy = {}
            trace.stats.segy.trace_header = SEGYTraceHeader()
            trace.stats.segy.trace_header.trace_sequence_number_within_line = int(i + 1)
            trace.stats.segy.trace_header.source_reciever_offset = int(trace.stats.distance)
            trace.stats.segy.trace_header.distance_from_center_of_the_source_point_to_the_center_of_the_receiver_group = int(trace.stats.distance)

    ##+++++ write +++++##
    stream.write(filename, format="SEGY", data_encoding=1, byteorder='>')
    print ("{:s} file saved".format(filename))

def traces_2_stream(folder, st_file_prefix, st_numbers, st_file_suffix, resample_rate, offsets, plot_pdf, outfile):

    file_names = np.array([])
    df = pd.DataFrame()

    stream = Stream()
    
    for i, num in enumerate(st_numbers):
        # print ("Reading file {:d} out of {:d}".format(i, len(st_numbers)))
        offset = offsets[i]

        file_name = folder+st_file_prefix+"{:04d}".format(num)+st_file_suffix
        file_names = np.append(file_names, file_name)

        trace_data = pd.read_csv(filepath_or_buffer=file_name, header=None, sep=" ", names = np.array(["time", "velocity", "NA"]), skipinitialspace=True)
        trace_data = trace_data[trace_data.time > 0]
        times = trace_data['time'].to_numpy().astype('float64')
        datas = trace_data['velocity'].to_numpy().astype('float64')
        trace = Trace()
        trace.data = datas
        trace.stats.distance = offset*1000
        trace.stats.sampling_rate = 1/((times[-1]-times[0])/len(times))
        trace_copy = trace.resample(resample_rate)

        stream += trace_copy

    write_to_segy('{:s}.segy'.format(outfile), stream, INLINE=1, delta=trace_copy.stats.delta)
    
    if plot_pdf:
        fig = plt.figure()
        stream.plot(fig=fig, type='section', scale=1, recordstart=0, recoordlength=10, offset_min=np.min(offsets)*1000, offset_max=np.max(offsets)*1000, fillcolors=('black', 'white'), linewidth=1, time_down=True)
        plt.savefig("{:s}.pdf".format(outfile), dpi=600)
        print ("{:s}.pdf file saved".format(outfile))
        
def main():

    parser = argparse.ArgumentParser(
        description="""Create SEGY common shot gathers from ascii format SPECFEM2D synthetic seismogram files.\n
        Channel number and offset are the only SEGY trace headers assgined.\n
        Byte ordering is big endian.""")

    parser.add_argument('--df', metavar='data folder', default='OUTPUT_FILES/',
                        action='store', type=str, required=False,
                        help="Folder where the output ascii seismograms from SPECFEM2D are saved. Defaults to 'OUTPUT_FILES/'. \
                        Note that you have to include the trailing '/' after the name of the folder.")

    parser.add_argument('--stype', metavar='seismograph type',
                        action='store', type=str, required=True,
                        help="Seimograph type. 'd' for displacement, 'v' for velocity.")

    parser.add_argument('--scomp', metavar='seismograph component',
                        action='store', type=str, required=True,
                        help="Seimograph component. 'Z' for vertical, 'X' for radial.")

    parser.add_argument('--stbeg', metavar='first station number', default=1,
                        action='store', type=int, required=False,
                        help="Identification number for the first station in the ascii seismogram files. Defaults to 1.")

    parser.add_argument('--stend', metavar='last station number',
                        action='store', type=int, required=True,
                        help="Identification number for the last station in the ascii seismogram files. \
                        You can use a number less than the number of seismogram files for smaller gathers")
    
    parser.add_argument('--offbeg', metavar='first station offset',
                        action='store', type=float, required=True,
                        help="Source-receiver offset (in km) for first station. Use negative values for stations to the west of the source.")

    parser.add_argument('--offend', metavar='last station offset',
                        action='store', type=float, required=True,
                        help="Source-receiver offset (in km) for last station. Use positive values for stations to the west of the source.")
    
    parser.add_argument('--offsp', metavar='station offset spacing',
                        action='store', type=float, required=True,
                        help="Spacing between adjacent stations (in km).")

    parser.add_argument('--resamp', metavar='resample rate',  default=200,
                        action='store', type=float, required=False,
                        help="Resample rate for the output SEGY file. Defaults to 200 Hz.")                    
    
    parser.add_argument('--plotpdf', metavar='plot pdf?',  default=False,
                        action='store', type=bool, required=False,
                        help="Whether to plot a pdf file of the gather for checking. Use True for plotting.")  
    
    parser.add_argument('--outname', metavar='segy file name',
                        action='store', type=str, required=True,
                        help="Name for the output segy file. The same name will be used for the output pdf file if --plotpdf True.")  
    args = parser.parse_args()

    #Get file folder from argparser
    file_folder = args.df

    #Data file prefix
    st_file_prefix = 'AA.S'

    #Data file suffix. Get from argparser depending on seismograph component and type
    st_file_suffix = '.BX{:s}.sem{:s}'.format(args.scomp, args.stype)

    #Array of station numbers from argparser
    st_numbers = np.arange(args.stbeg, args.stend+1,1)

    #Array of station numbers from argparser
    offsets = np.arange(args.offbeg, args.offend+args.offsp, args.offsp)

    #Set new resample rate from argparser
    resample_rate = args.resamp

    #Whether to plot pdf or not. Get from argparser
    plot_pdf = args.plotpdf

    #File name for the output segy file. Get from parser
    outfile = args.outname
    if outfile.endswith(".segy"):
        outfile = outfile[:-5]
    elif outfile.endswith(".sgy"):
        outfile = outfile[:-4]
    else:
        outfile = outfile
    #Create stream and write segy file
    traces_2_stream(file_folder, st_file_prefix, st_numbers, st_file_suffix, resample_rate, offsets, plot_pdf, outfile)


if __name__ == "__main__":
    main()