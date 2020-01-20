# !/usr/bin/python
# -*- coding: UTF-8 -*-
""" Purpose: Deploy jobs to sentinel hub batch processor

    Requirements: none
"""

__author__ = "Jan Wevers - jan.wevers@brockmann-consult.de"
__copyright__ = "Copyright (C) 2020 Brockmann Consult GmbH"
__license__ = "Proprietary license"
__version__ = "1.0"

import os
import argparse
import time


def prepare_prepro_folder(L1C):
    PRE_folder = '/'.join(L1C.split('/')[:len(L1C.split('/')) - 2]) + '/' + 'PRE'
    if not os.path.isdir(PRE_folder):
        os.makedirs(PRE_folder)
    PRE = '/'.join(L1C.split('/')[:len(L1C.split('/')) - 2]) + '/' + 'PRE' + '/' + L1C.split('/')[-1][:-5] + '_prepro.dim'

    return PRE


def prepare_output_folder(PRE):
    OUT_folder = '/'.join(PRE.split('/')[:len(PRE.split('/')) - 2]) + '/' + 'OUT'
    if not os.path.isdir(OUT_folder):
        os.makedirs(OUT_folder)
    OUT = '/'.join(PRE.split('/')[:len(PRE.split('/')) - 2]) + '/' + 'OUT' + '/' + PRE.split('/')[-1][:-4] + '_idepix.tif'

    return OUT


def preprocess(L1C, DEM, PRE, version):
    cmd = 'gpt S2_idePix_Part1_data_preparation_v' + version + '.xml -PsourceFileL1C=' + L1C + ' -PsourceFileElev=' + DEM + ' -PtargetFile=' + PRE
    print(cmd)
    os.system(cmd)


def idepix(PRE, OUT, idepix_version):
    # cmd = 'gpt S2_IdePix_Part2_pixel_identification_v' + idepix_version + '.xml -c 2560M -PsourceFilePrePro=' + PRE + ' -PtargetFile=' + OUT
    cmd = 'gpt S2_IdePix_Part2_pixel_identification_v' + idepix_version + '.xml -PsourceFilePrePro=' + PRE + ' -PtargetFile=' + OUT
    print(cmd)
    os.system(cmd)

def prepro_idepix(L1C, DEM, OUT):
    cmd = 'gpt S2_idePix.xml -PsourceFileL1C=' + L1C + ' -PsourceFileElev=' + DEM + ' -PtargetFile=' + OUT
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    CLI = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    # Your sentinelhub client credentials
    CLI.add_argument(
        "-sfL1C",
        "--PsourceFileL1C",
        type=str,
        default='',
        required=False,
        metavar="L1C product",
        help='Provide Path to the L1C SAFE file to be processed'
    )
    CLI.add_argument(
        "-sfDEM",
        "--PsourceFileElev",
        type=str,
        default='',
        required=False,
        metavar="Secret",
        help='Provide Path to the DEM file to be used for processing'
    )
    CLI.add_argument(
        "-sfPRE",
        "--PsourceFilePre",
        type=str,
        default='',
        required=False,
        metavar="Secret",
        help='Provide Path to preprocessed data to be used for IdePix'
    )
    CLI.add_argument(
        "-pv",
        "--prepro_version",
        type=str,
        default='5',
        required=False,
        metavar="Secret",
        help='Provide version number of the prepro graph to be used (1, 2, 3 or 4)'
    )
    CLI.add_argument(
        "-iv",
        "--idepix_version",
        type=str,
        default='2',
        required=False,
        metavar="Secret",
        help='Provide version number of the idepix graph to be used (1 or 2)'
    )
    CLI.add_argument(
        "-p",
        action="store_true",
        default=False,
        help="set -p flag if you only want to run preprocessing, default is False"
    )
    CLI.add_argument(
        "-i",
        action="store_true",
        default=False,
        help="set -i flag if you only want to run IdePix on preprocessed data, default is False"
    )
    CLI.add_argument(
        "-a",
        action="store_true",
        default=False,
        help="set -a flag if you want to run both steps, preprocessing and IdePix on preprocessed data, default is False"
    )
    CLI.add_argument(
        "-o",
        action="store_true",
        default=False,
        help="set -o flag if you want to run both steps in one graph, preprocessing and IdePix on preprocessed data, default is False"
    )

    args = CLI.parse_args()
    L1C = args.PsourceFileL1C.replace("\\", "/")
    DEM = args.PsourceFileElev.replace("\\", "/")
    PRE = args.PsourceFilePre.replace("\\", "/")
    prepro_version = args.prepro_version
    idepix_version = args.idepix_version

    if args.a:
        PRE = prepare_prepro_folder(L1C)
        OUT = prepare_output_folder(PRE)
        if L1C == '':
            print('No L1C file provided')
        elif DEM == '':
            print('No DEM provided')
        else:
            start_time_pre = time.time()
            print('Preprocessing started: %s' % start_time_pre)
            preprocess(L1C, DEM, PRE, prepro_version)
            stop_time_pre = time.time()
            print('Preprocessing finished at: %s' % stop_time_pre)
            print('Preprocessing took %s seconds' % (stop_time_pre - start_time_pre))

            start_time_id = time.time()
            print('IdePix processing started: %s' % start_time_id)
            idepix(PRE, OUT, idepix_version)
            stop_time_id = time.time()
            print('IdePix processing finished at: %s' % stop_time_id)
            print('IdePix processing took %s seconds' % (stop_time_id - start_time_id))
            print('Complete processing took %s seconds' % (stop_time_id - start_time_pre))

    else:
        if args.p:
            PRE = prepare_prepro_folder(L1C)
            OUT = prepare_output_folder(PRE)
            if L1C == '':
                print('No L1C file provided')
            elif DEM == '':
                print('No DEM provided')
            else:
                start_time_pre = time.time()
                print('Preprocessing started: %s' % start_time_pre)
                preprocess(L1C, DEM, PRE, prepro_version)
                stop_time_pre = time.time()
                print('Preprocessing finished at: %s' % stop_time_pre)
                print('Preprocessing took %s seconds' % (stop_time_pre - start_time_pre))
        elif args.i:
            if PRE == '':
                print('No preprocessed data provided')
            else:
                OUT = prepare_output_folder(PRE)
                start_time_id = time.time()
                print('IdePix processing started: %s' % start_time_id)
                idepix(PRE, OUT, idepix_version)
                stop_time_id = time.time()
                print('IdePix processing finished at: %s' % stop_time_id)
                print('IdePix processing took %s seconds' % (stop_time_id - start_time_id))
        elif args.o:
            PRE = prepare_prepro_folder(L1C)
            OUT = prepare_output_folder(PRE)
            if L1C == '':
                print('No L1C file provided')
            elif DEM == '':
                print('No DEM provided')
            else:
                start_time_id = time.time()
                print('Processing started: %s' % start_time_id)
                prepro_idepix(L1C, DEM, OUT)
                stop_time_id = time.time()
                print('Processing finished at: %s' % stop_time_id)
                print('Processing took %s seconds' % (stop_time_id - start_time_id))
        else:
            print('No processor has been selected. Please set either -p, -i, or -a flag')