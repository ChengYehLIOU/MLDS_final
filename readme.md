
## Download model
Download ResNet50 pre-train model:  

	bash downloadResNet50.sh

Download our best fine-tuned model:  

    bash downloadBestModel.sh

## Set up the environment
Our environment:  
1. python 3.5.2  
2. keras 2.0.6
3. tenserflow 1.1.0

Reqired package:
1. numpy
2. opencv-python


## How to run our code

#### Training
	python3 train_frcnn.py -o <Parser> -p <DataPath> --input_weight_path <InputModelPath> --output_weight_path <OutputModelPath> --num_epochs <EpochNum>

>-p: Path to training data  
>-o: Which parser you want to use ('deepQ_Synth' or 'deepQ_Real')  
>--input_weight_path: Input path for weights. (Default is pre-train model)  
>--output_weight_path: Output path for weights.  

Train with synthetic data:  

	python3 train_frcnn.py -p ~/MLDS/final/data/ -o deepQ_Synth --output_weight_path model_frcnn.hdf5 --num_epochs 200

Fine-tune with real data:  

	python3 train_frcnn.py -p ~/MLDS/final/data/ -o deepQ_Real --input_weight_path model_frcnn.hdf5 --output_weight_path model_ft.hdf5 --num_epochs 5
    
#### Testing

Test by hand detect judger:  

	python3 test_judger.py -p ./ 
