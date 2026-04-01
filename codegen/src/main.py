import json
import os
import copy
from pathlib import Path
import shutil

from jinja2 import Environment, FileSystemLoader, select_autoescape

import utils.concepts
import utils.config
import utils.state_space
import utils.delphi
import utils.general


def find_project_root(marker_file="pyproject.toml"):
  """Walk up from the current file until a marker file is found."""
  current = Path(__file__).resolve().parent
  while current != current.parent:
    if (current / marker_file).exists():
      return current
    current = current.parent
  err_msg = f"Project root not found, could not find '{marker_file}'"
  raise FileNotFoundError(err_msg)


def assert_path_exists(path: str):
  if not Path(path).exists():
    err_msg = f"Path does not exist '{path}'"
    raise FileNotFoundError(err_msg)


ROOT = find_project_root()
LF_ROOT = os.path.abspath(os.path.join(ROOT, ".."))
SCHEMAS_DIR = os.path.join(LF_ROOT, "leapfrog-core", "model_schemas")
LF_CORE_INCLUDE = os.path.join(LF_ROOT, "leapfrog-core", "include")
GENERATED_CPP_DEST = os.path.join(LF_CORE_INCLUDE, "generated")
GENERATED_DELPHI_DEST = os.path.join(LF_ROOT, "delphi")
assert_path_exists(SCHEMAS_DIR)
assert_path_exists(LF_CORE_INCLUDE)
assert_path_exists(GENERATED_DELPHI_DEST)

Path(GENERATED_CPP_DEST).mkdir(exist_ok=True)


def relative_file_path(*paths):
  dirname = os.path.dirname(__file__)
  return os.path.join(dirname, *paths)


def load_json(*paths):
  with open(os.path.join(*paths)) as f:
    return json.load(f)


def load_children_model_schemas(paths):
  if isinstance(paths, str):
    return load_json(SCHEMAS_DIR, paths)
  else:
    return [load_json(SCHEMAS_DIR, p) for p in paths]


def generate(template_path, dest_path, *args, **kwargs):
  template = env.get_template(template_path)
  output = template.render(*args, **kwargs)
  Path(os.path.dirname(dest_path)).mkdir(exist_ok=True)
  with open(dest_path, "w") as f:
    f.write(output)

supported_languages = ["r", "python"]
supported_num_types = ["real_type", "int"]

def process_var_config(name, cfg, is_par = False):
  if not cfg.get("num_type"):
    unsupported_num_type_err_msg = f'num_type for {name} should be one of {" or ".join(supported_num_types)}'
    assert cfg["num_type"] in supported_num_types, unsupported_num_type_err_msg

  if not cfg.get("dims"):
    cfg["type"] = "scalar"
  else:
    dims_not_list_err_msg = f'dims for {name} should be a list'
    assert isinstance(cfg["dims"], list), dims_not_list_err_msg
    cfg["type"] = "tensor"

  if not is_par: return
  if not cfg.get("alias"):
    cfg["alias"] = { l: name for l in supported_languages }
  else:
    alias = cfg["alias"]
    for l in supported_languages:
      if not alias.get(l):
        alias[l] = name
      else:
        alias_not_string_err_msg = f'{l} alias for {name} should be a string'
        assert isinstance(alias[l], str), alias_not_string_err_msg


def add_output_year_dim(cfg):
  if not cfg.get("dims"):
    cfg["dims"] = ["output_years"]
  else:
    cfg["dims"].append("output_years")


def generate_hpp(template_name, *args, **kwargs):
  template_path = f'cpp/{template_name}.j2'
  dest_path = os.path.join(GENERATED_CPP_DEST, f"{template_name}.hpp")
  generate(template_path, dest_path, *args, **kwargs)


def generate_delphi(template_name, *args, **kwargs):
  template_path = f'delphi/{template_name}.j2'
  dest_path = os.path.join(GENERATED_DELPHI_DEST, f"{template_name}.pas")
  generate(template_path, dest_path, *args, **kwargs)


def copy_cpp_file(source):
  file_name = os.path.basename(source)
  dest_path = os.path.join(GENERATED_CPP_DEST, file_name)
  shutil.copyfile(source, dest_path)


dat = load_json(SCHEMAS_DIR, "FullModel.json")
dat = { k: load_children_model_schemas(v) for k, v in dat.items() }


for config in dat["configs"]:
  config["output_state"] = copy.deepcopy(config["state"])

  for name, cfg in config["pars"].items():
    process_var_config(name, cfg, True)

  for name, cfg in config["intermediate"].items():
    process_var_config(name, cfg)

  for name, cfg in config["state"].items():
    process_var_config(name, cfg)

  for name, cfg in config["output_state"].items():
    add_output_year_dim(cfg)
    process_var_config(name, cfg)

template_dir = relative_file_path("..", "templates")
file_loader = FileSystemLoader(template_dir)
env = Environment(
  loader = file_loader,
  trim_blocks = True,
  lstrip_blocks = True,
  autoescape = select_autoescape(),
  keep_trailing_newline = True
)

generate_hpp("model_variants", dat)
generate_hpp("state_space", utils.state_space.extract_state_space_info(dat) | vars(utils.state_space))
generate_hpp("concepts", dat | vars(utils.concepts))
generate_hpp("config", dat | vars(utils.config) | vars(utils.general))
generate_hpp("config_mixer", dat)
generate_hpp("py_interface/py_adapters", dat | vars(utils.config) | vars(utils.general))
generate_hpp("cpp_interface/hdf5_utils", dat | vars(utils.config) | vars(utils.general))
generate_hpp("cpp_interface/cpp_adapters", dat | vars(utils.config) | vars(utils.general))
generate_hpp("r_interface/r_adapters", dat | vars(utils.config) | vars(utils.general))
generate_hpp("c_interface/c_adapters", dat | vars(utils.config) | vars(utils.general))
generate_hpp("c_interface/c_types", dat | vars(utils.config) | vars(utils.delphi) | vars(utils.general))
copy_cpp_file(os.path.join(template_dir, "cpp", ".clang-format"))
generate_delphi("LeapfrogInterface", dat | vars(utils.delphi) | vars(utils.general))
