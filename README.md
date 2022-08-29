![GAN](docs/images/GAN.jpg)

# **NB synthetic**
A Simple and robust unsupervised synthetic data generator.

License: MIT

Development Status: Beta

Homepage: [https://github.com/NextBrain-ml/tabular-synthetic-data/]

## **Overview**
Next Brain Synthetic is a simple but robust tabular synthetic data generation library. Synthetic data generation is living a golden age in image generation or speech generation applications. Since the introduction of Generative Adversarial Networks by Ian J. Goodfellow in 2014 [^1]., this algorithm have became essential in data generation, overperforming the already existing ones like Variational Autoencoders or Boltzman Machines. GAN are one of the most versatile neural network architectures in use today.
   GANs are made up of two components: generators and discriminators. The generator model produces synthetic samples from random noise collected using a distribution, which are passed to the discriminator, which attempts to differentiate between the two. Both the generator and the discriminator enhance their abilities until the discriminator can no longer tell the difference between actual and synthetic samples. The simultaneous training of generator and discriminator models is inherently unstable[^2]. Since its presentation, several variants of GAN have been created in order to increase both, its stabiliuty and its accuracy. For example, with the introduction of additional parameters as an extra condition, discriminator has an additional help the Discriminators in the classsification between real and synthetic data. This variant is known as Conditional GAN or CGAN and moves the algorithm from the 'unsuperised learning' field to the 'supervised learning' one, by using this additional 'condition'. Another variant of CGAN are the Auxilary Classifier GAN or ACGAN. The list of improived GAN is long and have been succesfully applied in image generarion applications. 

   
## **Why a basic library for synthetic tabular data generation?**

   When it comes to tabular data, the story of GAN have evolved quietly in comparison with image[^3], video[^4] and speech[^5] generation. There are not many libraries to generate synthetic tabular data and are mostly based in conditional GAN architectures[^6][^7][^8]. However, tabular data are by far the most common in the world. Even more, the majority of potential data applications in many industries has to rely in small datasets and, as Data Scinetists use to say, 'poor quality' data. This is the reason why in a data centric approach[^9], the creation of tools for this kind of data is fundamental. For example, we are helping a large hospital in Spain's psychiatric department in a data analysis project. They presented us with a comprehensive research based on data collected over the last ten years. Psychiatric hospitalizations are critical, and this research began with the goal of developing early detection and prevention protocols. We were provided with the results in the form of a spreadsheet with 38 columns and 300 rows. Certainly, that is a small amount of data for any data scientist. It was, however, a challenging effort for them. What are we going to say to them?  Should we tell them that this data is insufficient for using Machine Learning?.Indeed, with this data, the validity of any statistical technique utilized will be put into question. However, this should not be an impediment to maximizing the value from this study by obtaining actionable insights that may be valuable.
   When we have serval dimensions in the original datasets, we have to choose one as an additional 'condition' for our GAN. We will use this dimension or features to condition the generation of the other features. This is certainly practical when we want to use the dataset to solve a supervised learning problem as for example classification or regression. Then we can use our target variable as condition for the GAN.  

## **Unconditional GANs for tabular data**

   As we mentioned, the evolution of GANs has brought interesting ideas as introducing extra information to the discriminator in order to get better accuracy and give more stability to the net. This variant method requires from a target that will condition the generated synthetic data.  If this target data hasn't enough quality (something that's common) we are adding an important bias to our new generated data. Moreover, many datasets has not an only a target feature, because users wants to make predicitions on different features in order to get more insights. So, to condition the synthetic data to a single feature will also add a bias in the generated data. This is why we have decided to use a non conditional GAN or non supervised GAN (also called vanilla GAN) and treat the synthetic data generation as an unsupervised learning problem. Probably the accuracy we get could be improved by condition the GAN with a reliable target variable, but we wanted to provide a versatile tool for a specific target users: small or medium data sets with poor data quality. 
  
## **Statistical tests**
   For checking the output accuracy we have to compare the original input data with the obtained synthetic data. So we have to address the problem of comparing samples from two probability distributions. There are different satatistical tests available for that purpose as the Student's t-test or the Wilcoxon signed-rank test (a nonparametric version of the paired Student’s t-test). For numerical features we also implement the Kolmogorov-Smirnov test. All the above test compartes one-to-one the probability distributions of each feature in the inùt datset and the synthetic data (called two samples test or homogeneity problem). But we also needed a test that was able to compare the similarity of both input/outup complete datasets. We have choosen a quite novel method called Maximum Mean Discrepancy (MMD). MMD is a statistical tests to determine if two samples are from different distributions. This test measures the distance between the means of the two samples mapped into a reproducing kernel Hilbert space (RKHS). Maximum Mean Discrepancy has found numerous applications in machine learning and nonparametric testing [^10][^11]. MMD tests whether distributions p and q are different on the basis of samples drawn from each of them, by finding a smooth function which is large on the points drawn from p, and small (as negative as possible) on the points from q. The core test statistic is the difference between the mean function values on the two samples; when this is large, the samples are likely from different distributions. This test performs very well in data with low sample size.


## **Limitations**
   Unsupervised GANs have been known to be unstable to train and often resulting in generators that produce unrealistic outputs. Some posible solutions have been adopting deep convolutional generative adversarial networks [^12]. But our target with this library are small and medium size datasets so we have desing a network architectura that is robust generating syntehtic dataset up to 5.000 instances. We have tested input dataset with the same number of instances and the newtork is perfectly stable and with an affordable computational cost. Tabular data hasn't to be labeled and the library works with both numerical and boolean inputs even mixed. Concerning the data dimnesionality, the library have been tested with datasets up to 200 dimensions. A limitation emerged from the test is when input data is high dimensional and with only nunerical features available. As a general rule, performance is better when we have dataset with mixed numerical and boolean data.   


## **References**
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
