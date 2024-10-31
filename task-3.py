import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, LeakyReLU, BatchNormalization
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Load the dataset
data_path = r'C:\Users\sonav\Downloads\Compressed\dreamskrin\merged_train_data.csv'
df = pd.read_csv(data_path, low_memory=False)

# Convert all columns to appropriate data types
for column in df.columns:
    try:
        df[column] = pd.to_numeric(df[column])
    except ValueError:
        pass

# Save original column names
original_columns = df.columns

# Preprocess the dataset with label encoding and standardization
def preprocess_data(df):
    label_encoders = {}
    for column in df.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le
    
    # Standardize numerical features
    numeric_features = df.select_dtypes(include=['int64', 'float64']).columns
    scaler = StandardScaler()
    df[numeric_features] = scaler.fit_transform(df[numeric_features])
    
    return df, label_encoders, scaler

# Preprocess the data
df, label_encoders, scaler = preprocess_data(df)
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

    # Optimizers with gradient clipping
    d_optimizer = Adam(learning_rate=0.0002, beta_1=0.5, clipvalue=0.5)
    g_optimizer = Adam(learning_rate=0.0002, beta_1=0.5, clipvalue=0.5)

    discriminator.compile(loss='binary_crossentropy', optimizer=d_optimizer, metrics=['accuracy'])
    gan.compile(loss='binary_crossentropy', optimizer=g_optimizer)

    for epoch in range(epochs):
        
        # Train Discriminator
        idx = np.random.randint(0, X_train.shape[0], batch_size)
        real_data = X_train[idx]
        
        noise = np.random.normal(0, 1, (batch_size, latent_dim))
        generated_data = generator.predict(noise)
        
        # Adding noise to the labels
        valid_with_noise = valid * 0.9 + np.random.rand(*valid.shape) * 0.1
        fake_with_noise = fake * 0.1 + np.random.rand(*fake.shape) * 0.1

        d_loss_real = discriminator.train_on_batch(real_data, valid_with_noise)
        d_loss_fake = discriminator.train_on_batch(generated_data, fake_with_noise)
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
        
        # Train Generator
        noise = np.random.normal(0, 1, (batch_size, latent_dim))
        g_loss = gan.train_on_batch(noise, valid)
        
        # Print the progress
        print(f"{epoch} [D loss: {d_loss[0]}, acc.: {100*d_loss[1]}%] [G loss: {g_loss}]")
        
        # Save generated samples at specified intervals
        if epoch % sample_interval == 0:
            sample_data(generator, latent_dim, epoch, X_train.shape[1], original_columns)

# Function to sample data and save
def sample_data(generator, latent_dim, epoch, output_dim, columns, samples=200000):
    noise = np.random.normal(0, 1, (samples, latent_dim))
    generated_data = generator.predict(noise)
    generated_df = pd.DataFrame(generated_data, columns=columns)
    
    # Inverse transform numerical features
    numeric_features = generated_df.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_features) > 0:
        generated_df[numeric_features] = scaler.inverse_transform(generated_df[numeric_features])
    
    # Inverse transform categorical features
    for column in generated_df.select_dtypes(include=['object']).columns:
        if column in label_encoders:
            le = label_encoders[column]
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
gan = build_gan(generator, discriminator)

# Train the GAN
train_gan(generator, discriminator, gan, X_train, latent_dim)