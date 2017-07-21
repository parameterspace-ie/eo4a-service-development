"""Example EO4A services for Sentinel-2 products"""
import logging
import os

from pywps import LiteralInput, LiteralOutput, UOM
from pywps.app import EO4AProcess
from pywps.app.Common import Metadata

__author__ = "Derek O'Callaghan"

logger = logging.getLogger('PYWPS')


class Sentinel2Rgb(EO4AProcess):
    """
    Generates an RGB raster for each input Sentinel-2 product.
    """

    def __init__(self):
        inputs = [
            LiteralInput(
                's2_product_dir',
                'Sentinel-2 product directory',
                data_type='string',
                abstract="""
                Contains one or more Sentinel-2 products. 
                """,
                min_occurs=1,
                max_occurs=1,
            ),
        ]
        outputs = [
            LiteralOutput(
                'rgb_dir',
                'RGB rasters directory',
                data_type='string',
                abstract="""
                Directory containing RGB rasters.
                """,
            )
        ]

        super(Sentinel2Rgb, self).__init__(
            identifier='sentinel2-rgb',
            abstract="""
            Example service that generates RGB rasters from Sentinel-2 products, using bands 4, 3, and 2 respectively.
            """,
            version='0.1',
            title="Sentinel-2 RGB",
            metadata=[Metadata('Sentinel')],
            profile='',
            inputs=inputs,
            outputs=outputs,
        )


    def _module_path(self):
        """
        Generates a relative path used to run any scripts etc as service commands.
        TODO: move to parent
        """
        return os.path.dirname(self.__module__.replace('.', os.path.sep))


    def _output_dir(self):
        return os.path.join(self.output_dir, 'rgb')
    
    
    def get_command(self, request, response):
        """The service command. Do not do any processing here."""
        logger.info('Request inputs: %s', request.inputs)

        return 'bash -x %s/sentinel2rgb %s %s' % (self._module_path(),
                                                  self._get_input(request, 's2_product_dir'),
                                                  self._output_dir()
                                                  )


    def set_output(self, request, response):
        """Set the output in the WPS response."""
        output = response.outputs['rgb_dir']
        output.data = self.get_dir_with_context(self._output_dir(), self.WORKFLOW_CONTEXT)
        output.uom = UOM('unity')
        
        
        
