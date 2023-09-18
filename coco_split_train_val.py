import json
import random
import os
import cv2
from tqdm import tqdm
"""
完成一整个coco格式json文件的划分,默认输出train:val:test=8:1:1

"""
# 训练、验证、测试比例
def split_coco(root,json_path,train_radio=0.8,val_radio=0.1998,test_radio=0):
    data=json.load(open(json_path))
    total_len=len(data["images"])
    train_num=int(total_len*train_radio)
    val_num=int(total_len*val_radio)
    test_num=total_len-train_num-val_num
    print(f"{'*'*20}划分后训练集合数量：{train_num},验证集数量:{val_num},测试集数量:{test_num}{'*'*20}")
    # 训练集
    print("*"*20,"开始处理训练集","*"*20)
    train_dic={"images":[],"categories":data["categories"],"annotations":[]}
    for num in tqdm(range(train_num)):
        img_id=data["images"][num]["id"]
        train_dic["images"].append(data["images"][num])
        for dic in data["annotations"]:
            if dic["image_id"]==img_id:
                train_dic["annotations"].append(dic)
    f=open(os.path.join(root,"train.json"),"w+")
    f.write(json.dumps(train_dic))
    f.close()
    # 验证集
    print("*"*20,"开始处理验证集","*"*20)
    val_dic={"images":[],"categories":data["categories"],"annotations":[]}
    for num in tqdm(range(train_num,train_num+val_num)):
        img_id=data["images"][num]["id"]
        val_dic["images"].append(data["images"][num])
        for dic in data["annotations"]:
            if dic["image_id"]==img_id:
                val_dic["annotations"].append(dic)
    f=open(os.path.join(root,"val.json"),"w+")
    f.write(json.dumps(val_dic))
    f.close()
    # 测试集
    print("*"*20,"开始处理测试集","*"*20)
    test_dic={"images":[],"categories":data["categories"],"annotations":[]}
    for num in tqdm(range(train_num+val_num,total_len)):
        img_id=data["images"][num]["id"]
        test_dic["images"].append(data["images"][num])
        for dic in data["annotations"]:
            if dic["image_id"]==img_id:
                test_dic["annotations"].append(dic)
    f=open(os.path.join(root,"test.json"),"w+")
    f.write(json.dumps(test_dic))
    f.close()
if __name__=="__main__":
    json_path="/data2/liangxiaoyuan/patent_layout/use_clean_dataset/checked_json_imgs/general_correct_no_BOX+.json"
    root="/data2/liangxiaoyuan/patent_layout/use_clean_dataset/checked_json_imgs"
    split_coco(root,json_path)