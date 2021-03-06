#!/usr/bin/env python

"""Validate STIX 2.0 documents against the specification.
"""

import logging
import os
import sys

from stix2validator import (ValidationError, codes, output, parse_args,
                            print_results, run_validation)

logger = logging.getLogger(__name__)


def main():
    # Parse command line arguments
    options = parse_args(sys.argv[1:], is_script=True)

    # Only print prompt if script is run on cmdline and no input is piped in
    if options.files == sys.stdin and os.isatty(0):
        print('Input STIX content, then press Ctrl+D: ')

    try:
        # Validate input documents
        results = run_validation(options)

        # Print validation results
        print_results(results)

        # Determine exit status code and exit.
        code = codes.get_code(results)
        sys.exit(code)

    except (ValidationError, IOError) as ex:
        output.error(
            "Validation error occurred: '%s'" % str(ex),
            codes.EXIT_VALIDATION_ERROR
        )
    except Exception:
        logger.exception("Fatal error occurred")
        sys.exit(codes.EXIT_FAILURE)


if __name__ == '__main__':
    main()
