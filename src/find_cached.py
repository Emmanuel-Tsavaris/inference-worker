"""
Finds the full LLM GGUF path from the Hugging Face cache.
"""

import os
import sys
import argparse

CACHE_DIR = "/runpod-volume/huggingface-cache/hub"


def find_model_path(model_name, gguf_in_repo="model.gguf"):
    """
    Find the path to a cached model.

    Args:
        model_name: The model name from Hugging Face

    Returns:
        The full path to the cached model, or None if not found
    """
    try:
        org, name = model_name.split("/", 1)
        model_root = os.path.join(CACHE_DIR, f"models--{org}--{name}")
        snapshots_dir = os.path.join(model_root, "snapshots")

        
        if os.path.isdir(snapshots_dir):
            snapshots = os.listdir(snapshots_dir)

            if snapshots:
                return os.path.join(snapshots_dir, snapshots[0], gguf_in_repo)

        return None
    except Exception as e:
        raise f"Error: There was a problem parsing the directory: {e}"


def main():
    """
    Main function to find and print the model path.
    """

    parser = argparse.ArgumentParser(
        description="Find the full GGUF path from the Hugging Face cache."
    )
    parser.add_argument(
        "model", type=str, help="The model name from Hugging Face"
    )
    parser.add_argument(
        "path",
        type=str,
        help="The path to the GGUF file within the model repository",
    )
    args = parser.parse_args()

    model_path = find_model_path(args.model, args.path)
    if model_path is None:
        print(
            f"Error: Cached model not found. Model='{args.model}', GGUF='{args.path}', Cache dir='{CACHE_DIR}'",
            file=sys.stderr,
        )
        sys.exit(1)
    print(model_path, end="")


if __name__ == "__main__":
    main()
