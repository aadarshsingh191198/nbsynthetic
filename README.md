![GAN](docs/images/GAN.jpg)

![alt text](https://badgen.net/github/license/micromatch/micromatch)
![alt text](https://img.shields.io/badge/version-0.1.0-green)
![alt text](https://img.shields.io/badge/python-3.7%20%7C%203.8-orange)


#### **An unsupervised synthetic data generator with a simple and reliable architecture developed as an open source project by NextBrain.ml**

# **1. Overview**
**nbsytnethic** is an open source project for a straightforward but robust tabular synthetic data generating package. In image generation or speech generation applications, synthetic data generation is in a golden era. Since Ian J. Goodfellow introduced Generative Adversarial Networks in 2014 [^1], this algorithm has become key in data generation, outperforming existing ones such as Variational Autoencoders and Boltzman Machines. GANs are one of the most versatile neural network architectures currently in use.</br>
   GANs are made up of two components: generators and discriminators. The generator model generates synthetic samples from random noise, collected using a distribution, which are then provided to the discriminator, which tries to discern between the two. Both the generator and the discriminator enhance their capabilities until the discriminator can no longer distinguish between real and synthetic samples. Training generator and discriminator models at the same time is generally unstable[^2]. Since its introduction, multiple variations of GAN have been developed to improve both its stability and accuracy. For example, with the addition of new parameters as an extra condition, the discriminator has an additional aid in classifying actual and fake data. This case is known as Conditional GAN or CGAN. This additional 'condition' switches the method from 'unsupervised' to a 'supervised' one. Another example is the Auxilary Classifier GAN, or ACGAN, which is a specific kind of CGAN version. The list of improved GANs that have been widely utilized in image generation applications is considerable, especially when it comes to image generation applications.
   
## **Why a basic library for synthetic tabular data generation**

   When it comes to tabular data, GAN's journey has evolved quietly in contrast to image[^3], video[^4], and speech[^5] generation. There are a few libraries for creating synthetic tabular data, and they are generally based on conditional GAN architectures[^6][^7][^8]. Tabular data, on the other hand, is by far the most frequent data resource in the world (there are about 700 million active spreadsheet users worldwide). The majority of possible data applications in many industries typically rely on limited datasets and 'low quality' data, as data scientists refer to it. This is why, in a data-centric approach[^9], the development of tools for this type of data is critical. </br>As an example, we are helping a psychiatric hospital with a data analysis project. They came to us with comprehensive research based on data collected over the last ten years. Psychiatric hospitalizations are critical, and this research began with the goal of improving early alerts and prevention protocols. We got the results in the form of a spreadsheet with 38 columns and 300 rows. Certainly, that is a small amount of data for any data scientist, and even less for a statistician. It was, however, a challenging effort for them to collect this data. It was data of 'low quality,' with many empty values (only seven rows had all 38 feature values). Should we tell them that this data is insufficient for using Machine Learning?. Indeed, with this data, the validity of any statistical method will be questioned. However, this should not be an impediment to helping them maximize the value from this effort by obtaining actionable insights that may be valuable. </br>
   Available packages for generated syntehtic data rely on CGAN architectures. When we have several dimensions in the original datasets, we have to choose one as an additional 'condition' for our GAN. We will use this dimension or feature to condition the generation of the other features. This is certainly practical when we want to use the dataset to solve a supervised learning problem, such as, for example, classification or regression. Then we can use our target variable as a condition for the GAN. But it's common that these small datasets have only a single target. Users want to get actionable insights from different features. So, to ask these users for a 'target' feature is something unrealistic. 

## **Unconditional GANs for tabular data**

   As we mentioned, the evolution of GANs has brought interesting ideas such as introducing extra information to the discriminator in order to get better accuracy and give more stability to the net. This variant method requires a target that will condition the generated synthetic data. If this target data doesn't have enough quality (something that's common), we are adding an important bias to our new generated data. Moreover, as we said, many datasets do not have a single target feature, because users want to make predictions on different features in order to get more insights. So, configuring the synthetic data to a single feature will also introduce a bias in the generated data. This is why we have decided to use a non-conditional GAN or non-supervised GAN (also called vanilla GAN) and treat the synthetic data generation as an unsupervised learning problem. The accuracy we get could probably be improved by conditioning the GAN with a reliable target variable, but we wanted to provide a versatile tool for this specific target: There are 700 million active spreadsheet users with small or medium data sets that have poor data quality. 
   
## **Statistical tests**
   To verify the output accuracy, we must compare the original input data with the synthetic data obtained. As a result, we must address the issue of comparing samples from two probability distributions. For this purpose, statistical tests such as the Student's t-test and the Wilcoxon signed-rank test (a nonparametric variation of the paired Student's t-test) are available. We also use the Kolmogorov-Smirnov test for numerical features. All of the above tests compare the probability distributions of each feature in the input dataset and the synthetic data one-to-one (called the two-sample test or homogeneity problem). </br> However, we also required a test that could compare the similarity of both input and output datasets. We used an innovative approach: measuring the Maximum Mean Discrepancy (MMD). MMD is a statistical test that checks if two samples belong to different distributions. This test calculates the difference in means between two samples, which are mapped onto a reproducing kernel Hilbert space (RKHS). The Maximum Mean Discrepancy has been extensively used in machine learning and nonparametric testing [^10][^11]. By finding a smooth function that is large on points drawn from p and small on points drawn from q. The statistic measurement is the difference between the mean function values of the two samples; when this difference is large, the samples are most likely from different distributions. Another reason we chose this test is that it performs well with data from small sample sizes.


## **Limitations**
  Unsupervised GANs are known for being difficult to train, resulting in generators that produce nonsensical outputs. Deep convolutional generative adversarial networks have been used in some potential solutions [^12]. However, our target audience for this library is small and medium-sized datasets, so we designed a network architecture capable of generating synthetic datasets (also known as "fake datasets", but we don't like that term) up to 5.000 instances. We evaluated input datasets with the same number of instances and found that the net is stable and has a low computational cost. The library accepts numerical and categorical inputs. In terms of data dimension, nbsynthetic has been tested with datasets with up to 200 dimensions. The test revealed a limitation when the input data is highly dimensional and only contains numerical features. In general, performance improves when the dataset has both numerical and categorical variables.

# **2. Requirements**
nbsynthetic has been developed and runs on Python 3.7 and Python 3.8.

# **3. Installation**
```
git clone git@github.com:NextBrain-ml/nbsynthetic/
cd nbsynthetic
make install
```
or directly in a python script:
```python
pip install git+https://github.com/NextBrain-ml/nbsynthetic.git
```

# **4. Quick setup guide**

## **4.1. Input data**
  The initial step is to load the data that will be used to fit the GAN. We could do this by importing:
  ```python
  from nbsynthetic.data import input_data
  ```
  passing in the filename and decimal character as parameters: <br/>
  ```python
  df = input_data(filename, decimal='.')
  ```
 Once imported, we must prepare this data with the following conditions.

-String values are not accepted by nbsynthetic. We must encode categorical features as a numeric array with strings. Any of the encoders provided in `sklearn.preprocessing` can be used. 
-We must check that datatypes are properly set. Numerical columns must have data types of 'float' or 'int'. Pandas Categorical will be used for categorical columns. 
-NaN values must be removed or replaced. 
- nbsynthetic does not accept Datetime columns. We have the option to remove them or transform into categorical features. nbsynthetic contains a module that makes this transformation: `data.data_preparation.manage_datetime_columns`, where the arguments are the dataframe and datetime column's name.

nbsynthetic includes a module that can perform all of the transformations described above: `nbsynthetic.data_transformation.SmartBrain`:
-Assigns datatypes correctly and deletes id columns. 
-Removes columns with a large percentage of NaN values, replaces NaN values where possible; and rejects the remaining when replacement was not possible. 
-Encodes categorial features. 
-And finally, this module is able to augment the dataset when the dataset length is too short or the ratio of data length to number of features is small. 

An example of how to do these steps using the nbsynthetic package:
   ```python
   from nbsynthetic.data import input_data
   from nbsynthetic.data_preparation import SmartBrain

   df = input_data('file_name', decimal=',')
   SB = SmartBrain() 
   df = SB.nbEncode(df) #GAN input data
   ```
  
## **4.2. Create a GAN instance**
   ```python
   from nbsynthetic.vgan import GAN
   ```

The arguments for the GAN instance are:
- `GAN` : Vanilla GAN
- `df` : input data
- `samples` : number of instances in the synthetic dataset <br/>
We have also additional parameters we can change in the GAN (it's not recomended, by the way).
- `initial_lr` (default value = 0.0002): Initial learning rate. For more information go [here](https://keras.io/api/optimizers/).
- `dropout` (default value = 0.5). Droput value. For more information go [here](https://keras.io/api/layers/).
- `epochs` (default value = 10). Number of epochs. For more information go [here](https://keras.io/api/models/model_training_apis/).

## **4.3. Generate a synthetic dataset**

   Then, we can directly create a synthetic dataset with the desired number of instances or samples. 
   ```python
   from nbsynthetic.synthetic import synthetic_data

   samples= 2000 #number of samples we want to generate
   newdf = synthetic_data(
       GAN, 
       df, 
       samples = samples
       )
   ```
   Complete code:
   ```python
   from nbsynthetic.data import input_data
   from nbsynthetic.data_preparation import SmartBrain
   from nbsynthetic.vgan import GAN
   from nbsynthetic.synthetic import synthetic_data

   df = input_data('file_name', decimal=',')
   SB = SmartBrain() 
   df = SB.nbEncode(df) 
```   samples= 2000 
   newdf = synthetic_data(
       GAN, 
       df, 
       samples = samples
       )
   ```
   
## **4.4. Statistical tests**
   The final step is to compare the synthetic dataset to the input dataset. As said before, we will employ various statistical tests. The Maximum Mean Discrepancy test is the most important (MMD).
```python
from nbsynthetic.statistics import mmd_rbf
mmd_rbf(df, newdf, gamma=None)
```
We can also run other statistical tests such as the Wilcoxon, Student t, and Kolmogorov Smirnov tests. We can import as follows:
```python
from nbsynthetic.statistics import Wilcoxon, Student_t, Kolmogorov_Smirnov

Wilcoxon(df, newdf)
Student_t(df, newdf)
Kolmogorov_Smirnov(df, newdf)
```
  We can also compare the original and synthetic distributions by plotting the histograms of each feature. We use [Plotly Open Source Graphing Library for Python](https://plotly.com/python/). </br>

```python
from nbsynthetic.statistics import plot_histograms
plot_histograms(df, newdf)
```
   
# **5. References**
[^1]: Goodfellow, I., Pouget-Abadie, J., Mirza, M., Xu, B., Warde-Farley, D., Ozair, S., ... & Bengio, Y. (2014). Generative adversarial nets. Advances in neural information processing systems, 27.
[^2]: Arjovsky, M., & Bottou, L. (2017). Towards principled methods for training generative adversarial networks. arXiv preprint arXiv:1701.04862.
[^3]: Karras, T., Laine, S., Aittala, M., Hellsten, J., Lehtinen, J., & Aila, T. (2020). Analyzing and improving the image quality of stylegan. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition (pp. 8110-8119).
[^4]: Clark, A., Donahue, J., & Simonyan, K. (2019). Adversarial video generation on complex datasets. arXiv preprint arXiv:1907.06571.
[^5]:Binkowski, M., Donahue, J., Dieleman, S., Clark, A., Elsen, E., Casagrande, N., ... & Simonyan, K. (2019). High fidelity speech synthesis with adversarial networks. arXiv preprint arXiv:1909.11646.
[^6]: Xu, L., Skoularidou, M., Cuesta-Infante, A., & Veeramachaneni, K. (2019). Modeling tabular data using conditional gan. Advances in Neural Information Processing Systems, 32.
[^7]: Mirza, M., & Osindero, S. (2014). Conditional generative adversarial nets. arXiv preprint arXiv:1411.1784.
[^8]: Lei Xu LIDS, Kalyan Veeramachaneni. (2018). Synthesizing Tabular Data using Generative Adversarial Networks. arXiv:1811.11264v1
[^9]: Motamedi, M., Sakharnykh, N., & Kaldewey, T. (2021). A data-centric approach for training deep neural networks with less data. arXiv preprint arXiv:2110.03613.
[^10]: Ilya Tolstikhin, Bharath K. Sriperumbudur, and Bernhard Schölkopf (2016). Minimax estimation of maximum mean discrepancy with radial kernels. In Proceedings of the 30th International Conference on Neural Information Processing Systems (NIPS'16). Curran Associates Inc., Red Hook, NY, USA, 1938–1946.
[^11]: A. Gretton, K. M. Borgwardt, M. Rasch, B. Schölkopf, and A. Smola. (2007). A kernel method for the two sample problem. In B. Schölkopf, J. Platt, and T. Hoffman, editors, Advances in Neural Information Processing Systems 19, pages 513–520, Cambridge, MA. MIT Press.
[^12]: Radford, A., Metz, L., & Chintala, S. (2015). Unsupervised representation learning with deep convolutional generative adversarial networks. arXiv preprint arXiv:1511.06434.
