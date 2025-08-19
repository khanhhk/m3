import tensorflow as tf
from tensorflow.keras.layers import Dense, InputLayer
from alibi_detect.od import IForest, OutlierVAE

def initialize_vae(n_features, latent_dim):
    """
    Make an vae model
    """
    encoder_net = tf.keras.Sequential(
      [
          InputLayer(input_shape=(n_features,)),
          Dense(20, activation=tf.nn.relu),
          Dense(15, activation=tf.nn.relu),
          Dense(7, activation=tf.nn.relu)
      ])

    decoder_net = tf.keras.Sequential(
      [
          InputLayer(input_shape=(latent_dim,)),
          Dense(7, activation=tf.nn.relu),
          Dense(15, activation=tf.nn.relu),
          Dense(20, activation=tf.nn.relu),
          Dense(n_features, activation=None)
      ])

    # initialize outlier detector
    vae = OutlierVAE(threshold=None,  # threshold for outlier score
                    score_type='mse',  # use MSE of reconstruction error for outlier detection
                    encoder_net=encoder_net,  # can also pass VAE model instead
                    decoder_net=decoder_net,  # of separate encoder and decoder
                    latent_dim=latent_dim,
                    samples=5)
    
    return vae

def initialize_isf(threshold=0., n_estimators=100):
    """
    Make an isolation forest model
    """
    isf = IForest(
        threshold=threshold,
        n_estimators=n_estimators
    )
    
    return isf