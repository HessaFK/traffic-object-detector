#Traffic Object Detector (Cars vs. Motorcycle)

It is an end-to-end computer vision application designed to detect and distingusih between cars and motorycles in real-world traffic streams. Developed initially in Google Colab using a custom dataset, this model has been containerized using Flask and Docker and is designed for seamless local deployment and web hosting.


## Project Overview and Context 

In urban traffic managment, distinguishing between vehicle types is vital for flow optimization, automated saftey monitoring, and municipal policy enforcement. 

### Model Specifications
* **Architecture**: YOLOv8 Nano (`yolov8n.pt`) chosen for fast, low-latency edge performance.
* **Input**: 3-channel RGB colored images ($640 \times 640$ spatial resolution).
* **Outputs**: Object bounding boxes `[x_center, y_center, width, height]`, class names (`car`, `bike`), and corresponding prediction confidence thresholds.


##App Preview in Action 

Below is a demonstration of the web application processing a standard traffic scen, accuratly localizing overlapping vehicle classes with tight bounding boxes:

![App Preview]()

##Live web App (Rendor Deployment)

The application is deployed live and dully functional on Render. You can access the interface and run inference on real traffic images instantly by visiting the web link:

[https://traffic-object-detector-1.onrender.com/]

##Local Setup via Docker

To fulfill local reproducible testing workflows, you can also run this application locally without configuring complex python environments or CUDA dependencies by utilizing Docker. 

###Prerequisites
* Ensure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running on your machine. 

###Instructions

1. Clone the Repository
2. Build the Docker Image 
3. Run the Container
4. Access the App Locally


##How to use the Interface 

The application features a clean and beginner-friendlt web dashboard, start with:

1. Upload an image from the "Choose File" button on the interface. 
2. Submit for Inference by clicking the "UUpload and Analyze", which sends it to the backend Flask API where the optimized YOLOv8 weights process the frame. 
3. View the visual results displaying the original image and the overlayed with colored bounding boxes along with the confidence scores. 

##Dataset and Model Evaluation 

The dataset is compiled, labeled, and split (70% Train, 20% Validation, 10% Test) using Roboflow. During the dat auditing, raw annotation sequences stored as instance segmentation polygons were successfully converted into a standarized 4 point bounding boxes to guarntee complete structural compliance with the training architecture. 

##Performance Summary
The model converged smoothly over 50-epoch training schedule, having the results:

car - 358 Instance Count - 69.1% precision, 69.8% recall, 72.8% accuracy
bike(Motorcyle) - 147 Instance Count - 44.1% precision - 36.1% Recall - 31.9% accuracy
Combined (All) - 505 Instance Count - 56.6% precision - 52.9% recall - 52.4% accuracy


##Known Issues and Limitations 

* The model performs significantly better on cars than on motorcylces, this is due to a little data imbalance where the motorcycle training sets mostly features single vehicles per image, whereas the car images contained dense, multi-instance environemtns. 
* The annotations done were in polygons, thus when standarizing them to bounding boxes inadvertently intergrated extra background pixels. Because motorcules have smaller, narrower spatial profiles, this extra background clutter sometiems confuses the model, causing it to miss detections or lower the confidence. 
* The further the vehicle is in teh background the highly occluded it is by the other larger vehicales show a steep decrease the confidence level. 

##Future Roadmap
* Conduct targeted data augmentation to balance motorcycle representation
* Refine bounding box tight-fitting boundaries to isolate background clutter. 

