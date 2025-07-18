DATASET="$1"
CUDA_VISIBLE_DEVICES=0 python main.py -mode train -dd "dataset/${DATASET}" -pm bert -cd "save/${DATASET}" -rd resource -knn True -beta 0.5 -sp 0.7
