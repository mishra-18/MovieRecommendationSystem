# END-TO-END Movies Recommendation System 🎬 🎥

## Overview  

**This is an End to End Movie based recommendation system. The movies are recommended with respect to the generated cosine similarity. The dataset for this project was built from scratch, the movie database used for the project is imdb_movie_data_2023. This dataset is generated by web scraping the official IMDb site. The recommendation system has also been deployed on Google Cloud with the help of Kubernetes cluster with 1 node. You can create your own docker image and run the app as explained later.**

#### You can visit the web app on the IP: http://34.168.9.81 (by the time you click on it, it might be possible that the GCP quota has expired, thus go through installation please)
![Screenshot 2024-01-03 152046](https://github.com/mishra-18/MovieRecommendationSystem/assets/155224614/90f10388-1980-4505-8449-ac104c97360a)

## Usage
* Clone the repository 
```
git clone https://github.com/mishra-18/MovieRecommendationSystem.git
```
* Navigate to the project
```
cd MovieRecommendationSystem
```



### Directly run app using streamlit

Install the Requirements.

``` 
pip install requirements.txt
```

Run the streamlit app
```
streamlit run app.py
```
###  Run using docker 🐋
* Build a doker Image
  
```
sudo docker build -t IMAGENAME:VERSION .
```

* Run the image and go to the shown IP adress



```
sudo docker run -p 8080:8051 IMAGENAME:VERSION
```
**Note** If you are using windows and you can't run the streamlit app with docker then you need to change the last line of Dockerfile to ```CMD["streamlit", "run", "app.py", "--server.port", "8051"]```. 

Then build the docker image, after docker run go to http://localhost:8080. You should now be able to access the web app.

## Generate your own Dataset 🎬
If you want to create your own imdb movie dataset with more movies. Simply navigate to the ``src``. Read the code structure and change the ```num_clicks``` default is 35. Also update the date in ```url``` to get the movie released till that date.
To create your own data run the Webscrapper
```python Webscrapper.py```
