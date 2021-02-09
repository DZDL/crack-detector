# Crack detector - CPU-only inference

![](docs/img/banner.png)

Check references & licenses!

- Neural network: [DeepCrack](https://github.com/yhlleo/DeepCrack)
- Code implementation: [DeepSegmentor (Pretrained weights)](https://github.com/yhlleo/DeepSegmentor)
- WebApp implementation: [crack-detector (only-cpu)](https://github.com/DZDL/crack-detector)

Web app powered by AI to detect cracks on surfaces.

# How to run 

## Web version

Clic [here](https://deepcrackcpu.herokuapp.com/) to see the demo of crack-detector in action for images and video (<5 min).

## Docker version

To downloand the image and run the contaider in detach mode, run the code below.

```
docker container run -p 8501:8501 --rm -d pablogod/crack-detector:latest
```
To shutdown the docker type this:

```
docker ps -aq # Check which id was assigned for the crack-detector instance
docker stop <weird id of crack-detector> # Type the id
```

## Local computer

Run this code locally on Linux based distros:
```
# Clone and install requirements
git clone https://github.com/DZDL/crack-detector
cd crack-detector
pip3 install -r requirementDocker.txt
# Download the pretrained weights
gdown --id 12-iXK656aGUIWCtN9gb0Ko7qotyn9ZcI -O myapp/DeepSegmentor/checkpoints/deepcrack/latest_net_G.pth
# Run streamlit
streamlit run app.py
# Then a webapp will open, check console output.
```

## Deploy docker on Heroku

Only maintainers of the repository can do this.
```
heroku login
docker ps
heroku container:login
heroku container:push web -a crack-detector
heroku container:release web -a crack-detector
```

<!-- - Automatic deploy comming (working)

https://www.r-bloggers.com/2020/12/creating-a-streamlit-web-app-building-with-docker-github-actions-and-hosting-on-heroku/ -->


# References

Database & code, more info check [DeepCrack](https://github.com/yhlleo/DeepCrack) &[DeepSegmentor (Pretrained weights)](https://github.com/yhlleo/DeepSegmentor).

```
@article{liu2019deepcrack,
  title={DeepCrack: A Deep Hierarchical Feature Learning Architecture for Crack Segmentation},
  author={Liu, Yahui and Yao, Jian and Lu, Xiaohu and Xie, Renping and Li, Li},
  journal={Neurocomputing},
  volume={338},
  pages={139--153},
  year={2019},
  doi={10.1016/j.neucom.2019.01.036}
}

@article{liu2019roadnet,
  title={RoadNet: Learning to Comprehensively Analyze Road Networks in Complex Urban Scenes from High-Resolution Remotely Sensed Images},
  author={Liu, Yahui and Yao, Jian and Lu, Xiaohu and Xia, Menghan and Wang, Xingbo and Liu, Yuan},
  journal={IEEE Transactions on Geoscience and Remote Sensing},
  volume={57},
  number={4},
  pages={2043--2056},
  year={2019},
  doi={10.1109/TGRS.2018.2870871}
}
```
