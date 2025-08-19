# How-to Guide

## Convert Yolov8 to ONNX format

```shell
conda create -n triton python=3.11
conda activate triton
pip install -r requirements.txt
python utils/yolo2onnx.py
```

You should see the 2 files `yolov8n.pt` and `yolov8n.onnx` in the root path of your project now. Please move the file `yolov8n.onnx` to `model_repo/yolov8n/1` before continuing to the next step.

Besides, you can also see a new file created in the path `images/output.jpg`, which was produced by inputing an image to the YOLO model (in `.pt`).

## Run a Triton container

```shell
docker compose -f docker-compose.yaml up -d
```

You can use the following command to check if our service is ready
```shell
curl -v localhost:8003/v2/health/ready
```

## Performance Analyzer
Before running the following command, please execute into the `triton-sdk` container first by running the following command:
```shell
docker exec -ti triton-sdk bash
```

### Profile our performance
Please replace all of my paths, i.e., `/home/quandv/Documents/fsds/m3/triton-server` to yours before running the following commands.

```shell
perf_analyzer --model-repository=/home/quandv/Documents/fsds/m3/triton-server/yolov8n/model_repo -m yolov8n -u 127.17.0.1:8003
```

### Tuning configs
```shell
model-analyzer profile \
    --model-repository /home/quandv/Documents/fsds/m3/triton-server/yolov8n/model_repo \
    --profile-models yolov8n --triton-launch-mode=docker \
    --output-model-repository-path /home/quandv/Documents/fsds/m3/triton-server/yolov8n/output_model_repo/yolov8n \
    --export-path /profile_results \
    --override-output-model-repository \
    --run-config-search-max-concurrency 2 \
    --run-config-search-max-model-batch-size 2 \
    --run-config-search-max-instance-count 2
```

**Note:** Use the [following link](https://docs.nvidia.com/deeplearning/triton-inference-server/archives/triton_inference_server_220/user-guide/docs/optimization.html) to further optimize

## Install Nsight System for system performance analysis
Please download and install [this package](https://developer.nvidia.com/downloads/assets/tools/secure/nsight-systems/2023_3/nsight-systems-2023.3.1_2023.3.1.92-1_amd64.deb/) first.

## Notes
- If you meet the problem `Error response from daemon: could not select device driver "nvidia" with capabilities: [[gpu]]`, please following [this tutorial](https://askubuntu.com/a/1400480) to fix :).
- If your meet this error `src/cpp/cuda.hpp:14:10: fatal error: cuda.h: No such file or directory` while installing `pycuda`, make sure you have installed CUDA Toolkit from [this website](https://developer.nvidia.com/cuda-downloads) and also [this](https://askubuntu.com/a/1427396).

## References
- [Triton Inference Server's tutorials](https://github.com/triton-inference-server/tutorials)
- [TensorRT example](https://github.com/NVIDIA/TensorRT/blob/main/samples/python/yolov3_onnx/onnx_to_tensorrt.py)
- [nsight-training](https://github.com/NVIDIA/nsight-training)
- [nsight-systems](https://developer.nvidia.com/nsight-systems)
- [Nvidia Deep Learning TensorRT documentation](https://docs.nvidia.com/deeplearning/tensorrt/developer-guide/index.html)
- [Another stuff related to TensorRT](https://github.com/aimuch/iAI/tree/main)
