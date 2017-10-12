"""
Example services that wrap GDAL tools.
"""
import logging
import os
import tempfile

from pywps import LiteralInput, LiteralOutput, UOM
from pywps.app import EO4AProcess
from pywps.app.Common import Metadata


__author__ = "Derek O'Callaghan"

logger = logging.getLogger('PYWPS')

class GdalInfo(EO4AProcess):
    """
    gdalinfo service
    
    Lists information about a raster dataset. See http://gdal.org/gdalinfo.html.
    """

    def __init__(self):
        inputs = [
            LiteralInput(
                'datasetname',
                'Input dataset path',
                data_type='string',
                abstract="""
                Full path to input dataset.
                """,
                min_occurs=1,
                max_occurs=1,
            ),
            LiteralInput(
                'json',
                'Display the output in json format',
                data_type='boolean',
                abstract="""
                Display the output in json format.
                """,
                min_occurs=0,
                max_occurs=1,
            ),
            LiteralInput(
                'mm',
                'Min/max values',
                data_type='boolean',
                abstract="""
                Force computation of the actual min/max values for each band in the dataset.
                """,
                min_occurs=0,
                max_occurs=1,
            ),
            LiteralInput(
                'stats',
                'Image statistics',
                data_type='boolean',
                abstract="""
                Read and display image statistics. Force computation if no statistics are stored in an image.
                """,
                min_occurs=0,
                max_occurs=1,
            ),
            LiteralInput(
                'approx_stats',
                'Image statistics',
                data_type='boolean',
                abstract="""
                Read and display image statistics. 
                Force computation if no statistics are stored in an image. 
                However, they may be computed based on overviews or a subset of all tiles. 
                Useful if you are in a hurry and don't want precise stats.
                """,
                min_occurs=0,
                max_occurs=1,
            ),
            LiteralInput(
                'hist',
                'Histograms',
                data_type='boolean',
                abstract="""
                Report histogram information for all bands. 
                """,
                min_occurs=0,
                max_occurs=1,
            ),
            LiteralInput(
                'nogcp',
                'No ground control points',
                data_type='boolean',
                abstract="""
                Suppress ground control points list printing. 
                It may be useful for datasets with huge amount of GCPs, such as L1B AVHRR or HDF4 MODIS which contain thousands of them. 
                """,
                min_occurs=0,
                max_occurs=1,
            ),
            LiteralInput(
                'nomd',
                'Suppress metadata printing',
                data_type='boolean',
                abstract="""
                Suppress metadata printing. Some datasets may contain a lot of metadata strings.
                """,
                min_occurs=0,
                max_occurs=1,
            ),
            LiteralInput(
                'norat',
                'Suppress printing of raster attribute table.',
                data_type='boolean',
                abstract="""
                Suppress printing of raster attribute table.
                """,
                min_occurs=0,
                max_occurs=1,
            ),
            LiteralInput(
                'noct',
                'Suppress printing of color table',
                data_type='boolean',
                abstract="""
                Suppress printing of color table.
                """,
                min_occurs=0,
                max_occurs=1,
            ),
            LiteralInput(
                'checksum',
                'Band checksums',
                data_type='boolean',
                abstract="""
                Force computation of the checksum for each band in the dataset.
                """,
                min_occurs=0,
                max_occurs=1,
            ),
            LiteralInput(
                'listmdd',
                'List all metadata domains available for the dataset',
                data_type='boolean',
                abstract="""
                List all metadata domains available for the dataset.
                """,
                min_occurs=0,
                max_occurs=1,
            ),
            LiteralInput(
                'mdd',
                'Report metadata for the specified domain',
                data_type='string',
                abstract="""
                Report metadata for the specified domain. Starting with GDAL 1.11, "all" can be used to report metadata in all domains.
                """,
                min_occurs=0,
                max_occurs=1,
            ),
            LiteralInput(
                'nofl',
                'Only display the first file of the file list',
                data_type='boolean',
                abstract="""
                Only display the first file of the file list.
                """,
                min_occurs=0,
                max_occurs=1,
            ),
            LiteralInput(
                'sd',
                'Subdatasets',
                data_type='string',
                abstract="""
                If the input dataset contains several subdatasets read and display a subdataset with specified number (starting from 1). 
                This is an alternative of giving the full subdataset name.
                """,
                min_occurs=0,
                max_occurs=1,
            ),
            LiteralInput(
                'proj4',
                "Report a PROJ.4 string corresponding to the file's coordinate system",
                data_type='boolean',
                abstract="""
                Report a PROJ.4 string corresponding to the file's coordinate system.
                """,
                min_occurs=0,
                max_occurs=1,
            ),
            LiteralInput(
                'oo',
                'Dataset open option (format specific) ',
                data_type='string',
                abstract="""
                Dataset open option (format specific).
                """,
                min_occurs=0,
                max_occurs=1,
            ),
        ]
        outputs = [
            LiteralOutput(
                'output',
                'gdalinfo output',
                data_type='string',
                abstract="""
                Will contain any output generated by gdalinfo.
                """,
            )
        ]

        super(GdalInfo, self).__init__(
            identifier='gdalinfo',
            abstract="""
            Lists information about a raster dataset. See <a href="http://gdal.org/gdalinfo.html" target="_blank">gdalinfo manual</a>.
            """,
            version='0.1',
            title="gdalinfo",
            metadata=[],
            profile='',
            inputs=inputs,
            outputs=outputs,
        )


    def get_command(self, request, response):
        """
        The service command that will be executed later. Do not do any processing here.
        
        Returns
        -------
        string
            The service command to be executed.
        """
        fd, self.temp_path = tempfile.mkstemp()
        os.close(fd)
        logger.info('Request inputs: %s', request.inputs)

        # Capture gdalinfo output in a temp file
        return 'gdalinfo %s %s %s > %s' % (self._boolean_params_str(request),
                                           self._optional_params_str(request),
                                           self._get_input(request, 'datasetname'),
                                           self.temp_path)


    def set_output(self, request, response):
        """Set the output from the WPS request."""
        output = ''
        with open(self.temp_path, 'rb') as tf:
            output += ''.join(tf.readlines()) 
        response.outputs['output'].data = output
        response.outputs['output'].uom = UOM('unity')
        
        # Remove the temp file
        os.remove(self.temp_path)
        
        
