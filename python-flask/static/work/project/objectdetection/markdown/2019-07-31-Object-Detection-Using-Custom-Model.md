---
title: Object Detection Using Custom Model
published: true
---


# Team sonjo
> 손장민 + 조혁준

# To Do
[ ]
[ ]
[ ] 


# Work Flow

0. [Configuration.](#configuration)

1.  [Take photo.](#take-photo)

2.  [Labeling.](#labeling)

3.  [XML to CSV.](#xml-to-csv)

4.  [Generate TFRECORD.](#generate-tfrecord)

5.  [Write label map.](#write-label-map)

6.  [Modify config file.](#modify-config-file)

7.  [Training.](#training)

8.  [Make pb format file.](#make-pb-format-file)

9.  [Convert pb file to tflite file.](#convert-pb-file-to-tflite-file)

10.  [Import tflite file to android.](#import-tflite-file-to-android)


# Configuration

> 환경 설정 단계입니다. 해당 프로젝트는 GPU 서버에서 처리하였습니다. 존나 쎈 컴퓨터에서 수행하였으므로 참조하시기 바랍니다.

## - Server

  > 서버와 관련된 내용입니다. ubuntu 기준입니다.

### Connection.

```bash
$ ssh -p $PORTNUM $ADDRESS
```
  - PORTNUM : 포트 번호
  - ADDRESS : 서버 주소
> 서버에 접속


### File transport.
```bash
$ scp -P $PORTNUM $FILENAME $ADDRESS:$DIR
```
  - PORTNUM : 포트 번호
  - FILENAME : 파일 이름
  - ADDRESS : 서버 주소
  - DIR : 저장될 디렉토리 위치(경로)
> dataset 과 도출한 output 을 서버와 공유


### GPU state.
```bash
$ watch -d -n .5 nvidia-smi
```
> gpu에 어떤 프로세스가 할당되고 실제로 training 시 확인


## - Docker

> 일일이 cuda, cudnn 과 같은 것들을 세팅하는데에는 너무 힘듭니다. docker를 이용하여 퀘적하게 설정합니다.

### Check container.

```bash
$ docker ps -a
```

  > - 현재 container 정보를 출력
  > - -a 를 빼고 수행하면 동작하고 있는 container 정보 만을 출력

### Multi users.
```bash
$ docker exec -it $CONTAINERNAME bash
```
- CONTAINERNAME : 컨테이너 이름 

> 하나의 container 에서 여러 명이 작업하는데 사용

### Pull.

```bash
$ docker pull tensorflow/tensorflow:nightly-devel-gpu-py3
```
> 텐서플로우 도커 이미지

## - Tensorflow Build

> 텐서플로우를 빌드합니다. 빌드가 완성된 tensorflow 에서는 tflite 변환하는 작업을 수행할 예정입니다.

### Docker run.
```bash
$ nvidia-docker run -net=host --runtime=nvidia -it -w /tensorflow -v $PWD:mnt --name $DOCKER_NAME tensorflow/tensorflow:nightly-devel-gpu-py3 bash
```

> docker 실행

### Build tensorflow.
```bash
$ bazel build --config=opt --config=cuda //tensorflow/tools/pip_package:build_pip_package
```

> tensorflow 빌드

## - Tensorflow Models
> Tensorflow models 에서는 Object Detection 을 위한 훈련을 수행할 예정입니다.

### Git.
```bash
$ git clone https://github.com/tensorflow/models.git
```

> git clone 수행


# Take Photo
> 어느정도 환경설정이 마무리되었으면 이제 dataset을 수집하기 위해 사진을 찍었습니다. 해당 프로젝트에서는 하나의 오브젝트마다 400 장의 사진을 촬영하였습니다. 명도와 같은 빛의 차이와 각도와 같이 여러 방향에서 다양하게 촬영하였습니다. 어느정도의 사진의 개수를 사용해야하는지에 대해서는 실험을 통해 성능의 차이를 확인할 수 있어야하겠습니다.

## - Preprocessor
> 보통 모바일 디바이스와 같은 촬용 기기로 촬영 하였습니다. 다양한 이미지들을 원하는 크기에 맞게 전처리과정을 거쳤습니다. 크기가 성능에 영향을 미치는지는 것에 대한 의문도 듭니다. 하지만 처리 속도가 개빨라집니다.

### Resize.

```python
from PIL import Image
import os

baseDir = "$DIR"
outDir = "$DIR"
imgList = os.listdir(baseDir)
for imgName in imgList:
	if(imgName.split('.')[1] =='jpeg'):
		img = Image.open(baseDir + imgName)
		img.thumbnail((600,600), Image.ANTIALIAS)
		img.save(outDir+imgName, "JPEG")
```

> 600 x 600 사이즈로 변환합니다.

# Labeling
> 물체의 위치정보를 파악하기 위해서는 사용자가 촬영한 사진을 일일이 labeling 하는 과정을 거쳤습니다. 완전 씹극혐 과정입니다. 이래서 머신러닝이 노가다라고 하나 봅니다.

## - Settings
> 디렉토리와 labeling 툴 설정입니다.

### Directory.
> Item
>> Item-raw
>> Item-resize
>> Item-train
>> Item-train-xml
>> Item-validation
>> Item-validation-xml

- 위와 같이 디렉토리를 구성
- validation 에는 보통 이미지의 5% 정도를 랜덤하게 구성


### Tool.
[https://rectlabel.com/](https://rectlabel.com/)
> 위 사이트에서 설치하여 사용


# XML to CSV
> 처리된 모든 파일을 작업할 디렉토리에 이동켰습니다. Tfrecord 포맷의 파일을 만들기 위해서는 이전 labeling 과정에서 발생한 xml 파일을 csv로 변화하여야 합니다.


## - Settings


### Directory.
> train (training 에 필요한 모든 이미지)
> train_xml (train 에 들어간 모든 이미지에 대한 labeling data / xml 파일)
> eval (evaluation 에 필요한 모든 이미지)
> eval_xml (eval 에 들어간 모든 이미지에 대한 labeling data / xml 파일)

### Code.
```python
import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
  
def  xml_to_csv(path):
	xml_list = []
	
	for xml_file in glob.glob(path + '/*.xml'):
		tree = ET.parse(xml_file)
		root = tree.getroot()
		
		for member in root.findall('object'):
			value = (root.find('filename').text,
			int(root.find('size')[0].text),
			int(root.find('size')[1].text),
			member[0].text,
			int(member[5][0].text),
			int(member[5][1].text),
			int(member[5][2].text),
			int(member[5][3].text)
			)
			xml_list.append(value)
			
	column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
	xml_df = pd.DataFrame(xml_list, columns=column_name)
	return xml_df

def  main():
	image_path = os.path.join(os.getcwd(), 'train_xml')
	#image_path = os.path.join(os.getcwd(), 'train_xml')

	xml_df = xml_to_csv(image_path)
	xml_df.to_csv('train.csv', index=None)
	#xml_df.to_csv('cola_labels.csv', index=None)
	print('Successfully converted xml to csv.')

main()
```

> directory 와 같은 path 는 설정한 경로대로 변경하면서 진행합니다. 

### Run.
```bash
$ python xml_to_csv.py 
```

# Generate TFRECORD

> 이제 저장한 이미지들과 csv 파일들을 이용하여 tfrecord 포맷을 만듭니다. 여기서도 몇가지 수정해야할 부분이 있습니다.


## Settings

### Code.

```python
"""  
Usage:  
# From tensorflow/models/  
# Create train data:  
python [generate_tfrecord.py](http://generate_tfrecord.py/) --csv_input=data/train_labels.csv --output_path=train.record  
# Create test data:  
python [generate_tfrecord.py](http://generate_tfrecord.py/) --csv_input=data/test_labels.csv --output_path=test.record  
"""  
from __future__ import division  
from __future__ import print_function  
from __future__ import absolute_import  
  
import os  
import io  
import pandas as pd  
import tensorflow as tf  
  
from PIL import Image  
from object_detection.utils import dataset_util  
from collections import namedtuple, OrderedDict  
  
flags = tf.app.flags  
flags.DEFINE_string('csv_input', './train.csv', 'Path to the CSV input')  
flags.DEFINE_string('output_path', 'train.tfrecord', 'Path to output TFRecord')  
flags.DEFINE_string('image_dir', './train', 'Path to images')  
#flags.DEFINE_string('csv_input', './eval.csv', 'Path to the CSV input')  
#flags.DEFINE_string('output_path', 'eval.tfrecord', 'Path to output TFRecord')  
#flags.DEFINE_string('image_dir', './eval', 'Path to images')  
FLAGS = flags.FLAGS  
  
  
# TO-DO replace this with label map  
def class_text_to_int(row_label):  
	if row_label == 'cola':  
		return 1  
	elif row_label == 'ChickenLeg':  
		return 2  
	elif row_label == 'PepsiCola':  
		return 3  
	elif row_label == 'ShinRamyun':  
		return 4  
	elif row_label == 'MarlboroGold':  
		return 5  
	elif row_label == 'Doritos':  
		return 6  
	elif row_label == 'Pocachip':  
		return 7  
	elif row_label == 'WhaleFood':  
		return 8  
	else:  
		None  
  
  
def split(df, group):  
	data = namedtuple('data', ['filename', 'object'])  
	gb = df.groupby(group)  
	return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]  
  
  
def create_tf_example(group, path):  
	with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:  
	encoded_jpg = fid.read()  
	encoded_jpg_io = io.BytesIO(encoded_jpg)  
	image = Image.open(encoded_jpg_io)  
	width, height = image.size  
  
	filename = group.filename.encode('utf8')  
	image_format = b'jpg'  
	xmins = []  
	xmaxs = []  
	ymins = []  
	ymaxs = []  
	classes_text = []  
	classes = []  
	  
	for index, row in group.object.iterrows():  
		xmins.append(row['xmin'] / width)  
		xmaxs.append(row['xmax'] / width)  
		ymins.append(row['ymin'] / height)  
		ymaxs.append(row['ymax'] / height)  
		classes_text.append(row['class'].encode('utf8'))  
		classes.append(class_text_to_int(row['class']))  
	  
	tf_example = tf.train.Example(features=tf.train.Features(feature={  
		'image/height': dataset_util.int64_feature(height),  
		'image/width': dataset_util.int64_feature(width),  
		'image/filename': dataset_util.bytes_feature(filename),  
		'image/source_id': dataset_util.bytes_feature(filename),  
		'image/encoded': dataset_util.bytes_feature(encoded_jpg),  
		'image/format': dataset_util.bytes_feature(image_format),  
		'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),  
		'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),  
		'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),  
		'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),  
		'image/object/class/text': dataset_util.bytes_list_feature(classes_text),  
		'image/object/class/label': dataset_util.int64_list_feature(classes),  
	}))  
	return tf_example  
	  
  
def main(_):  
	writer = tf.python_io.TFRecordWriter(FLAGS.output_path)  
	path = os.path.join(FLAGS.image_dir)  
	examples = pd.read_csv(FLAGS.csv_input)  
	grouped = split(examples, 'filename')  
	for group in grouped:  
	tf_example = create_tf_example(group, path)  
	writer.write(tf_example.SerializeToString())  
	  
	writer.close()  
	output_path = os.path.join(os.getcwd(), FLAGS.output_path)  
	print('Successfully created the TFRecords: {}'.format(output_path))  
  
  
if __name__ == '__main__':  
	tf.app.run()
```

>  - csv_input : csv 파일 경로
>  - outputpath : output 파일 경로
>  - image_dir : image 경로
>  - class_text_to_int : class 이름

### Run.

```bash
$ python generate_tfrecord.py
```



# Write Label Map
> training 에 필요한 label map 을 생성합니다. 보유한 클래스에 맞는 형식으로 작성해야합니다.


## - Settings

### Open.

```bash
$ vim labelmap.pbtxt
```
> pbtxt 포맷으로 생성합니다.

### Code.

```vim
item {
	id: 1
	name: 'cola'
}
item {
	id: 2
	name: 'ChickenLeg'
}
item {
	id: 3
	name: 'PepsiCola'
}
item {
	id: 4
	name: 'ShinRamyun'
}
item {
	id: 5
	name: 'MarlboroGold'
}
item {
	id: 6
	name: 'Doritos'
}
item {
	id: 7
	name: 'Pocachip'
}
item {
	id: 8
	name: 'WhaleFood'
}
```
> 다음과 같은 형식으로 작성하여 저장(:wq)합니다.



# Modify Config File
> /models/research/object_detection/samples/configs 경로에서 학습에 필요한 config 파일을 /object_detection/ 으로 이동시킨 후 수정합니다. 본 프로젝트는 ssd_mobilenet_v1.config 파일을 수정하였습니다. finetuing 과정을 거치기 위함입니다.


## - Settings

### Open.

```bash
$ vim ssd_mobilenet_v1.config
```

### Download.

```bash
$ wget http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_2018_01_28.tar.gz
```

> COCO-trained models 에서 ssd_mobilenet_v1_coco 를 다운받습니다. 다른 모델은 [COCO-trained models](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) 에서 받아보실 수 있습니다.

### Code.

```vim
# SSD with Mobilenet v1, configured for Oxford-IIIT Pets Dataset.
# Users should configure the fine_tune_checkpoint field in the train config as
# well as the label_map_path and input_path fields in the train_input_reader and
# eval_input_reader. Search for "PATH_TO_BE_CONFIGURED" to find the fields that
# should be configured.

model {
  ssd {
    num_classes: 8 
    box_coder {
      faster_rcnn_box_coder {
        y_scale: 10.0
        x_scale: 10.0
        height_scale: 5.0
        width_scale: 5.0
      }
    }
    matcher {
      argmax_matcher {
        matched_threshold: 0.5
        unmatched_threshold: 0.5
        ignore_thresholds: false
        negatives_lower_than_unmatched: true
        force_match_for_each_row: true
      }
    }
    similarity_calculator {
      iou_similarity {
      }
    }
    anchor_generator {
      ssd_anchor_generator {
        num_layers: 6
        min_scale: 0.2
        max_scale: 0.95
        aspect_ratios: 1.0
        aspect_ratios: 2.0
        aspect_ratios: 0.5
        aspect_ratios: 3.0
        aspect_ratios: 0.3333
      }
    }
    image_resizer {
      fixed_shape_resizer {
        height: 300
        width: 300
      }
    }
    box_predictor {
      convolutional_box_predictor {
        min_depth: 0
        max_depth: 0
        num_layers_before_predictor: 0
        use_dropout: false
        dropout_keep_probability: 0.8
        kernel_size: 1
        box_code_size: 4
        apply_sigmoid_to_scores: false
        conv_hyperparams {
          activation: RELU_6,
          regularizer {
            l2_regularizer {
              weight: 0.00004
            }
          }
          initializer {
            truncated_normal_initializer {
              stddev: 0.03
              mean: 0.0
            }
          }
          batch_norm {
            train: true,
            scale: true,
            center: true,
            decay: 0.9997,
            epsilon: 0.001,
          }
        }
      }
    }
    feature_extractor {
      type: 'ssd_mobilenet_v1'
      min_depth: 16
      depth_multiplier: 1.0
      conv_hyperparams {
        activation: RELU_6,
        regularizer {
          l2_regularizer {
            weight: 0.00004
          }
        }
        initializer {
          truncated_normal_initializer {
            stddev: 0.03
            mean: 0.0
          }
        }
        batch_norm {
          train: true,
          scale: true,
          center: true,
          decay: 0.9997,
          epsilon: 0.001,
        }
      }
    }
    loss {
      classification_loss {
        weighted_sigmoid {
        }
      }
      localization_loss {
        weighted_smooth_l1 {
        }
      }
      hard_example_miner {
        num_hard_examples: 3000
        iou_threshold: 0.99
        loss_type: CLASSIFICATION
        max_negatives_per_positive: 3
        min_negatives_per_image: 0
      }
      classification_weight: 1.0
      localization_weight: 1.0
    }
    normalize_loss_by_num_matches: true
    post_processing {
      batch_non_max_suppression {
        score_threshold: 1e-8
        iou_threshold: 0.6
        max_detections_per_class: 100
        max_total_detections: 100
      }
      score_converter: SIGMOID
    }
  }
}

train_config: {
  batch_size: 24
  optimizer {
    rms_prop_optimizer: {
      learning_rate: {
        exponential_decay_learning_rate {
          initial_learning_rate: 0.004
          decay_steps: 800720
          decay_factor: 0.95
        }
      }
      momentum_optimizer_value: 0.9
      decay: 0.9
      epsilon: 1.0
    }
  }
  fine_tune_checkpoint: "/data/models/research/object_detection/ssd_mobilenet_v1_coco_2018_01_28/model.ckpt"
  from_detection_checkpoint: true
  load_all_detection_checkpoint_vars: true
  # Note: The below line limits the training process to 200K steps, which we
  # empirically found to be sufficient enough to train the pets dataset. This
  # effectively bypasses the learning rate schedule (the learning rate will
  # never decay). Remove the below line to train indefinitely.
  num_steps: 200000
  data_augmentation_options {
    random_horizontal_flip {
    }
  }
  data_augmentation_options {
    ssd_random_crop {
    }
  }
}

train_input_reader: {
  tf_record_input_reader {
    input_path: "/data/train.tfrecord"
  }
  label_map_path: "/data/labels.pbtxt"
}

eval_config: {
  metrics_set: "coco_detection_metrics"
  num_examples: 10
}

eval_input_reader: {
  tf_record_input_reader {
    input_path: "/data/eval.tfrecord"
  }
  label_map_path: "/data/labels.pbtxt"
  shuffle: false
  num_readers: 1
}
```

> - num_classes : 사용한 클래스 수
> - input_path : tfrecord 경로
> - label_map_path : pbtxt 경로


# Training
> training 을 위해 /models/research/object_detection/model_main.py 파일을 수정합니다.

## - Settings

### Open.
```bash
$ vim model_main.py
```
> /models/research/object_detection/ 경로에 존재합니다.

### Code.

```python
# Copyright 2017 The TensorFlow Authors. All Rights Reserved.  
#  
# Licensed under the Apache License, Version 2.0 (the "License");  
# you may not use this file except in compliance with the License.  
# You may obtain a copy of the License at  
#  
# [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)  
#  
# Unless required by applicable law or agreed to in writing, software  
# distributed under the License is distributed on an "AS IS" BASIS,  
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
# See the License for the specific language governing permissions and  
# limitations under the License.  
# ==============================================================================  
"""Binary to run train and evaluation on object detection model."""  
  
from __future__ import absolute_import  
from __future__ import division  
from __future__ import print_function  
  
from absl import flags  
import os  
  
#os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID" # see issue #152  
#os.environ["CUDA_VISIBLE_DEVICES"]="1"  
  
  
import tensorflow as tf  
  
from object_detection import model_hparams  
from object_detection import model_lib  
  
flags.DEFINE_string(  
	'model_dir', '/data/dataset/trained_model/', 'Path to output model directory '  
	'where event and checkpoint files will be written.')  
flags.DEFINE_string('pipeline_config_path', '/[data/models/research/object_detection/ssd_mobilenet_v1.config'](http://data/models/research/object_detection/ssd_mobilenet_v1.config'), 'Path to pipeline config '  
					'file.')  
flags.DEFINE_integer('num_train_steps', 200000, 'Number of train steps.')  
flags.DEFINE_boolean('eval_training_data', False,  
					'If training data should be evaluated for this job. Note '  
					'that one call only use this in eval-only mode, and '  
					'`checkpoint_dir` must be supplied.')  
flags.DEFINE_integer('sample_1_of_n_eval_examples', 1, 'Will sample one of '  
					'every n eval input examples, where n is provided.')  
flags.DEFINE_integer('sample_1_of_n_eval_on_train_examples', 5, 'Will sample '  
					'one of every n train input examples for evaluation, '  
					'where n is provided. This is only used if '  
					'`eval_training_data` is True.')  
flags.DEFINE_string(  
	'hparams_overrides', None, 'Hyperparameter overrides, '  
	'represented as a string containing comma-separated '  
	'hparam_name=value pairs.')  
flags.DEFINE_string(  
	'checkpoint_dir', None, 'Path to directory holding a checkpoint. If '  
	'`checkpoint_dir` is provided, this binary operates in eval-only mode, '  
	'writing resulting metrics to `model_dir`.')  
flags.DEFINE_boolean(  
	'run_once', False, 'If running in eval-only mode, whether to run just '  
	'one round of eval vs running continuously (default).'  
)  
FLAGS = flags.FLAGS  
  
  
def main(unused_argv):  
	config = tf.estimator.RunConfig(model_dir='/data/dataset/trained_model/')  
	  
	train_and_eval_dict = model_lib.create_estimator_and_inputs(  
			run_config=config,  
			hparams=model_hparams.create_hparams(FLAGS.hparams_overrides),  
			pipeline_config_path='/data/models/research/object_detection/ssd_mobilenet_v1.config',  
			train_steps=FLAGS.num_train_steps,  
			sample_1_of_n_eval_examples=FLAGS.sample_1_of_n_eval_examples,  
			sample_1_of_n_eval_on_train_examples=(  
					FLAGS.sample_1_of_n_eval_on_train_examples))  
	estimator = train_and_eval_dict['estimator']  
	train_input_fn = train_and_eval_dict['train_input_fn']  
	eval_input_fns = train_and_eval_dict['eval_input_fns']  
	eval_on_train_input_fn = train_and_eval_dict['eval_on_train_input_fn']  
	predict_input_fn = train_and_eval_dict['predict_input_fn']  
	train_steps = train_and_eval_dict['train_steps']  
	  
	if FLAGS.checkpoint_dir:  
		if FLAGS.eval_training_data:  
			name = 'training_data'  
			input_fn = eval_on_train_input_fn  
		else:  
			name = 'validation_data'  
			# The first eval input will be evaluated.  
			input_fn = eval_input_fns[0]  
		if FLAGS.run_once:  
			estimator.evaluate(input_fn,  
								steps=None,  
								checkpoint_path=tf.train.latest_checkpoint(  
								FLAGS.checkpoint_dir))  
		else:  
		model_lib.continuous_eval(estimator, FLAGS.checkpoint_dir, input_fn,  
								train_steps, name)  
	else:  
		train_spec, eval_specs = model_lib.create_train_and_eval_specs(  
				train_input_fn,  
				eval_input_fns,  
				eval_on_train_input_fn,  
				predict_input_fn,  
				train_steps,  
				eval_on_train_data=False)  
		  
		# Currently only a single Eval Spec is allowed.  
		tf.estimator.train_and_evaluate(estimator, train_spec, eval_specs[0])  
  
  
if __name__ == '__main__':  
	tf.app.run()
```

> - model_dir : ckpt 와 같이 output 이 저장될 경로
> - pipeline_config_path : config 파일의 경로
> - num_train_steps : 학습 step 수
> 해당 파라미터를 환경에 맞게 수정합니다. 본 프로젝트의 환경에서는 200000 steps 기준으로 24시간 정도 소요됩니다. 어느 정도 예측도를 측정하기 위한 방법이 필요합니다.


### Multi gpu.
```vim
$ vim train.py
```

> /models/research/object_detection/legacy/train.py 에서 num_clones 부분을 gpu 수 만큼 변경하면 됩니다. 시도는 해봤는데 train 하는 프로세스가 4개의 gpu 를 모두 잡긴하는데 결국에는 하나의 gpu 에서 수행합니다. 해당 문제를 해결하는 방법이 필요합니다. 


### Run.

```bash
$ python model_main.py
```


# Make pb Format File
> training 과정을 거치면서 model_dir 경로에 model.ckpt-200000-data-00000-of-00001, model.ckpt-200000.index, model.ckpt-20000.meta 와 같은 파일이 3개 만들어 집니다. 이 파일들을 따로 저장해 둡니다.

## Settings

### Open.

```bash
$ vim export_tflite_ssd_graph.py
```
> /models/research/object_detection/ 경로에서 찾습니다.

### Code.

```python
# Copyright 2018 The TensorFlow Authors. All Rights Reserved.  
#  
# Licensed under the Apache License, Version 2.0 (the "License");  
# you may not use this file except in compliance with the License.  
# You may obtain a copy of the License at  
#  
# [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)  
#  
# Unless required by applicable law or agreed to in writing, software  
# distributed under the License is distributed on an "AS IS" BASIS,  
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
# See the License for the specific language governing permissions and  
# limitations under the License.  
# ==============================================================================  
r"""Exports an SSD detection model to use with tf-lite.  
  
Outputs file:  
* A tflite compatible frozen graph - $output_directory/tflite_graph.pb  
  
The exported graph has the following input and output nodes.  
  
Inputs:  
'normalized_input_image_tensor': a float32 tensor of shape  
[1, height, width, 3] containing the normalized input image. Note that the  
height and width must be compatible with the height and width configured in  
the fixed_shape_image resizer options in the pipeline config proto.  
  
In floating point Mobilenet model, 'normalized_image_tensor' has values  
between [-1,1). This typically means mapping each pixel (linearly)  
to a value between [-1, 1]. Input image  
values between 0 and 255 are scaled by (1/128.0) and then a value of  
-1 is added to them to ensure the range is [-1,1).  
In quantized Mobilenet model, 'normalized_image_tensor' has values between [0,  
255].  
In general, see the `preprocess` function defined in the feature extractor class  
in the object_detection/models directory.  
  
Outputs:  
If add_postprocessing_op is true: frozen graph adds a  
	TFLite_Detection_PostProcess custom op node has four outputs:  
	detection_boxes: a float32 tensor of shape [1, num_boxes, 4] with box  
	locations  
	detection_classes: a float32 tensor of shape [1, num_boxes]  
	with class indices  
	detection_scores: a float32 tensor of shape [1, num_boxes]  
	with class scores  
	num_boxes: a float32 tensor of size 1 containing the number of detected boxes  
else:  
	the graph has two outputs:  
		'raw_outputs/box_encodings': a float32 tensor of shape [1, num_anchors, 4]  
		containing the encoded box predictions.  
		'raw_outputs/class_predictions': a float32 tensor of shape  
		[1, num_anchors, num_classes] containing the class scores for each anchor  
		after applying score conversion.  
  
Example Usage:  
--------------  
python object_detection/export_tflite_ssd_graph \  
		--pipeline_config_path path/to/ssd_mobilenet.config \  
		--trained_checkpoint_prefix path/to/model.ckpt \  
		--output_directory path/to/exported_model_directory  
  
The expected output would be in the directory  
path/to/exported_model_directory (which is created if it does not exist)  
with contents:  
	- tflite_graph.pbtxt  
	- tflite_graph.pb  
Config overrides (see the `config_override` flag) are text protobufs  
(also of type pipeline_pb2.TrainEvalPipelineConfig) which are used to override  
certain fields in the provided pipeline_config_path. These are useful for  
making small changes to the inference graph that differ from the training or  
eval config.  
  
Example Usage (in which we change the NMS iou_threshold to be 0.5 and  
NMS score_threshold to be 0.0):  
python object_detection/export_tflite_ssd_graph \  
		--pipeline_config_path path/to/ssd_mobilenet.config \  
		--trained_checkpoint_prefix path/to/model.ckpt \  
		--output_directory path/to/exported_model_directory  
		--config_override " \  
					model{ \  
					ssd{ \  
						post_processing { \  
							batch_non_max_suppression { \  
										score_threshold: 0.0 \  
										iou_threshold: 0.5 \  
							} \  
						} \  
				} \  
			} \  
			"  
"""  
  
import tensorflow as tf  
from google.protobuf import text_format  
from object_detection import export_tflite_ssd_graph_lib  
from object_detection.protos import pipeline_pb2  
import os  
os.environ["CUDA_VISIBLE_DEVICES"]="1"  
  
flags = tf.app.flags  
flags.DEFINE_string('output_directory', '/data/dataset/tflite_ssd_graph', 'Path to write outputs.')  
flags.DEFINE_string(  
		'pipeline_config_path', '/[data/models/research/object_detection/ssd_mobilenet_v1.config'](http://data/models/research/object_detection/ssd_mobilenet_v1.config'),  
		'Path to a pipeline_pb2.TrainEvalPipelineConfig config '  
		'file.')  
flags.DEFINE_string('trained_checkpoint_prefix', '/[data/dataset/testing_model/model.ckpt-200000'](http://data/dataset/testing_model/model.ckpt-200000'), 'Checkpoint prefix.')  
flags.DEFINE_integer('max_detections', 10,  
					'Maximum number of detections (boxes) to show.')  
flags.DEFINE_integer('max_classes_per_detection', 1,  
					'Number of classes to display per detection box.')  
flags.DEFINE_integer(  
		'detections_per_class', 10,  
		'Number of anchors used per class in Regular Non-Max-Suppression.')  
flags.DEFINE_bool('add_postprocessing_op', True,  
				'Add TFLite custom op for postprocessing to the graph.')  
flags.DEFINE_bool(  
		'use_regular_nms', False,  
		'Flag to set postprocessing op to use Regular NMS instead of Fast NMS.')  
flags.DEFINE_string(  
		'config_override', '', 'pipeline_pb2.TrainEvalPipelineConfig '  
		'text proto to override pipeline_config_path.')  
		  
FLAGS = flags.FLAGS  
  
  
def main(argv):  
	del argv # Unused.  
	flags.mark_flag_as_required('output_directory')  
	flags.mark_flag_as_required('pipeline_config_path')  
	flags.mark_flag_as_required('trained_checkpoint_prefix')  
	  
	pipeline_config = pipeline_pb2.TrainEvalPipelineConfig()  
	  
	with tf.gfile.GFile(FLAGS.pipeline_config_path, 'r') as f:  
		text_format.Merge(f.read(), pipeline_config)  
	text_format.Merge(FLAGS.config_override, pipeline_config)  
	export_tflite_ssd_graph_lib.export_tflite_graph(  
			pipeline_config, FLAGS.trained_checkpoint_prefix, FLAGS.output_directory,  
			FLAGS.add_postprocessing_op, FLAGS.max_detections,  
			FLAGS.max_classes_per_detection, FLAGS.use_regular_nms)  
  
  
if __name__ == '__main__':  
	tf.app.run(main)

```
> - output_directory : pb 파일이 저장될 경로
> - pipeline_config_path : 사용할 config 파일 경로
> - trained_checkpoint_prefix : ckpt 파일이 저장된 경로


### Run.

```bash
$ python export_tflite_ssd_graph.py
```


# Convert pb File to tflite File
> pb 파일을 모바일 디바이스에 올리기 위해 tflite 포맷 파일으로 변환하는 작업입니다. 이제는 models 가 아니라 tensorflow 디렉토리에서 수행됩니다.



## - Settings


### Directory.
```bash
$ export OUTPUT_DIR=$DIR
```
> - DIR : pb 파일이 저장된 경로
> - 해당 디렉토리에서 생성된 tflite 파일을 찾을 수 있습니다.


### Run.
```bash
bazel run --config=opt tensorflow/lite/toco:toco -- --input_file=$OUTPUT_DIR/tflite_graph.pb --output_file=$OUTPUT_DIR/detect.tflite --input_shapes=1,300,300,3 --input_arrays=normalized_input_image_tensor --output_arrays='TFLite_Detection_PostProcess','TFLite_Detection_PostProcess:1','TFLite_Detection_PostProcess:2','TFLite_Detection_PostProcess:3'  --inference_type=FLOAT --allow_custom_ops
```

> 해당 스크립트를 사용하면 tflite 파일이 생성됩니다.



# Import tflite File to Android
> 생성된 tflite 파일을 android 에 임포트합니다.


## - Settings

### Git.
```bash
$ git clone https://github.com/tensorflow/examples.git
```

> /examples/lite/examples/object_detection/android/ 경로를 android studio 에서 open 합니다.


### Import.
>/examples/lite/examples/object_detection/android/app/src/main/assets/ 경로에 생성한 tflite 파일을 detect.tflite 이름으로 이동시킵니다. 그리고 labelmap.txt 파일을 생성한 tflite 포맷에 맞게 수정합니다.




# Reference

[https://www.tensorflow.org/](https://www.tensorflow.org/)
[https://towardsdatascience.com/detecting-pikachu-on-android-using-tensorflow-object-detection-15464c7a60cd](https://towardsdatascience.com/detecting-pikachu-on-android-using-tensorflow-object-detection-15464c7a60cd)
[https://github.com/tensorflow/models](https://github.com/tensorflow/models)
[https://github.com/tensorflow](https://github.com/tensorflow)
[https://github.com/tensorflow/tensorflow](https://github.com/tensorflow/tensorflow)

