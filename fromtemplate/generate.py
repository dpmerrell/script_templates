"""
    Master script for generating files/directories
    from templates.
"""


from fromtemplate.config_util import prepare_params
from fromtemplate.generate_dir import generate_dir
from os.path import basename
from pathlib import Path


"""
    Generate a file or directory from a template.
"""
def fromtemplate(new_file_path, kind=None, config_yaml=None, verbose=True):

    # Get the new file's `kind`
    file_basename = basename(new_file_path)
    if kind is None:
        # Try to infer the new file's `kind` from its suffix.
        # The `suffix` is everything after the first period in the basename.
        kind = ".".join(file_basename.split(".")[1:])
        if kind == "":
            raise ValueError(f"{new_file_path} does NOT have a file suffix. You MUST provide the `--kind` argument to fromtemplate!")
    
    template_path, fields = prepare_params(file_basename, kind, config_yaml) 

    # Generate the result; note that `generate_dir` already
    # recursively checks whether its argument is a directory
    # or file, so we can call it on files as well.
    if Path(template_path).exists():
        generate_dir(new_file_path, template_path, fields, verbose=verbose)
    else:
        raise ValueError(f"Error generating {new_file_path}. No template exists for kind `{kind}`")

    return 


"""
    Command line interface for `fromtemplate`.
"""
def fromtemplate_script():
    
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("new_file_path", help="Path to the newly generated file.")
    parser.add_argument("--kind", default=None, help="`kind` of file or directory to generate.")
    parser.add_argument("--config-yaml", default=str(Path.home().joinpath(".fromtemplate","config.yaml")),
                                         help="Path to a YAML configuration file. By default, looks for one at $HOME/.fromtemplate/config.yaml.")
    args = parser.parse_args()
    fromtemplate(args.new_file_path,
                 kind=args.kind,
                 config_yaml=args.config_yaml,
                 verbose=True
                )


if __name__=="__main__":

    fromtemplate_script()

