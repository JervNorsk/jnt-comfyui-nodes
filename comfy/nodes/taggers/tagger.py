###############################################################################
# Dependencies
# -----------------------------------------------------------------------------
import os
import sys
import importlib

from .... import externals
from ....utils.logger import LOG
from ... import nodes


###############################################################################
# Constants
# -----------------------------------------------------------------------------
JNT_CONFIG = {
    "version": "0.0.1",
    "id": "jnt",
    "name": "JNT",
    "category": "JNT"
}

###############################################################################
# Declarations
# -----------------------------------------------------------------------------
class JntTagger:
    """
    TODO: write documentation
    """
    CONFIG = {
        "id": f"{JNT_CONFIG.get('id')}.tagger",
        "name": f"{JNT_CONFIG.get('name')} Tagger",
    }
    DEFAULT = {
        "model": "wd-convnext-tagger-v3",
        "generic_threshold": 0.35,
        "character_threshold": 0.85,
        "replace_underscore": False,
        "trailing_comma": False,
        "exclude_tags": "",
        "ortProviders": ["CUDAExecutionProvider", "CPUExecutionProvider"],
        "HF_ENDPOINT": "https://huggingface.co"
    }

    # -------------------------------------------------------------------------
    CATEGORY = f"{JNT_CONFIG['category']}"

    # -------------------------------------------------------------------------
    FUNCTION = "exec_wd14tagger"

    # -------------------------------------------------------------------------
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "model": (cls.get_wd14tagger_models(), { "default": cls.DEFAULT["model"] }),
                "general_threshold": ("FLOAT",{ "default": cls.DEFAULT["generic_threshold"], "min": 0.0, "max": 1, "step": 0.05, "display": "slider" }),
                "character_threshold": ("FLOAT",{ "default": cls.DEFAULT["character_threshold"], "min": 0.0, "max": 1, "step": 0.05, "display": "slider" })
            },
            "optional": {}
        }
    RETURN_TYPES = ("STRING","TEXT")
    # RETURN_NAMES = ()
    OUTPUT_IS_LIST = (False,)
    # OUTPUT_NODE = True

    # -------------------------------------------------------------------------
    __wd14tagger = None

    @classmethod
    def get_wd14tagger(cls):
        if cls.__wd14tagger is None:
            cls.__wd14tagger = externals.WD14TAGGER().wd14tagger

        return cls.__wd14tagger


    @classmethod
    def get_wd14tagger_models(cls):
        tagger = cls.get_wd14tagger()

        return tagger.known_models + [
            name for name,
            _ in (os.path.splitext(m) for m in tagger.get_installed_models()) if name not in tagger.known_models
        ]

    @classmethod
    def exec_wd14tagger(cls, image, model, general_threshold, character_threshold):
        tags =  cls.get_wd14tagger().WD14Tagger.tag(
            cls,
            image,
            model,
            general_threshold,
            character_threshold
        )
        return tags, tags

###############################################################################
# Bootstrap
# -----------------------------------------------------------------------------
nodes.register_custom_nodes("jnt.tagger", "JNT Tagger", JntTagger)
