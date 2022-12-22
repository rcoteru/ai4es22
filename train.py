"""
Trains the neural network.

Quite self explanatory.

@author Raúl Coterillo
@version ??-12-2022
"""


from pytorch_lightning.callbacks import LearningRateMonitor, ModelCheckpoint
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from pytorch_lightning import Trainer, seed_everything

from network import BasicConvolutionalRegressor
from data import ImageDataModule
from pathlib import Path
import time

# Settings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

FOLDER = Path("models/test")

RANDOM_STATE = 0
seed_everything(RANDOM_STATE)

# Data Setup
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

print("Computing dataset...")
start_time = time.perf_counter()
dm = ImageDataModule(
    csv_file="csvs/train.csv",
    test_size=0.2,
    eval_size=0.2,
    batch_size=64,
    dataset_sample=0.2,
    random_state=RANDOM_STATE,
    image_shape=[110,330]
)
end_time = time.perf_counter()
print("DONE! ", end_time - start_time, "seconds")

# Model Setup
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

print("Creating model...", end="")
start_time = time.perf_counter()
model = BasicConvolutionalRegressor(
    learning_rate=1e-5
)
end_time = time.perf_counter()
print("DONE! ", end_time - start_time, "seconds")

# Trainer Setup
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

print("Setup the trainer...")
start_time = time.perf_counter()

early_stop = EarlyStopping(monitor="val_mae", mode="min", patience=10)
lr_monitor = LearningRateMonitor(logging_interval='step')
model_checkpoint = ModelCheckpoint(FOLDER, save_last=True)

trainer = Trainer(
    default_root_dir=FOLDER,
    callbacks=[lr_monitor, model_checkpoint, early_stop],
    log_every_n_steps=1,
    check_val_every_n_epoch=1,
    max_epochs=200, 
    deterministic = True
)

end_time = time.perf_counter()
print("DONE! ", end_time - start_time, "seconds")

# Training time!
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

print("Begin training...")
trainer.fit(model, datamodule=dm)
trainer.validate(model, datamodule=dm)
trainer.test(model, datamodule=dm)