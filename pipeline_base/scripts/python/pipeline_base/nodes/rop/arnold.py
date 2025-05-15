from cyclone.nodes.base import BaseNode


class Arnold(BaseNode):

    defaults = {
        "trange": 1,  # set default range-mode to range
        "camera": "/obj/${SHOTNAME}_shotcam",
        "ar_ass_file": "$PATH_IFD/$HIPNAME/$OS/`$OS`.$F4.ass",
        "ar_picture": "$PATH_RENDERS/$USER/$HIPNAME/$OS/`$HIPNAME`_`$OS`.$F4.exr",
        "ar_picture_tiling": True,
        "ar_picture_append": True,
        "ar_exr_half_precision": True,
        "ar_abort_on_license_fail": True,
        "ar_texture_auto_maketx": False,
    }
