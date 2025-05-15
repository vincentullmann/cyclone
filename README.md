
# 🌀 Cyclone Framework

Collection of random houdini bits

## Setup

choose one of these:

- include the provided `cyclone.json` in your `HOUDINI_PACKAGE_DIR`.
- copy the `cyclone.json` into a path included in your `HOUDINI_PACKAGE_DIR`
  Can be any `$HOUDINI_PATH/packages`, for example your `$HOME/houdini20.0/packages`
  - adjust the values "hpath` to point to this repo
- append the paths by hand in your `$HOUDINI_PATH`

example: running `hython` on linux

```bash
export HOUDINI_PACKAGE_DIR=`pwd`:${HOUDINI_PACKAGE_DIR}
# interactive session
rez env houdini -- hython

# running tests
rez env houdini pytest -- hython -m pytest

```

## TODO

investigate if `inlinecpp` can be of any use for us when wrapping/hooking the nodes
(https://www.sidefx.com/docs/houdini/hom/extendingwithcpp.html#extending_hou_classes)
