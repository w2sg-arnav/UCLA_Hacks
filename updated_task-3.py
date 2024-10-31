import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, LeakyReLU, BatchNormalization
from tensorflow.keras.models import Sequential
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Load the dataset
feeds_file_path = 'C:\\Users\\sonav\\Downloads\\Compressed\\dreamskrin\\train_data_feeds.csv'
ads_file_path = 'C:\\Users\\sonav\\Downloads\\Compressed\\dreamskrin\\train_data_ads.csv'

def optimize_types(df):
    for col in df.select_dtypes(include=['int64', 'float64']).columns:
        if pd.api.types.is_integer_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], downcast='signed')
        else:
            df[col] = pd.to_numeric(df[col], downcast='float')
    return df

def load_and_optimize_csv(file_path, chunk_size=1000):
    chunks = []
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        chunk = chunk.dropna()
        chunk = optimize_types(chunk)
        chunks.append(chunk)
    df = pd.concat(chunks, ignore_index=True)
    return df

# Load and optimize datasets
df_feeds = load_and_optimize_csv(feeds_file_path)
df_ads = load_and_optimize_csv(ads_file_path)

# Preprocess the dataset with label encoding
def preprocess_data(df):
    label_encoders = {}
    for column in df.select_dtypes(include=['object']).columns:
        df[column] = df[column].astype(str)  # Ensure all object columns are strings
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le
    
    # Standardize numerical features
    numeric_features = df.select_dtypes(include=['int32', 'float32']).columns
    scaler = StandardScaler()
    df[numeric_features] = scaler.fit_transform(df[numeric_features])
    
    return df, label_encoders, scaler, numeric_features

# Preprocess the data
df, label_encoders, scaler, numeric_features = preprocess_data(df_ads)
X_train = df.values

# Define the GAN architecture
# Generator
def build_generator(latent_dim, output_dim):
    model = Sequential()
    model.add(Dense(128, input_dim=latent_dim))
    model.add(LeakyReLU(alpha=0.2))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Dense(256))
    model.add(LeakyReLU(alpha=0.2))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Dense(512))
    model.add(LeakyReLU(alpha=0.2))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Dense(output_dim, activation='tanh'))
    return model

# Discriminator
def build_discriminator(input_dim):
    model = Sequential()
    model.add(Dense(512, input_dim=input_dim))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dense(256))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dense(1, activation='sigmoid'))
    return model

# GAN
def build_gan(generator, discriminator):
    model = Sequential()
    model.add(generator)
    model.add(discriminator)
    return model

# Training the GAN
def train_gan(generator, discriminator, gan, data, latent_dim, epochs=10000, batch_size=64, sample_interval=2000):
    # Rescale -1 to 1
    X_train = (data - 0.5) * 2
    
    valid = np.ones((batch_size, 1))
    fake = np.zeros((batch_size, 1))
    
    for epoch in range(epochs):
        
        # Train Discriminator
        idx = np.random.randint(0, X_train.shape[0], batch_size)
        real_data = X_train[idx]
        
        noise = np.random.normal(0, 1, (batch_size, latent_dim))
        generated_data = generator.predict(noise)
        
        d_loss_real = discriminator.train_on_batch(real_data, valid)
        d_loss_fake = discriminator.train_on_batch(generated_data, fake)
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
        
        # Train Generator
        noise = np.random.normal(0, 1, (batch_size, latent_dim))
        g_loss = gan.train_on_batch(noise, valid)
        
        # Print the progress
        print(f"{epoch} [D loss: {d_loss[0]}, acc.: {100*d_loss[1]}%] [G loss: {g_loss}]")
        
        # Save generated samples at specified intervals
        if epoch % sample_interval == 0:
            sample_data(generator, latent_dim, epoch, data.shape[1], df.columns, numeric_features)

# Function to sample data and save
def sample_data(generator, latent_dim, epoch, output_dim, original_columns, numeric_features, samples=200000):
    noise = np.random.normal(0, 1, (samples, latent_dim))
    generated_data = generator.predict(noise)
    generated_df = pd.DataFrame(generated_data, columns=original_columns)
    
    # Inverse transform numeric features
    generated_df[numeric_features] = scaler.inverse_transform(generated_df[numeric_features])
    
    # Reverse label encoding for categorical features
    for column, le in label_encoders.items():
        generated_df[column] = le.inverse_transform(generated_df[column].astype(int))
    
    generated_df.to_csv(f"synthetic_data_epoch_{epoch}.csv", index=False)

# Set random seed for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Define dimensions
latent_dim = 100
output_dim = X_train.shape[1]

# Build and compile the GAN
generator = build_generator(latent_dim, output_dim)
discriminator = build_discriminator(output_dim)
discriminator.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
discriminator.trainable = False
gan = build_gan(generator, discriminator)
gan.compile(loss='binary_crossentropy', optimizer='adam')

# Train the GAN
train_gan(generator, discriminator, gan, X_train, latent_dim)
