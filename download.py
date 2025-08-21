from datasets import load_dataset

# 下载整个数据集
dataset = load_dataset("lvhaidong/LAFAN1_Retargeting_Dataset")

# 如果想保存到本地磁盘（避免每次都重新下载）
dataset.save_to_disk("LAFAN1_Retargeting_Dataset_full")
