import argparse
import json
import os
from modelLab import logger
import json

def is_winml_runtime(runtime):
    return runtime == "WCR" or runtime == "WCR_CUDA" or runtime == "QNN_LLM"

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="path to input config file")
    parser.add_argument("--runtime", required=True, help="runtime")
    return parser.parse_args()

def main():
    args = parse_arguments()
    if is_winml_runtime(args.runtime):
        from modelLab import register_execution_providers_to_onnxruntime
        register_execution_providers_to_onnxruntime()
    import olive
    import olive.workflows

    with open(args.config, 'r', encoding='utf-8') as file:
        oliveJson = json.load(file)
        # TODO disable evaluator
        oliveJson.pop("evaluator", None)
        oliveJson.pop("evaluators", None)

    olive.workflows.run(oliveJson)
    # check model.onnx and throw if not exist
    onnx_file_path = os.path.join(os.path.dirname(args.config), "model_config.json")
    if not os.path.isfile(onnx_file_path):
        error = f"Model file not generated: {onnx_file_path}"
        logger.error(error)
        raise Exception(error)
    logger.info("Model lab succeeded for conversion.\nModel config: %s", onnx_file_path)

if __name__ == "__main__":
    main()
