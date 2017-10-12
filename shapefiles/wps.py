"""Example EO4A services for shapefile products"""
import logging
import os

from pywps import LiteralInput, LiteralOutput, UOM
from pywps.app import EO4AProcess
from pywps.app.Common import Metadata

__author__ = "Ana Juracic"

logger = logging.getLogger(__name__)

class MergeShapefiles(EO4AProcess):
    """
    Merges multiple shapefiles into a single file.
    """

    def __init__(self):
        inputs = [
            LiteralInput(
                'input_dir', 'Directory with input files',
                abstract="""
                Path to a directory containing input shapefiles that will be merged together.
                """,
                data_type='string',
                min_occurs=1,
                max_occurs=1
            ),
            LiteralInput(
                'filename', 'Name of output file',
                abstract="""
                Name of output file (no direcories and no extension). Default is 'example'. 
                """,
                data_type='string',
                min_occurs=0,
                max_occurs=1,
                default='example'
            )
        ]
        outputs = [
            LiteralOutput(
                'output_dir',
                'Output directory',
                data_type='string',
                abstract="""
                Path to a directory containing the output file.
                """,
            )
        ]
        
        super(MergeShapefiles, self).__init__(
            identifier='merge_shapefiles',
            abstract="""
            Merge multiple shapefiles into a single file.
            """,
            version='0.1',
            title="Merge Shapefiles",
            metadata=[Metadata('Vector')],
            profile='',
            inputs=inputs,
            outputs=outputs,
        )


    def _output_dir(self):
        return os.path.join(self.output_dir, 'merged')


    def get_command(self, request, response):
        """The service command. Do not do any processing here."""
        logger.info('Request inputs: %s', request.inputs)

        return 'bash -x %s/merge_shapefiles.sh %s %s %s' % (
            self._package_path,
            self._get_input(request, 'input_dir'),
            self._output_dir(),
            self._get_input(request, 'filename', default='example'),
            )


    def set_output(self, request, response):
        """Set the output from the WPS request."""
        output = response.outputs['output_dir']
        output.data = self._output_dir()
        output.uom = UOM('unity')
