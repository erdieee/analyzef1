#!/usr/bin/env python3
"""
Main analyzef1 script
"""

import logging
from typing import Any, List

from analyzef1.ui import AnalyzeF1UI

logger = logging.getLogger('analyzef1')

LOGFORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOGFORMAT)

def main(sysargv: List[str] = None) -> None:
    """
    This function will initiate the script.
    :return: None
    """
    logger.info('Starting analyzef1 ...')
    
    AnalyzeF1UI()
    
if __name__ == "__main__": 
    main()