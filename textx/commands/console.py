#!/usr/bin/env python
import sys
import argparse
from textx.metamodel import metamodel_from_file
from textx.export import metamodel_export, model_export
from textx.exceptions import TextXError


def textx():
    """
    textx console command.
    """

    class MyParser(argparse.ArgumentParser):
        """
        Custom argument parser for printing help message in case of an error.
        See http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
        """
        def error(self, message):
            sys.stderr.write('error: %s\n' % message)
            self.print_help()
            sys.exit(2)

    parser = MyParser(description='textX checker and visualizer')
    parser.add_argument('cmd', help='Command - "check", "visualize" '
                                    'or "generate"')
    parser.add_argument('metamodel', help='Meta-model file name')
    parser.add_argument('model', help='Model file name', nargs='?')
    parser.add_argument('-i', help='case-insensitive parsing',
                        action='store_true')
    parser.add_argument('-d', help='run in debug mode',
                        action='store_true')
    parser.add_argument('--out-folder', '-o',
                        help='output folder for metamodel generation. Default'
                             ' value is "."',
                        default='.')

    args = parser.parse_args()

    if args.cmd not in ['visualize', 'check', 'generate']:
        print("Unknown command {}. Command must be one of"
              " 'visualize', 'check', 'generate'.".format(args.cmd))
        sys.exit(1)

    try:
        metamodel = metamodel_from_file(args.metamodel, ignore_case=args.i,
                                        debug=args.d)
        print("Meta-model OK.")
    except TextXError as e:
        print("Error in meta-model file.")
        print(e)
        sys.exit(1)

    if args.model:
        try:
            model = metamodel.model_from_file(args.model, debug=args.d)
            print("Model OK.")
        except TextXError as e:
            print("Error in model file.")
            print(e)
            sys.exit(1)

    if args.cmd == "visualize":
        print("Generating '%s.dot' file for meta-model." % args.metamodel)
        print("To convert to png run 'dot -Tpng -O %s.dot'" % args.metamodel)
        metamodel_export(metamodel, "%s.dot" % args.metamodel)

        if args.model:
            print("Generating '%s.dot' file for model." % args.model)
            print("To convert to png run 'dot -Tpng -O %s.dot'" % args.model)
            model_export(model, "%s.dot" % args.model)
    elif args.cmd == "generate":
        try:
            from pyecoregen.ecore import EcoreGenerator
        except ImportError:
            print('The PyEcore generation support is disable, please install '
                  'pyecoregen to enable it.')
            sys.exit(2)
        dest = args.out_folder
        generator = EcoreGenerator()
        # Iterate on each resources from the metamodel resource set in case
        # the grammar references other ones (i.e: the meta-model references
        # other ones).
        for resource in metamodel.resource_set.resources.values():
            package = resource.contents[0]
            print("Generating '%s' PyEcore package for "
                  "meta-model in folder '%s'." % (package.name, dest))
            generator.generate(package, dest)
