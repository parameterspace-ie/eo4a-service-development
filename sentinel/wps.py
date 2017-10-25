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
    Generates an RGB composite raster for each input Sentinel-2 product.
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
            LiteralInput(
                'r_band',
                'R band',
                data_type='integer',
                abstract="""
                R band number (default=4).,
                """,
                default="4",
                min_occurs=0,
                max_occurs=1,
            ),
            LiteralInput(
                'g_band',
                'G band',
                data_type='integer',
                abstract="""
                G band number (default=3).,
                """,
                default="3",
                min_occurs=0,
                max_occurs=1,
            ),
            LiteralInput(
                'b_band',
                'B band',
                data_type='integer',
                abstract="""
                B band number (default=2).,
                """,
                default="2",
                min_occurs=0,
                max_occurs=1,
            ),
            LiteralInput(
                'resolution',
                'Sentinel-2 product resolution (default=60)',
                data_type='integer',
                abstract="""
                The default resolution of 60m is used for level 2 products generated by <a href="http://step.esa.int/main/third-party-plugins-2/sen2cor/" target="_blank">Sen2Cor</a>, as this generates raster layers of manageable size for the pathfinder.
                """,
                default="60",
                min_occurs=0,
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
            Example service that generates composite RGB rasters from Sentinel-2 products, using bands 4, 3, and 2 respectively by default. 
            However, alternative bands may also be used, such as the false color (R=8, G=4, B=3).
            """,
            version='0.1',
            title="Sentinel-2 RGB",
            metadata=[Metadata('Raster')],
            profile='',
            inputs=inputs,
            outputs=outputs,
        )


    def _output_dir(self):
        return os.path.join(self.output_dir, 'rgb')
    
    
    def get_command(self, request, response):
        """The service command. Do not do any processing here."""
        logger.info('Request inputs: %s', request.inputs)

        return 'bash -x %s/sentinel2rgb %s %02d %02d %02d R60m %s' % (self._package_path,
                                                                    self._get_input(request, 's2_product_dir'),
                                                                    # TODO: use defaults from input definitions
                                                                    int(self._get_input(request, 'r_band')),
                                                                    int(self._get_input(request, 'g_band')),
                                                                    int(self._get_input(request, 'b_band')),
                                                                    #'R%sm' % self._get_input(request, 'resolution'),
                                                                    self._output_dir(),
                                                                    )


    def set_output(self, request, response):
        """Set the output in the WPS response."""
        output = response.outputs['rgb_dir']
        output.data = self._output_dir()
        output.uom = UOM('unity')
        
        
class Sentinel2Ndvi(EO4AProcess):
    """
    Generates an NDVI raster for each input Sentinel-2 product.
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
            LiteralInput(
                'nir_band',
                'NIR band',
                data_type='integer',
                abstract="""
                NIR band number (default=8).,
                """,
                default="8",
                min_occurs=0,
                max_occurs=1,
            ),
            LiteralInput(
                'red_band',
                'Red band',
                data_type='integer',
                abstract="""
                Red band number (default=4).,
                """,
                default="4",
                min_occurs=0,
                max_occurs=1,
            ),
            LiteralInput(
                'resolution',
                'Sentinel-2 product resolution (default=60)',
                data_type='integer',
                abstract="""
                The default resolution of 60m is used for level 2 products generated by <a href="http://step.esa.int/main/third-party-plugins-2/sen2cor/" target="_blank">Sen2Cor</a>, as this generates raster layers of manageable size for the pathfinder.
                """,
                default="60",
                min_occurs=0,
                max_occurs=1,
            ),
        ]
        outputs = [
            LiteralOutput(
                'ndvi_dir',
                'NDVI rasters directory',
                data_type='string',
                abstract="""
                Directory containing NDVI rasters.
                """,
            )
        ]

        super(Sentinel2Ndvi, self).__init__(
            identifier='sentinel2-ndvi',
            abstract="""
            Example service that generates Normalized Difference Vegetation Index (NDVI) rasters from Sentinel-2 products with NDVI = (NIR-Red)/(NIR+Red), using NIR = band 8 and Red = band 4 by default. 
            However, alternative band numbers may also be specified.
            """,
            version='0.1',
            title="Sentinel-2 NDVI",
            metadata=[Metadata('Raster')],
            profile='',
            inputs=inputs,
            outputs=outputs,
        )


    def _output_dir(self):
        return os.path.join(self.output_dir, 'ndvi')
    
    
    def get_command(self, request, response):
        """The service command. Do not do any processing here."""
        logger.info('Request inputs: %s', request.inputs)

        def get_band(band):
            band_val = str(self._get_input(request, band)).upper()
            if band_val != '8A':
                band_val =  '%02d' % int(band_val)
            return band_val

        return 'bash -x %s/sentinel2ndvi %s %s %s %s %s' % (self._package_path,
                                                                    self._get_input(request, 's2_product_dir'),
                                                                    # TODO: use defaults from input definitions
                                                                    get_band('nir_band'),
                                                                    get_band('red_band'),
                                                                    'R%sm' % self._get_input(request, 'resolution'),
                                                                    self._output_dir(),
                                                                    )


    def set_output(self, request, response):
        """Set the output in the WPS response."""
        output = response.outputs['ndvi_dir']
        output.data = self._output_dir()
        output.uom = UOM('unity')
        
        
        
