import argparse
import json
import logging
import os
import sys
from pathlib import Path

from intersect_sdk import (
    IntersectService,
    IntersectServiceConfig,
    default_intersect_lifecycle_loop,
)

logger = logging.getLogger(__name__)

"""
This launches the service.  Separate file due to module/import structure, plus we possibly want the capability to be a separate unit
"""

if __name__ == '__main__':
    # boilerplate config file setup
    parser = argparse.ArgumentParser(description='Automated client')
    parser.add_argument(
        '--config',
        type=Path,
        default=os.environ.get(
            'DIAL_TRANSFORMER_CONFIG_FILE',
            Path(__file__).parents[2] / 'local-conf.json',
        ),
    )
    args = parser.parse_args()
    try:
        with Path(args.config).open('rb') as f:
            from_config_file = json.load(f)
    except (json.decoder.JSONDecodeError, OSError) as e:
        logger.critical('unable to load config file: %s', str(e))
        sys.exit(1)

    config = IntersectServiceConfig(
        hierarchy=from_config_file['intersect-hierarchy'],
        **from_config_file['intersect'],
    )

    logging.basicConfig(level=logging.INFO)

    # IMPORTANT: import this after logging configuration
    from .capability import TransformerCapability

    capability = TransformerCapability()

    service = IntersectService([capability], config)
    default_intersect_lifecycle_loop(
        service,
    )