class GdalWarp(EO4AProcess):
    """
    gdalwarp service
    
    Image reprojection and warping utility. See http://gdal.org/gdalwarp.html.
    """

    def __init__(self):
        inputs = [
            LiteralInput(
                'srcfile',
                'Source file name',
                data_type='string',
                abstract="""
                Full path to source file name.
                """,
                min_occurs=1,
                max_occurs=1,
            ),
            LiteralInput(
                'dstfile',
                'Destination file name',
                data_type='string',
                abstract="""
                Full path to destination file name.
                """,
                min_occurs=1,
                max_occurs=1,
            ),
            LiteralInput(
                'tr',
                'Output file resolution',
                data_type='string',
                abstract="""
                Set output file resolution (in target georeferenced units). 
                -tr xres yres 
                """,
                min_occurs=0,
            ),                  
            LiteralInput(
                'co',
                '"NAME=VALUE"',
                data_type='string',
                abstract="""
                Passes a creation option to the output format driver. 
                Multiple -co options may be listed. 
                See format specific documentation for legal creation options for each format at http://gdal.org/formats_list.html
                """,
                min_occurs=0,
            ),
            LiteralInput(
                'overwrite',
                "Overwrite the target dataset if it already exists",
                data_type='boolean',
                abstract="""
                Overwrite the target dataset if it already exists.
                """,
                min_occurs=0,
                max_occurs=1,
            ),                  
        ]
        outputs = [
            LiteralOutput(
                'dstfile',
                'Destination file name',
                data_type='string',
                abstract="""
                Full path to destination file name, generated by gdalwarp.
                """,
            )
        ]

        super(GdalWarp, self).__init__(
            identifier='gdalwarp',
            abstract="""
            Image reprojection and warping utility. See <a href="http://gdal.org/gdalwarp.html" target="_blank">gdalwarp manual</a>.
            """,
            version='0.1',
            title="gdalwarp",
            metadata=[],
            profile='',
            inputs=inputs,
            outputs=outputs,
        )


    def get_command(self, request, response):
        """
        The service command that will be executed later. Do not do any processing here.
        
        Returns
        -------
        string
            The service command to be executed.
        """
        logger.info('Request inputs: %s', request.inputs)

        return 'gdalwarp %s %s %s %s' % (self._boolean_params_str(request),
                                         self._optional_params_str(request),
                                         self._get_input(request, 'srcfile'),
                                         self._get_input(request, 'dstfile'),
                                        )


    def set_output(self, request, response):
        """Set the output from the WPS request."""
        # For now, the user specifies the dstfile as an input, and it is set as an output, 
        # matching gdalwarp.
        response.outputs['dstfile'].data = self._get_input(request, 'dstfile')
        response.outputs['dstfile'].uom = UOM('unity')

